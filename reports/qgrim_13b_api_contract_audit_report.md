# QGRIM 13B — Public API Contract Audit

## Scope and disposition

13B was a **read-only API audit** of the documentation-synchronized branch `qgrim-docs-sync` at `05b10eb`, descended from the frozen engineering artifact `3e88909`. No source files, tests, API behavior, branches, or historical commits were modified.

The audit establishes that QGRIM’s primary documented workflows are usable and internally coherent, while several low-level and edge-case APIs lack explicit validation contracts. These are maintenance findings for a future API-design phase, not recovery defects.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| Engineering baseline | `3e88909` |
| Documentation branch | `05b10eb`, clean |
| Test files modified | None |
| Sampler compatibility | `progress=False` intentionally unresolved |

## Public interface inventory

The module-level public functions are `assemble`, `disassemble`, `hex_export`, `fidelity`, `draw_circuit`, `sample_circuit`, `render_histogram`, `chsh_test`, `list_circuits`, `save_program`, `load_program`, `repl`, `main_menu`, `cli`, and the menu helpers. The primary public class is the `QGRIMSim` dataclass; `AsmError` is the public assembler exception type.

`QGRIMSim` exposes both high-level methods and low-level state fields through its dataclass constructor. High-level methods include `reset`, `clone`, `run`, `state_formula`, `bloch_sphere`, `bloch_sphere_str`, `entanglement_entropy`, `fidelity`, `dump`, `probability_table`, and `snapshot`. Lower-level methods include `step`, gate implementations, and noise helpers.

| Surface | Current contract evidence |
|---|---|
| `assemble(source)` | Returns 16-bit instruction words; malformed source raises `AsmError` |
| `disassemble(words)` | Returns human-readable assembly lines for valid word lists |
| `hex_export(words)` | Returns FPGA-style text for valid words |
| `QGRIMSim(...)` | Constructs a 16-state simulator; validates `noise_p` |
| `QGRIMSim.run(program)` | Executes assembled words and returns `None`; empty program is a no-op |
| `QGRIMSim.reset()` | Restores `|0000⟩`, clears measurement/trace state, returns `None` |
| `QGRIMSim.clone()` | Returns a simulator copy including state and runtime fields |
| `bloch_sphere(q)` | Returns `(x,y,z)` for ordinary valid qubit use |
| `entanglement_entropy(partition_a)` | Returns entropy in bits; validates supplied partition entries |
| module/global `fidelity` | Returns squared overlap for compatible state sequences |
| `sample_circuit` | Returns bitstring-count dictionary for integer shot counts |
| `save_program` | Returns success/error text and writes a file |
| `load_program` | Returns `(source_text, error_message)` rather than raising for missing files |
| `chsh_test` | Returns formatted result text for positive shot counts |

The runtime inventory reports 19 built-in circuits, matching the synchronized README.

## Accepted and rejected input behavior

The assembler contract is the clearest public boundary. Valid hardware instructions, simulator-only extensions, macros, qubit-domain checks, phase-field checks, and basis-field checks are handled through `AsmError`. Entropy and noise use deliberate `TypeError` and `ValueError` categories.

| Probe | Observed result | Classification |
|---|---|---|
| Valid QASM | Accepted; words returned | Coherent |
| Unknown mnemonic or malformed operands | `AsmError` | Explicit contract |
| Qubit outside `0..3` | `AsmError` | Explicit contract |
| Public phase index outside `0..15` | `AsmError` | Explicit 4-bit field contract |
| Entropy duplicate/negative/out-of-range entry | `ValueError` | Explicit contract |
| Entropy non-integer entry | `TypeError` | Explicit contract |
| `noise_p` finite real in `[0,1]` | Accepted | Explicit 12D contract |
| `noise_p` NaN/infinite/out of range | `ValueError` | Explicit 12D contract |
| `noise_p` boolean/string/None | `TypeError` | Explicit 12D contract |
| Valid seeded sampling | Deterministic count dictionary | Coherent |
| `shots=0` or negative | Empty dictionary | Underspecified edge behavior |
| Non-integer `shots` | Python `TypeError` | Low-level leakage |

## API inconsistencies and future engineering findings

The following observations are not being repaired in 13B because the phase is explicitly read-only.

First, `bloch_sphere(q)` does not perform explicit qubit-domain validation. `q=-1` leaks `ValueError: negative shift count`, while `q=4` is accepted and returns a meaningless coordinate computed with a mask outside the four-qubit state. This is a concrete future API-hardening candidate.

Second, `QGRIMSim` is a dataclass whose constructor exposes `state`, `pc`, `halted`, `measurements`, `pi`, `trace`, and `_rng` as initialization fields. These are useful low-level controls but are not clearly separated from the supported public API. A future API design should decide whether to retain state injection or provide a narrower constructor.

Third, `QGRIMSim.fidelity` assumes a 16-element comparison sequence and leaks `IndexError` for short input, while the module-level `fidelity` can compare short sequences without enforcing the simulator’s 16-amplitude domain. State length and normalization contracts are not explicit.

Fourth, `chsh_test(0)` raises `ZeroDivisionError`, while a negative shot count is accepted and produces formatted output. `sample_circuit` similarly accepts zero and negative shot counts as empty runs but leaks native `TypeError` for floats and `None`. These are coherent enough for current internal call paths but lack deliberate public validation.

Fifth, file APIs intentionally use return-value error reporting: `load_program` returns `(None, message)` for missing files, while `save_program` returns an error string. This is a valid style but differs from assembler and numerical APIs that raise exceptions. A future library-facing API should document this distinction or normalize it deliberately.

Sixth, `render_histogram` accepts an empty count dictionary with zero shots but does not validate that the count total equals the supplied shot count. `draw_circuit` and other formatting helpers likewise rely on native Python errors for invalid objects.

## Sampler decision

The sampler’s `progress=False` question remains intentionally unresolved. The public signature is:

```text
sample_circuit(source, shots=1024, seed=0xACE1, noise_p=0.0)
```

The original test expects `progress=False`, but the implementation, documentation, call sites, and history do not establish whether this was intended as a display flag, a planned feature, or a stale test contract. The 13B decision is therefore:

> Do not add compatibility behavior and do not alter the original test during the API audit.

A future 13D API decision may retain the unsupported keyword or introduce an actual documented progress contract with tests. Either would be new engineering, not recovery.

## Documentation consistency

The synchronized README and `PROVENANCE.md` correctly distinguish historical baseline, recovery branch, engineering reconstruction, hardening, numerical approximation, and intentionally unresolved sampler behavior. The CLI ISA help now lists `IFX`, `IFZ`, `MARK`, and `REFLECT` as simulator-only extensions.

The documentation is consistent with the current QGRIM source registry and the new noise contract. The remaining mismatch is conceptual rather than factual: several low-level methods are importable and callable but are not clearly labeled as public API versus internal implementation. That is a future API-documentation task.

## Final classification

13B passes as a read-only audit. The primary assembler → simulator → measurement → sampling → analysis workflows are coherent for their demonstrated inputs. Explicit contracts exist for assembler errors, entropy partitions, noise probability inputs, simulator-only extensions, and algorithmic reconstructions.

The audit also identifies a bounded set of API hardening candidates: explicit Bloch qubit validation, shot-count validation, CHSH shot validation, state-length/normalization checks for fidelity, constructor-field exposure, histogram count validation, and a deliberate file-error policy. None was changed in 13B.

The repository remains clean on `qgrim-docs-sync` at `05b10eb`; `main`, `qgrim-recovery`, and `qgrim-engineering-qft-grover` remain unchanged. Future work should proceed as a new API-design phase, beginning with the deliberate sampler decision only after deciding whether these broader contract issues have priority.

## Supporting artifacts

- `/home/ubuntu/qgrim_13b_api_baseline.txt` — branch and baseline state.
- `/home/ubuntu/qgrim_13b_api_inventory.txt` — public signatures, dataclass fields, and built-in registry.
- `/home/ubuntu/qgrim_13b_api_boundary_probe.txt` — accepted/rejected input observations.
- `/home/ubuntu/qgrim_13b_consistency_audit.txt` — documentation and call-site consistency checks.
- `/home/ubuntu/qgrim_13a_final_verification.txt` — inherited post-documentation regression evidence.
