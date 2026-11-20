# AI Risk Assessment Methodology

## Scope

Assess a defined AI system and use case, not a model in isolation. Record business purpose, affected users/populations, data flows, provider/deployer role, deployment environment, jurisdictions, autonomy and human oversight.

## Inherent risk dimensions

Score each from 1 (limited) to 5 (very high), with a written rationale:

- Impact: consequence of incorrect, harmful or unavailable output.
- Data sensitivity: sensitivity, volume and identifiability of input, retrieval and output data.
- Autonomy: degree of independent action and ability to affect external systems or people.
- Exposure: user population, internet reachability, integrations and attack surface.
- Model uncertainty: opacity, variability, evaluation gaps, drift and supply-chain uncertainty.

Sum scores (5–25): Low 5–9; Moderate 10–14; High 15–19; Critical 20–25. These are example portfolio bands and must be calibrated to organizational risk appetite.

## Control effectiveness and residual risk

The reference engine gives each implemented control an effectiveness value from 1–3. It only counts when the control is applicable, status is `implemented`, and at least one evidence reference exists. Residual score = max(5, inherent score − sum of effective control points). Map residual bands using the same thresholds. This intentionally simple calculation is explainable but is not a statistical probability model.

## Required treatment

- Critical: do not launch or continue without executive risk decision and verified critical controls.
- High: documented treatment plan, accountable owner and target date; approval before production.
- Moderate: planned treatment and periodic review.
- Low: maintain baseline controls and monitoring.

Never allow a numerical score to override a mandatory legal, safety, privacy or security requirement. Record uncertainty and assumptions separately. Reassess after material changes, incidents, model/provider updates, new data use, new integrations or at least annually.
