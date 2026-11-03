"""
logic.py · Core decision computation engine.
Evaluates pump records to calculate maintenance priorities.
"""


def evaluate_pump_health(records: list[dict]) -> dict:
    if not records:
        return {
            "ranked_pumps": [],
            "pump_summary": {},
            "overcurrent_alerts": [],
            "low_voltage_events": 0,
            "most_urgent_pump": "None",
        }

    stats = {}
    low_voltage_events = 0

    for r in records:
        pid = r["pump_id"]
        v = r["voltage"]
        i = r["current"]
        status = r["status"]

        if pid not in stats:
            stats[pid] = {
                "total_runs": 0,
                "fails": 0,
                "warns": 0,
                "currents": [],
                "voltages": [],
            }

        stats[pid]["total_runs"] += 1
        stats[pid]["currents"].append(i)
        stats[pid]["voltages"].append(v)

        if status == "FAIL":
            stats[pid]["fails"] += 1
        elif status == "WARN":
            stats[pid]["warns"] += 1

        if v < 180:
            low_voltage_events += 1

    pump_summary = {}
    for pid, data in stats.items():
        avg_i = sum(data["currents"]) / len(data["currents"])
        avg_v = sum(data["voltages"]) / len(data["voltages"])
        # Risk formula: (2 * FAIL) + (1 * WARN) + (1 if mean current > 16.0A)
        risk_score = (
            (data["fails"] * 2) + data["warns"] + (1 if avg_i > 16.0 else 0)
        )

        pump_summary[pid] = {
            "total_runs": data["total_runs"],
            "fails": data["fails"],
            "warns": data["warns"],
            "avg_current": round(avg_i, 2),
            "avg_voltage": round(avg_v, 1),
            "risk_score": risk_score,
            "requires_service": (risk_score >= 2 or data["fails"] > 0),
        }

    # Rank pumps descending by urgency
    ranked_pumps = sorted(
        pump_summary.items(),
        key=lambda item: (
            item[1]["risk_score"],
            item[1]["fails"],
            item[1]["avg_current"],
        ),
        reverse=True,
    )

    overcurrent_alerts = [
        pid for pid, d in pump_summary.items() if d["avg_current"] > 16.0
    ]
    most_urgent = ranked_pumps[0][0] if ranked_pumps else "None"

    return {
        "ranked_pumps": ranked_pumps,
        "pump_summary": pump_summary,
        "overcurrent_alerts": overcurrent_alerts,
        "low_voltage_events": low_voltage_events,
        "most_urgent_pump": most_urgent,
    }