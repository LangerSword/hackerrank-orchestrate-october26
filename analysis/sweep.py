"""False-COMPLETE sweep + unconsumed-line counter."""
import argparse, csv, json
from collections import Counter, defaultdict
from pathlib import Path
from idscan import Index, scan, snippet, iter_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", required=True)
    ap.add_argument("--output", default="output.csv")
    ap.add_argument("--evidence", default="dataset")
    ap.add_argument("--ignore", default=None, help="regex on relative path")
    ap.add_argument("--consumed", default=None)
    ap.add_argument("--out", default="analysis/complete_candidates.csv")
    a = ap.parse_args()

    idx = Index(a.subjects)
    status = {r["case_id"]: r["deletion_status"]
              for r in csv.DictReader(open(a.output, newline=""))}
    complete = {c for c, s in status.items() if s == "COMPLETE"}
    cons = json.loads(Path(a.consumed).read_text()) if a.consumed else None

    def consumed(rel, n, tok):
        if cons is None or rel not in cons:
            return False
        c = cons[rel]
        return n in set(c.get("lines", [])) or tok.lower() in set(c.get("tokens", []))

    rows, per_case, unconsumed = [], defaultdict(list), Counter()
    for rel, n, line, hits in scan(idx, a.evidence, a.ignore):
        for kind, tok, subj, match in hits:
            c = consumed(rel, n, tok)
            if cons is not None and not c:
                unconsumed[rel] += 1
            if c:
                continue
            for case in idx.subject_cases[subj]:
                if case in complete:
                    r = dict(case_id=case, subject=subj, file=rel, line=n,
                             kind=kind, match=match, token=tok,
                             snippet=snippet(line, tok))
                    rows.append(r)
                    per_case[case].append(r)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    cols = ["case_id", "subject", "file", "line", "kind", "match", "token", "snippet"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["match"] != "loose", r["case_id"], r["file"], r["line"])))

    loose_cases = {r["case_id"] for r in rows if r["match"] == "loose"}
    print(f"COMPLETE cases: {len(complete)}")
    print(f"  with >=1 unconsumed hit: {len(per_case)}" if cons else
          f"  with >=1 raw hit (no --consumed; expect many legit): {len(per_case)}")
    print(f"  with a LOOSE-only hit (priority): {len(loose_cases)}")
    print(f"candidates written to {a.out}")
    if cons is not None:
        print("\nunconsumed subject-token lines per file (parser gap counter):")
        for rel, k in unconsumed.most_common(25):
            print(f"  {k:6d}  {rel}")
    list(iter_files(a.evidence, a.ignore))
    sk = getattr(iter_files, "skipped", [])
    if sk:
        print(f"\nNOT scanned (non-text, e.g. PDF/PNG): {len(sk)} files; first 10: {sk[:10]}")


if __name__ == "__main__":
    main()
