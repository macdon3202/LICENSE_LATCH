# Test resource manifest

## Live source

Only exact npm registry version endpoints constructed by the contract:

```text
https://registry.npmjs.org/{percent-encoded-package}/{percent-encoded-version}
```

Live evidence must record the exact package/version pair, deployed contract,
transactions, consensus/execution status and authoritative post-write readback.

## Reviewed live candidate

Checked against the registry before deployment:

- package: `ethers`
- old version: `6.14.0` — declared `MIT`, SHA-512 integrity present
- new version: `6.15.0` — declared `MIT`, SHA-512 integrity present
- policy: `PERMISSIVE_STANDARD`
- expected semantic branch: `COMPATIBLE / DECLARATION_STABLE`

The candidate is only a resource review. It becomes live evidence only after a
deployed contract independently retrieves it and a finalized transaction plus
exact readback are recorded.

## Local synthetic fixtures

Direct-mode tests use mocked registry JSON and mocked structured LLM output to
cover semantic branches reproducibly. These fixtures are test inputs only and
must never be represented as external or StudioNet evidence.

## Forbidden evidence

- claimant-authored Markdown as license truth;
- arbitrary user URL;
- README text treated as authoritative license metadata;
- local fixture described as live evidence;
- transaction submission without finalized consensus, execution and readback.
