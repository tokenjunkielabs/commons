# VCTC ERP + Grants Management pursuit carrier

Operation `VCTC-ERP-GMS-TEAMING-PURSUIT-ZMQV5R9-20260916` tracks the public Ventura County Transportation Commission 2026 ERP/GMS solicitation without pretending Token Junkie Labs is an ERP OEM or qualified prime.

The September 16 discovery snapshot records all four buyer-controlled documents as **unretrieved** in `official_sources.json`: that execution could read the RFP through a PDF reader but did not obtain raw document bytes. The original discovery inputs remain unchanged.

The [October 3 retained generation](captures/20261003/README.md) now binds the official board and four linked files to exact hashes and sizes. The existing CLI consumed those inputs at 2026-10-03T19:49:15+00:00 and returned **HOLD_REQUIREMENT_MATRIX_REQUIRED**: zero requirement rows and nine unresolved team gates. The retained generation adds source custody; the proposal and qualification work remains open.

## States

- `HOLD_CONTROLLING_RFP_REQUIRED`
- `HOLD_CONTRACT_APPENDIX_REQUIRED`
- `HOLD_APPENDIX_BYTES_REQUIRED`
- `HOLD_DEADLINE_PASSED`
- `HOLD_REQUIREMENT_MATRIX_REQUIRED`
- `HOLD_MANDATORY_REQUIREMENT_GAPS`
- `HOLD_IMPLEMENTATION_EVIDENCE_PLAN`
- `HOLD_TEAM_QUALIFICATION`
- `READY_FOR_OWNER_PROPOSAL_REVIEW`

Even the strongest state is owner review only. The assessment hard-codes false authority for buyer contact, pre-proposal registration, questions, proposal submission, signature, pricing commitment, contract acceptance, insurance certification, production mutation, award/payment/revenue claims.

## Trusted-source boundary

Candidate packet source rows must exactly match a separately HMAC-authenticated `vctc-source-authority/v1` object. The key comes only from `VCTC_SOURCE_AUTHORITY_KEY_HEX`; candidate/source/assessment bytes cannot supply it. This is an integrity boundary for the locally retained official-source generation, not a claim that a hash establishes buyer authenticity by itself.

## CLI

The [retained-generation instructions](captures/20261003/README.md#actual-cli-observation-and-source-authority) use the recovered bytes. The commands below consume the unchanged historical discovery inputs.

```bash
export VCTC_SOURCE_AUTHORITY_KEY_HEX='<64+ hex chars>'
python -m opportunities.vctc_erp_gms_2026.cli sign-sources official_sources.json source_authority.json --key-id owner-2026-09
python -m opportunities.vctc_erp_gms_2026.cli compile example.discovery.json source_authority.json assessment.json --key-id owner-2026-09
python -m opportunities.vctc_erp_gms_2026.cli verify example.discovery.json source_authority.json assessment.json --key-id owner-2026-09
```

`sign-sources` is an owner/source-custody step. Do not sign guessed SHA values. Retrieve exact buyer bytes first.

## Commercial posture

The RFP permits ERP + qualified third-party GMS teaming / multiple awards. The truthful TJLabs lane is paid specialist implementation evidence: migration reconciliation, interface replay/idempotency, requirement→UAT traceability, exception/retest control and audit-ready cutover evidence. Product qualifications, similar-project references, public-sector or comparable-entity experience, OEM support, demo, insurance and physical submission belong to the qualified prime/vendor and must be independently evidenced.
