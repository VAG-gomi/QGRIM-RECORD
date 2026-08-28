# QGRIM-RECORD

`QGRIM-RECORD` is the **forensic, recovery, engineering, and release record** for the QGRIM project. It is not a second QGRIM implementation and is not intended to replace the source repositories.

This repository records what was observed, what was reconstructed, what was deliberately engineered, what was independently verified, and what remains unresolved. Source snapshots are labeled by branch and commit so that they cannot be mistaken for new runtime code.

## Current status

The release-oriented engineering artifact is frozen at `321598b` on the `qgrim-packaging` branch of the implementation repository. Its direct-execution release surface is coherent and independently audited. The official test result remains:

```text
150 passed, 1 failed
```

The one failure is intentionally preserved and is documented in [`FAILURE_REGISTER.md`](FAILURE_REGISTER.md). It is not hidden by deleting the test or inventing an unsupported API parameter.

## Provenance sequence

```text
a504f6c  historical baseline
   ↓
72edc13  recovery branch
   ↓
3e88909  engineering reconstruction and numerical hardening
   ↓
05b10eb  documentation and provenance synchronization
   ↓
df48f3a  Tier-1 public API hardening
   ↓
321598b  direct-execution release-surface synchronization
   ↓
QGRIM-RECORD  independent record and evidence archive
```

The historical `main` branch remains immutable. The recovery and engineering branches are preserved separately in the implementation repository.

## Repository map

| Path | Purpose |
|---|---|
| `QGRIM_STATUS.md` | Current verified status and explicit limitations |
| `PROVENANCE.md` | Stage-by-stage history and classification policy |
| `FAILURE_REGISTER.md` | Exact remaining test failure and causal mechanism |
| `RELEASE_RECORD.md` | Release-oriented engineering baseline and acceptance statement |
| `13A_RECOVERY.md` | Recovery and forensic phase index |
| `13B_ENGINEERING.md` | Engineering reconstruction, hardening, and documentation index |
| `13C_API_DECISION.md` | Public API decision record |
| `13D_API_HARDENING.md` | Tier-1 API hardening record |
| `13E_RELEASE_AUDIT.md` | Post-hardening release audit |
| `13F_PACKAGING_AUDIT.md` | Packaging and repository disposition audit |
| `13G-A_PACKAGING_DISPOSITION.md` | Packaging disposition decision |
| `13G-B_RELEASE_SURFACE.md` | Direct-execution release surface synchronization |
| `13G-C_RELEASE_AUDIT.md` | Read-only release-artifact audit |
| `evidence/` | Raw audit output, test output, and forensic traces |
| `reports/` | Detailed phase reports |
| `source-snapshots/` | Labeled snapshots of relevant implementation files |
| `uploaded-context/` | User-supplied cross-project context artifacts, not QGRIM runtime code |

## Important boundaries

The implementation repository is the source of executable behavior. This repository preserves evidence and does not silently repair, delete, or reinterpret that source. In particular, `progress=False` remains an unresolved historical/API contract mismatch.

The QGRIM project uses a four-qubit Q4.12-like fixed-point model. Small numerical deviations are expected and documented. QFT and Grover are validated engineering reconstructions, not claims about the exact historical author intent. `IFX`, `IFZ`, `MARK`, and `REFLECT` are simulator-only reconstructed extensions and are not historical FPGA ISA instructions.

## References

- Implementation repository: `VAG-gomi/QGRIM_-ENGINE-`
- Frozen release-oriented branch: `qgrim-packaging` at `321598b`
- Historical baseline: `main` at `a504f6c`

## License

See the preserved implementation license in the source repository and the copied release snapshot context. This record archive adds documentation and evidence; it does not change licensing terms.

## Author

Manus AI

## Date

2026-08-28
