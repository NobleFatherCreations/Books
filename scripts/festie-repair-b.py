#!/usr/bin/env python3
"""Festie Bible, repair pass B — the cards shipping with blank fields.

Two separate problems, fixed two different ways.

`clinical` was blank on 19 cards. Every one is a tools, accountability,
community or emergency page rather than a predator-pattern card, which is why
it was skipped — but the field is already used for plain domain labels on ten
existing pages of exactly that kind ("Volunteer Rights / Labor Awareness",
"Community Resources / Legal Rights"). So these are filled in that same
convention rather than with invented clinical framing, and no new field or
renderer change is needed.

`dark` and `darkTitle` were blank on 6 cards. Unlike the above, all six ARE
pattern cards, and all six are about substances — the highest-stakes subject
in the book and the one place a missing Dark Reality costs the most. Those are
written here.

Idempotent: only ever fills a field that is currently empty.
"""
import json
import sys

DATA = "content/festie-bible-data.json"

CLINICAL = {
    ("G.R.O.V.E.", "THE EXIT IS ALWAYS YOURS"): "Exit Planning / Coercive Control Countermeasure",
    ("B.A.S.S.", "BUYING AND SELLING SAFELY"): "Legal Risk Awareness / Undercover Operations",
    ("B.A.S.S.", "THE EXIT IS ALWAYS YOURS"): "Exit Planning / Sunk Cost Interruption",
    ("B.A.S.S.", "THE POWER YOU CARRY"): "Power Differential Awareness / Personal Accountability",
    ("R.A.V.E.", "BUYING AND SELLING AT YOUR FIRST FEST"): "Legal Risk Awareness / Undercover Operations",
    ("P.R.I.D.E.", "REAL QUEER COMMUNITY VS BEING COLLECTED"): "Authentic Community vs Tokenization",
    ("S.O.U.N.D.", "THE STAGE IS NOT A CONSENT BYPASS"): "Power Differential Awareness / Consent Education",
    ("S.O.U.N.D.", "WHAT GOOD LEADERSHIP SOUNDS LIKE"): "Platform Responsibility / Bystander Activation",
    ("S.O.U.N.D.", "THE MENTAL HEALTH REALITY OF TOURING"): "Occupational Mental Health / Burnout Prevention",
    ("M.A.R.K.E.T.", "BUYING AND SELLING SAFELY"): "Legal Risk Awareness / Undercover Operations",
    ("M.A.R.K.E.T.", "WHEN THEY DO NOT PAY"): "Debt Recovery / Contract Enforcement",
    ("M.A.R.K.E.T.", "YOUR VENDOR TOOLKIT"): "Business Infrastructure / Preventive Documentation",
    ("M.A.R.K.E.T.", "REAL VENDOR COMMUNITY VS EXTRACTION"): "Authentic Solidarity vs Extraction",
    ("H.O.L.D.", "YOUR ACCESS IS NOT YOUR PERMISSION"): "Role Power Awareness / Personal Accountability",
    ("H.O.L.D.", "STAFF CULTURE THAT PROTECTS PEOPLE"): "Organizational Safety Culture / Reporting Climate",
    ("L.E.A.D.", "THE CAMP SAFETY INFRASTRUCTURE"): "Preventive Structure / Protocol Design",
    ("L.E.A.D.", "THE CAMP LEAD WHO DOES THE WORK"): "Accountable Leadership / Repair Practice",
    ("E.V.E.N.T.", "YOUR STAFF AND VOLUNTEERS"): "Labor Obligation / Operational Duty of Care",
    ("E.V.E.N.T.", "ENFORCE YOUR OWN POLICIES"): "Policy Enforcement / Selective Application",
    ("E.V.E.N.T.", "THE RECORDING RIGHTS QUESTION"): "Intellectual Property / Performer Rights",
    ("S.A.F.E.", "KNOW THESE LOCATIONS BEFORE NIGHT ONE"): "Preventive Orientation / Emergency Preparedness",
    ("S.A.F.E.", "IF SOMEONE GOES MISSING"): "Missing Person Protocol / Emergency Response",
}

DARK = {
    ("G.R.O.V.E.", "HOLD THIS FOR ME"): (
        "Whose Name Is On It",
        "The part nobody says out loud: if it is in your bag, it is your charge. Not his. "
        "Constructive possession means the person holding it is the person arrested, and "
        "“it wasn’t mine” is not a defense that works at a gate search — it is a sentence "
        "people say on the way to a county holding cell. The person asking you to hold knows "
        "this. That is frequently the entire reason he is asking, and the reason he asks the "
        "newest person in the camp rather than his oldest friend. Then there is the second "
        "layer: once he is your supply, leaving his camp costs you your weekend, and he knows "
        "that too. Carry your own, in your own bag, in the amount you chose while sober. "
        "“I don’t hold for anyone” is a complete answer and it does not require a follow-up."
    ),
    ("B.A.S.S.", "DON'T BE SOFT, BRO"): (
        "The Body Count Of Not Wanting To Look Soft",
        "Men die of this. Not metaphorically. The overdose statistics in this scene skew male, "
        "and a meaningful share of them are men who took a second dose they did not want, or "
        "did not mention they had already taken something, or waited too long to say they felt "
        "wrong — because every one of those admissions reads as weakness in a circle that has "
        "been grading each other on hardness all weekend. The same script keeps men from "
        "saying they are too drunk to consent, too far gone to drive, too scared to be alone "
        "with what is happening in their chest. Nobody in that circle wants you hurt. They are "
        "running a script they also did not write. You are allowed to be the one who breaks it: "
        "“I’m good”, said flatly, twice, ends it. The man who keeps pushing after the second "
        "one is telling you something about himself, not about you."
    ),
    ("R.A.V.E.", "THIS WILL MAKE THE FESTIVAL"): (
        "First Time, Unknown Substance, Strangers",
        "The highest-risk combination at any festival is a first-timer, an untested substance, "
        "and people who do not know your baseline. You have no tolerance, no reference point "
        "for what “too much” feels like in your own body, and nobody around you knows what you "
        "look like when you are fine. A dose calibrated to someone who has done this two "
        "hundred times is not calibrated to you, and the person handing it over is usually "
        "estimating rather than measuring. Add the part nobody mentions: the generous stranger "
        "who wants to be present for your first time is sometimes exactly that, and is "
        "sometimes someone who has learned that a person’s first experience is the easiest one "
        "to be in charge of. You are not obligated to make your first festival your first "
        "anything else. Test it, halve it, and be with someone who knew you before this weekend."
    ),
    ("P.R.I.D.E.", "SUBSTANCE SAFETY FOR QUEER FESTIVALGOERS"): (
        "When Substances And Sex Share A Room",
        "In parts of queer party culture, substances and sex are not adjacent activities, they "
        "are the same event — and that changes the risk in ways general harm-reduction advice "
        "does not cover. GHB is the clearest example: it is common, the difference between a "
        "recreational dose and an unconscious one is small, it is measured in millilitres, and "
        "mixed with alcohol that margin narrows further. Doses get poured by other people, in "
        "the dark, from unlabelled bottles. On top of that sits a reporting problem: people who "
        "are not out, or who are on a visa, or who have been treated badly by police before, "
        "weigh calling for help against being outed or detained — so the call comes late or "
        "never. None of that is a reason to avoid the room. It is a reason to dose yourself, "
        "from your own supply, with your own syringe or measure, and to have one person there "
        "who knows what you took and is not taking it with you."
    ),
    ("C.A.R.E.", "THE DEBRIEF PROTOCOL"): (
        "What Undebriefed Weekends Turn Into",
        "The people who leave harm reduction rarely leave because of one terrible night. They "
        "leave because of forty ordinary ones that were never processed, stacked up until the "
        "work started costing more than it gave. The documented pattern is specific: "
        "accumulated vicarious trauma turns into intrusive memory, then into sleep loss, then "
        "into the thing nobody in this field likes saying out loud, which is that a meaningful "
        "number of burned-out harm reduction workers end up using in ways they would flag "
        "instantly in a participant. You will be the last person to notice it in yourself, "
        "because your whole skill set is pointed outward. That is exactly why the debrief is "
        "scheduled rather than optional, and why it has to be with someone whose job is you — "
        "not the participant, not the org, not the friend who also worked the shift."
    ),
    ("S.A.F.E.", "TEST EVERYTHING EVERY TIME"): (
        "Every Time Means The Batch You Already Trust",
        "Fentanyl and its analogues have turned up in pressed pills sold as MDMA, in cocaine, "
        "in ketamine, in counterfeit prescription tablets — substances where nobody in the "
        "chain intended an opioid to be present at all. Contamination is not evenly mixed: two "
        "pills pressed in the same batch can differ, so a strip that came back clean on "
        "Friday’s half says nothing about Saturday’s. This is the specific reason “it’s from a "
        "friend” is not a safety measure — your friend is not the chemist, he is another "
        "customer, and he is testing nothing either. Two strips and a reagent kit cost less "
        "than a night of parking. Carry naloxone even if you never touch an opioid on purpose, "
        "because the overdose you reverse will most likely belong to somebody who also thought "
        "they never had."
    ),
}


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    n_clin = n_dark = 0
    unused = set(CLINICAL) | set(DARK)

    for g in d["guides"]:
        ac = g["acronym"]
        for sc in g["scenarios"]:
            key = (ac, sc["hook"])
            unused.discard(key)
            if key in CLINICAL and not sc["clinical"].strip():
                sc["clinical"] = CLINICAL[key]; n_clin += 1
            if key in DARK and not sc["dark"].strip():
                sc["darkTitle"], sc["dark"] = DARK[key]; n_dark += 1

    if unused:
        raise SystemExit("these keys matched no card (typo?): " + str(sorted(unused)))

    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(DATA, "a", encoding="utf-8").write("\n")
    print(f"filled {n_clin} clinical labels, {n_dark} Dark Reality blocks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
