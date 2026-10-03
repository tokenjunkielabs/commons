# Written questions - current internal reconciliation

The written-question deadline was 2026-09-25 at 2:00 PM Central Time. The numbered text below preserves the earlier internal draft; it is historical wording, not a ready-to-send question packet. Use [AMENDMENTS.md](AMENDMENTS.md) and the State answer references below before assigning further internal work.

References in this table are **State question numbers in Amendment 2**, not Attachment 1 requirement IDs. PARTIAL means the answer addresses only part of the earlier question; OPEN means the specific premise is not settled; RECONCILE flags inconsistent sizing answers; UPDATED flags a changed premise. These are internal dispositions, not statements that a product meets a requirement.

| Internal question | State questions | Disposition | Remaining owner focus |
|---|---|---|---|
| 1 | 6-7, 11-12, 19, 54, 61, 73-74, 95, 111-112 | PARTIAL | Detailed interface contract and ownership |
| 2 | 9, 25, 39, 46, 48-49, 53, 55, 57, 90-91, 113 | PARTIAL | Named integration and responsibility evidence |
| 3 | 10, 21-22, 31, 40, 96 | PARTIAL | Bank format and exception handling |
| 4 | 34, 104 | PARTIAL | Map every service and subprocessor |
| 5 | 58 | OPEN | AI-disabled evaluation assumption |
| 6 | 34, 44, 63 | PARTIAL | Prime/subcontractor report coverage |
| 7 | 1, 3-4, 20, 36-37, 52, 60, 76, 78-81, 85-88, 110 | RECONCILE | Quote basis, peaks and training assumptions |
| 8 | 31, 40, 62, 70, 77, 99 | UPDATED | Configuration/cutover scope and new-system retention |
| 9 | 26, 33, 64, 66, 94 | PARTIAL | Supported-model and transition evidence |
| 10 | 24, 27-28, 74, 95 | PARTIAL | Correction and acknowledgement ownership |
| 11 | 32, 36, 51 | PARTIAL | Tenant/segregation design |
| 12 | 34, 108 | PARTIAL | Measurement windows, RTO/RPO and DR cadence |

The response owner should record the precise remaining assumption and supporting prime/OEM evidence. Do not turn a partial answer into a product guarantee. The existing pursuit and partner-contact owners remain responsible for any authorized external action.

## Historical internal wording

1. For interfaces in Requirements 37, 39, 40, 42, 70 and 114–117, what current Edison/Oracle modules, API or file protocols, message formats, authentication methods, batch windows, and non-production endpoints should respondents assume?
2. For payment-card processing in Requirement 40, which Worldpay/FIS products and integration modes are presently contracted, and does the State expect the cashiering vendor or the processor to own devices, tokenization, settlement, chargeback and PCI scope?
3. For Check 21 / RDC / ICL Requirements 42, 53, 78 and 120, what current image/file specifications, financial institutions, endorsement rules, retention periods and transmission channels must be supported?
4. For Requirement 12 and the RFI’s general US-only data rule, does “continental United States” also apply to telemetry, security logs, support tooling, backups, DR replicas and subprocessors? Please identify any approved exceptions.
5. For AI Requirements 24–28, would a solution with all AI features disabled be evaluated equivalently where AI is not needed for cashiering, and what evidence should accompany an AI-disabled architecture?
6. For Requirement 11, will a prime/OEM SOC 2 Type II report covering the hosted product suffice when implementation/integration subcontractors do not host or process State production data?
7. For UAT/training Technical Question 7, can the State provide expected agency/location/cashier counts, representative transaction volumes, concurrency, tender mix, peak periods, and number of State testers/trainers?
8. For migration, what historical transaction, batch, document/image and configuration retention horizon is expected, and which legacy sources are in scope?
9. For hardware Requirement 74, please identify current/target models for receipt printers, drawers, card devices and check scanners, including any legacy transition period the State expects.
10. For Requirements 97–113 and 116–117, what is the State’s authoritative system of record for deposit, accounting-distribution and bank-reconciliation status, and where must corrections originate?
11. Does the State expect a single statewide tenant/configuration with agency-level segregation, or multiple agency tenants/instances under a shared reporting layer?
12. Please identify target RTO/RPO, planned maintenance expectations, required uptime/SLA measurement windows, and any State-mandated DR test cadence beyond the RFI’s request for vendor evidence.

No buyer message was sent from this artifact. The current authority record remains in response_manifest.json.
