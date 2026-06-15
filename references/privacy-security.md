# Privacy and Security

Qualification review often touches sensitive documents. Minimize exposure.

## Data Classification

| Level | Examples | Handling |
|---|---|---|
| public | Published platform policy, public registry pages | Cite normally |
| business_confidential | Contracts, invoices, supplier lists, prices, internal emails | Summarize only necessary fields |
| pii | Legal representative name, ID, phone, email, address | Redact unless needed for internal record |
| highly_sensitive | ID number, passport, bank account, beneficial owner info, signatures | Mask values and avoid reproducing images/text |

## Redaction Rules

- Mask identity numbers except last 4 characters when needed.
- Mask bank accounts, phone numbers, emails, and private addresses in user-facing summaries.
- Do not quote full contracts or long authorization letters.
- Do not store or restate document images unless explicitly required.
- Separate applicant-facing messages from internal risk notes.

## Human Escalation Triggers

Escalate when:

- suspected forged document or altered image
- sanctions/export-control concern
- beneficial owner or identity issue
- conflicting official sources
- legal dispute over brand authorization
- high-value applicant or account enforcement impact
- product may be medical/drug/controlled/highly regulated

## Applicant-Facing vs Internal Notes

Applicant-facing:

- "The submitted authorization does not show the target marketplace and territory."
- "Please provide a current authorization letter from the trademark owner or an authorized distributor."

Internal:

- "Signature style mismatch across documents; possible alteration. Manual verification recommended."

Do not expose internal fraud suspicion unless the user is explicitly building internal reviewer notes.

