#!/usr/bin/env python3
"""Offline continuous-compliance normalizer for synthetic JSON finding exports."""
import argparse
import json
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

SEVERITIES = {"critical", "high", "medium", "low"}
STATUSES = {"open", "in_progress", "resolved", "accepted"}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def load_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def validate(snapshot, mapping_doc, control_ids):
    errors = []
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("sources"), list):
        return ["snapshot must contain a sources array"]
    mappings = mapping_doc.get("mappings") if isinstance(mapping_doc, dict) else None
    if not isinstance(mappings, list):
        return ["mapping document must contain a mappings array"]
    signal_map = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append("each mapping must be an object")
            continue
        signal, cid = mapping.get("signal"), mapping.get("control_id")
        if not signal or not cid:
            errors.append("each mapping requires signal and control_id")
            continue
        if signal in signal_map:
            errors.append(f"duplicate mapping for signal {signal}")
        signal_map[signal] = mapping
        if cid not in control_ids:
            errors.append(f"{signal}: unknown control_id {cid}")
    seen = set()
    for source in snapshot["sources"]:
        if not isinstance(source, dict) or not source.get("source_id"):
            errors.append("each source requires source_id")
            continue
        findings = source.get("findings")
        if not isinstance(findings, list):
            errors.append(f"{source['source_id']}: findings must be an array")
            continue
        for item in findings:
            if not isinstance(item, dict):
                errors.append(f"{source['source_id']}: finding must be an object")
                continue
            fid = item.get("finding_id")
            required = ("finding_id", "signal", "asset", "severity", "status",
                        "observed_at", "evidence_ref", "summary")
            missing = [key for key in required if not item.get(key)]
            if missing:
                errors.append(f"{fid or '<unknown>'}: missing {', '.join(missing)}")
                continue
            if fid in seen:
                errors.append(f"duplicate finding_id {fid}")
            seen.add(fid)
            if item["severity"] not in SEVERITIES:
                errors.append(f"{fid}: invalid severity {item['severity']}")
            if item["status"] not in STATUSES:
                errors.append(f"{fid}: invalid status {item['status']}")
            try:
                parsed = datetime.fromisoformat(item["observed_at"].replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    errors.append(f"{fid}: observed_at must include timezone")
            except (TypeError, ValueError, AttributeError):
                errors.append(f"{fid}: observed_at must be ISO-8601 with timezone")
            if item["signal"] not in signal_map:
                errors.append(f"{fid}: unmapped signal {item['signal']}")
            if item["status"] == "resolved" and not item.get("resolution_evidence_ref"):
                errors.append(f"{fid}: resolved finding requires resolution_evidence_ref")
    return errors


def build_report(snapshot, mapping_doc, generated_on=None):
    generated_on = generated_on or date.today().isoformat()
    mappings = {item["signal"]: item for item in mapping_doc["mappings"]}
    normalized, by_control = [], defaultdict(list)
    for source in snapshot["sources"]:
        for item in source["findings"]:
            mapping = mappings[item["signal"]]
            record = {
                "finding_id": item["finding_id"], "source_id": source["source_id"],
                "source_type": source.get("source_type", "unspecified"),
                "signal": item["signal"], "control_id": mapping["control_id"],
                "asset": item["asset"], "severity": item["severity"],
                "status": item["status"], "observed_at": item["observed_at"],
                "evidence_ref": item["evidence_ref"],
                "resolution_evidence_ref": item.get("resolution_evidence_ref"),
                "summary": item["summary"], "recommendation": mapping["recommendation"],
                "owner_role": mapping.get("owner_role", "Control owner")
            }
            normalized.append(record)
            by_control[record["control_id"]].append(record)
    controls = []
    for cid, records in sorted(by_control.items()):
        active = [r for r in records if r["status"] in ("open", "in_progress")]
        accepted = [r for r in records if r["status"] == "accepted"]
        resolved = [r for r in records if r["status"] == "resolved"]
        state = "attention_required" if active else (
            "risk_accepted" if accepted else "no_open_findings_in_snapshot")
        controls.append({
            "control_id": cid, "snapshot_findings": len(records),
            "open_or_in_progress": len(active), "accepted_risk": len(accepted),
            "resolved": len(resolved), "assessment_state": state
        })
    backlog = [r for r in normalized if r["status"] in ("open", "in_progress")]
    backlog.sort(key=lambda r: (SEVERITY_ORDER[r["severity"]], r["control_id"], r["finding_id"]))
    severity_counts = Counter(r["severity"] for r in normalized)
    status_counts = Counter(r["status"] for r in normalized)
    return {
        "schema_version": "1.0", "snapshot_id": snapshot.get("snapshot_id", "unspecified"),
        "generated_on": generated_on, "source_count": len(snapshot["sources"]),
        "finding_count": len(normalized), "severity_summary": dict(severity_counts),
        "status_summary": dict(status_counts), "control_summary": controls,
        "findings": normalized, "remediation_backlog": backlog,
        "important_note": "No mapped findings in a snapshot is not evidence that a control passed or that the organization is compliant. Validate evidence and closure with accountable control owners."
    }


def markdown_report(report):
    lines = ["# Continuous Compliance Snapshot", "",
             f"- Snapshot: {report['snapshot_id']}",
             f"- Generated: {report['generated_on']}",
             f"- Sources: {report['source_count']}",
             f"- Findings: {report['finding_count']}", "",
             "## Severity summary", ""]
    for severity in ("critical", "high", "medium", "low"):
        lines.append(f"- {severity.title()}: {report['severity_summary'].get(severity, 0)}")
    lines += ["", "## Control attention", "",
              "| Control | Findings | Open / in progress | Accepted | Resolved | State |",
              "|---|---:|---:|---:|---:|---|"]
    for item in report["control_summary"]:
        lines.append(f"| {item['control_id']} | {item['snapshot_findings']} | {item['open_or_in_progress']} | {item['accepted_risk']} | {item['resolved']} | {item['assessment_state']} |")
    lines += ["", "## Remediation backlog", ""]
    for item in report["remediation_backlog"]:
        lines += [f"### {item['finding_id']} — {item['severity'].upper()}",
                  f"- Asset: {item['asset']}",
                  f"- Source: {item['source_id']} ({item['source_type']})",
                  f"- Control: {item['control_id']}",
                  f"- Suggested owner: {item['owner_role']}",
                  f"- Evidence: {item['evidence_ref']}",
                  f"- Action: {item['recommendation']}", ""]
    lines += ["## Interpretation", "", report["important_note"],
              "This is a synthetic local portfolio demonstration, not an audit conclusion or compliance determination.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", default="data/source-findings.json")
    parser.add_argument("--rules", default="data/control-mappings.json")
    parser.add_argument("--controls", default="../data/control-catalogue.json")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()
    snapshot, rules, catalogue = load_json(args.sources), load_json(args.rules), load_json(args.controls)
    control_ids = {item["id"] for item in catalogue["controls"]}
    errors = validate(snapshot, rules, control_ids)
    if errors:
        parser.error("; ".join(errors))
    report = build_report(snapshot, rules)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "latest.md").write_text(markdown_report(report), encoding="utf-8")
    print(f"Normalized {report['finding_count']} findings across {report['source_count']} sources; output: {out}")


if __name__ == "__main__":
    main()
