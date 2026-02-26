"""Quick verification script for full pipeline."""
from engine.graph import PrecedenceGraph
from engine.rpw_solver import solve_rpw
from engine.greedy_solver import solve_greedy
from engine.metrics import compute_all_metrics
from engine.energy_waste import calculate_energy_waste
from engine.jes_generator import generate_jes
from data.parser import parse_csv

df = parse_csv("sample_tasks.csv")
g = PrecedenceGraph()
g.load_from_dataframe(df)

stations_rpw = solve_rpw(g, 15)
stations_greedy = solve_greedy(g, 15)

m_rpw = compute_all_metrics(stations_rpw, 15, g.total_work_content())
m_greedy = compute_all_metrics(stations_greedy, 15, g.total_work_content())

e = calculate_energy_waste(stations_rpw, 15)
jes = generate_jes(stations_rpw, 15)

print("=== FULL PIPELINE VERIFICATION ===")
print(f"Tasks loaded: {g.summary()['task_count']}")
print(f"Total work content: {g.total_work_content()} sec")
print()
print(f"RPW:    {m_rpw['num_stations']} stations | Efficiency: {m_rpw['line_efficiency']}%")
print(f"Greedy: {m_greedy['num_stations']} stations | Efficiency: {m_greedy['line_efficiency']}%")
print()
print(f"Energy waste: {e.total_energy_kwh:.4f} kWh/cycle")
print(f"Cost:         ${e.total_cost:.4f}/cycle")
print(f"CO2:          {e.total_co2_kg:.4f} kg/cycle")
print()
print(f"JES generated for {len(jes)} stations")
for sid, data in jes.items():
    print(f"  Station {sid}: {len(data['steps'])} steps, {data['utilization_pct']}% util")
print()
print("ALL OK")
