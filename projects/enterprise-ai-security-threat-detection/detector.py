"""Local synthetic AI security event detector and report generator."""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
VALID_ENVIRONMENTS = {"development", "staging", "production"}
VALID_OUTCOMES = {"allow", "deny", "detect", "blocked"}
SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_events(events):
    if not isinstance(events, list):
        raise ValueError("Events must be a JSON array")
    seen = set()
    required = {"event_id", "timestamp", "event_type", "workload", "environment", "actor", "resource", "outcome", "details"}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"Event {index} must be an object")
        missing = required - event.keys()
        if missing:
            raise ValueError(f"Event {index} missing fields: {sorted(missing)}")
        if not isinstance(event["event_id"], str) or not event["event_id"].strip():
            raise ValueError(f"Event {index} has invalid event_id")
        if event["event_id"] in seen:
            raise ValueError(f"Duplicate event_id: {event['event_id']}")
        seen.add(event["event_id"])
        try:
            datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValueError(f"Event {event['event_id']} has invalid ISO-8601 timestamp")
        if event["environment"] not in VALID_ENVIRONMENTS:
            raise ValueError(f"Event {event['event_id']} has invalid environment")
        if event["outcome"] not in VALID_OUTCOMES:
            raise ValueError(f"Event {event['event_id']} has invalid outcome")
        if not isinstance(event["details"], dict):
            raise ValueError(f"Event {event['event_id']} details must be an object")
    return events


def detect(events, rules):
    rule_index = {rule["event_type"]: rule for rule in rules}
    incidents = []
    for event in validate_events(events):
        rule = rule_index.get(event["event_type"])
        if not rule:
            continue
        incidents.append({
            "incident_id": f"{rule['rule_id']}:{event['event_id']}",
            "event_id": event["event_id"],
            "rule_id": rule["rule_id"],
            "event_type": event["event_type"],
            "severity": rule["severity"],
            "risk_score": int(rule["risk_score"]),
            "workload": event["workload"],
            "environment": event["environment"],
            "actor": event["actor"],
            "resource": event["resource"],
            "outcome": event["outcome"],
            "framework_refs": rule["framework_refs"],
            "recommendation": rule["recommendation"],
        })
    incidents.sort(key=lambda item: (SEVERITY_ORDER[item["severity"]], item["risk_score"]), reverse=True)
    return incidents


def build_report(events, incidents):
    severities = Counter(item["severity"] for item in incidents)
    workloads = Counter(item["workload"] for item in incidents)
    return {
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "scope": "synthetic-local-events-only",
        "summary": {
            "events_processed": len(events),
            "incidents_detected": len(incidents),
            "risk_score": min(100, sum(item["risk_score"] for item in incidents)),
            "by_severity": {key: severities.get(key, 0) for key in ("critical", "high", "medium", "low")},
            "by_workload": dict(workloads),
        },
        "incidents": incidents,
        "limitations": "Deterministic example rules over synthetic events; not a production detection or SIEM platform."
    }


def render_markdown(report):
    summary = report["summary"]
    lines = [
        "# Enterprise AI Security Detection Report", "",
        f"- Scope: `{report['scope']}`",
        f"- Events processed: **{summary['events_processed']}**",
        f"- Incidents detected: **{summary['incidents_detected']}**",
        f"- Aggregate risk score (capped at 100): **{summary['risk_score']}**", "",
        "## Severity summary", "",
        "| Critical | High | Medium | Low |",
        "|---:|---:|---:|---:|",
        f"| {summary['by_severity']['critical']} | {summary['by_severity']['high']} | {summary['by_severity']['medium']} | {summary['by_severity']['low']} |", "",
        "## Incidents", "",
        "| Rule | Severity | Workload | Environment | Resource | Recommended action |",
        "|---|---|---|---|---|---|",
    ]
    for item in report["incidents"]:
        lines.append(f"| {item['rule_id']} | {item['severity']} | {item['workload']} | {item['environment']} | {item['resource']} | {item['recommendation']} |")
    lines += ["", f"> {report['limitations']}", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "scenarios" / "sample-events.json"))
    parser.add_argument("--rules", default=str(ROOT / "config" / "detection-rules.json"))
    parser.add_argument("--output-dir", default=str(ROOT / "reports"))
    args = parser.parse_args()
    events = load_json(args.input)
    rules = load_json(args.rules)
    incidents = detect(events, rules)
    report = build_report(events, incidents)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "latest.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
