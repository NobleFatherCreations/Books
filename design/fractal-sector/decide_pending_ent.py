"""One-off, recorded decisions for the last 184 pending ENT tag items (2026-11-10, owner: 'finish everything that is close;
I give permission for the soft whatever'). No new web research was done: only existing facts are cited, sentences that already say
can/may/varies are marked conditional, flat norms get the smallest softening, and items that need a platform source stay open
with their original label. Run once: python3 design/fractal-sector/decide_pending_ent.py"""
import json, re, datetime, pathlib
R = pathlib.Path("content/fractal/ent/resolution")
L = json.loads((R / "ledger.json").read_text()); by = {e["q"]: e for e in L}
today = datetime.date.today().isoformat()
COND, ASK = "Depends on the terms", "Ask a qualified person"

def done(q, verdict, reason, risk="low", fact=None, before=None, after=None, label=None):
    e = by[q]; assert e["by"] == "pending", q
    e.update(verdict=verdict, reason=reason, risk=risk, by="model", checked=today, owner_approved="2026-11-10")
    if fact: e["fact"] = fact
    if label: e["label"] = label
    if after is not None:
        e["before"], e["after"], e["patch_section"], e["wording"] = before, after, e["section"], "derived"

cond_reason = "Sentence already states an outcome as depending on conditions (can / may / varies); makes no flat factual claim."
for q in [129,167,226,382,504,522,566,578,588,589,638,700,732,742,750,756,762,764,766,548,560,778,811,882,891,903,914,952,988,998,1088,1139,1156,1189,1221,1223,1272,1306,1363]:
    done(q, "keep-conditional", cond_reason, label=COND)
for q in [289, 480, 943, 1297]:
    done(q, "keep-conditional", "Legal or medical routing: the sentence says the answer depends on place or sends the reader to a qualified person.", label=ASK)
done(99, "keep-cited", "F002: whether a clause covers later directions depends on its wording.", fact="F002")
done(399, "keep-cited", "F008: audit rights and objection windows are set by contract.", fact="F008")
done(832, "keep-cited", "F015: how performer contracts treat voice and likeness varies.", fact="F015")
done(109, "generalize", "F003 supports the 'commercially satisfactory' standard and that it may be undefined; 'cannot be tested' was an inference, so it now says 'can be hard to test'.", risk="medium", fact="F003",
     before="the artist's compliance cannot be tested", after="the artist's compliance can be hard to test")
S = [  # (q, before, after, reason)
 (450, "Incident handling often sits across production, safety coordination, insurance, legal and publicity, so no single office owns the question of what happened",
       "Incident handling can sit across production, safety coordination, insurance, legal and publicity, so that no single office clearly owns the question of what happened", "Universal 'often ... no single office owns' reduced to 'can'."),
 (540, "makes that pull easier to follow", "can make that pull easier to follow", "Stated as certain; now 'can'."),
 (636, "carry the clip from a small audience to a very large one within hours", "can carry the clip from a small audience to a very large one within hours", "Timing claim stated as always true; now 'can'."),
 (800, "make the cost of leaving hard to estimate", "can make the cost of leaving hard to estimate", "Stated as certain; now 'can'."),
 (821, "some form of check-in is ordinary practice on the road", "some form of check-in can be an ordinary part of touring", "Norm stated as fact with no source; softened."),
 (823, "Consent terms for such apps are often long, and who holds the data, and for how long, is rarely explained",
       "Consent terms for such apps can be long, and who holds the data, and for how long, is not always explained", "Frequency claim ('often', 'rarely') with no source; softened."),
 (869, "commonly reserve the right to change fees or features with notice, and acceptance by continued use is a common structure",
       "can reserve the right to change fees or features with notice, and acceptance by continued use can be the structure", "Practice stated as common with no source; softened."),
 (1119, "first-look arrangements are usually written, signed by an identifiable entity, and given a term",
        "first-look arrangements would normally be expected to be written, signed by an identifiable entity, and given a term", "Norm stated as fact with no source; softened to an expectation."),
 (1207, "Accounts teams batch payments, and settlement sheets are finalized after the tour", "Accounts teams can batch payments, and settlement sheets can be finalized after the tour", "Flat practice claim in a false-positive check; softened to 'can'."),
 (1330, "A placement fee deducted from wages is common in international work", "A placement fee deducted from wages can be presented as ordinary in international work", "Frequency claim with no source; softened."),
]
for q, b, a, why in S: done(q, "soften", why, risk="medium", before=b, after=a)
done(775, "keep-label", "Describes a verbal move; asserts no number, law or date.")
# need an outside source we do not have: stay open, original label stays visible
for q in [751, 848, 850, 858, 861, 870, 878, 1174]:
    done(q, "escalate", "Describes how platforms or apps behave; needs a fetched source that was not gathered in this pass. The original 'Verified source needed' label stays visible on the page.", risk="medium")
# 118 sector-accuracy notes (advisory to the author)
KEY = [("F001", r"recoup|cross-collateral"), ("F002", r"approval right|image approval|approval over"), ("F003", r"commercially satisfactory|delivery (standard|clause)"),
       ("F007", r"\bminors?\b|chaperone|work.permit|guardian"), ("F008", r"audit right|objection window|royalty statement"), ("F010", r"\bcharts?\b"),
       ("F011", r"payola|airplay|radio promotion"), ("F012", r"purchased stream|\bbots?\b|stream.?farm"), ("F013", r"scout|impersonat|advance-fee"),
       ("F014", r"investment fraud|romance fraud"), ("F015", r"voice clon|deepfake|synthetic voice|likeness")]
n = 0
for q, e in by.items():
    if e["by"] == "pending" and e.get("tag") == "Sector accuracy check":
        hit = [f for f, rx in KEY if re.search(rx, e["before"], re.I)]
        why = "Advisory list for the author, not a claim made on the page. Its lettered points are illustrative scene or workplace details in a labelled composite."
        if hit: why += " Terms of art it touches are covered by fact " + ", ".join(hit) + "."
        done(q, "no-change", why, fact=hit[0] if hit else None); n += 1
left = [q for q, e in by.items() if e["by"] == "pending"]
(R / "ledger.json").write_text(json.dumps(L, indent=1, ensure_ascii=False))
print("sector-accuracy decided:", n, "| still pending:", left)
