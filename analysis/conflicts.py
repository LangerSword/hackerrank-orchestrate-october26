"""Identity conflict scan."""
import argparse, csv
from pathlib import Path
from idscan import Index, scan, snippet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", required=True)
    ap.add_argument("--evidence", default="dataset")
    ap.add_argument("--ignore", default=None)
    ap.add_argument("--out", default="analysis/conflict_lines.csv")
    a = ap.parse_args()
    idx = Index(a.subjects)

    print("== (a) identifiers owned by >1 subject ==")
    n = 0
    for (kind, key), subs in sorted(idx.owner.items()):
        if len(subs) > 1:
            n += 1
            print(f"  {kind:5s} {key}  ->  {sorted(subs)}")
    print(f"  total: {n}\n")

    rows = []
    for rel, ln, line, hits in scan(idx, a.evidence, a.ignore):
        subs = {s for _, _, s, _ in hits}
        if len(subs) >= 2:
            rows.append(dict(file=rel, line=ln, subjects="|".join(sorted(subs)),
                             tokens="|".join(f"{k}:{t}:{m}" for k, t, _, m in hits),
                             snippet=snippet(line, hits[0][1], 90)))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, ["file", "line", "subjects", "tokens", "snippet"])
        w.writeheader()
        w.writerows(rows)
    print(f"== (b) cross-subject lines: {len(rows)} -> {a.out}")
    for r in rows[:15]:
        print(f"  {r['file']}:{r['line']}  {r['subjects']}")


if __name__ == "__main__":
    main()
