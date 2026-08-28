# QGRIM Provenance and Maintenance Map

This file records the boundary between what was inherited, what was recoverable from evidence, and what was newly engineered. It is documentation only; it does not alter simulator behavior.

## Branch and commit anchors

```text
a504f6c  main
   │
   └── evidence-driven recovery
       72edc13  qgrim-recovery
           │
           └── post-recovery engineering
               a57f8a7  standard forward-QFT reconstruction
               be28bf0  standard Grover reconstruction
               3e88909  numerical/input hardening
```

| Anchor | Stage | Meaning |
|---|---|---|
| `a504f6c` | Historical | Original repository baseline; preserved on `main` |
| `896cc79`–`72edc13` | Recovery | Test infrastructure reconstruction and evidence-driven repairs |
| `a57f8a7` | Engineering reconstruction | Explicit standard forward-QFT contract; not historical recovery |
| `be28bf0` | Engineering reconstruction | Explicit standard Grover oracle/diffusion contract; simulator-only basis operators |
| `3e88909` | Engineering hardening | Finite `noise_p` validation and non-recursive noise injection |

## Behavior categories

**Historical behavior** means behavior present in the original baseline, whether correct or defective. It is not inferred to be intended merely because it exists in `main`.

**Recovery behavior** means a narrow change supported by surviving tests, source structure, mathematical invariants, or clear implementation evidence. Reconstructed `conftest.py` is recovery infrastructure, but its tolerance literals and seed behavior are explicitly reconstruction choices rather than recovered historical facts.

**Engineering reconstruction** means a new implementation chosen after forensic analysis established that the surviving algorithmic circuit was not the advertised operator. QFT and Grover are in this category. Their mathematical contracts are explicit and independently verified, but their exact original historical intent remains unrecoverable.

**Engineering hardening** means new input validation or robustness work based on observed boundary failures. The `noise_p` contract in `3e88909` belongs here.

**Numerically approximate behavior** is expected wherever Q4.12 quantization is applied. Small norm drift, phase error, and round-trip residuals must be evaluated against the documented fixed-point error budget rather than exact floating-point identities.

**Intentionally unresolved behavior** includes the sampler’s `progress=False` mismatch. One historical test expects the keyword, but the implementation, documentation, call sites, and earlier history do not establish its intended semantics. It remains unsupported until a separate API decision is made.

## File roles

| File or path | Role |
|---|---|
| `QGRIM_ENGINE.py` | Primary assembler, simulator, analysis helpers, built-in circuits, CLI, and REPL |
| `test_*.py` | Surviving repository tests; ordinary pytest does not discover extensionless `test_y_py` |
| `conftest.py` | Reconstructed test infrastructure; not claimed to be the historical file |
| `README.md` | User/developer documentation synchronized with the frozen engineering artifact |
| `PROVENANCE.md` | This provenance and maintenance map |
| `main.py` | Minimal workspace greeting; not the QGRIM engine entry point |
| `screen_shot.py` | Captured menu text; not executable Python |
| `QGRIM_Engine _V2.2 ( Future )` | Retained placeholder containing `Future version` |
| `replit_readme.md` | Broader workspace/blueprint description not represented by the current tracked tree |

The auxiliary files are retained pending a separate packaging/repository-cleanup audit. They are not silently deleted or promoted to primary runtime surfaces.

## Freeze rule

The validated reconstructed engineering artifact is `3e88909` on `qgrim-engineering-qft-grover`. Future work must begin on a new branch and be labeled as documentation, packaging, API, feature, or hardening engineering. The historical `main` branch, the `qgrim-recovery` branch, and the forensic record must remain preserved.
