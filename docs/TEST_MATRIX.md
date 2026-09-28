# Test matrix

| Scenario | Expected result | Local |
|---|---|---:|
| Stable MIT declaration | `COMPATIBLE` | yes |
| MIT to Apache-2.0 under permissive policy | `ALLOWED_DRIFT` | yes |
| MIT to GPL under permissive policy | `INCOMPATIBLE` | yes |
| Dual/exception/ambiguous declaration | `REVIEW_REQUIRED` | yes |
| Missing integrity or license | `UNRESOLVED` | yes |
| Wrong package identity/version | `UNRESOLVED` | yes |
| Registry 404 | `UNRESOLVED` | yes |
| Malformed model schema | fail closed | yes |
| Prompt injection in license field | treated as data / review | yes |
| Malformed integrity declaration | `UNRESOLVED` | yes |
| Consensus failure | `UNRESOLVED` | yes |
| Duplicate version pair | revert + no mutation | yes |
| Invalid package/policy/same version | revert + no mutation | yes |
| Scoped package URL encoding | correct fixed origin | yes |

Live matrix is added only after deployment; local mocks are never labeled live.
