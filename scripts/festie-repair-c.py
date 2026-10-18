#!/usr/bin/env python3
"""Festie Bible, repair pass C — ledger reconciliation and a duplicate title.

Idempotent. Run festie-build.py afterwards.
"""
import json
import sys

DATA = "content/festie-bible-data.json"

# The page carried two separate v1 lines while sites.json carries one v1
# entry, so the two ledgers could never reconcile by count. Merged into the
# one entry that describes the launch.
V1_OLD_A = ("Launched The Festie Bible as its own door on the hub: 12 field guides "
            "rebuilt from the original 183-page collection.")
V1_OLD_B = ("Fixed the systemic label-collision and near-invisible interior brand mark "
            "from the source document.")
V1_NEW = ("Launched The Festie Bible as its own door on the hub: 12 field guides rebuilt "
          "from the original 183-page collection, with the source document’s label "
          "collisions and near-invisible interior brand mark fixed on the way in.")

# S.A.F.E. #6 and #7 shipped under the same hook, so the guide's jump index
# listed the same title twice under SEE SOMETHING with no way to tell them
# apart. #6 is intervening as a bystander; #7 is reading how altered someone
# is and deciding whether to stay. Only the second is renamed.
DUP_OLD = "SEE SOMETHING — DO SOMETHING"
DUP_NEW = "HOW ALTERED IS TOO ALTERED"


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    notes = []

    # --- merge the duplicate v1 changelog entries -----------------------
    cl = d["changelog"]
    a = next((i for i, c in enumerate(cl) if isinstance(c, dict) and c["summary"] == V1_OLD_A), None)
    b = next((i for i, c in enumerate(cl) if isinstance(c, dict) and c["summary"] == V1_OLD_B), None)
    if a is not None and b is not None:
        cl[a]["summary"] = V1_NEW
        cl.pop(b)
        notes.append("merged the two v1 changelog entries into one")

    # --- rename the duplicate S.A.F.E. hook -----------------------------
    for g in d["guides"]:
        if g["acronym"] != "S.A.F.E.":
            continue
        dupes = [sc for sc in g["scenarios"] if sc["hook"] == DUP_OLD]
        if len(dupes) == 2:
            # the second one is the impairment-reading card
            dupes[1]["hook"] = DUP_NEW
            notes.append(f"renamed the second '{DUP_OLD}' to '{DUP_NEW}'")

    if not notes:
        print("(already clean)")
        return 0
    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(DATA, "a", encoding="utf-8").write("\n")
    for n in notes:
        print("  " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
