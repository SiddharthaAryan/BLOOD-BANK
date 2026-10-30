# Blood Donor Desk: security and handover guide

## Current status: prototype, not production
The GitHub repository is public. It contains the earlier front-end demonstrations, deny-all Firestore rules, and an unconnected Firebase client module. No Firebase project has been connected or deployed. The Firebase client is not yet integrated with the UI or tested against a project; OCR mapping and checkbox extraction are not validated. Do not use real donor information.

## Intended data flow
A staff member reviews an extracted or manually entered fictional form. A signed-in staff-only interface saves a small structured record to Firestore and retrieves it for dashboard/export. Do not store scanned images unless the hospital explicitly approves their lifecycle and access controls. Public donor submission requires a separately designed and validated ingestion route. The current client does not implement it.

## Controls and limitations
- **Authentication:** Firebase Authentication establishes identity. Restrict access to approved staff; disable public sign-up and use MFA/AIIMS identity controls where required. A logged-in user is not automatically authorised.
- **Authorisation:** Firestore Security Rules enforce access for web clients. The existing root firestore.rules DENIES ALL reads and writes. Do not enable test mode or allow-all rules. Role rules must be designed, deployed and emulator-tested before the app can access data; no role-based rules are implemented yet.
- **Public repository:** code and Firebase web configuration can be visible, but never commit service-account private keys, credentials, donor data, uploads, exports or backups. Firebase configuration is not an access control; security depends on authentication, rules and infrastructure controls.
- **Browser security:** the sample module uses session authentication and the default in-memory Firestore cache. Use managed devices, protect endpoints and sessions, and review dependencies. OCR from third parties adds supply-chain risk; choose an institution-approved OCR/data flow and evaluate its privacy and accuracy. The module does not implement OCR.
- **Protection from abuse:** assess App Check, rate limiting and bot protections for public-facing features. App Check is an additional layer, not user authorisation.
- **Integrity and accountability:** implement server-enforced validation, tamper-resistant audit logging, distinct staff roles and verified exports; do not rely on hidden UI elements or editable client code.
- **Availability:** encrypted backups and restore exercises, monitoring, incident response, offline contingency and vendor support are not implemented. Determine data and log locations with AIIMS IT.
- **Clinical:** complete form mapping, informed-consent workflow, clinician review, actual spreadsheet columns and independent validation are prerequisites. OCR confidence is not a probability of medical correctness; humans must verify every value.

## Security testing before deployment
Test signed-out, unapproved user and approved user access; record read/write boundaries; malformed inputs; attempts to set roles; export permissions; XSS; dependency vulnerabilities; backup restore; and incident response. Arrange an independent security assessment and remediation. Assess applicable CERT-In, privacy and blood-centre requirements with AIIMS IT/legal. No claim of being hackproof or compliant can be made from this prototype.

## Handover
AIIMS should control its own production project, repository, hosting, billing, administrative accounts, roles, backups and monitoring. Keep a configuration template and reproducible deployment instructions, keep secrets out of the repository, document ownership and incident contacts, train staff, and demonstrate restore and takeover. Use a separate project and synthetic records for all development.

## Project setup needed
Create a separate Firebase demo project and web app. Send only its public web configuration object. A Firebase connector/project access is not present in this session, so project creation, rule deployment, account creation, hosting and verification cannot be performed remotely yet. Keep deny-all rules until a narrow rule set is written and tested.
