# LicenseLatch specification

## Proof obligation

For exact npm package versions `old` and `new`, establish whether the license
declarations published by the npm registry are unambiguous and whether the new
normalized family is permitted by a contract-fixed policy.

## Falsifiers

- either endpoint is unavailable or invalid;
- returned package identity or version differs;
- registry integrity declaration or license declaration is absent;
- validator observations disagree on consequential fields;
- declaration is dual, exceptional, custom or ambiguous;
- normalized new family is outside the selected policy.

## Evidence boundary

The source is `https://registry.npmjs.org/{package}/{version}` constructed by
the contract. User-controlled URLs are impossible. The content digest binds the
exact adjudicated registry subset: name, version, license declaration,
`dist.integrity`/`shasum`, and repository metadata. It is not a tarball digest
recomputation and does not claim repository or package-file completeness.

## Judgment boundary

Validators normalize natural-language or SPDX-like declarations into a closed
family set and identify ambiguity, combinations and exceptions. Deterministic
code alone maps those findings to the fixed policy and final state.

## Persistence

Each `(package, old version, new version, policy)` tuple is single-use and
immutable. Failed source verification creates a fail-closed `UNRESOLVED`
assessment, preserving an auditable point-in-time result.
