# Record Scope Policy

`QGRIM-RECORD` is an evidence and provenance repository. It is not a second QGRIM implementation, a release package, or an automatically generated mirror.

The archive may contain labeled source snapshots, test snapshots, uploaded context artifacts, reports, and raw audit outputs. A snapshot is historical evidence or a release record and must not be edited to alter executable behavior.

The implementation repository remains the authority for runtime source. The historical `main` branch and recovery branches remain outside this repository and are preserved in their original Git history.

The archive intentionally records an imperfect but honest verification result: 150 official tests passed and one historical/API contract test remains unresolved. No content in this archive may claim that QGRIM is fully green or that the exact lost author intent has been recovered.

Future changes should add new dated or phase-labeled records rather than rewrite prior evidence. Any future API implementation, packaging conversion, cleanup, or feature work must be recorded as a separate engineering decision in the implementation repository and then referenced here.

## Author and date

Manus AI, 2026-08-28.
