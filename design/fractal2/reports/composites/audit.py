#!/usr/bin/env python3
"""Writes docs/COMPOSITES-AUDIT-2026-11-13.md. The order tables come from audit-data.json (written by build.py, which fails if a tactic is
missing or out of order). The resonance notes are the reviewer's judgment, written for the owner."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
A = json.loads((HERE / "audit-data.json").read_text())
BEFORE = {1: 2688, 2: 2197, 3: 2062, 4: 2133, 5: 2639}

RES = {
1: ("Trauma Bond Engine (coach, age 17)", "Strong, low risk",
 ["Adolescent attachment to an authority figure who controls access is something he will have seen in students and athletes. The \"pain becomes proof of love\" beat lands because the mother says the line out of love.",
  "The coach is a person, not a villain: he was coached the same way, he gave free hours, he still believes in you. That keeps a psychologist from defending the coach and lets him stay with the kid.",
  "The cost is specific and developmental (a game that stopped being joy, a body that plays through injury, a reflex answer that closes questions)."],
 ["The term \"trauma bonding\" and the owner's breakdown language (\"bonding neurochemistry,\" \"survival response\") are stated more firmly than the research supports; the Value-and-Impact report rates the evidence for the order effect as moderate. A psychologist will notice. The story itself makes no neuroscience claim.",
  "The owner's breakdown calls the pattern \"abuse.\" A reader may debate whether harsh coaching crosses that line. The story shows it as a pattern with a cost and leaves the label to the breakdown."],
 "Keep. If the Universal PDF carries the breakdown text, mark the neuroscience as \"my understanding\" per the project rule on contested science."),
2: ("Normalization Engine (teacher, years 1 to 3)", "Strong, low to medium risk",
 ["Teacher burnout and the \"it's always been like that\" culture are familiar from consultation work. The staff-room scene (fourteen calm faces, the quiet arithmetic of doubting yourself) is the most recognisable moment.",
  "Nobody is wrong. Ruth's comfort, Ms. Bell's \"it is what it is\" and Priya's laugh are each shown as care, which makes the system the cause.",
  "The cost image (the notebook from year one, a stranger's handwriting you'd like to apologise to) gives the psychologist something to feel without being told he failed."],
 ["The owner's counselor line (\"There's a waitlist for the free lunch program\") is a factual-sounding claim about one system. In his district it may not be true. It is the owner's verbatim line and the story is marked as a composite.",
  "A school counselor is a close colleague of a school psychologist. Ms. Bell is shown as overloaded and kind, not careless, which should keep it from reading as an attack."],
 "Keep. Do not add statistics about class size or lunch programs; one wrong figure would cost the rest."),
3: ("Public Shaming Ritual (sixth grader)", "Strong, medium risk",
 ["Public behavior boards and clip charts are a topic school psychologists have opinions on. Mrs. Pruitt is warm and runs a grade-wide system for a reason (one adult, 150 kids), so he can agree with the diagnosis without feeling the teacher is condemned.",
  "The child's POV is concrete: the folder, the index card for two houses, the girl crying before the marker touches the board, the nickname that spreads, midnight checking, the adult who still checks his bag.",
  "\"I think the system really worked\" is the most useful line for him: the intervention produced compliance, and nobody could see the cost."],
 ["The owner's civilizational echo (\"American education was built on public shaming\") is a sweeping claim and the single most likely sentence to draw \"that's not my experience.\" It is the owner's verbatim text and sits several pages after the story.",
  "A reader who works with PBIS may hear the story as criticism of positive behavior systems. It is about a public-display homework board, and the system page says so."],
 "Keep. Consider a one-line framing before the sweeping echo (\"this is my reading of the history\")."),
4: ("The Paper Child (psychologist POV)", "Highest relevance, highest risk",
 ["It is written from his seat: the file as flashlight, WISC-style block design, eligibility, the reflex of writing the strengths on page six. A real practitioner will know these details are right.",
  "The psychologist does everything right and still cannot stop the sequence, which is the point: the architecture, not the person, produced the outcome.",
  "The mother's keys, the signature that is \"very small,\" and \"he already knows what he is\" give the cost to the child; the half granola bar and the 2 a.m. grief give the cost to the adult."],
 ["The psychologist is the one who says \"This is how we get him help,\" so the manufactured-consent beat sits on his profession. A defensive read: \"you're saying we pressure parents.\" The breakdown states that nobody manufactured anything and the structure did, but the first reaction may come before that page.",
  "\"The referral is the only road to more adults\" will be false in a district with working tiered supports. The story limits it with \"In this building.\"",
  "Selective records, expert intimidation and the label are described as outputs of how the process is built, not of bad intent. If he feels judged, it will be here."],
 "Keep, and offer it to him last or with the system page next to it. Ask him one question first: does the meeting in the story look like a real one? His answer is the best correction available."),
5: ("The Calling Trap (psychologist POV)", "Highest resonance, medium risk",
 ["Caseload, legal timelines, the dashboard that counts the evaluation and not the grief group: these will be recognised at once, and the director who was once a psychologist herself prevents a \"villain administrator\" reading.",
  "The cost is the strongest in the set because it is the hardest to say aloud: the work you came to do is a distance you can't look at.",
  "\"Who would they have?\" lets him see the trap without anyone calling him weak."],
 ["It can read as a complaint about his own employer. Carol, Amanda and the dashboard builder are all written as good people, but a reader in a stretched district may take it personally. That may also be why it will matter most.",
  "I removed the video-evaluation detail for the replacement beat (tele-assessment is legitimate practice and would have started an argument). The replacement is now a rotating contractor on Thursdays."],
 "Keep. It is the most likely to make him feel seen."),
}

lines = ["# Composites audit: five cold opens (2026-11-13)", "",
 "Audited against the built PDF (`library/fractal2/review/Five-Machines-One-School.pdf`). Two questions per story: does the cold open use every tactic of its chain, in order? and how will it read to a school psychologist?", "",
 "## 1. Do the cold opens use every tactic, in order?", "",
 "Method: each tactic has one anchor phrase that appears in its story. `build.py` fails if a phrase is missing or if the anchors are not in chain order, so this table is a build output, not an opinion.", "",
 "| Story | Tactics | All present | In order | Story words (before → now) |", "|---|---|---|---|---|"]
for a in A:
    lines.append(f"| {a['n']}. {a['name']} | {len(a['tactics'])} | yes | yes | {BEFORE[a['n']]:,} → {a['words']:,} ({round(100*(1-a['words']/BEFORE[a['n']]))}% shorter) |")
lines += ["", "Anchor by anchor:", ""]
for a in A:
    lines += [f"**{a['n']}. {a['name']}**", "", "| # | Tactic | Scene | The line that carries it |", "|---|---|---|---|"]
    for k, t in enumerate(a["tactics"], 1):
        lines.append(f"| {k} | {t['tactic']} | {t['scene']} | \"{t['phrase']}\" |")
    lines.append("")
lines += ["What the trim kept: every anchor line, the 24 key lines from the owner's three scripts (checked word for word), each story's turning image, and the closing cost. What it cut: second examples of the same beat, scene-setting that repeated what an earlier line had already shown, and several explanatory sentences that told the reader what a beat meant.", "",
 "One structural note: the three Education stories were written in second person with the owner's own past-tense lines inside present-tense narration (for example, \"You called the counselor\" next to \"you ask if he's okay\"). That seam comes from keeping the owner's sentences verbatim. It is visible but not jarring.", "",
 "## 2. How each story will read to a school psychologist", ""]
for n in range(1, 6):
    title, verdict, strengths, risks, rec = RES[n]
    lines += [f"### {n}. {title}: {verdict}", "", "What will resonate:", ""] + [f"- {s}" for s in strengths] + ["", "What may cause friction:", ""] + [f"- {r}" for r in risks] + ["", f"Recommendation: {rec}", ""]
lines += ["### The \"on purpose\" pages", "",
 "Each story now has a one-page version where a person steers the same chain deliberately: an advisor, a principal who is a friend, a department chair, an ex-husband who is an assistant principal, a district director. None of the five villains is a school psychologist. Each page ends by naming the story you just read as the unintentional version, then says the feeling is the same from inside and the way out is the same. The ex-husband page is the highest-risk one: it touches custody, and a reader who knows custody records may say \"that isn't how it works.\" The page keeps it to what an educator could plausibly do with access he already has.", "",
 "### Across all five", "",
 "1. The most likely objection is \"that doesn't happen in my district.\" Defenses already in place: every story is labeled a composite, every cost page opens with \"nobody did anything wrong,\" no story states a statistic, and each system page names the structure (rationing, defensibility, budget cycle, one adult and 26 kids) instead of blaming a role.",
 "2. The most likely emotional reaction is recognition, not offense, if he reads the stories in the order: the three Education stories (not his profession) first, then The Paper Child and The Calling Trap last.",
 "3. The sweeping sentences are the owner's, not mine: \"American education was built on public shaming\" and the neurochemistry language. If you want a softer first read for him, those are the two places to add \"in my reading\" or \"in my understanding.\"",
 "4. No claim in the new prose is a statistic or a legal claim. Names, towns, and ages are invented."]
out = pathlib.Path(__file__).parents[4] / "docs" / "COMPOSITES-AUDIT-2026-11-13.md"
out.write_text("\n".join(lines) + "\n"); print("wrote", out)
