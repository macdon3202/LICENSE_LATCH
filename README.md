# LicenseLatch

LicenseLatch is a contract-only GenLayer application that creates an immutable
assessment of **npm registry license-declaration drift** between two exact
package versions.

> Does the new registry-published license declaration remain inside a fixed
> dependency policy, and is the change unambiguous enough for automation?

It is not legal advice. It does not claim that it audited every file in the npm
tarball. The contract deliberately limits its claim to metadata independently
retrieved from the authoritative npm registry version endpoints.

## Distinct architecture

```text
exact package + old/new versions + closed policy
                         ↓
two authoritative registry snapshots in one transaction
                         ↓
identity/version/integrity-presence/content-digest binding
                         ↓
bounded semantic license normalization
                         ↓
exact consequential consensus
                         ↓
deterministic policy matrix
                         ↓
one immutable version-pair assessment
```

There is no registration phase, observer role, deadline, supersession chain or
mutable lifecycle. `assess_upgrade()` atomically retrieves, adjudicates and
persists one replay-protected snapshot pair.

## States

- `COMPATIBLE` — declaration is semantically stable and allowed.
- `ALLOWED_DRIFT` — declaration changed but both the new family and evidence
  remain policy-compliant.
- `INCOMPATIBLE` — the new family is blocked by the closed policy.
- `REVIEW_REQUIRED` — dual licensing, exceptions or ambiguity prevent safe
  automation.
- `UNRESOLVED` — authoritative source or mandatory binding was not established.

## Policies

- `MIT_APACHE_ONLY`
- `PERMISSIVE_STANDARD`
- `NO_STRONG_COPYLEFT`

## Verify

```bash
python -m pytest -q
python -X utf8 -m genvm_linter.cli check contracts/license_latch.py
```

StudioNet deployment:
[`0x029c5325891c737a8e04a6702aFE284BeD1d672b`](https://explorer-studio.genlayer.com/address/0x029c5325891c737a8e04a6702aFE284BeD1d672b)

Live evidence: [`docs/STUDIONET_E2E.md`](docs/STUDIONET_E2E.md),
[`docs/studionet-e2e.json`](docs/studionet-e2e.json), and
[`docs/studionet-adversarial.json`](docs/studionet-adversarial.json).

Current local verification: **22 tests passing**, GenVM lint and semantic
validation passing.
