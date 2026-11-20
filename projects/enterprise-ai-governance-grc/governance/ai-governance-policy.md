# Enterprise AI Governance Policy — Reference

## 1. Purpose and scope

Establish accountable oversight for AI systems acquired, built, fine-tuned, integrated or operated by an organization. Applies across experimentation, development, procurement, deployment, material change, monitoring and retirement, including third-party AI services and embedded AI features.

## 2. Governance principles

1. Named business owner and technical owner for every AI system.
2. Risk-proportionate review before production use and after material change.
3. Data minimization, purpose limitation, privacy and approved data handling.
4. Human oversight proportionate to impact and autonomy.
5. Secure-by-design architecture, identity, isolation, logging and incident response.
6. Traceable model/data provenance, versioning and change control.
7. Transparent user communication and documented limitations.
8. Continuous monitoring, independent challenge and timely retirement.

## 3. Required lifecycle gates

| Gate | Required outputs | Accountable approval |
|---|---|---|
| Intake | Use case, owner, purpose, users, vendor/model, data categories | Business owner |
| Classification | Impact, autonomy, exposure, affected people, jurisdiction | AI governance function |
| Assessment | Threat model, privacy review, risk score, control plan | Security + privacy + risk |
| Build/procure | Architecture, supplier due diligence, data/model provenance | Technical owner + procurement |
| Pre-production | Control evidence, testing, human oversight, rollback plan | Risk-based approver |
| Operate | Monitoring, incidents, drift, periodic review, change log | Service owner |
| Retire | Access revocation, data retention/disposal, model/artifact disposition | Business + technical owner |

No production release should bypass mandatory security, privacy, legal or safety gates. Exceptions must be time-bound, risk-accepted by an authorized role, and supported by compensating controls.

## 4. Roles

- Executive sponsor: funds and sets risk appetite.
- AI governance committee: resolves cross-functional risk and policy questions.
- Business owner: owns purpose, impact and residual business risk.
- Model/service owner: owns lifecycle, performance and operational controls.
- Security: threat model, security architecture, testing and incident readiness.
- Privacy/legal: privacy impact, jurisdiction and regulatory interpretation.
- Data owner: classification, permitted use, quality and retention.
- Internal audit: independent assurance; does not own control operation.

## 5. Minimum inventory fields

Unique ID, name, purpose, owner, provider, model/version, deployment type, users, affected population, data categories, jurisdictions, autonomy, external exposure, impact tier, lifecycle status, last review, next review, risk and approval references.

## 6. Exceptions and review

Exceptions require a business rationale, impacted assets, risk statement, compensating controls, approver, owner, expiry date and reassessment trigger. Expired exceptions are treated as open governance issues. Review at least annually and on material changes, incidents, provider/model changes, new data use or regulatory changes.

## 7. Evidence and enforcement

Retain approval records, assessments, test results, model cards, data lineage, supplier reviews, access reviews, monitoring records, incident records and retirement evidence according to the enterprise retention schedule. The organization should define enforcement and escalation mechanisms before production adoption.
