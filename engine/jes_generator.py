"""
jes_generator.py — Electronic Job Element Sheet (JES) Generator
Ciano et al. (2021) — Operator 4.0 digital work instructions.

Generates step-by-step, timed work instructions for each station.
"""

from typing import List, Dict, Any
from datetime import datetime
import html


def generate_jes(
    stations: List[Dict[str, Any]],
    cycle_time: float,
    line_name: str = "Main Assembly Line",
) -> Dict[int, Dict[str, Any]]:
    """
    Generate JES data for all stations.

    Args:
        stations   : Solver output
        cycle_time : Cycle time
        line_name  : Line name (for JES header)

    Returns:
        {
            station_id: {
                "station_id": int,
                "line_name": str,
                "cycle_time": float,
                "total_time": float,
                "utilization_pct": float,
                "steps": [
                    {
                        "step": 1,
                        "task_id": "T1",
                        "task_name": "Body Cutting",
                        "duration": 6.0,
                        "cumulative_time": 6.0,
                        "remaining_time": 9.0,
                        "key_points": str,
                    },
                    ...
                ],
                "generated_at": str,
            }
        }
    """
    all_jes = {}

    for station in stations:
        sid = station["station_id"]
        steps = []
        cumulative = 0.0

        for i, task in enumerate(station["task_details"], start=1):
            cumulative += task["duration"]
            remaining = round(cycle_time - cumulative, 4)

            # Auto-generate key points
            key_points = _auto_key_points(task, i, len(station["task_details"]))

            steps.append({
                "step": i,
                "task_id": task["id"],
                "task_name": task["name"],
                "duration": task["duration"],
                "cumulative_time": round(cumulative, 4),
                "remaining_time": max(remaining, 0),
                "key_points": key_points,
            })

        utilization = round((station["total_time"] / cycle_time) * 100, 1) if cycle_time > 0 else 0

        all_jes[sid] = {
            "station_id": sid,
            "line_name": line_name,
            "cycle_time": cycle_time,
            "total_time": station["total_time"],
            "utilization_pct": utilization,
            "steps": steps,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    return all_jes


def format_jes_markdown(jes_data: Dict[str, Any]) -> str:
    """
    Convert a single station's JES data to readable Markdown format.

    Args:
        jes_data: Single station dict from generate_jes() output

    Returns:
        Markdown string
    """
    sid = jes_data["station_id"]
    lines = [
        f"# 🏭 Work Instructions — Station {sid}",
        "",
        "| Info | Value |",
        "|------|-------|",
        f"| **Line** | {jes_data['line_name']} |",
        f"| **Cycle Time** | {jes_data['cycle_time']} sec |",
        f"| **Station Load** | {jes_data['total_time']} sec |",
        f"| **Utilization** | {jes_data['utilization_pct']}% |",
        f"| **Generated** | {jes_data['generated_at']} |",
        "",
        "---",
        "",
        "## 📋 Work Steps",
        "",
    ]

    for step in jes_data["steps"]:
        safe_name = html.escape(str(step['task_name']))
        safe_id = html.escape(str(step['task_id']))
        safe_kp = html.escape(str(step['key_points']))

        lines.append(
            f"### Step {step['step']}: {safe_name} "
            f"(`{safe_id}`)"
        )
        lines.append("")
        lines.append(f"- ⏱️ **Duration:** {step['duration']} sec")
        lines.append(
            f"- 📊 **Cumulative:** {step['cumulative_time']} / "
            f"{jes_data['cycle_time']} sec"
        )
        lines.append(f"- ⏳ **Remaining:** {step['remaining_time']} sec")
        if safe_kp:
            lines.append(f"- 📌 **Note:** {safe_kp}")
        lines.append("")

    # Utilization bar
    pct = jes_data["utilization_pct"]
    bar_filled = int(pct / 5)
    bar_empty = 20 - bar_filled
    bar = "█" * bar_filled + "░" * bar_empty
    lines.append("---")
    lines.append("")
    lines.append(f"**Load:** [{bar}] {pct}%")
    lines.append("")

    return "\n".join(lines)


def _auto_key_points(task: Dict, step_num: int, total_steps: int) -> str:
    """Generate automatic tips/warnings based on the task."""
    points = []

    # First step
    if step_num == 1:
        points.append("Start cycle, check materials")

    # Last step
    if step_num == total_steps:
        points.append("Final step — inspect output")

    # Long-duration tasks (6+ seconds)
    if task["duration"] >= 6:
        points.append("Long task — check ergonomics")

    # Short tasks (2 seconds or less)
    if task["duration"] <= 2:
        points.append("Quick step — do not skip")

    return "; ".join(points) if points else ""
