# QGRIM 13E — Post-Hardening Regression and Release-Readiness Audit

## Scope and disposition

13E was a strictly read-only audit of the Tier-1 API-hardening artifact `df48f3a` on `qgrim-api-hardening`. No source files, tests, documentation, branches, or historical commits were modified.

The result is **release-readiness pass for a validated engineering baseline**, with the intentionally preserved sampler ambiguity remaining the only official test failure.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| `qgrim-api-decision` | `05b10eb`, unchanged |
| 13D artifact | `df48f3a` |
| 13E branch state | `qgrim-api-hardening`, clean |
| 13E source/test changes | None |

## Regression results

The new Tier-1 API tests passed completely:

```text
46 passed
```

The independent integration matrix also passed completely:

```text
18/18 passed
```

The official pytest suite reported:

```text
150 passed, 1 failed
```

The sole failure remains exactly the deliberately unresolved historical/API ambiguity:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

13E did not modify this behavior, the sampler implementation, or the original test.

## Algorithm integrity

The independent QFT audit remains unchanged. The reconstructed forward QFT has process-style fidelity `0.9986614071991402`, Q4.12 operator unitarity error approximately `0.0017731`, and inverse round-trip maximum error `0.00079617`. These are within the documented fixed-point numerical model and do not indicate a semantic regression.

The independent Grover audit remains exact for its specified contract. The oracle is diagonal with only index 5 negated, oracle reference error is `0.0`, diffusion reference error is approximately `5.55e-16`, one iteration reaches target probability `0.47265625`, and the final norm is `1.0`.

The 12D noise audit remains unchanged: finite legal probabilities operate normally, NaN and infinities are rejected at construction, the non-recursive noise guard passes, and the public/internal PHASE layering remains unchanged.

## API integrity

The 13D boundary behavior remains deliberate and stable:

| Surface | Verified behavior |
|---|---|
| `sample_circuit(shots=0)` | Accepted and returns `{}` |
| Negative sampler shots | `ValueError` |
| Boolean/non-integer sampler shots | `TypeError` |
| Positive CHSH count | Accepted with unchanged useful output |
| Zero/negative CHSH count | `ValueError` |
| Boolean/non-integer CHSH count | `TypeError` |
| Bloch q in `0..3` | Accepted with unchanged coordinates |
| Invalid Bloch q | `TypeError` or deliberate range `ValueError` |
| Valid 16-element fidelity vectors | Unchanged squared-overlap results |
| Wrong-length/non-numeric/non-finite fidelity vectors | Deliberate `TypeError` or `ValueError` |
| `progress=False` | Still unsupported; intentionally unresolved |

The before/after comparison found no change for valid seeded sampling, positive CHSH calls, valid Bloch indices, valid fidelity vectors, or assembly output. All observed differences were the four explicit API hardening decisions.

## Provenance and exact scope

The final provenance chain is:

```text
a504f6c  historical main
   ↓
72edc13  evidence-driven recovery
   ↓
3e88909  engineering reconstruction + numerical hardening
   ↓
05b10eb  documentation/provenance synchronization
   ↓
df48f3a  Tier-1 public API hardening
   ↓
13E      read-only release/readiness verification
```

The 13E working tree is clean. The branch pointers remain fixed at `df48f3a`, `05b10eb`, `3e88909`, `72edc13`, and `a504f6c` as recorded above. No changes were pushed.

The 13D diff remains limited to `QGRIM_ENGINE.py` and the new `test_api_contracts.py`. 13E added no repository modifications.

## Release-readiness classification

13E passes as a post-hardening regression and release-readiness audit. The artifact is internally coherent enough to freeze as the next validated engineering baseline. This does not mean every possible edge behavior has been redesigned: file API consistency, additional low-level API validation, stale-file cleanup, and sampler progress semantics remain separate future engineering decisions.

The remaining official failure is informative rather than hidden. It proves that the repository has not been made artificially green by inventing semantics for `progress=False`.

> QGRIM has crossed from recovery into ordinary engineering maintenance. `df48f3a` is a validated Tier-1 API-hardening artifact suitable for freeze, with its remaining ambiguity and limitations explicitly classified.

## Supporting evidence

- `/home/ubuntu/qgrim_13e_release_matrix.md` — 13E scope and no-fix boundary.
- `/home/ubuntu/qgrim_13e_final_regression.txt` — complete read-only release gate.
- `/home/ubuntu/qgrim_13e_api_tests.txt` — focused API test output.
- `/home/ubuntu/qgrim_13e_integration.txt` — 18-check integration output.
- `/home/ubuntu/qgrim_13e_qft.txt` — QFT operator audit.
- `/home/ubuntu/qgrim_13e_grover.txt` — Grover operator audit.
- `/home/ubuntu/qgrim_13e_noise.txt` — numerical/noise audit.
- `/home/ubuntu/qgrim_13e_api_boundary.txt` — full API boundary probe.
