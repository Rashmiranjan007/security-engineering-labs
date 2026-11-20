"""Normalize synthetic EKS telemetry into the enterprise AI SOC event contract."""
from datetime import datetime


SIGNAL_TYPES = {
    "k8s_exec_into_ai_pod",
    "privileged_ai_workload",
    "service_account_token_anomaly",
    "network_policy_drift",
    "container_image_digest_mismatch",
    "runtime_threat_detection",
}
ENVIRONMENTS = {"development", "staging", "production"}
OUTCOMES = {"allow", "deny", "detect", "blocked"}


def normalize_event(source):
    required = {
        "source_event_id", "timestamp", "signal_type", "cluster", "namespace",
        "pod", "node", "workload", "actor", "resource", "environment",
        "outcome", "details",
    }
    if not isinstance(source, dict):
        raise ValueError("Source event must be an object")
    missing = required - source.keys()
    if missing:
        raise ValueError(f"Source event missing fields: {sorted(missing)}")
    if source["signal_type"] not in SIGNAL_TYPES:
        raise ValueError(f"Unsupported EKS signal type: {source['signal_type']}")
    if source["environment"] not in ENVIRONMENTS:
        raise ValueError("Invalid environment")
    if source["outcome"] not in OUTCOMES:
        raise ValueError("Invalid outcome")
    if not isinstance(source["details"], dict):
        raise ValueError("Source event details must be an object")
    if not all(isinstance(source[key], str) and source[key].strip() for key in
               ("source_event_id", "cluster", "namespace", "pod", "node", "workload", "actor", "resource")):
        raise ValueError("Source identifiers and workload context must be non-empty strings")
    try:
        datetime.fromisoformat(source["timestamp"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValueError("Invalid ISO-8601 timestamp")

    return {
        "event_id": source["source_event_id"],
        "timestamp": source["timestamp"],
        "event_type": source["signal_type"],
        "workload": source["workload"],
        "environment": source["environment"],
        "actor": source["actor"],
        "resource": source["resource"],
        "outcome": source["outcome"],
        "details": {
            **source["details"],
            "source_system": "synthetic-eks-telemetry",
            "cluster": source["cluster"],
            "namespace": source["namespace"],
            "pod": source["pod"],
            "node": source["node"],
            "source_event_id": source["source_event_id"],
        },
    }


def normalize_batch(events, batch_id):
    if not isinstance(events, list) or not events:
        raise ValueError("Input must be a non-empty JSON array")
    if not isinstance(batch_id, str) or not batch_id.strip() or len(batch_id) > 40:
        raise ValueError("Batch ID must be a non-empty string of at most 40 characters")
    normalized = []
    seen = set()
    for source in events:
        event = normalize_event(source)
        event["event_id"] = f"{batch_id}-{event['event_id']}"
        if event["event_id"] in seen:
            raise ValueError(f"Duplicate source event ID: {event['event_id']}")
        seen.add(event["event_id"])
        normalized.append(event)
    return normalized
