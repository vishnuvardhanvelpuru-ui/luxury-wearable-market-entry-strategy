# Validation report

Checked 19 September 2026. All business inputs and outputs are synthetic.

| Layer | Work actually performed | Result |
|---|---|---|
| Raw data | 120 unique people; 600 unique person/strategy pairs; 30 people per segment; valid keys and binary interest | Passed |
| MySQL | Schema, seed, analysis views and quality checks executed on MySQL 8.0.46 in an isolated local instance | Passed |
| SQL reconciliation | 20 segment rows, 45 annual forecast rows and 15 strategy/scenario rows compared column by column with independent Python calculations | Passed |
| Price sensitivity | Four price points executed in MySQL and reconciled to generated outputs and Excel formulas | Passed |
| Excel | 15 NPVs, all forecast and segment results, and four price NPVs compared with reference outputs; no formula-error cells | Passed |
| Exported workbook | Saved XLSX cached results independently read from XML, not only in-memory calculations; all cash rows and 15 NPVs reconciled | Passed |
| Workbook appearance | All 12 sheets rendered and reviewed; helper header clipping corrected; readable numeric formats applied | Passed |
| Sensitivity | Approximate break-even thresholds identify volume/risk trade-off; licensing has negative risk-adjusted unit contribution | Reviewed |
| Power BI dataset | 45 forecast rows and 20 segment rows use unique composite keys and matching dimension IDs | Passed |
| DAX / PBIX | DAX definitions and filter guards reviewed; not executed in the Power BI engine | Manual Action Required |

`mysql_reconciliation.json` records maximum absolute differences. Forecast and NPV differences are below $0.000001; the largest segment difference is $0.000034 due to SQL AVG precision. Acceptance tolerance is $0.02 for currency; IDs and whole wearable units match exactly. These are consistency checks, not empirical validation of synthetic assumptions.

The initial comparison exposed Python banker rounding vs MySQL/Excel half-up rounding at a half-unit boundary. Positive forecast rounding was made consistent; all reported results use the corrected units. Co-branding Base units are 10,049.

Excel authoring runtime exported successfully but returned a nonzero process code during teardown. The finished XLSX was independently inspected as a valid ZIP/XML workbook, its cached formula results were reconciled, and its rendered sheets reviewed. No unverified success is inferred from the process exit code.

## Evidence files
- `mysql_segment_analysis.csv`, `mysql_forecast.csv`, `mysql_strategy_summary.csv`: actual MySQL result exports.
- `03_analysis.txt`, `04_quality_checks.txt`, `mysql_pricing.txt`: actual query outputs.
- `excel_reconciliation.json`, `excel_error_scan.json`: formula results and zero-error scan.
- `scripts/check_outputs.py`: standalone repeatable delivered-file checks.

## Manual completion criteria
Follow `powerbi/BUILD_GUIDE.md`, run all strategy/scenario and filter checks, then save the PBIX and three screenshots. Only then replace the pending status in `POWER_BI_CHECKS.md`. A static HTML mockup is provided for layout guidance and is never represented as a Power BI screenshot or dashboard.
