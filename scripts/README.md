# Reproduction

Python 3.10+ standard library: `python scripts/generate_case.py` recreates seed 307, input CSVs, SQL seed/views and core CSV analysis including sensitivity. It overwrites the original synthetic sample. `python scripts/check_outputs.py` validates outputs and delivered Excel caches. Run after any change.

MySQL 8.0+: execute SQL scripts in filename order in Workbench. No password or server-specific path is stored here. Actual results from MySQL 8.0.46 are supplied in validation/.

Excel authoring: `scripts/build_excel.mjs` uses Node.js and `@oai/artifact-tool` (authoring runtime 2.8.58+ API). This library is an optional environment dependency, not bundled. Run `node scripts/build_excel.mjs` only where that package is available. The delivered XLSX itself is standalone and recalculates with standard Excel formulas. Building it checks every forecast and segment output plus NPV and pricing, then renders sheet previews into ignored work/. A runtime inspection sidecar can be ignored. Do not commit node_modules or inspection sidecars.

No download, package installation, API key or live connection is necessary to inspect the delivered CSVs, SQL, workbook or Power BI specification. The generator is deterministic; it does not fetch public sources. Public sources were manually reviewed at the recorded date.
