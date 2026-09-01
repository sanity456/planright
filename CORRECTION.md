# Correction and release record

Repository: planright

Contract: EntitlementVersionJoin

Corrected release verified: 2026-09-01T09:04:49.896102Z

## Findings applied

This repository was checked against both steward findings from the rejected Boxcomplete and Baggate submissions:

1. A leader-provided digest is not proof of its attached substantive payload. Every result that affects state must be canonicalized, independently compared, and rebound after consensus.
2. A shared permissionless registry with fixed global capacity can be captured or exhausted. Operational catalogs must be explicitly owner-scoped, bounded per catalog, or safely reclaimable.
3. Corrected repository source is insufficient when the submitted Studio/Explorer address still runs an earlier build. The active address, deployed source, ABI, transaction, and evidence URLs must identify one release.

## Contract-specific correction

Feature resolution now uses the same catalog-bound feature canonicalizer in the validator and after consensus; a merely well-shaped but catalog-invalid leader result is rejected.

## Verified release lock

Current StudioNet address: 0x9c65134000Cc72363EB384827f423B82839020d4

Deployment transaction: 0x1f12b8a767d5b077c559d5607232af66db886e5c0d8f8528c871dceff55e35c6

Source SHA-256: b4f21fd33258701a3ef8b77d9b2bdc932180d2737697497f1d14182e005d6b2d

Superseded address: 0x86Ca5B4E128B7Ffb540feA1601b85E25b48aAC2d

The deployment manifest records exact byte-for-byte source readback, exact full ABI/schema equality, successful finalized execution for all 5 release transactions, role-separated external wallets, and the final state observed from StudioNet. The superseded address is historical only and must not be used in a new submission.

## Regression evidence

GenVM lint and strict typecheck: pass

Direct tests: 11 pass

Five-validator integration tests: 1 pass

Leader-payload or post-consensus injection regression tests: pass

Registry isolation and reclaim tests: not applicable

## Review boundary

No live source collection. Catalogs, versions, subscription masks, and references are public provider declarations and are not authenticated.

It does not grant product access, authenticate a provider, bill add-ons, or replace an authoritative entitlement system.

This record documents the implemented controls and verified release. It does not promise a particular human review outcome.
