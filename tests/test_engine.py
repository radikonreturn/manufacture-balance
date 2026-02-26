"""
test_engine.py — Unit tests for engine modules
"""

import sys
import os
import pytest
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine.graph import PrecedenceGraph
from engine.rpw_solver import solve_rpw
from engine.greedy_solver import solve_greedy
from engine.metrics import (
    line_efficiency,
    balance_delay,
    smoothness_index,
    theoretical_min_stations,
    bottleneck_score,
    compute_all_metrics,
)
from engine.energy_waste import calculate_energy_waste, annual_savings
from engine.jes_generator import generate_jes, format_jes_markdown


# ------------------------------------------------------------------ #
#  Test Fixtures
# ------------------------------------------------------------------ #

@pytest.fixture
def sample_df():
    """Simple 5-task test data."""
    return pd.DataFrame({
        "task_id": ["T1", "T2", "T3", "T4", "T5"],
        "task_name": ["Cutting", "Drilling", "Bending", "Welding", "Assembly"],
        "duration": [6, 4, 3, 5, 2],
        "predecessors": ["", "T1", "T1", "T2", "T3 T4"],
    })


@pytest.fixture
def sample_graph(sample_df):
    g = PrecedenceGraph()
    g.load_from_dataframe(sample_df)
    return g


@pytest.fixture
def full_df():
    """10-task full test data (same as sample_tasks.csv)."""
    return pd.DataFrame({
        "task_id": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"],
        "task_name": [
            "Body Cutting", "Hole Drilling", "Bending", "Welding A",
            "Welding B", "Surface Grinding", "Paint Preparation", "Painting",
            "Quality Inspection", "Packaging",
        ],
        "duration": [6, 4, 3, 5, 4, 3, 2, 6, 4, 2],
        "predecessors": [
            "", "T1", "T1", "T2", "T2 T3",
            "T4", "T5", "T6 T7", "T8", "T9",
        ],
    })


# ------------------------------------------------------------------ #
#  Graph Tests
# ------------------------------------------------------------------ #

class TestPrecedenceGraph:

    def test_load_basic(self, sample_graph):
        assert len(sample_graph.tasks) == 5
        assert sample_graph.tasks["T1"]["duration"] == 6

    def test_entry_tasks(self, sample_graph):
        entries = sample_graph.get_entry_tasks()
        assert entries == ["T1"]

    def test_exit_tasks(self, sample_graph):
        exits = sample_graph.get_exit_tasks()
        assert exits == ["T5"]

    def test_topological_sort(self, sample_graph):
        order = sample_graph.topological_sort()
        assert len(order) == 5
        # T1 must always be first
        assert order[0] == "T1"
        # T5 must always be last
        assert order[-1] == "T5"
        # T2 must come before T4
        assert order.index("T2") < order.index("T4")

    def test_cycle_detection(self):
        df = pd.DataFrame({
            "task_id": ["A", "B", "C"],
            "task_name": ["a", "b", "c"],
            "duration": [1, 2, 3],
            "predecessors": ["C", "A", "B"],  # A->B->C->A cycle!
        })
        g = PrecedenceGraph()
        with pytest.raises(ValueError, match="[Cc]ycle"):
            g.load_from_dataframe(df)

    def test_total_work_content(self, sample_graph):
        assert sample_graph.total_work_content() == 20  # 6+4+3+5+2

    def test_positional_weights(self, sample_graph):
        rpw = sample_graph.all_positional_weights()
        # T1 should have the highest RPW (entry point)
        assert rpw["T1"] == max(rpw.values())
        # T5 should have the lowest RPW (only its own duration)
        assert rpw["T5"] == 2


# ------------------------------------------------------------------ #
#  RPW Solver Tests
# ------------------------------------------------------------------ #

class TestRPWSolver:

    def test_basic_solve(self, sample_graph):
        stations = solve_rpw(sample_graph, cycle_time=10)
        assert len(stations) >= 2
        # All tasks must be assigned
        all_tasks = set()
        for s in stations:
            all_tasks.update(s["tasks"])
        assert all_tasks == {"T1", "T2", "T3", "T4", "T5"}

    def test_station_respects_cycle_time(self, sample_graph):
        stations = solve_rpw(sample_graph, cycle_time=10)
        for s in stations:
            assert s["total_time"] <= 10

    def test_task_too_long(self, sample_graph):
        with pytest.raises(ValueError, match="exceeds cycle time"):
            solve_rpw(sample_graph, cycle_time=3)  # T1=6 > 3

    def test_idle_time_calculation(self, sample_graph):
        stations = solve_rpw(sample_graph, cycle_time=15)
        for s in stations:
            assert abs(s["idle_time"] - (15 - s["total_time"])) < 0.01


# ------------------------------------------------------------------ #
#  Greedy Solver Tests
# ------------------------------------------------------------------ #

class TestGreedySolver:

    def test_basic_solve(self, sample_graph):
        stations = solve_greedy(sample_graph, cycle_time=10)
        assert len(stations) >= 2
        all_tasks = set()
        for s in stations:
            all_tasks.update(s["tasks"])
        assert all_tasks == {"T1", "T2", "T3", "T4", "T5"}

    def test_task_too_long(self, sample_graph):
        with pytest.raises(ValueError, match="exceeds cycle time"):
            solve_greedy(sample_graph, cycle_time=3)


# ------------------------------------------------------------------ #
#  Metrics Tests
# ------------------------------------------------------------------ #

class TestMetrics:

    def test_perfect_balance(self):
        """Perfect balance: every station fully loaded."""
        stations = [
            {"station_id": 1, "total_time": 10, "idle_time": 0, "tasks": ["T1"]},
            {"station_id": 2, "total_time": 10, "idle_time": 0, "tasks": ["T2"]},
        ]
        assert line_efficiency(stations, 10) == 100.0
        assert balance_delay(stations, 10) == 0.0
        assert smoothness_index(stations, 10) == 0.0

    def test_imperfect_balance(self):
        stations = [
            {"station_id": 1, "total_time": 8, "idle_time": 2, "tasks": ["T1"]},
            {"station_id": 2, "total_time": 6, "idle_time": 4, "tasks": ["T2"]},
        ]
        eff = line_efficiency(stations, 10)
        assert eff == 70.0  # (8+6)/(2*10)*100

    def test_theoretical_min(self):
        assert theoretical_min_stations(20, 10) == 2
        assert theoretical_min_stations(21, 10) == 3

    def test_bottleneck_score(self):
        stations = [
            {"station_id": 1, "total_time": 9.5, "idle_time": 0.5, "tasks": []},
            {"station_id": 2, "total_time": 5, "idle_time": 5, "tasks": []},
        ]
        scores = bottleneck_score(stations, 10)
        assert scores[0]["is_bottleneck"] is True  # 95%
        assert scores[1]["is_bottleneck"] is False  # 50%


# ------------------------------------------------------------------ #
#  Energy Waste Tests
# ------------------------------------------------------------------ #

class TestEnergyWaste:

    def test_basic_calculation(self):
        stations = [
            {"station_id": 1, "total_time": 8, "idle_time": 2, "tasks": []},
            {"station_id": 2, "total_time": 6, "idle_time": 4, "tasks": []},
        ]
        report = calculate_energy_waste(
            stations, cycle_time=10,
            kwh_per_second=0.001, cost_per_kwh=2.0, co2_per_kwh=0.5,
        )
        # Total idle = 2 + 4 = 6s
        assert report.total_idle_time == 6
        # Energy = 6 * 0.001 = 0.006 kWh
        assert abs(report.total_energy_kwh - 0.006) < 1e-6
        # Cost = 0.006 * 2 = 0.012
        assert abs(report.total_cost - 0.012) < 1e-4
        # CO2 = 0.006 * 0.5 = 0.003
        assert abs(report.total_co2_kg - 0.003) < 1e-6

    def test_annual_savings(self):
        before = calculate_energy_waste(
            [{"station_id": 1, "total_time": 5, "idle_time": 5, "tasks": []}],
            cycle_time=10, kwh_per_second=0.001, cost_per_kwh=2.0, co2_per_kwh=0.5,
        )
        after = calculate_energy_waste(
            [{"station_id": 1, "total_time": 9, "idle_time": 1, "tasks": []}],
            cycle_time=10, kwh_per_second=0.001, cost_per_kwh=2.0, co2_per_kwh=0.5,
        )
        savings = annual_savings(before, after, cycles_per_day=100, working_days_per_year=250)
        assert savings["saved_kwh_annual"] > 0
        assert savings["saved_cost_annual"] > 0


# ------------------------------------------------------------------ #
#  JES Generator Tests
# ------------------------------------------------------------------ #

class TestJESGenerator:

    def test_generate_jes(self, sample_graph):
        stations = solve_rpw(sample_graph, cycle_time=15)
        jes = generate_jes(stations, cycle_time=15)
        assert len(jes) == len(stations)
        for sid, data in jes.items():
            assert "steps" in data
            assert len(data["steps"]) > 0

    def test_markdown_output(self, sample_graph):
        stations = solve_rpw(sample_graph, cycle_time=15)
        jes = generate_jes(stations, cycle_time=15)
        first_jes = list(jes.values())[0]
        md = format_jes_markdown(first_jes)
        assert "Work Instructions" in md
        assert "Step 1" in md
        assert "Station" in md


# ------------------------------------------------------------------ #
#  Integration Test
# ------------------------------------------------------------------ #

class TestIntegration:

    def test_full_pipeline(self, full_df):
        """End-to-end test: CSV -> Graph -> Solve -> Metrics -> Energy -> JES"""
        # 1. Graph
        graph = PrecedenceGraph()
        graph.load_from_dataframe(full_df)
        assert graph.summary()["task_count"] == 10

        # 2. Solve
        ct = 15
        stations_rpw = solve_rpw(graph, ct)
        stations_greedy = solve_greedy(graph, ct)

        # Both solutions must assign all tasks
        for stations in [stations_rpw, stations_greedy]:
            all_tasks = set()
            for s in stations:
                all_tasks.update(s["tasks"])
            assert len(all_tasks) == 10

        # 3. Metrics
        metrics = compute_all_metrics(stations_rpw, ct, graph.total_work_content())
        assert 0 < metrics["line_efficiency"] <= 100
        assert metrics["num_stations"] >= metrics["theoretical_min_stations"]

        # 4. Energy
        energy = calculate_energy_waste(stations_rpw, ct)
        assert energy.total_energy_kwh >= 0
        assert len(energy.per_station) == len(stations_rpw)

        # 5. JES
        jes = generate_jes(stations_rpw, ct)
        assert len(jes) == len(stations_rpw)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
