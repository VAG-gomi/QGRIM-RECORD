# QGRIM Provenance

This record separates historical facts from recovery inferences and later engineering decisions. Commit identifiers refer to the implementation repository `VAG-gomi/QGRIM_-ENGINE-`.

## Provenance chain

| Stage | Reference | Classification | Meaning |
|---|---|---|---|
| Historical source | `main` / `a504f6c` | Historical artifact | Original surviving repository state; preserved unchanged |
| Test infrastructure | `896cc79` | Recovery | Reconstructed missing `conftest.py`; not claimed to be the original file |
| Syntax barrier | `baca14c` | Recovery | Minimum structural repair to make the engine parse |
| Qubit validation | `73f29f3` | Recovery repair | Enforced the documented four-qubit domain |
| Entropy reduction | `af21a5c` | Engineering repair | Smaller-side reduced-density calculation |
| Eigenvalue solver | `6d41f78` | Recovery repair | Replaced defective degenerate-spectrum iteration |
| Bloch coordinates | `c8aaafd` | Recovery repair | Corrected standard Bloch Y sign |
| Teleportation control | `18926db` | Engineering reconstruction | Added simulator-only `IFX`/`IFZ` control semantics |
| Entropy validation | `72edc13` | Engineering hardening | Rejected duplicate/invalid partition indices |
| Algorithm reconstruction | `a57f8a7` and `be28bf0` | New engineering | Reconstructed standard forward QFT and four-qubit Grover |
| Acceptance baseline | `be28bf0` | Validated engineering artifact | Integrated QFT/Grover engineering baseline |
| Numerical hardening | `3e88909` | New engineering | Validated finite `noise_p` and blocked recursive noise injection |
| Documentation | `05b10eb` | Maintenance | Synchronized README, provenance, and ISA documentation |
| API hardening | `df48f3a` | New engineering | Added Tier-1 public API input contracts and tests |
| Release surface | `321598b` | Maintenance | Added direct-execution release manifest and `test_y_py` disclosure |

## Frozen branches

`main` remains the immutable historical artifact. `qgrim-recovery` preserves the recovery sequence. `qgrim-engineering-qft-grover`, `qgrim-docs-sync`, `qgrim-api-hardening`, and `qgrim-packaging` preserve later engineering stages. None of these branches may be rewritten or conflated with historical source.

## Engineering extensions

`IFX`, `IFZ`, `MARK`, and `REFLECT` are simulator-only reconstructed extensions. They are not claims about the historical hardware ISA and are not intended for FPGA execution.

## Historical uncertainty

The exact original intent of the QFT and Grover circuits cannot be recovered from the surviving specification, so their repairs are explicitly mathematical engineering reconstructions. The `progress=False` test expectation is retained as unresolved because no surviving implementation or history establishes its intended semantics.

## Record policy

Files in this repository are evidence, reports, snapshots, and context. They are not a second implementation. A copied source snapshot is labeled with its originating branch and commit and must not be edited as if it were the runtime source.

## Author and date

Manus AI, 2026-08-28.
