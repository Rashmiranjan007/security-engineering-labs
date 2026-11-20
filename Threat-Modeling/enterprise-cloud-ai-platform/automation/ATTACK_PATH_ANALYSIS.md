# Attack Path Analysis Engine

A defensive, graph-based modeling utility that connects architecture relationships and explicitly documented weaknesses into candidate attack paths. It is designed to help architects prioritize chains of control failures rather than review each finding in isolation.

## What it does

- Reads a JSON graph containing entry points, target assets, components, relationships, and modeled weaknesses.
- Enumerates simple directed paths from each entry point to each target, with a configurable maximum depth.
- Collects unique weaknesses along each path and ranks paths using a transparent cumulative score.
- Reports the affected assets, weakness IDs, business impact, and suggested control break-points.
- Produces deterministic JSON suitable for design reviews and CI artifacts.

## Run it

Requires Python 3.10+ and the standard library only.

```bash
cd Threat-Modeling/enterprise-cloud-ai-platform/automation
python attack_path_engine.py --input sample-attack-graph.json --output attack-path-report.json
python -m unittest -v
```

Use `--max-depth 10` to change the maximum number of nodes in a candidate path. The default is 8.

## Input model

See [sample-attack-graph.json](sample-attack-graph.json). The schema uses:

- `nodes`: unique component IDs, labels, optional `weakness_ids`, and optional target `business_impact`.
- `edges`: directed relationships with source, target, and optional weakness IDs.
- `weaknesses`: unique IDs, title, likelihood (1–5), impact (1–5), and mitigation suggestions.
- `entrypoints` and `targets`: node IDs used as path starts and business-critical destinations.

Weaknesses may be attached to a node or an edge. This allows modeling a component weakness or a trust-boundary/relationship weakness.

## Scoring and interpretation

For each candidate path, the engine sums likelihood × impact for each unique weakness on that path and caps the displayed prioritization score at 25. Ratings follow the project scale: 1–4 Low, 5–9 Moderate, 10–16 High, 17–25 Critical. The uncapped sum is retained for transparency.

This is deliberately a prioritization heuristic—not a probability, exploitability verdict, CVSS score, or residual-risk calculation. It does not model conditional dependencies, attacker skill, compensating controls, or real network reachability. A path is only as accurate as the architecture and weakness inventory supplied by the reviewer.

## Example chains to challenge during review

1. Internet edge → tenant API → customer database: authentication and object-level authorization weaknesses combine into a potential cross-tenant data exposure path.
2. CI runner → artifact registry → production cluster: broad OIDC trust and weak artifact integrity controls could create a software supply-chain path.
3. AI agent → tool broker → internal administrative API: prompt-driven tool selection becomes dangerous if the broker and downstream service do not independently authorize actions.

These are fictional candidate scenarios, not findings about a real environment. The sample graph intentionally models only the relationships needed to demonstrate the engine.

## Governance

- Validate every edge and weakness with the service owner and current architecture evidence.
- Add prerequisites and compensating controls during human review; do not assume graph reachability means exploitability.
- Map each accepted path to the threat register, security requirements, and validation plan.
- Prioritize breaking high-impact chains at multiple independent control points.
- Record owner, evidence, residual risk, and time-bound exception approval outside the generated report.

## Limitations and safe use

The engine performs static graph analysis only. It does not scan, probe, exploit, or interact with any environment. Do not load credentials, production secrets, personal data, or sensitive internal topology into public sample files.
