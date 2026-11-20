#!/usr/bin/env python3
"""Offline AI governance assessment and report generator; standard library only."""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path

DIMENSIONS = ("impact", "data_sensitivity", "autonomy", "exposure", "model_uncertainty")
BANDS = ((20, "Critical"), (15, "High"), (10, "Moderate"), (5, "Low"))


def band(score):
    for floor, label in BANDS:
        if score >= floor:
            return label
    return "Unrated"


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate(inventory, catalogue):
    errors = []
    systems = inventory.get("systems")
    controls = catalogue.get("controls")
    if not isinstance(systems, list) or not systems:
        errors.append("inventory.systems must be a non-empty array")
        systems = []
    if not isinstance(controls, list) or not controls:
        errors.append("catalogue.controls must be a non-empty array")
        controls = []
    control_ids = [c.get("id") for c in controls if isinstance(c, dict)]
    if len(control_ids) != len(set(control_ids)):
        errors.append("control IDs must be unique")
    known = set(control_ids)
    system_ids = []
    for system in systems:
        if not isinstance(system, dict):
            errors.append("each system must be an object")
            continue
        sid = system.get("id", "<missing>")
        system_ids.append(sid)
        missing = [key for key in ("name", "purpose", "business_owner", "technical_owner",
                                    "last_review", "review_interval_days", "dimensions",
                                    "required_controls", "control_evidence") if key not in system]
        if missing:
            errors.append(f"{sid}: missing fields: {', '.join(missing)}")
        dims = system.get("dimensions", {})
        for key in DIMENSIONS:
            value = dims.get(key) if isinstance(dims, dict) else None
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                errors.append(f"{sid}: dimension {key} must be an integer from 1 to 5")
        for cid in system.get("required_controls", []):
            if cid not in known:
                errors.append(f"{sid}: unknown required control {cid}")
        try:
            date.fromisoformat(system.get("last_review", ""))
        except (TypeError, ValueError):
            errors.append(f"{sid}: last_review must be YYYY-MM-DD")
        interval = system.get("review_interval_days")
        if not isinstance(interval, int) or isinstance(interval, bool) or interval <= 0:
            errors.append(f"{sid}: review_interval_days must be a positive integer")
    if len(system_ids) != len(set(system_ids)):
        errors.append("system IDs must be unique")
    return errors


def assess(inventory, catalogue, today=None):
    today = today or date.today()
    controls = {item["id"]: item for item in catalogue["controls"]}
    results = []
    for system in inventory["systems"]:
        inherent = sum(system["dimensions"][key] for key in DIMENSIONS)
        evidence_map = system.get("control_evidence", {})
        effective_controls = []
        gaps = []
        for cid in system.get("required_controls", []):
            control = controls[cid]
            record = evidence_map.get(cid, {})
            status = record.get("status", "not_implemented")
            evidence = record.get("evidence", [])
            if status == "implemented" and isinstance(evidence, list) and evidence:
                effective_controls.append({"id": cid, "points": control["effectiveness"]})
            else:
                gaps.append({"id": cid, "title": control["title"], "status": status,
                             "evidence_missing": not bool(evidence)})
        reduction = sum(item["points"] for item in effective_controls)
        residual = max(5, inherent - reduction)
        last_review = date.fromisoformat(system["last_review"])
        next_review = last_review + timedelta(days=system["review_interval_days"])
        overdue = next_review < today
        results.append({
            "id": system["id"], "name": system["name"], "lifecycle": system.get("lifecycle", "unknown"),
            "business_owner": system["business_owner"], "technical_owner": system["technical_owner"],
            "inherent_score": inherent, "inherent_band": band(inherent),
            "residual_score": residual, "residual_band": band(residual),
            "effective_controls": effective_controls, "control_gaps": gaps,
            "overdue_review": overdue, "next_review": next_review.isoformat(),
            "required_control_count": len(system.get("required_controls", [])),
            "implemented_with_evidence": len(effective_controls)
        })
    counts = {label: sum(1 for item in results if item["residual_band"] == label)
              for label in ("Critical", "High", "Moderate", "Low")}
    return {"schema_version": "1.0", "generated_on": today.isoformat(),
            "system_count": len(results), "risk_summary": counts, "assessments": results}


def markdown_report(report):
    lines = ["# AI Governance Assessment Report", "",
             f"Generated: {report['generated_on']}", "",
             f"Systems assessed: **{report['system_count']}**", "",
             "## Residual risk summary", "",
             "| Critical | High | Moderate | Low |",
             "|---:|---:|---:|---:|",
             "| " + " | ".join(str(report["risk_summary"][key])
                                for key in ("Critical", "High", "Moderate", "Low")) + " |",
             "", "## System assessments", ""]
    for item in report["assessments"]:
        lines += [f"### {item['id']} — {item['name']}", "",
                  f"- Lifecycle: {item['lifecycle']}",
                  f"- Owners: {item['business_owner']} (business); {item['technical_owner']} (technical)",
                  f"- Inherent risk: {item['inherent_band']} ({item['inherent_score']}/25)",
                  f"- Residual risk: {item['residual_band']} ({item['residual_score']}/25)",
                  f"- Controls with implementation evidence: {item['implemented_with_evidence']}/{item['required_control_count']}",
                  f"- Next review: {item['next_review']} — {'OVERDUE' if item['overdue_review'] else 'current'}",
                  "", "Control gaps:"]
        if item["control_gaps"]:
            lines.extend([f"- {gap['id']} — {gap['title']} (status: {gap['status']}; evidence missing: {gap['evidence_missing']})"
                          for gap in item["control_gaps"]])
        else:
            lines.append("- None recorded.")
        lines.append("")
    lines += ["## Interpretation", "",
              "This report is a deterministic educational assessment based on supplied inventory and evidence references. It is not legal advice, an audit opinion, certification, proof of compliance, or a substitute for accountable human risk decisions.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", default="data/ai-inventory.json")
    parser.add_argument("--controls", default="data/control-catalogue.json")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()
    inventory, catalogue = load_json(args.inventory), load_json(args.controls)
    errors = validate(inventory, catalogue)
    if errors:
        parser.error("; ".join(errors))
    report = assess(inventory, catalogue)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "latest.md").write_text(markdown_report(report), encoding="utf-8")
    print(f"Assessed {report['system_count']} AI systems. Reports: {out / 'latest.json'} and {out / 'latest.md'}")


if __name__ == "__main__":
    main()
