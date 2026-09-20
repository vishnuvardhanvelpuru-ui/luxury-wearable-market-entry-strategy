# Power BI report build guide

**Manual Action Required:** Build and save `Case3_Dashboard.pbix` in local Power BI Desktop. No PBIX or live dashboard has been fabricated. The supplied CSVs, Power Query imports, DAX definitions, theme, visual specification and acceptance values are complete. DAX was reviewed against the model, but has not run in the Power BI engine. The HTML preview is a static layout mockup, not a Power BI report.

## 1. Load seven tables
Open a blank report. Transform data → Manage parameters → New parameter `RootFolder`, type Text, with your extracted repository folder plus a final `/` (e.g. `C:/Projects/luxury-wearable-strategy/`). Create seven blank queries named exactly `Strategy`, `Scenario`, `Year`, `Segment`, `Forecast`, `SegmentAnalysis`, `Assumptions`. For each, paste the matching `.pq` file in Advanced Editor. Close & Apply. No Python or MySQL connection is required for the report.

Alternatively Get Data → Text/CSV can load the same files; rename tables exactly as above and apply the types in the `.pq` files. IDs, years, periods, units and counts are whole numbers; monetary amounts and factors are decimal numbers; labels are text. Set keys/year/period to **Do not summarize**. Disable automatic date/time for this file. Use the supplied theme from View → Themes → Browse themes.

## 2. Create relationships
Delete unintended auto-detected relationships. All listed relationships are active, one-to-many, single-direction from dimension to fact:

| One side | Many side |
|---|---|
| Strategy[strategy_id] | Forecast[strategy_id] |
| Scenario[scenario_id] | Forecast[scenario_id] |
| Year[year] | Forecast[year] |
| Strategy[strategy_id] | SegmentAnalysis[strategy_id] |
| Segment[segment_id] | SegmentAnalysis[segment_id] |

`Assumptions` is a disconnected single-row parameter table. Do not connect the two facts. Do not relate Segment to Forecast: economics are at strategy/scenario/year grain, not segment grain. Do not load strategy_summary into the report; its stored NPV would duplicate the DAX calculation. Sort Scenario[scenario] by Scenario[scenario_id]. Hide technical IDs and precomputed cash/discounted_cash from the report field list after validation. Keep them in the model for reconciliation.

## 3. Create measures
Copy one definition at a time from `measures.dax`, excluding comments if desired. Keep the dependency order. Format money as `$#,##0;($#,##0)`, margin/risk/rate as `0.0%`, units/counts as `#,##0`. Keep negative values visible. Do not use implicit SUM of risks, prices or sample WTP.

Finance measures return blank if strategy/scenario context includes several alternatives. This prevents an invalid total across mutually exclusive options. Chart axes and matrix rows supply single-strategy context even with no strategy slicer. Scenario must be single-select. NPV and maximum-risk measures intentionally ignore Year filters; title them `3-year` to avoid confusion. Annual cash and units respect Year. Customer measures require one strategy but do not change with scenario/year because they describe the synthetic survey and base annual demand.

## 4. Build three pages
Canvas 1280 × 720, background #F7F7F4, 24px margins; title 24pt, visual titles 13pt, data labels >=11pt. Navy #243746 for primary data, muted gold #B58A48 for sibling brand, muted red for negative cash and gate failures. Every page footer: `SYNTHETIC DATA · Fictional company · USD · 2027–2029 scenario`. Use no unsupported custom visuals. See `dashboard_mockup.html` for static placement reference.

### Page 1 — Entry decision
No strategy slicer; retain all five strategies for comparison. Scenario slicer is single-select, defaults to Base; sync only to page 3. No Year or Segment slicer on this page.

| Position x,y,w,h | Visual | Exact fields and settings |
|---|---|---|
| 24,16,920,56 | Text | Luxury Brand Paradox — entry decision; subtitle: No entry benchmark = $0 |
| 1020,16,236,64 | Dropdown slicer | Scenario[scenario]; single select ON, select-all OFF |
| 24,104,768,330 | Clustered bar | Y: Strategy[strategy], X: [NPV 3Y]; sort descending NPV; labels USD millions, 2 decimals; zero line; tooltips [Risk Gate], [Max Displacement 3Y], [Brand Haircut] |
| 816,104,440,130 | Text | Base case: no option passes the investment test; scenario selector updates visuals, not this explicitly base-case text |
| 816,250,440,184 | Card + text | [No Entry NPV], $0; text: No entry excludes the optional $100k discovery proposal |
| 24,460,1232,204 | Matrix | Rows Strategy[strategy]; values [NPV 3Y], [Max Displacement 3Y], [Brand Haircut], [Risk Gate], [Decision Gate]; totals OFF; negative NPV red |

Disable cross-filtering from bar to matrix (Format → Edit interactions → None), so clicking one strategy does not hide alternatives. Scenario slicer filters both. Use visual title `3-year NPV by entry package`.

### Page 2 — Customer and price fit
Strategy slicer single-select defaults Separate sibling brand; do not sync to page 1 or page 3. No Scenario/Year slicer. All visuals use SegmentAnalysis. The scenario-independent page deliberately separates customer evidence from financial scenario outputs.

| Position x,y,w,h | Visual | Exact fields and settings |
|---|---|---|
| 24,16,920,56 | Text | Customer and price fit; subtitle: Stated interest plus willingness-to-pay; 30 synthetic respondents per segment |
| 980,16,276,64 | Dropdown slicer | Strategy[strategy], single select ON |
| 24,104,285,90 | Card | [Sample N] |
| 333,104,285,90 | Card | [Qualified Rate]; title Sample qualification rate |
| 642,104,285,90 | Card | [Base Annual Units]; title Calibrated base annual units |
| 951,104,305,90 | Card | MAX(Strategy[price]); title Test price USD |
| 24,224,600,280 | Clustered bar | Y Segment[segment]; X [Base Annual Units]; sort descending; tooltips [Qualified Rate], [Qualified N], [Mean WTP], [Reachable Audience] |
| 648,224,608,280 | Clustered column | X Segment[segment]; Y [Qualified Rate]; data labels percent |
| 24,528,1232,136 | Matrix | Rows Segment[segment]; values [Sample N], [Qualified N], [Mean WTP], [Reachable Audience]; totals ON, mean uses weighted DAX |

Turn chart-to-chart cross-filtering OFF to retain segment comparability. Cards and charts respond to Strategy slicer. Qualification rate is sample-weighted, not audience-weighted; audience weighting is used in projected units. Do not label it market conversion. Detailed four-price sensitivity stays in Excel/CSV to keep this report small.

### Page 3 — Economics and heritage risk
Strategy slicer single-select defaults Separate sibling brand. Scenario slicer single-select defaults Base, synchronized with page 1. No Year slicer; all three annual periods remain visible.

| Position x,y,w,h | Visual | Exact fields and settings |
|---|---|---|
| 24,16,710,56 | Text | Economics and heritage risk |
| 758,16,260,64 | Dropdown slicer | Strategy[strategy] |
| 1040,16,216,64 | Dropdown slicer | Scenario[scenario] |
| 24,104,285,90 | Card | [NPV 3Y] |
| 333,104,285,90 | Card | [Direct Margin] |
| 642,104,285,90 | Card | [Max Displacement 3Y]; title Max annual displacement; subtitle Limit 2.0% |
| 951,104,305,90 | Card | [Brand Haircut]; subtitle Limit 0.5% |
| 24,224,600,260 | Line and clustered column | X Year[year]; column [Company Revenue]; line [Operating Cash]; shared USD axis, zero visible, display millions |
| 648,224,608,260 | Clustered column | X Year[year]; Y [Mechanical Loss], [Brand Loss]; legend measure names; USD thousands |
| 24,510,950,154 | Matrix | Rows Year[year]; values [Wearable Units], [Company Revenue], [Variable Cost], [Fixed Cost], [Mechanical Loss], [Brand Loss], [Operating Cash] |
| 1000,510,256,154 | Card | [Decision Gate] |

Disable chart-to-chart cross-filtering to avoid making three-year cards look annual. Both slicers filter all visuals. Matrix totals valid for flows; do not add prices or risk rates as summed columns.

## 5. Acceptance checks before saving
Compare unrounded values with `../data/processed/strategy_summary.csv` and `../validation/mysql_strategy_summary.csv`. Differences under $0.02 are rounding only. Base scenario: extension -6,274,905.74; sibling -3,519,508.77; partnership -2,545,741.72; licensing -4,183,000.73; hybrid -3,057,718.37. Sibling Base total units 22,156, revenue $18,522,416; max displacement 1.19184%; haircut 0.2%; survey qualified 44/120; base annual units 7,640. [Cash Reconciliation] must equal zero for every strategy/scenario/year.

Test switching all five strategies and three scenarios. Clearing scenario selection must make finance measures blank. Selecting multiple strategies must blank finance cards, while per-strategy chart rows remain valid. No Year filter should change [NPV 3Y]. Segment selections must not change finance data. Confirm totals are hidden on alternative-comparison matrix. Check titles/footer and export three screenshots to `powerbi/screenshots/` after saving the PBIX. Record Power BI version/date and DAX acceptance results in `validation/POWER_BI_CHECKS.md`; until then it remains Manual Action Required.

References: [Microsoft star-schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema), [relationships](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand). The layout and business gates are project design choices.
