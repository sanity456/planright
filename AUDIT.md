# Audit record

Status: PASS for the corrected source, local verification, and current StudioNet release.

Contract: EntitlementVersionJoin

Mechanism: versioned catalog snapshot -> semantic feature identifier -> deterministic three-mask entitlement join.

## Review-blocker results

- GenVM lint and strict typecheck: PASS
- Direct security and state tests: 11 PASS
- Five-validator GLSim integration tests: 1 PASS
- Leader substantive payload or closed-domain result binding: PASS
- Deterministic post-consensus revalidation before state writes: PASS
- Registry ownership, bounded capacity, and safe reclaim: not applicable; no permissionless fixed-cap operational registry
- Concrete GenVM runner hash on source line 1: PASS
- ABI regenerated from the corrected source: PASS
- Source collection and provenance boundary: PASS
- StudioNet workflow: PASS, 5 finalized successful transactions
- Exact deployed-source byte readback: PASS
- Exact full on-chain schema equality with abi.json: PASS
- Mechanism-specific terminal-state readback: PASS
- Fresh external wallets, no workspace wallet, no other-owner wallet, no cross-repository reuse: PASS
- Submission evidence lock: current address `0x9c65134000Cc72363EB384827f423B82839020d4`; superseded address `0x86Ca5B4E128B7Ffb540feA1601b85E25b48aAC2d` is historical only

## Residual boundary

No live source collection. Catalogs, versions, subscription masks, and references are public provider declarations and are not authenticated.

It does not grant product access, authenticate a provider, bill add-ons, or replace an authoritative entitlement system.
