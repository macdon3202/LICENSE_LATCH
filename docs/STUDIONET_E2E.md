# StudioNet evidence

## Deployment

- Contract: [`0x029c5325891c737a8e04a6702aFE284BeD1d672b`](https://explorer-studio.genlayer.com/address/0x029c5325891c737a8e04a6702aFE284BeD1d672b)
- Version readback: `LICENSE_LATCH_V1`
- Architecture readback: `ATOMIC_AUTHORITY_BOUND_SNAPSHOT_PAIR`

## Real npm assessment

- Pair: `ethers@6.14.0` → `ethers@6.15.0`
- Policy: `PERMISSIVE_STANDARD`
- Transaction: [`0x551231…040a`](https://explorer-studio.genlayer.com/tx/0x55123104629e7bf6ee4d75ece426e17ec647554b0cbd4b7f02a8a3b816ec040a)
- Receipt: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Readback: `COMPATIBLE / DECLARATION_STABLE`
- Both exact npm SHA-512 integrity declarations and both independently
  recomputed registry-subset digests are stored in assessment `1`.

Exact machine-readable evidence: [`studionet-e2e.json`](studionet-e2e.json).

## Live failure and rollback paths

- Exact replay: [`0xeafef2…50a8`](https://explorer-studio.genlayer.com/tx/0xeafef2cb23ca360588572b00e42de809e1bff62b0ed4d728d7dc2cf2f3e350a8) — `FINALIZED / MAJORITY_AGREE / ERROR`; full config and assessment `1` unchanged.
- Same-version input: [`0xb9ab93…6ec6`](https://explorer-studio.genlayer.com/tx/0xb9ab9303a69cb578b8a151d69c67181ba3d6f4fae2c6d553f9ce55c21ce06ec6) — `FINALIZED / MAJORITY_AGREE / ERROR`; counter unchanged.
- Nonexistent exact npm version: [`0x0da0fd…1c47`](https://explorer-studio.genlayer.com/tx/0x0da0fd8bcb022dbd7966048b09841921811742d97d25d24db98f74f499ef1c47) — `FINALIZED / MAJORITY_AGREE / SUCCESS`; readback `UNRESOLVED / SOURCE_NOT_VERIFIED`.

Exact machine-readable failure ledger:
[`studionet-adversarial.json`](studionet-adversarial.json).

Validator disagreement and malformed model output are covered in Direct Mode;
they cannot be deterministically induced against the public validator set and
are not misrepresented as live evidence.

The contract certifies registry-published declaration compatibility only. It
does not claim full tarball inspection or legal advice.
