# Submersible Borewell Pump Daily Telemetry & Decision Layer

**Problem** — Rural drinking-water submersible pumps experience frequent motor burnouts because maintenance personnel miss subtle voltage drops, dry-run conditions, and silt load spikes hidden in paper field logs. This software automates raw field-log ingestion, rejects hazardous out-of-spec electrical spikes into an audit log, and computes urgent maintenance decisions before a motor fails.

**User** — Gram Panchayat Water Supply and Borewell Maintenance Technicians responsible for village drinking water assets across rural blocks.

**Input format** — Records in `data/sample.txt` follow a pipe-delimited schema:
`2026-10-01|PUMP-01|220|14.2|OK`
* `2026-10-01`: Log entry date in ISO `YYYY-MM-DD` format.
* `PUMP-01`: Target borewell unit identifier (`PUMP-XX`).
* `220`: Single-phase motor AC voltage in Volts (Physical tolerance: 160V to 280V).
* `14.2`: Motor current draw in Amperes (Operational envelope: 0.0A to 40.0A; values above 16.0A indicate mechanical silt friction).
* `OK`: High-level operational status flag (`OK`, `WARN`, `FAIL`).

**How to run** —
```bash
python main.py
```

**What it produces** —
```text
====================================================================
    VILLAGE BOREWELL PUMP TELEMETRY & DECISION REPORT (FINAL)
====================================================================
Generated On  : 2026-11-03 16:40:12
Source Path   : data/sample.txt
Record Audit  : 14 Valid Processed | 2 Anomalies Flagged
--------------------------------------------------------------------

1. ACTIONABLE MAINTENANCE DECISIONS
--------------------------------------------------------------------
MOST URGENT PUMP UNIT REQUIRING ATTENTION : PUMP-03
OVERCURRENT STRESS ALERTS (>16.0 A)       : PUMP-03
LOW VOLTAGE DIP INCIDENTS (<180 V)        : 0 events

PUMP SERVICE PRIORITY RANKING:
RANK  PUMP ID       FAILS  WARNS    MEAN I(A)   SCORE        STATUS
--------------------------------------------------------------------
1     PUMP-03           1      1        17.93       4  OVERDUE/WARN
2     PUMP-02           0      0        15.00       0        NORMAL
3     PUMP-04           0      0        14.50       0        NORMAL
4     PUMP-01           0      0        14.05       0        NORMAL

2. AGGREGATE SYSTEM METRICS
------------------------------------
METRIC                             VALUE
------------------------------------
Total Valid Records                   14
System Mean Voltage (V)            211.9
System Mean Current (A)            15.45
------------------------------------

3. HARDENED DATA AUDIT · REJECTED ENTRIES
--------------------------------------------------------------------
LINE  REASON                              RAW INPUT
--------------------------------------------------------------------
9     Malformed syntax: Expected YYYY-    2026-10-03|PUMP-03|180|21.0
13    Out of physical bounds: Voltage     2026-10-05|PUMP-01|440|13.8|OK
====================================================================
```

**Known limitations** —
1. Does not detect missing calendar dates when a technician forgets to record telemetry for multiple consecutive days.
2. Rigidly hardcoded to single-phase AC motors (160V–280V); commercial three-phase 415V irrigation pumps will be rejected by the validation boundary.
3. Operates entirely as a local CLI pipeline and lacks automated mobile or cloud notification delivery.

**Future work** —
1. Automated CSV work-order export for local field linemen to load directly into mobile handhelds.
2. Moving-average trend analysis on current draw ($dI/dt$) to forecast mechanical bearing seizure 48 hours prior to motor failure.
3. Cellular GSM/SMS integration to alert Panchayat officers automatically during severe voltage surges.

**Built by** — Shreeya Routray (2502190005) & Ayushi Srivastava (2502190039), MSM, CS-1281, Nov 2026.