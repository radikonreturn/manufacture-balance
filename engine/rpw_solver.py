"""
rpw_solver.py — Ranked Positional Weight (RPW) Solver
Line balancing algorithm based on Helgeson & Birnie (1961).

Steps:
1. Compute RPW for each task (own duration + longest successor path)
2. Sort by descending RPW
3. Assign to stations sequentially — respecting cycle time and precedence
"""

from typing import List, Dict, Any
from .graph import PrecedenceGraph


def solve_rpw(graph: PrecedenceGraph, cycle_time: float) -> List[Dict[str, Any]]:
    """
    Solve line balancing using the RPW algorithm.

    Args:
        graph      : PrecedenceGraph object (tasks + precedences loaded)
        cycle_time : Station cycle time (takt time)

    Returns:
        stations: [
            {
                "station_id": 1,
                "tasks": ["T1", "T3"],
                "task_details": [{"id": "T1", "name": "...", "duration": 5.0}, ...],
                "total_time": 12.0,
                "idle_time": 3.0,
            },
            ...
        ]

    Raises:
        ValueError: If any task duration exceeds cycle_time
    """
    # ----- Pre-check -----
    for tid, info in graph.tasks.items():
        if info["duration"] > cycle_time:
            raise ValueError(
                f"Task '{tid}' duration ({info['duration']}) "
                f"exceeds cycle time ({cycle_time})! "
                f"Increase the cycle time or split the task."
            )

    # ----- Compute RPW and sort descending -----
    rpw_values = graph.all_positional_weights()
    sorted_tasks = sorted(rpw_values.keys(), key=lambda t: rpw_values[t], reverse=True)

    # ----- Assign to stations -----
    assigned = set()
    stations: List[Dict[str, Any]] = []

    while len(assigned) < len(graph.tasks):
        station_tasks = []
        station_time = 0.0
        station_id = len(stations) + 1

        for tid in sorted_tasks:
            if tid in assigned:
                continue

            # Precedence check: all predecessors must be assigned
            predecessors_done = all(p in assigned for p in graph.predecessors[tid])
            if not predecessors_done:
                continue

            # Capacity check
            if station_time + graph.tasks[tid]["duration"] <= cycle_time:
                station_tasks.append(tid)
                station_time += graph.tasks[tid]["duration"]
                assigned.add(tid)

        if not station_tasks:
            # Prevent infinite loop if no task can be assigned
            remaining = [t for t in graph.tasks if t not in assigned]
            raise ValueError(
                f"No tasks could be assigned to station {station_id}. "
                f"Remaining tasks: {remaining}. Check precedence constraints."
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
