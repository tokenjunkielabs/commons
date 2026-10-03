# Tennessee 31701-03850 response lab

Additive response-material slice for Commons issue #15882. The sibling acceptance_lab is a separate synthetic donor and is not modified here.

The current source basis is the State of Tennessee RFI dated 2026-09-11 plus Amendments 1 and 2, reviewed 2026-10-03. The RFI response is due 2026-10-13 at 2:00 PM Central Time (UTC-05:00). The written-question deadline passed on 2026-09-25 at 2:00 PM Central Time; the original draft is now an internal reconciliation register. See [AMENDMENTS.md](AMENDMENTS.md) for official source links and the current decisions. The RFI permits one vendor question submission, limits responses to 20 pages with 12-point minimum text, requires numbered Technical/Cost answers, and prohibits embedded external landing-page links.

response_manifest.json binds the complete 1–120 requirement posture map in requirement_crosswalk.csv. The four postures are PRIME_PRODUCT_EVIDENCE, SPECIALIST_WORKSHARE, DEMO_SUPPORTED, and GAP_QUESTION. DEMO_SUPPORTED always means synthetic control behavior only, not installed-product or compliance proof.

Run the completeness check with:

    python revenue/opportunities/tn_31701_03850_cashiering/response_lab/validator.py revenue/opportunities/tn_31701_03850_cashiering/response_lab/response_manifest.json

This directory is internal response preparation. It authorizes no Tennessee or partner contact, question submission, proposal submission, contract acceptance, payment or revenue recognition.
