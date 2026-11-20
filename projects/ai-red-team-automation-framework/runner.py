"""Run synthetic AI security scenarios against the local deterministic mock."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from mock_target import MockTarget

ROOT = Path(__file__).parent
WEIGHTS = {"critical": 10, "high": 7, "medium": 4, "low": 2, "informational": 1}


def run_suite(profile="secure"):
    cases = json.loads((ROOT / "test-cases" / "scenarios.json").read_text(encoding="utf-8"))
    target = MockTarget(profile)
    results = []
    for case in cases:
        observed = target.execute(case)
        passed = observed["blocked"] is case["expected"]["blocked"]
        results.append({
            "id": case["id"],
            "category": case["category"],
            "severity": case["severity"],
            "description": case["description"],
            "expected_blocked": case["expected"]["blocked"],
            "observed_blocked": observed["blocked"],
            "passed": passed,
            "risk_weight": 0 if passed else WEIGHTS[case["severity"]],
            "control": case["control"],
        })
    failed = [item for item in results if not item["passed"]]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "local-deterministic-mock-only",
        "profile": profile,
        "summary": {
            "total": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "risk_score": sum(item["risk_weight"] for item in results),
        },
        "results": results,
    }


def markdown_report(report):
    summary = report["summary"]
    lines = [
        "# AI Red Team Automation Report", "",
        f"- Profile: `{report['profile']}`",
        f"- Scope: `{report['scope']}`",
        f"- Generated: {report['generated_at']}",
        f"- Results: **{summary['passed']}/{summary['total']} passed**",
        f"- Failed-control risk score: **{summary['risk_score']}**", "",
        "| Test | Category | Severity | Result | Observed blocked |",
        "|---|---|---|---|---|",
    ]
    for item in report["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        lines.append(f"| {item['id']} | {item['category']} | {item['severity']} | {status} | {item['observed_blocked']} |")
    lines += ["", "> Synthetic local simulation only; not evidence of production security.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("secure", "intentionally-vulnerable"), default="secure")
    args = parser.parse_args()
    report = run_suite(args.profile)
    output = ROOT / "reports"
    output.mkdir(exist_ok=True)
    (output / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "latest.md").write_text(markdown_report(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
