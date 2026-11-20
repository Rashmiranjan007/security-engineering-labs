# Local AI Security SOC Lab

A loopback-only, synthetic SOC simulation that extends the detection engine with event ingestion, alert correlation, incident ownership, a controlled lifecycle, an audit trail, and response playbooks.

## Start

From this directory:

```bash
python server.py
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765). The console and API are served from the same local process.

## Lab workflow

1. Select **Ingest synthetic events** to load the six sample events.
2. Review generated alerts, severity, owners, and correlation groups.
3. Select an incident to inspect evidence metadata, the timeline, and its event-specific response playbook.
4. Assign an owner/team; assignment is recorded in the audit trail.
5. Move an incident through the controlled lifecycle: `new -> triaged -> contained -> remediated -> closed`.
6. Refresh the console to see the persisted local state.

## API

- `GET /api/health` — local service health
- `GET /api/state` — events, incidents, and audit history
- `GET /api/playbooks` — response playbooks
- `POST /api/events` — ingest one event or a JSON array
- `POST /api/demo-ingest` — ingest the included synthetic sample
- `PATCH /api/incidents/{incident_id}` — update owner or perform the next lifecycle transition

Example:

```bash
curl -X POST http://127.0.0.1:8765/api/demo-ingest -H 'Content-Type: application/json' -d '{}'
curl http://127.0.0.1:8765/api/state
curl -X PATCH 'http://127.0.0.1:8765/api/incidents/AI-DET-002%3Aevt-1002' \
  -H 'Content-Type: application/json' \
  -d '{"status":"triaged","actor":"soc-analyst","note":"Signal validated"}'
```

Correlation groups are calculated using workload, actor, and a 15-minute UTC time bucket. Duplicate event IDs are rejected across batches. Lifecycle transitions are enforced and recorded in the audit trail.

## Security boundaries and limitations

- Synthetic local simulation only; no cloud, SIEM, model, cluster, or external endpoint integrations.
- The HTTP service binds only to `127.0.0.1:8765` and has no authentication. Do not change the bind address or expose it to a network.
- The demo API is intentionally unauthenticated because it is loopback-only; it is not suitable for shared hosts.
- No real credentials, personal data, employer logs, or production events should be ingested.
- Local state is stored in `state.json`; stop the server and delete this file manually to reset the demo.
- Playbook actions are guidance only. No containment or remediation action is executed automatically.
- This is an engineering portfolio lab, not a production incident-management system or SOAR platform.
