# Blood Donor Desk — handover and setup

## Status
Concept prototype only. No Firebase integration, staff authentication, approved clinical questionnaire, consent, or production security controls are implemented yet. Never use real donor data. Both current pages use browser-session data. scan.html loads OCR code and language data from external servers and its accuracy is not validated.

## Ownership
The current GitHub repository and any personal Firebase project are for a fictional-data demo only. For a real service, AIIMS should choose and own its approved repository, hosting, identity, database, billing and operational access. Do not transfer patient records via GitHub. Never commit service-account keys or passwords.

## Setup of a demo project
1. Create a separate Firebase project and register a web app.
2. Create Firestore in production mode, and verify deny-all rules in firestore.rules. Do not switch to test mode.
3. Enable email/password authentication for the demo. Do not enable open registration.
4. Provide the Firebase web app configuration to the developer, never passwords or private keys.
5. Integration still requires implementation, access rules, deployment and testing; configuration alone does not connect the existing pages.

## Before any real-world use
- Blood bank to approve questionnaire, consent, donor and medical officer workflow and Excel field mapping.
- AIIMS IT/security to approve hosting, vendor, access, identity, logs, backups, incident response, data handling and retention.
- Implement and test least-privilege access, protections for public submissions, staff authentication, auditability, secure configuration and recovery.
- Evaluate OCR accuracy against representative test forms, require human verification and decide whether storing images is necessary.
- Conduct independent security assessment and remediation, clinical validation and institutional approval.
- Prepare deployment, maintenance, access management, backup/restore and incident procedures; demonstrate restore and institutional takeover.

## Open questions
Confirm approved full paper form, current spreadsheet template, e-RaktKosh or other system integration, hosting policy, and named institutional owners. Data residency and all applicable requirements must be reviewed with the hospital.
