# 13G-C — Release Artifact Audit

The read-only 13G-C audit confirmed that every required direct-execution release-surface file exists, no excluded workspace artifact is required by the primary manifest, and the source checkout remains reproducible through `--help`, `--list`, `--isa`, representative `--run`, and module import.

The runtime uses only the standard library. The 46 focused API tests, 18-check integration matrix, QFT audit, Grover audit, and noise audit remained passing. The official suite remained 150 passed and one failure: `progress=False` is rejected before `sample_circuit()` execution.

The branch and historical pointers remained clean and unchanged. The result was to freeze `321598b` as a release-oriented engineering baseline without implying formal installer packaging.

See the full report in `reports/qgrim_13g_c_release_audit_report.md` and raw outputs in `evidence/`.
