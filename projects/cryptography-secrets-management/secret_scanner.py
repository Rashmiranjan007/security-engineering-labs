"""Read-only heuristic scanner for common secret patterns in text files."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

RULES = {
    "aws_access_key_id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key_pem": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token_like": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "generic_assignment": re.compile(
        r"(?i)\b(?:password|passwd|client_secret|api_key|access_token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
}
MAX_FILE_BYTES = 2 * 1024 * 1024
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}


def scan_file(path: Path) -> list[dict[str, int | str]]:
    """Return rule/path/line metadata only; never return matched values."""
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return []
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    findings = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        for rule_name, pattern in RULES.items():
            if pattern.search(line):
                findings.append({
                    "file": str(path),
                    "line": line_number,
                    "rule": rule_name,
                })
    return findings


def scan_path(root: Path) -> list[dict[str, int | str]]:
    """Scan a selected file or directory; skip common generated/vendor folders."""
    if root.is_file():
        return scan_file(root)
    if not root.is_dir():
        raise ValueError(f"Path does not exist or is not a file/directory: {root}")
    findings = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        findings.extend(scan_file(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only local secret-pattern scanner")
    parser.add_argument("path", type=Path, help="Explicit file or directory to scan")
    parser.add_argument("--json", action="store_true", help="Print JSON findings")
    args = parser.parse_args()
    try:
        findings = scan_path(args.path)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for item in findings:
            print(f"{item['file']}:{item['line']}: {item['rule']}")
        print(f"Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
