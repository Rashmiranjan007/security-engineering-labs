# Enterprise AI Governance, Risk & Compliance (GRC) Framework

A practical reference implementation for governing enterprise AI systems across intake, classification, risk assessment, control selection, approval, monitoring, audit evidence and retirement.

## What is included

- Governance policy, lifecycle gates, roles and RACI.
- AI system inventory and risk assessment methodology.
- A versioned control catalogue mapped at a high level to NIST AI RMF, ISO/IEC 42001, EU AI Act topics, ISO/IEC 27001 and OWASP LLM application risks.
- A deterministic Python assessment engine that calculates inherent and residual risk, flags missing evidence and overdue review dates, and generates JSON/Markdown reports.
- Vendor due-diligence questionnaire, model card template, audit evidence register and AI incident playbook.
- A local dashboard that visualizes the generated assessment report.
- A continuous-compliance extension that normalizes synthetic findings from AI security, EKS/cloud posture and model-supply-chain exports, maps them to controls, and generates an evidence-linked remediation backlog.
- Unit tests and GitHub Actions validation.

## Quick start

Requires Python 3.10+; standard library only. From the repository root:

```bash
cd projects/enterprise-ai-governance-grc
python tools/governance_engine.py --inventory data/ai-inventory.json --controls data/control-catalogue.json --output-dir reports
python -m unittest discover -s tests -v
python -m http.server 8000
```

Open [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/). The dashboard loads `../reports/latest.json` relative to its page. Run the engine first.

### Continuous compliance integration

From the GRC project directory:

```bash
cd continuous-compliance
python tools/compliance_pipeline.py --sources data/source-findings.json --rules data/control-mappings.json --output-dir reports
python -m unittest discover -s tests -v
python -m http.server 8001
```

Open [http://localhost:8001/dashboard/](http://localhost:8001/dashboard/). This demo normalizes eight synthetic findings from three source families and maps them to the GRC control catalogue. It does not call vendor APIs or create tickets.

To assess a different inventory, supply a JSON file following the schema in `docs/data-schema.md`. The engine never calls external services or changes systems.

## Assessment model

Each system has five inherent-risk dimensions scored 1–5: impact, data sensitivity, autonomy, exposure and model uncertainty. Their sum (5–25) maps to Low (5–9), Moderate (10–14), High (15–19) or Critical (20–25). Residual risk is calculated by subtracting documented, applicable control effectiveness points from the inherent score, with a floor of 5. This is a transparent portfolio scoring model, not a validated actuarial model or regulatory classification.

A control is treated as implemented only when its status is `implemented` and it has at least one evidence reference. Missing evidence prevents the control from reducing residual risk. The engine also flags overdue reviews and required controls that are not implemented with evidence.

## Framework mapping and legal caveat

Mappings are indicative crosswalks for learning and control organization, not statements of equivalence or certification. The EU AI Act has risk-based and role-specific obligations with phased applicability; whether an obligation applies depends on the system, provider/deployer role, use case and current law. Validate against official, current texts and qualified counsel. NIST AI RMF and ISO/IEC 42001 are not laws. OWASP LLM risks are technical guidance, not a GRC certification.

## Project map

- `governance/` — policy and operating model.
- `risk-management/` — methodology and sample risk register.
- `data/` — synthetic AI inventory and control catalogue.
- `compliance/` — mapping notes and framework boundaries.
- `model-governance/` — model card and lifecycle gate.
- `third-party-risk/` — supplier assessment questionnaire.
- `audit/` — evidence register and audit procedure.
- `incident-management/` — AI incident response playbook.
- `tools/` — offline assessment and reporting engine.
- `dashboard/` — dependency-free local report viewer.
- `tests/` — automated validation.
- `continuous-compliance/` — source export contract, control mappings, finding normalizer, remediation backlog, dashboard and tests.

## Production adoption considerations

Replace sample controls and weights with an approved enterprise control baseline; integrate authoritative identity, asset, model registry, ticketing, GRC, SIEM and evidence systems; use immutable evidence storage and access controls; add legal/privacy review; establish accountable control owners; and validate scoring with risk stakeholders. Do not use this demo as the sole basis for approval, regulatory compliance, or high-impact decisions.

All inventory, assessment and evidence examples are synthetic. This project does not provide legal advice, audit assurance, certification or a claim of compliance.
