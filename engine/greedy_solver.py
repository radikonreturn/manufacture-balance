"""
greedy_solver.py — Greedy (Largest Candidate Rule) Solver
Line balancing using the Largest Candidate Rule heuristic.

Steps:
1. Sort tasks by descending duration
2. For each station, assign the largest eligible task (precedence OK + capacity OK)
3. Open a new station when no more tasks fit
"""

from typing import List, Dict, Any
from .graph import PrecedenceGraph


def solve_greedy(graph: PrecedenceGraph, cycle_time: float) -> List[Dict[str, Any]]:
    """
    Solve line balancing using the Greedy (Largest Candidate Rule) algorithm.

    Args:
        graph      : PrecedenceGraph object
        cycle_time : Station cycle time

    Returns:
        List of stations (same format as RPW solver)

    Raises:
        ValueError: If any task duration exceeds cycle_time
    """
    # ----- Pre-check -----
    for tid, info in graph.tasks.items():
        if info["duration"] > cycle_time:
            raise ValueError(
                f"Task '{tid}' duration ({info['duration']}) "
                f"exceeds cycle time ({cycle_time})!"
            )

    # ----- Sort by descending duration -----
    sorted_tasks = sorted(
        graph.tasks.keys(),
        key=lambda t: graph.tasks[t]["duration"],
        reverse=True,
    )

    # ----- Assign to stations -----
    assigned = set()
    stations: List[Dict[str, Any]] = []

    while len(assigned) < len(graph.tasks):
        station_tasks = []
        station_time = 0.0
        station_id = len(stations) + 1

        # Keep trying while tasks can be assigned in this iteration
        changed = True
        while changed:
            changed = False
            for tid in sorted_tasks:
                if tid in assigned:
                    continue

                # Precedence check
                predecessors_done = all(
                    p in assigned for p in graph.predecessors[tid]
                )
                if not predecessors_done:
                    continue

                # Capacity check
                if station_time + graph.tasks[tid]["duration"] <= cycle_time:
                    station_tasks.append(tid)
                    station_time += graph.tasks[tid]["duration"]
                    assigned.add(tid)
                    changed = True

        if not station_tasks:
            remaining = [t for t in graph.tasks if t not in assigned]
            raise ValueError(
                f"No tasks could be assigned to station {station_id}. "
                f"Remaining: {remaining}"
            )

        stations.append({
            "station_id": station_id,
            "tasks": station_tasks,
            "task_details": [
                {
                    "id": tid,
                    "name": graph.tasks[tid]["name"],
                    "duration": graph.tasks[tid]["duration"],
                }
                for tid in station_tasks
            ],
            "total_time": round(station_time, 4),
            "idle_time": round(cycle_time - station_time, 4),
        })

    return stations
