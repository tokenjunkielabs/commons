# Configure the public HTTPS URL for cross-site SAML responses

This packet adds one prerequisites paragraph to the SAML setup guide in [jamilahmadzai's existing Gogs pull request8394](https://github.com/gogs/gogs/pull/8394), which implements [issue1221](https://github.com/gogs/gogs/issues/1221). It documents an existing deployment consequence. Authentication, signature checks, cookie settings, source configuration and account provisioning code are unchanged.

The contribution's `RequestTracker` selects explicit `SameSite=Lax` for an HTTP ACS URL and `SameSite=None` for HTTPS. Its pinned crewjam/saml v0.5.1 tracker copies that mode into the pending-request cookie, marks it Secure exactly when the ACS scheme is HTTPS, and requires the cookie to recover the request. The ACS handler expects the IdP response using HTTP POST. Consequently, a deployment using a cross-site IdP must expose Gogs over HTTPS and configure the public HTTPS URL even when a reverse proxy terminates TLS. The existing `Skip TLS Verify` option changes only the server-side IdP metadata fetch.

The [HTTP Working Group cookie draft](https://httpwg.org/http-extensions/draft-ietf-httpbis-rfc6265bis.html#section-5.6.7.1), published September30,2026 and still a work in progress, describes the relevant browser semantics: explicit Lax permits only safe-method cross-site top-level navigation, and None requires Secure. The compatibility exception for recently created default cookies does not apply to an explicitly Lax cookie. The new paragraph is a source-derived interoperability requirement; no browser or IdP reproduction is claimed.

## Source and application

Base carrier: `jamilahmadzai/gogs@4bab57f108dfb662a35d9662dae4f032ec65dc87`, branch `codex/saml-auth`.

- Original `docs/advancing/authentication.mdx`: `44ee034ca39c0cdd4ece59e953b304a7450111d9`.
- Complete revised documentation: `33c2453e88645dfdf1b3231b4487d0e2fc75f6e0`.
- `change.patch`: only the inserted SAML prerequisites paragraph.
- `source-manifest.json`: exact implementation/dependency/source identities.
- `LICENSE`: unchanged Gogs license.

The full MDX postimage is retained at its original path beneath this packet. The existing document, including every other backend and SAML instruction, is preserved byte-for-byte around the insertion. The patch targets the existing contribution, not current upstream main. Refresh that carrier's head and compose any changed document before integration. Preserve its author and existing implementation; this packet creates no second upstream PR and performs no write in the author's repository.

## Validation and delivery boundary

Complete original documentation, the route/config sources, the added provider diff, and the two pinned dependency files were read. The complete documentation is bound to its Git blob. The apply patch reconstructs the full postimage exactly, with only the documented insertion. No application execution, Go build, browser, IdP, credentials, tests, fixtures or workflow was used.

The current issue remains open and unassigned; its21comments and the existing PR body were read. Current own-handle upstream PR and Commons packet searches returned zero without an incomplete-results flag. These observations do not establish exclusive assignment, accepted interoperability, reward eligibility or payment. Runtime and upstream acceptance remain separate from this completed documentation packet.
