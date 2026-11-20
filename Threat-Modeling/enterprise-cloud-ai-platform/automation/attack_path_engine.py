#!/usr/bin/env python3
"""Defensive attack-path prioritization over an explicitly supplied architecture graph.

This is a transparent modeling heuristic. It does not discover vulnerabilities,
execute exploits, or prove that a path is reachable in a deployed environment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_model(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        model = json.load(handle)
    validate_model(model)
    return model


def validate_model(model: dict[str, Any]) -> None:
    if model.get("schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    for key in ("nodes", "edges", "weaknesses", "entrypoints", "targets"):
        if not isinstance(model.get(key), list):
            raise ValueError(f"{key} must be an array")
    node_ids = [n.get("id") for n in model["nodes"]]
    weakness_ids = [w.get("id") for w in model["weaknesses"]]
    if None in node_ids or len(node_ids) != len(set(node_ids)):
        raise ValueError("node IDs must be present and unique")
    if None in weakness_ids or len(weakness_ids) != len(set(weakness_ids)):
        raise ValueError("weakness IDs must be present and unique")
    known_nodes, known_weaknesses = set(node_ids), set(weakness_ids)
    for edge in model["edges"]:
        if edge.get("source") not in known_nodes or edge.get("target") not in known_nodes:
            raise ValueError(f"edge references unknown node: {edge}")
    for node in model["nodes"]:
        if not set(node.get("weakness_ids", [])) <= known_weaknesses:
            raise ValueError(f"node {node['id']} references unknown weakness")
    for edge in model["edges"]:
        if not set(edge.get("weakness_ids", [])) <= known_weaknesses:
            raise ValueError("edge references unknown weakness")
    if not set(model["entrypoints"]) <= known_nodes or not set(model["targets"]) <= known_nodes:
        raise ValueError("entrypoints and targets must reference known nodes")
    for weakness in model["weaknesses"]:
        for field in ("likelihood", "impact"):
            value = weakness.get(field)
            if not isinstance(value, int) or not 1 <= value <= 5:
                raise ValueError(f"{weakness.get('id')}: {field} must be an integer from 1 to 5")


def analyze(model: dict[str, Any], max_depth: int = 8) -> dict[str, Any]:
    validate_model(model)
    nodes = {n["id"]: n for n in model["nodes"]}
    weaknesses = {w["id"]: w for w in model["weaknesses"]}
    adjacency: dict[str, list[dict[str, Any]]] = {node_id: [] for node_id in nodes}
    for edge in model["edges"]:
        adjacency[edge["source"]].append(edge)

    paths: list[dict[str, Any]] = []

    def walk(current: str, target: str, visited: list[str], used_weaknesses: list[str]) -> None:
        if current == target:
            if used_weaknesses:
                unique_ids = list(dict.fromkeys(used_weaknesses))
                details = [weaknesses[w_id] for w_id in unique_ids]
                raw_score = sum(w["likelihood"] * w["impact"] for w in details)
                score = min(25, raw_score)
                paths.append({
                    "entrypoint": visited[0],
                    "target": target,
                    "node_path": visited,
                    "weakness_ids": unique_ids,
                    "weaknesses": details,
                    "raw_cumulative_score": raw_score,
                    "prioritization_score": score,
                    "rating": "CRITICAL" if score >= 17 else "HIGH" if score >= 10 else "MODERATE" if score >= 5 else "LOW",
                    "business_impact": nodes[target].get("business_impact", "Not specified"),
                    "recommended_break_points": list(dict.fromkeys(
                        control for w in details for control in w.get("mitigations", [])
                    )),
                })
            return
        if len(visited) >= max_depth:
            return
        for edge in adjacency[current]:
            nxt = edge["target"]
            if nxt in visited:
                continue
            next_weaknesses = used_weaknesses + nodes[nxt].get("weakness_ids", []) + edge.get("weakness_ids", [])
            walk(nxt, target, visited + [nxt], next_weaknesses)

    for entry in model["entrypoints"]:
        for target in model["targets"]:
            walk(entry, target, [entry], nodes[entry].get("weakness_ids", []))

    # Stable de-duplication in case multiple graph declarations produce the same chain.
    unique: dict[tuple[str, ...], dict[str, Any]] = {}
    for path in paths:
        key = tuple(path["node_path"])
        if key not in unique or path["prioritization_score"] > unique[key]["prioritization_score"]:
            unique[key] = path
    ranked = sorted(unique.values(), key=lambda p: (-p["prioritization_score"], p["node_path"]))
    for index, path in enumerate(ranked, 1):
        path["rank"] = index
    return {
        "model_name": model.get("name", "Unnamed architecture"),
        "method": "sum of likelihood × impact for unique weaknesses on a path, capped at 25",
        "score_note": "A prioritization heuristic, not a probability, exploitability verdict, or residual-risk score.",
        "path_count": len(ranked),
        "attack_paths": ranked,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Architecture graph JSON")
    parser.add_argument("--output", help="Write JSON report to this path; stdout if omitted")
    parser.add_argument("--max-depth", type=int, default=8)
    args = parser.parse_args()
    if args.max_depth < 2:
        parser.error("--max-depth must be at least 2")
    report = analyze(load_model(args.input), args.max_depth)
    rendered = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
