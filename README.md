# Submersible Borewell Pump Daily Telemetry & Decision Layer

**Problem** — Rural drinking-water submersible pumps burn out frequently because maintenance personnel miss subtle voltage drops, prolonged dry runs, and mechanical silt friction recorded in manual logs. This program ingests raw field logs, discards corrupted or out-of-spec power surges into a transparent audit log, and delivers actionable maintenance decisions identifying overdue and high-risk pumps.

**User** — Gram Panchayat Water Supply and Borewell Maintenance Technicians responsible for village water security across multiple pump blocks.

**Input format** — Plaintext pipe-delimited records stored in `data/sample.txt`:
```text
YYYY-MM-DD|PUMP_ID|VOLTAGE|CURRENT|STATUS