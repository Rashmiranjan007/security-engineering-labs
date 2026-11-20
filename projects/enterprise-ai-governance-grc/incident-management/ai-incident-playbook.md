# AI Security and Governance Incident Playbook

## Trigger examples

Sensitive-data disclosure; cross-tenant retrieval; prompt injection leading to unauthorized action; unsafe agent/tool execution; model or dependency compromise; training-data poisoning; material model drift; vendor incident; loss of human oversight; prohibited or harmful use.

## Response phases

1. **Detect and report:** capture system ID, model/version, time, reporter, affected users/data, event IDs and initial impact. Do not paste secrets or personal data into public ticketing channels.
2. **Triage:** classify confidentiality, integrity, availability, safety, privacy and regulatory impact. Identify provider/deployer roles and affected jurisdictions.
3. **Contain:** disable affected tool/action, revoke credentials, isolate tenant or endpoint, roll back model/configuration, suspend data connector, or route to human-only workflow. Choose proportionate reversible actions.
4. **Preserve evidence:** secure logs, model/configuration digests, prompts/outputs where lawful, approvals, access records and timeline with chain-of-custody controls.
5. **Notify and escalate:** involve incident commander, security, privacy, legal, business owner, supplier and regulators/customers when required by applicable obligations and timelines. Legal/privacy teams determine notification duties.
6. **Recover:** validate clean model/configuration, credentials, data permissions, safeguards and monitoring before restoring service.
7. **Learn:** root-cause analysis, control gap, risk-register update, corrective actions, accountable owners and closure evidence.

## Severity guidance

- Critical: confirmed large-scale sensitive-data exposure, unauthorized high-impact action, model compromise affecting multiple systems, or immediate safety threat.
- High: material tenant boundary failure, exploitable tool authorization flaw, or significant integrity compromise.
- Medium: contained policy bypass or limited exposure without confirmed material impact.
- Low: near miss or low-impact control failure.

Severity is context-dependent. Preserve the incident commander’s authority to raise severity. This playbook does not prescribe legal notification timelines; verify current law and contract terms.
