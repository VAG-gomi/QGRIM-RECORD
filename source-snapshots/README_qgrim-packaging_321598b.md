# QGRIM Engine v2.1

QGRIM is a **classical, four-qubit state-vector simulator** implemented in a single Python module. It tracks 16 complex amplitudes, applies Q4.12-style fixed-point quantization at the simulator’s stored-state boundaries, supports Born-rule measurement and collapse, and provides a small assembler, simulator, sampler, analysis helpers, CLI, and interactive REPL.

QGRIM is not a quantum computer and does not provide quantum speedup. It runs quantum-circuit mathematics on a conventional CPU. The hardware-facing descriptions in this repository refer to a proposed FPGA-oriented ISA/model, not physical qubits.

## Current validated artifact

The current engineering artifact is `3e88909` on the `qgrim-engineering-qft-grover` branch. It is a validated post-recovery reconstruction, not a claim that every line reflects the original author’s unrecoverable intent.

The repository has three important provenance anchors:

| Reference | Meaning |
|---|---|
| `a504f6c` on `main` | Immutable historical repository baseline |
| `72edc13` on `qgrim-recovery` | Evidence-driven recovery and validation branch |
| `3e88909` on `qgrim-engineering-qft-grover` | Frozen engineering reconstruction plus numerical/input hardening |

The engineering branch contains two explicitly reconstructed algorithmic contracts. The three-qubit QFT is a standard forward QFT with q0 as the least significant bit. Grover is one standard four-qubit iteration marking basis index 5 (`|0101⟩` under the same convention). These implementations were added after forensic analysis showed that the surviving historical circuits did not implement their advertised operators.

The final hardening commit defines `noise_p` as a finite real probability in `[0.0, 1.0]`, rejects invalid values deliberately, and prevents a noise-triggered Pauli operation from recursively re-entering the noise injector.

## Running QGRIM

The primary runtime is `QGRIM_ENGINE.py` and requires only the Python standard library.

```bash
python3 QGRIM_ENGINE.py --list
python3 QGRIM_ENGINE.py --run bell
python3 QGRIM_ENGINE.py --run grover
python3 QGRIM_ENGINE.py --run qft
python3 QGRIM_ENGINE.py --shots bell 512
python3 QGRIM_ENGINE.py --noise 0.02 --run bell
python3 QGRIM_ENGINE.py --isa
python3 QGRIM_ENGINE.py --help
```

The repository’s test infrastructure uses pytest. The extensionless `test_y_py` file is intentionally not discovered by ordinary pytest; external expanded test counts must be reported separately from the official suite.

## Built-in circuits

The current source registry contains **19 built-in circuits**:

`bell`, `bell_nomeas`, `ghz`, `cluster4`, `deutsch`, `deutsch_balanced`, `bv`, `grover`, `qft`, `teleport`, `superdense`, `phase_kickback`, `toffoli`, `superpos_all`, `t_gate`, `qrng`, `y_gate`, `cz_demo`, and `qpe`.

The built-in registry is a collection of demonstrations and test fixtures. The presence of a circuit does not by itself establish mathematical correctness; the repaired QFT and Grover contracts are supported by separate operator audits.

## Instruction and simulator boundaries

The assembler encodes 16-bit words as `[15:12] opcode | [11:8] A | [7:4] B | [3:0] IMM`. Hardware-oriented instructions include `H`, `X`, `CNOT`, `MEASURE`, `PHASE`, `INIT`, `SWAP`, `LOAD_AMP`, `TRACE`, `WAIT`, and `HALT`. Macro aliases include `S`, `T`, `Z`, `SDG`, `TDG`, `CX`, `NOT`, `CY`, `CH`, and `TOFFOLI`.

The simulator also supports software-only extensions that are not sent to FPGA hardware:

| Extension | Meaning | Status |
|---|---|---|
| `Y`, `CZ`, `CCX`, `RZ` | Simulator software extensions and aliases | Existing software behavior |
| `IFX m q` | Apply X to q if stored measurement m is 1 | Engineering reconstruction for teleportation control |
| `IFZ m q` | Apply Z-equivalent correction to q if stored measurement m is 1 | Engineering reconstruction for teleportation control |
| `MARK basis` | Negate exactly one selected basis amplitude | Engineering-only Grover primitive |
| `REFLECT basis` | Negate every basis amplitude except the selected basis | Engineering-only Grover primitive |

`IFX`, `IFZ`, `MARK`, and `REFLECT` use reserved instruction fields for simulator execution. They are not historical hardware-ISA claims and must not be exported as if they were FPGA-compatible operations.

## Numerical model and limitations

QGRIM uses a Q4.12-like representation: the stored real and imaginary components are quantized on a grid with step `1/4096`. Repeated operations can therefore introduce small norm and phase errors. A single Hadamard may produce norm approximately `0.999786`; this is an expected numerical characteristic of the model, not a unitary-operator proof failure.

The repaired QFT matches its exact forward-QFT reference within the measured Q4.12 error budget. In the independent audit, process-style fidelity was approximately `0.99866` and a random-state forward/inverse round trip had maximum error on the order of `8e-4`. Grover’s basis-phase oracle and diffusion operator are exactly matched by the simulator-only primitives in the tested operator construction, and one iteration reaches target probability `0.47265625` for index 5.

Entropy uses a smaller-side reduced-density calculation and a complex-Hermitian Jacobi eigensolver. Valid partitions include empty and full cuts; duplicate, negative, out-of-range, and non-integer entries are rejected. Bloch coordinates, teleportation branch corrections, measurement collapse, and seeded sampling have been independently audited.

The noise input contract is finite real `noise_p` in `[0,1]`. Invalid values raise deliberate `TypeError` or `ValueError` exceptions. The sampler’s `progress=False` behavior remains intentionally unresolved: one historical test expects that keyword, but the surviving implementation, documentation, call sites, and history do not establish what it was meant to do. It has not been added merely to make the test count green.

## Verification status

The official pytest suite currently reports:

```text
104 passed, 1 failed
```

The one failure is the preserved sampler/API ambiguity:

```text
sample_circuit(..., progress=False)
TypeError: unexpected keyword argument 'progress'
```

The engineering branch’s independent acceptance matrix passes all 18 integration checks. This includes core gates, entropy, Bloch coordinates, teleportation, QFT, Grover, measurement, sampling, noise, and API boundaries. The official suite count is intentionally not represented as fully green.

## Provenance and file roles

The project’s epistemic stages are:

```text
historical artifact → evidence-driven recovery → engineering reconstruction → input hardening → release/readiness audit
```

`QGRIM_ENGINE.py` is the primary runtime and assembler. `test_*.py` files are the surviving tests; `conftest.py` is reconstructed recovery infrastructure and is explicitly not claimed to be historical. `README.md`, `PROVENANCE.md`, and `RELEASE_SURFACE.md` are synchronized maintenance documentation.

The intended distribution is a direct-execution source surface, not an installer package. The exact release surface is documented in [`RELEASE_SURFACE.md`](RELEASE_SURFACE.md): it includes `QGRIM_ENGINE.py`, the primary documentation and license, `conftest.py`, the standard `test_*.py` files, and the separately listed extensionless `test_y_py`. Ordinary `pytest` does not discover `test_y_py`; complete verification requires a separate explicit harness, and the file should not be renamed silently.

Several tracked files are auxiliary or stale and are not part of the primary direct-execution release surface. `main.py` is a minimal workspace greeting. `screen_shot.py` is captured menu text rather than executable Python. `QGRIM_Engine _V2.2 ( Future )` is a placeholder containing `Future version`. `replit_readme.md` describes a broader workspace/blueprint layout that is not represented by this repository’s current tracked tree. `pyproject_toml.`, `uv.lock`, and `.npmrc` are retained workspace/package residue rather than active QGRIM packaging metadata. These files are retained pending a separate packaging/cleanup decision; they have not been deleted, renamed, or moved merely because they look unusual.

## Maintenance boundary

Recovery is complete. The current engineering artifact is frozen for maintenance and release-readiness purposes. Future changes should begin on a new branch and be labeled as documentation, packaging, API, feature, or hardening engineering. They should not rewrite `main`, `qgrim-recovery`, or the forensic record.
