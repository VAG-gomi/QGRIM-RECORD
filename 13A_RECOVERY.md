# 13A — Recovery and Forensic Phase Index

This record indexes the recovery work performed against the surviving QGRIM repository. Recovery preserved `main` and used isolated checkpoints rather than rewriting history.

## Recovery checkpoints

| Checkpoint | Scope | Classification |
|---|---|---|
| `896cc79` | Reconstructed missing `conftest.py` from surviving tests and engine | Recovery infrastructure; not claimed historical original |
| `baca14c` | Removed the parse barrier caused by four stray non-Python lines | Minimum structural recovery |
| `73f29f3` | Enforced valid qubit domain `0..3` | Recovery repair |
| `af21a5c` | Used the smaller reduced side for entropy | Engineering repair based on measured bottleneck |
| `6d41f78` | Replaced defective degenerate-spectrum iteration with Hermitian Jacobi diagonalization | Recovery repair of observed numerical failure |
| `c8aaafd` | Corrected Bloch Y sign | Recovery repair under standard coordinate convention |
| `18926db` | Added simulator-only `IFX`/`IFZ` for teleportation control | Engineering reconstruction; not historical ISA recovery |
| `72edc13` | Validated entropy partition inputs | Engineering hardening |

## Forensic decisions

QFT was shown not to match standard three-qubit QFT under tested conventional interpretations. Grover’s surviving oracle and diffusion were shown not to implement the advertised algorithm. Neither was repaired during forensic phases; later repairs were separately labeled engineering reconstruction.

The sampler `progress=False` expectation was isolated as an API binding failure with no recoverable semantics. It remains preserved in the failure register.

## Detailed records

Detailed reports and raw audit outputs are preserved in `reports/` and `evidence/`, including the phase 10 behavioral audit and phase 11A–11G reports.

## Boundary

This file records recovery and forensic work. It does not claim that any reconstructed helper, tolerance, API, or algorithm exactly reproduces lost historical source.
