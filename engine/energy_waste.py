"""
energy_waste.py — 9th Waste: Energy Waste Calculator
Ciliberto et al. (2021) — Energy waste concept in Sustainable Lean Manufacturing.

Calculates wasted energy from idle stations, its cost, and carbon footprint.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class StationEnergyDetail:
    """Energy waste detail for a single station."""
    station_id: int
    idle_time: float           # seconds
    energy_kwh: float          # kWh
    cost: float                # currency
    co2_kg: float              # kg CO2


@dataclass
class EnergyReport:
    """Total energy waste report."""
    total_idle_time: float     # seconds (all stations)
    total_energy_kwh: float    # kWh
    total_cost: float          # currency
    total_co2_kg: float        # kg CO2
    per_station: List[StationEnergyDetail] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_idle_time": round(self.total_idle_time, 4),
            "total_energy_kwh": round(self.total_energy_kwh, 6),
            "total_cost": round(self.total_cost, 4),
            "total_co2_kg": round(self.total_co2_kg, 6),
            "per_station": [
                {
                    "station_id": s.station_id,
                    "idle_time": round(s.idle_time, 4),
                    "energy_kwh": round(s.energy_kwh, 6),
                    "cost": round(s.cost, 4),
                    "co2_kg": round(s.co2_kg, 6),
                }
                for s in self.per_station
            ],
        }


def calculate_energy_waste(
    stations: List[Dict[str, Any]],
    cycle_time: float,
    kwh_per_second: float = 0.002,
    cost_per_kwh: float = 2.5,
    co2_per_kwh: float = 0.47,
) -> EnergyReport:
    """
    Calculate energy waste from station idle times.

    Args:
        stations       : Solver output (each station has total_time and idle_time)
        cycle_time     : Cycle time (seconds)
        kwh_per_second : Energy consumed per second per station (power in kW / 3600)
                         Default: 0.002 kWh/s ~ 7.2 kW power
        cost_per_kwh   : Unit energy cost (currency/kWh)
                         Default: 2.5 (approximate industrial tariff)
        co2_per_kwh    : CO2 emission factor (kg CO2/kWh)
                         Default: 0.47 kg/kWh (grid average)

    Returns:
        EnergyReport dataclass
    """
    per_station = []
    total_idle = 0.0
    total_kwh = 0.0
    total_cost = 0.0
    total_co2 = 0.0

    for s in stations:
        idle = s.get("idle_time", cycle_time - s["total_time"])
        kwh = idle * kwh_per_second
        cost = kwh * cost_per_kwh
        co2 = kwh * co2_per_kwh

        detail = StationEnergyDetail(
            station_id=s["station_id"],
            idle_time=idle,
            energy_kwh=kwh,
            cost=cost,
            co2_kg=co2,
        )
        per_station.append(detail)

        total_idle += idle
        total_kwh += kwh
        total_cost += cost
        total_co2 += co2

    return EnergyReport(
        total_idle_time=total_idle,
        total_energy_kwh=total_kwh,
        total_cost=total_cost,
        total_co2_kg=total_co2,
        per_station=per_station,
    )


def annual_savings(
    before: EnergyReport,
    after: EnergyReport,
    cycles_per_day: int = 480,
    working_days_per_year: int = 250,
) -> Dict[str, float]:
    """
    Compare before/after improvement -> annual savings.

    Args:
        before              : Current state energy report
        after               : Improved state energy report
        cycles_per_day      : Daily cycle count (8h x 60 = 480 default)
        working_days_per_year: Working days per year

    Returns:
        {
            "saved_kwh_per_cycle": float,
            "saved_kwh_annual": float,
            "saved_cost_annual": float,
            "saved_co2_annual": float,
        }
    """
    cycles_per_year = cycles_per_day * working_days_per_year

    saved_kwh = before.total_energy_kwh - after.total_energy_kwh
    saved_cost = before.total_cost - after.total_cost
    saved_co2 = before.total_co2_kg - after.total_co2_kg

    return {
        "saved_kwh_per_cycle": round(saved_kwh, 6),
        "saved_kwh_annual": round(saved_kwh * cycles_per_year, 2),
        "saved_cost_annual": round(saved_cost * cycles_per_year, 2),
        "saved_co2_annual": round(saved_co2 * cycles_per_year, 2),
        "cycles_per_year": cycles_per_year,
    }
