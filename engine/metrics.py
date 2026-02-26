"""
metrics.py — Line Balancing Performance Metrics
Computes classic ALB metrics and Kaizen/I4.0 bottleneck scores.
"""

import math
from typing import List, Dict, Any


def line_efficiency(stations: List[Dict], cycle_time: float) -> float:
    """
    Line efficiency (%) = sum(station_loads) / (n x CT) x 100
    100% = perfect balance.
    """
    n = len(stations)
    if n == 0 or cycle_time <= 0:
        return 0.0
    total_work = sum(s["total_time"] for s in stations)
    return round((total_work / (n * cycle_time)) * 100, 2)


def balance_delay(stations: List[Dict], cycle_time: float) -> float:
    """
    Balance delay (%) = 100 - line efficiency
    0% = perfect balance (no idle time).
    """
    return round(100 - line_efficiency(stations, cycle_time), 2)


def smoothness_index(stations: List[Dict], cycle_time: float) -> float:
    """
    Smoothness Index (SI) = sqrt(sum((ST_max - ST_i)^2))
    ST_max = highest station load
    SI = 0 -> perfect balance.
    """
    if not stations:
        return 0.0
    times = [s["total_time"] for s in stations]
    max_time = max(times)
    si = math.sqrt(sum((max_time - t) ** 2 for t in times))
    return round(si, 4)


def theoretical_min_stations(total_work_content: float, cycle_time: float) -> int:
    """
    Theoretical minimum number of stations = ceil(total_work / CT)
    """
    if cycle_time <= 0:
        return 0
    return math.ceil(total_work_content / cycle_time)


def bottleneck_score(stations: List[Dict], cycle_time: float) -> List[Dict]:
    """
    Bottleneck score per station (%).
    Score = (station_load / cycle_time) x 100
    100% = fully loaded (potential bottleneck).
    """
    results = []
    for s in stations:
        score = round((s["total_time"] / cycle_time) * 100, 2) if cycle_time > 0 else 0
        results.append({
            "station_id": s["station_id"],
            "load_percent": score,
            "is_bottleneck": score >= 90,  # 90%+ -> bottleneck warning
        })
    return results


def compute_all_metrics(
    stations: List[Dict],
    cycle_time: float,
    total_work_content: float,
) -> Dict[str, Any]:
    """
    Compute all metrics at once.

    Returns:
        {
            "line_efficiency": float,
            "balance_delay": float,
            "smoothness_index": float,
            "num_stations": int,
            "theoretical_min_stations": int,
            "cycle_time": float,
            "total_work_content": float,
            "bottleneck_scores": [...]
        }
    """
    return {
        "line_efficiency": line_efficiency(stations, cycle_time),
        "balance_delay": balance_delay(stations, cycle_time),
        "smoothness_index": smoothness_index(stations, cycle_time),
        "num_stations": len(stations),
        "theoretical_min_stations": theoretical_min_stations(
            total_work_content, cycle_time
        ),
        "cycle_time": cycle_time,
        "total_work_content": total_work_content,
        "bottleneck_scores": bottleneck_score(stations, cycle_time),
    }
