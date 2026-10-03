# VCTC ERP/GMS response architecture

This is a buyer-weighted internal architecture, not a proposal and not authority to contact or submit to VCTC.

| Buyer evaluation area | Points | Prime/OEM responsibility | TJLabs specialist evidence seam |
| --- | ---: | --- | --- |
| Firm Qualifications | 15 | Three similar projects completed within ten years; separate public-sector or comparable-entity experience; product authority and corporate facts | No inherited credentials; bind only independently evidenced TJLabs work |
| Proposed Solution | 10 | ERP/GMS product architecture, licensing, SaaS, module fit | Integration/migration evidence model and deterministic handoff |
| Functional Requirements | 20 | Exact Appendix A row responses and product configuration | Requirement fingerprinting, coverage ledger, evidence refs, gap/HOLD semantics |
| Implementation Approach | 20 | PM, schedule, configuration, change/training, cutover | Source→target reconciliation; interface replay/idempotency; UAT lineage; exception/retest register |
| Support & Maintenance | 15 | OEM/prime support model, SLAs, upgrades, escalation | Evidence continuity / incident-to-change trace support if separately scoped |
| Cost | 20 | Exact Appendix B response and commercial authority | Bounded subcontract milestones only after prime scope and workbook columns are known |

## Implementation evidence work packages

1. **Migration reconciliation** — exact source/target record counts, opening balances, open AP/AR items, vendor/project/grant crosswalks, transformation provenance, rejects and disposition.
2. **Interface replay** — proposed work for the RFP's potential Wells Fargo, Outlook, Entra ID SSO, Atrix 1099, DocuSign and ERP↔GMS interfaces; retries, idempotency, duplicate-effect checks, rollback/recovery and evidence receipts.
3. **Requirement→UAT traceability** — Appendix A requirement fingerprint → configured behavior → test case → observed result → exception → retest → human disposition.
4. **Cutover evidence** — frozen generation identities, open-item reconciliation, exception threshold, rollback gate and owner signoff.
5. **Audit-ready binder** — source manifests, decision log, transformation lineage, test/evidence index, exception disposition and acceptance evidence. No claim of buyer acceptance without explicit buyer evidence.

## Source meaning and scope

The [official RFP](https://www.goventura.org/wp-content/uploads/2026/09/RFP-Enterprise-Resource-Planning-System.pdf) separates three similar projects completed within ten years from public-sector/comparable-entity experience (printed pp. 13–14; physical pp. 12–13). Legacy v1 identifiers remain compatible: `THREE_SIMILAR_PUBLIC_SECTOR_PROJECTS` maps to the first criterion and `PUBLIC_SECTOR_REFERENCES` to the second. Their names do not require all three projects to be public-sector projects. Both remain `UNKNOWN`.

Interfaces are potential (printed p. 17; physical p. 16). Detailed conversion planning covers balances/open transactions and finalization before contracting (printed p. 20; physical p. 19); generic services also mention historical data (printed p. 8; physical p. 7). Keep this workshare proposed and reconcile scope before commitment.

## Hard gates

- Exact current Appendix A/B bytes must be recovered before response/cost readiness.
- Prime/OEM must own similar-project references, public-sector or comparable-entity experience, product claims, support model, demo, insurance and physical submission.
- Appendix C subcontracting / insurance obligations are contract gates, not application-generated facts.
- Any buyer communication uses only the designated procurement route and requires separately authorized human action.
