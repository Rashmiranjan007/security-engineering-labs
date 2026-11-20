"""Local-only SOC workflow core for synthetic AI security telemetry."""
import hashlib
from datetime import datetime, timezone

VALID_STATUSES = ("new", "triaged", "contained", "remediated", "closed")
TRANSITIONS = {
    "new": {"triaged"},
    "triaged": {"contained"},
    "contained": {"remediated"},
    "remediated": {"closed"},
    "closed": set(),
}


def _correlation_id(event):
    parsed = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    bucket = int(parsed.timestamp()) // 900
    material = f"{event['workload']}|{event['actor']}|{bucket}".encode()
    return "CORR-" + hashlib.sha256(material).hexdigest()[:10].upper()


def ingest(state, events, rules, detected_at=None):
    """Validate, deduplicate, detect and correlate a batch of events."""
    from pathlib import Path
    import sys
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from detector import detect, validate_events

    validate_events(events)
    known = {item["event_id"] for item in state["events"]}
    duplicates = [item["event_id"] for item in events if item["event_id"] in known]
    if duplicates:
        raise ValueError(f"Duplicate event IDs already ingested: {', '.join(duplicates)}")

    matched = detect(events, rules)
    timestamp = detected_at or datetime.now(timezone.utc).isoformat()
    new_incidents = []
    event_by_id = {event["event_id"]: event for event in events}
    for incident in matched:
        event = event_by_id[incident["event_id"]]
        incident.update({
            "status": "new",
            "owner": "AI Security Operations",
            "correlation_id": _correlation_id(event),
            "created_at": timestamp,
            "updated_at": timestamp,
            "timeline": [{"status": "new", "at": timestamp, "actor": "detection-engine", "note": "Incident created from matched telemetry."}],
        })
        new_incidents.append(incident)

    state["events"].extend(events)
    state["incidents"].extend(new_incidents)
    for incident in new_incidents:
        state["audit"].append({
            "at": timestamp, "actor": "detection-engine", "action": "incident_created",
            "incident_id": incident["incident_id"], "correlation_id": incident["correlation_id"],
        })
    return {"accepted": len(events), "duplicates": 0, "incidents_created": len(new_incidents),
            "correlation_groups": len({item["correlation_id"] for item in new_incidents})}


def update_incident(state, incident_id, update, actor="soc-analyst", at=None):
    """Apply a valid lifecycle transition and/or assign an incident owner."""
    incident = next((item for item in state["incidents"] if item["incident_id"] == incident_id), None)
    if incident is None:
        raise KeyError("Incident not found")
    if not isinstance(update, dict):
        raise ValueError("Update must be an object")
    if not isinstance(actor, str) or not actor.strip() or len(actor) > 100:
        raise ValueError("Actor must be a non-empty string of at most 100 characters")
    timestamp = at or datetime.now(timezone.utc).isoformat()
    changed = False

    if "status" in update:
        target = update["status"]
        if not isinstance(target, str) or target not in VALID_STATUSES:
            raise ValueError("Invalid incident status")
        current = incident["status"]
        if target not in TRANSITIONS[current]:
            raise ValueError(f"Invalid lifecycle transition: {current} -> {target}")
        note = str(update.get("note", ""))[:500]
        incident["status"] = target
        incident["timeline"].append({"status": target, "at": timestamp, "actor": actor, "note": note})
        state["audit"].append({"at": timestamp, "actor": actor, "action": "status_changed",
                               "incident_id": incident_id, "from": current, "to": target, "note": note})
        changed = True

    if "owner" in update:
        owner = update["owner"]
        if not isinstance(owner, str) or not owner.strip() or len(owner) > 100:
            raise ValueError("Owner must be a non-empty string of at most 100 characters")
        previous = incident["owner"]
        incident["owner"] = owner.strip()
        state["audit"].append({"at": timestamp, "actor": actor, "action": "owner_changed",
                               "incident_id": incident_id, "from": previous, "to": incident["owner"]})
        changed = True

    if not changed:
        raise ValueError("Provide a status transition or owner assignment")
    incident["updated_at"] = timestamp
    return incident
