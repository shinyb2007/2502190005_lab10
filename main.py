"""
main.py · Pipeline runner and formatted report generator.
CS-1281 Python Programming Lab · Work Order 10
"""

import datetime
import os
import sys
from datalayer import load, summarise
from logic import evaluate_pump_health


def main():
    data_path = os.path.join("data", "sample.txt")
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Hardening Check 1: Missing file check
    try:
        records, problems = load(data_path)
    except FileNotFoundError as err:
        print(f"[ERROR] Honest Exit: {err}", file=sys.stderr)
        sys.exit(1)

    # Hardening Check 2: Empty file check
    if len(records) == 0 and len(problems) == 0:
        print(
            f"[REFUSED] Empty File: '{data_path}' has no records to process.",
            file=sys.stderr,
        )
        sys.exit(2)

    summary = summarise(records)
    decisions = evaluate_pump_health(records)

    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_path = os.path.join(reports_dir, f"report_{stamp}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=" * 68 + "\n")
        f.write(
            "    VILLAGE BOREWELL PUMP TELEMETRY & DECISION REPORT (FINAL)\n"
        )
        f.write("=" * 68 + "\n")
        f.write(
            f"Generated On  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write(f"Source Path   : {data_path}\n")
        f.write(
            f"Record Audit  : {len(records)} Valid Processed | {len(problems)} Flagged\n"
        )
        f.write("-" * 68 + "\n\n")

        # Section 1: Decisions
        f.write("1. ACTIONABLE MAINTENANCE DECISIONS\n")
        f.write("-" * 68 + "\n")
        f.write(
            f"MOST URGENT PUMP UNIT REQUIRING ATTENTION : {decisions['most_urgent_pump']}\n"
        )
        f.write(
            f"OVERCURRENT STRESS ALERTS (>16.0 A)       : {', '.join(decisions['overcurrent_alerts']) or 'None'}\n"
        )
        f.write(
            f"LOW VOLTAGE DIP INCIDENTS (<180 V)        : {decisions['low_voltage_events']} events\n\n"
        )

        f.write("PUMP SERVICE PRIORITY RANKING:\n")
        f.write(
            f"{'RANK':<6}{'PUMP ID':<12}{'FAILS':>7}{'WARNS':>7}{'MEAN I(A)':>11}{'SCORE':>8}{'STATUS':>14}\n"
        )
        f.write("-" * 68 + "\n")
        for rank, (pid, pdata) in enumerate(decisions["ranked_pumps"], start=1):
            service_label = (
                "OVERDUE/WARN" if pdata["requires_service"] else "NORMAL"
            )
            f.write(
                f"{rank:<6}{pid:<12}{pdata['fails']:>7}{pdata['warns']:>7}{pdata['avg_current']:>11.2f}{pdata['risk_score']:>8}{service_label:>14}\n"
            )
        f.write("\n")

        # Section 2: Operational Averages
        f.write("2. AGGREGATE SYSTEM METRICS\n")
        f.write("-" * 36 + "\n")
        f.write(f"{'METRIC':<24}{'VALUE':>12}\n")
        f.write("-" * 36 + "\n")
        f.write(f"{'Total Valid Records':<24}{summary['total']:>12}\n")
        f.write(f"{'System Mean Voltage (V)':<24}{summary['avg_v']:>12.1f}\n")
        f.write(f"{'System Mean Current (A)':<24}{summary['avg_i']:>12.2f}\n")
        f.write("-" * 36 + "\n\n")

        # Section 3: Data Audit Table
        f.write("3. HARDENED DATA AUDIT · REJECTED ENTRIES\n")
        f.write("-" * 68 + "\n")
        if problems:
            f.write(f"{'LINE':<6}{'REASON':<36}{'RAW INPUT'}\n")
            f.write("-" * 68 + "\n")
            for line_no, reason, raw in problems:
                f.write(f"{line_no:<6}{reason[:34]:<36}{raw}\n")
        else:
            f.write("None. All data rows conformed cleanly.\n")
        f.write("=" * 68 + "\n")

    print("[SUCCESS] Ingestion & Decision pipeline completed.")
    print(f"[DECISION] Most Urgent Unit: {decisions['most_urgent_pump']}")
    print(f"[REPORT] Saved -> {out_path}")


if __name__ == "__main__":
    main()