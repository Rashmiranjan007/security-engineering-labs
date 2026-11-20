# Cloud Security Posture — Operating Checklist

## Before deployment
- [ ] Confirm the target is a dedicated lab account.
- [ ] Confirm the Terraform role uses short-lived credentials and least privilege.
- [ ] Review provider and module versions.
- [ ] Run formatting, validation, and IaC scanning.
- [ ] Review the plan and change approval.

## After deployment
- [ ] Confirm all S3 public-access-block settings are enabled.
- [ ] Confirm default encryption is enabled.
- [ ] Confirm versioning is enabled.
- [ ] Confirm bucket policy grants only required principals and actions.
- [ ] Confirm audit events are captured by the account's logging service.

## Exception governance
Any exception should identify the affected resource, business justification, compensating control, accountable owner, approver, expiry date, and retest date. Exceptions should be time-bound and tracked to closure.
