# Local AI Security SOC Lab

A loopback-only, synthetic SOC simulation that extends the detection engine with event ingestion, alert correlation, incident ownership, a controlled lifecycle, an audit trail, and response playbooks.

## Start the SOC API

From the project root:

```bash
cd soc-lab
python server.py
```

The service binds only to `127.0.0.1:8765`. Open [http://127.0.0.1:8765](http://127.0.0.1:8765) for health status or use the companion console served separately (instructions below).

## Start the console

In a second terminal, from the project root:

```bash
python -m http.server 8000
```

Open [http://localhost:8000/soc-lab/](http://localhost:8000/soc-lab/). The console polls the local API and supports synthetic event ingestion, incident filtering, owner assignment, lifecycle transitions, and playbook viewing.

## API examples

Health check:

```bash
curl http://127.0.0.1:8765/api/health
```

Ingest the included synthetic events:

```bash
curl -X POST http://127.0.0.1:8765/api/events \
  -H 'Content-Type: application/json' \
  --data-binary @../scenarios/sample-events.json
```

View incidents and audit trail:

```bash
curl http://127.0.0.1:8765/api/state
```

Update a lifecycle state (replace the incident ID):

```bash
curl -X PATCH http://127.0.0.1:8765/api/incidents/AI-DET-002:evt-1002 \
  -H 'Content-Type: application/json' \
  -d '{"status":"triaged","actor":"soc-analyst","note":"Signal validated"}'
```

Allowed transitions are strictly ordered: `new -> triaged -> contained -> remediated -> closed`. Owner assignment is independent of status and is audited. Duplicate event IDs are rejected across ingestion batches. Events are correlated by workload, actor, and a 15-minute UTC time bucket.

## Security boundaries and limitations

- Synthetic local simulation only; no cloud, SIEM, model, cluster, or external endpoint integrations.
- HTTP service binds to loopback only and has no authentication; do not change the bind address or expose it to a network.
- No real credentials, personal data, employer logs, or production events should be ingested.
- Local state is stored in `state.json`; delete that file manually to reset the demo.
- This is an engineering portfolio lab, not a production incident-management system or SOAR platform.
- Playbook actions are guidance only; no containment or remediation action is executed automatically.
