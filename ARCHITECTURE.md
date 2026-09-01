# Architecture

Project: EntitlementVersionJoin

Reusable primitive: versioned catalog snapshot -> semantic feature identifier -> deterministic three-mask entitlement join.

The contract separates caller-attested public inputs, validator-agreed semantic fields, deterministic state transitions, and role-bound final actions. It stores canonical JSON strings in GenVM maps, validates every identifier and bound before consensus, and keeps source references explicitly unverified.

The mechanism is not a renamed assessment record. Its state transitions, role topology, storage layout, deterministic algorithm, and public ABI are specific to this project.

<!-- correction-release-start -->
## Consensus and storage safety boundary

Feature resolution now uses the same catalog-bound feature canonicalizer in the validator and after consensus; a merely well-shaped but catalog-invalid leader result is rejected.

The on-chain state transition consumes only the canonical value returned by the post-consensus binding boundary. This contract does not expose a shared permissionless fixed-cap operational registry.
<!-- correction-release-end -->
