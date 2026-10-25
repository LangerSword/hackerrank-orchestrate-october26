#!/usr/bin/env python3
"""Measure abstain / oracle / guess under exact-step F1 and positional fields."""
from __future__ import annotations

import copy
import csv
import difflib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("step_no", "phase", "system_id", "resource_id", "operation",
          "state", "evidence_id")
CONTENT = ("phase", "system_id", "resource_id", "operation", "state", "evidence_id")


def load(path: Path) -> dict:
    return {r["case_id"]: r for r in csv.DictReader(path.open(newline="", encoding="utf-8"))}


def steps(row: dict) -> list[dict]:
    return json.loads(row["steps_json"])


def missing_steps(gold: dict, pred: dict) -> dict[str, list[tuple[int, dict]]]:
    out = {}
    for case_id, row in gold.items():
        gs, ps = steps(row), steps(pred[case_id])
        sm = difflib.SequenceMatcher(
            a=[tuple(s.get(k) for k in CONTENT) for s in gs],
            b=[tuple(s.get(k) for k in CONTENT) for s in ps],
        )
        missing = []
        for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
            if tag in ("delete", "replace"):
                missing.extend((i, gs[i]) for i in range(i1, i2))
        if missing:
            out[case_id] = missing
    return out


def guess_step(gold_step: dict, rng: random.Random) -> dict:
    system = gold_step.get("system_id", "")
    if system == "analytics_platform":
        return {"step_no": 0, "phase": "VERIFICATION", "system_id": system,
                "resource_id": f"analytics_{rng.randint(1, 9999):04d}",
                "operation": "VERIFY_RECORD_ANONYMIZED", "state": "ANONYMIZED",
                "evidence_id": ""}
    if system == "security_service":
        return {"step_no": 0, "phase": "VERIFICATION", "system_id": system,
                "resource_id": f"audit_record_{rng.randint(1, 9999)}",
                "operation": "VERIFY_RECORD_PRESENT", "state": "PRESENT",
                "evidence_id": gold_step.get("evidence_id", "")}
    return {"step_no": 0, "phase": "VERIFICATION", "system_id": "account_service",
            "resource_id": f"account_{rng.randint(1, 9999):03d}",
            "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT",
            "evidence_id": ""}


def score(gold: dict, pred: dict) -> tuple[int, int, float, float, float]:
    fields = total = match = 0
    for case_id, row in gold.items():
        gs, ps = steps(row), steps(pred[case_id])
        total += len(gs) * len(FIELDS)
        for i, gstep in enumerate(gs):
            if i < len(ps):
                fields += sum(gstep.get(k) == ps[i].get(k) for k in FIELDS)
        # exact-step content match (step_no excluded)
        remaining = [tuple(s.get(k) for k in CONTENT) for s in ps]
        for gstep in gs:
            key = tuple(gstep.get(k) for k in CONTENT)
            if key in remaining:
                match += 1
                remaining.remove(key)
    precision = match / sum(len(steps(p)) for p in pred.values()) if pred else 0.0
    recall = match / sum(len(steps(g)) for g in gold.values())
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return fields, total, precision, recall, f1


def main() -> int:
    gold = load(ROOT / "dataset/sample_output.csv")
    pred = load(ROOT / "analysis/sample_output.csv")
    missing = missing_steps(gold, pred)
    print(f"cases with missing steps: {len(missing)}; missing: {sum(len(v) for v in missing.values())}")

    current_fields, total, precision, recall, f1 = score(gold, pred)
    print(f"omit      fields {current_fields}/{total} ({current_fields/total:.1%}) "
          f"P/R/F1 {precision:.3f}/{recall:.3f}/{f1:.3f}")

    oracle = {cid: {"case_id": cid, "deletion_status": row["deletion_status"],
                    "steps_json": row["steps_json"]} for cid, row in gold.items()}
    of, ot, op, orr, of1 = score(gold, oracle)
    print(f"oracle    fields {of}/{ot} ({of/ot:.1%}) P/R/F1 {op:.3f}/{orr:.3f}/{of1:.3f}")

    rng = random.Random(20261025)
    trials = 4000
    sums = [0.0, 0.0, 0.0, 0.0, 0.0]
    p = 0.438
    for _ in range(trials):
        trial = {}
        for case_id, row in gold.items():
            ps = copy.deepcopy(steps(pred[case_id]))
            for offset, (gold_index, gstep) in enumerate(missing.get(case_id, [])):
                chosen = copy.deepcopy(gstep) if rng.random() < p else guess_step(gstep, rng)
                chosen["step_no"] = 0
                ps.insert(gold_index, chosen)
            for i, step in enumerate(ps, start=1):
                step["step_no"] = i
            trial[case_id] = {"case_id": case_id,
                              "deletion_status": row["deletion_status"],
                              "steps_json": json.dumps(ps)}
        vals = score(gold, trial)
        for i, val in enumerate(vals):
            sums[i] += val
    print(f"guess p={p:.3f} fields {sums[0]/trials:.0f}/{total} ({sums[0]/trials/total:.1%}) "
          f"P/R/F1 {sums[2]/trials:.3f}/{sums[3]/trials:.3f}/{sums[4]/trials:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
