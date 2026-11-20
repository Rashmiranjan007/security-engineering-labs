#!/usr/bin/env python3
"""Small, dependency-free threat risk scoring utility.

Usage:
  python tools/risk_engine.py --likelihood 4 --impact 5
  python tools/risk_engine.py --likelihood 3 --impact 4 --control-effectiveness 0.5

Control effectiveness is a documented estimate in [0, 1], not proof of mitigation.
Use 0 until a control is implemented and supported by operating evidence.
"""
from __future__ import annotations

import argparse
import json


def band(score: float) -> str:
    if score >= 17:
        return "CRITICAL"
    if score >= 10:
        return "HIGH"
    if score >= 5:
        return "MODERATE"
    return "LOW"


def calculate(likelihood: int, impact: int, effectiveness: float) -> dict:
    if likelihood not in range(1, 6) or impact not in range(1, 6):
        raise ValueError("likelihood and impact must be integers from 1 to 5")
    if not 0 <= effectiveness <= 1:
        raise ValueError("control effectiveness must be between 0 and 1")

    inherent = likelihood * impact
    # The residual estimate is intentionally conservative and rounded up.
    residual = max(1, int(inherent * (1 - effectiveness) + 0.999999))
    return {
        "likelihood": likelihood,
        "impact": impact,
        "inherent_score": inherent,
        "inherent_band": band(inherent),
        "control_effectiveness_estimate": effectiveness,
        "residual_score_estimate": residual,
        "residual_band_estimate": band(residual),
        "warning": (
            "Residual score is an estimate only. Do not reduce risk based on planned "
            "controls; validate design and operating evidence and document rationale."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--likelihood", type=int, required=True)
    parser.add_argument("--impact", type=int, required=True)
    parser.add_argument("--control-effectiveness", type=float, default=0.0)
    args = parser.parse_args()
    try:
        print(json.dumps(calculate(args.likelihood, args.impact, args.control_effectiveness), indent=2))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
