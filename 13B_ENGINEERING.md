# 13B — Engineering Reconstruction and Hardening Index

After recovery and forensics, QGRIM entered ordinary engineering. These changes were made on descendants of the recovered artifact and were never represented as historical recovery.

## Algorithm reconstruction

Commit `a57f8a7` reconstructed a standard forward three-qubit QFT under an explicit positive-exponent convention with q0 as the least-significant bit. Commit `be28bf0` reconstructed one standard four-qubit Grover iteration for target index 5 using explicit simulator-only `MARK` and `REFLECT` primitives. Independent full-operator audits verified both contracts.

## Numerical and input hardening

Commit `3e88909` validated finite real `noise_p` values in `[0,1]` and prevented recursive noise injection. Earlier recovered work repaired entropy solver degeneracy and partition inputs. Q4.12 drift remains documented rather than hidden.

## API engineering

Commit `df48f3a` added Tier-1 contracts for sample shot counts, CHSH shot counts, Bloch qubit indices, and fidelity vectors, with 46 focused tests. The sampler `progress=False` mismatch was deliberately left unresolved because its semantics were not recoverable.

## Acceptance and release surfaces

The post-repair acceptance baseline was audited through 13E. Documentation and direct-execution release-surface synchronization followed in `05b10eb` and `321598b`. The final official result remains 150 passed and one intentionally unresolved historical/API failure.

## Detailed records

See the corresponding reports in `reports/` and raw outputs in `evidence/`. The source snapshot in `source-snapshots/` is labeled with the originating branch and commit.
