# 13G-A — Packaging Disposition

The read-only disposition phase traced suspicious files through references, imports, Git history, and direct-execution behavior. The result was a conservative decision not to delete or move artifacts without stronger evidence.

The primary release surface is the direct-execution runtime, documentation, license, reconstructed test infrastructure, tests, and explicit release manifest. The workspace files are retained as unresolved or archival context and excluded from the primary release surface.

Formal pip packaging, package restructuring, and historical cleanup were deferred as independent future engineering tracks. This decision preserved the frozen `df48f3a` behavior.

See `reports/qgrim_13g_packaging_audit_report.md` and the corresponding trace in `evidence/`.
