# EntitlementVersionJoin

A reusable feature catalog and time-bounded plan-version registry where validators map a capability request to one feature and code joins frozen base, add-on, and grandfathered masks.

The repository is standalone and the contract is reusable: one deployment can hold multiple independent records for unrelated callers. It has no frontend and moves no funds.

## Native mechanism

versioned catalog snapshot -> semantic feature identifier -> deterministic three-mask entitlement join.

## Actors

plan provider, subscriber, GenLayer validators.

## Source boundary

No live source collection. Catalogs, versions, subscription masks, and references are public provider declarations and are not authenticated.

## Safety boundary

It does not grant product access, authenticate a provider, bill add-ons, or replace an authoritative entitlement system.

All inputs and results are public. Untrusted public data is delimited in prompts and cannot change the closed response schema. A malformed or non-consensus model result fails without committing the intended state transition.

## Verification

    genvm-lint check contracts/entitlement_version_join.py
    genvm-lint typecheck contracts/entitlement_version_join.py --strict
    python -m pytest tests/direct -q -p no:cacheprovider
    python tests/run_glsim.py --port 4000 --validators 5 --no-browser
    python -m pytest tests/integration -q -s -p no:cacheprovider

See ARCHITECTURE.md, SECURITY.md, SOURCE_PROVENANCE.md, AUDIT.md, SUBMISSION_CHECKLIST.md, and deployments/studionet.json.

MIT licensed.

<!-- correction-release-start -->
## Corrected release integrity

The full twelve-repository correction audit applied both steward findings to this contract. Feature resolution now uses the same catalog-bound feature canonicalizer in the validator and after consensus; a merely well-shaped but catalog-invalid leader result is rejected.

The current StudioNet release is `0x9c65134000Cc72363EB384827f423B82839020d4`. Its source bytes and full schema were read back from StudioNet and matched this repository exactly. Use `CORRECTION.md`, `REVIEW_RESPONSE.txt`, and the commit-pinned `deployments/studionet.json` for submission evidence; do not reuse the superseded address `0x86Ca5B4E128B7Ffb540feA1601b85E25b48aAC2d`.
<!-- correction-release-end -->
