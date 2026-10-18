# -*- coding: utf-8 -*-
"""The 78 check-field completions for scripts/festie-repair-truncated-checks.py.

Each entry is keyed by (guide slug, scenario hook) and gives the full,
completed check line in the book's standard modern format:
  ACRONYM — "LETTER" CHECK: "question?" — trailing clause.

Every completion was written after reading the scenario's full archetype,
who, and truth fields, so the finished clause continues the exact stem the
original writer cut off, in that scenario's own established shape and tone
-- not a generic filler. None of the wording that was already there (up to
the cutoff) was changed; each closes the quote and adds one clause.
"""

COMPLETIONS = {
 ("grove", "I'M HEALING YOU"):
  'G.R.O.V.E. — “G” CHECK: “What is my gut saying about this person — underneath the role they’re performing right now?” — if the answer doesn’t match the title, trust the gut over the role.',
 ("grove", "TEST EVERYTHING"):
  'G.R.O.V.E. — “G” CHECK: “What is my gut saying about this substance, this source, this situation — before I put it in my body?” — test it anyway, even when the gut says yes. Verification isn’t distrust of magic, it’s respect for your own body.',
 ("grove", "SEE SOMETHING, HOLD SOMETHING"):
  'G.R.O.V.E. — “O” CHECK: “Is someone out alone in a way that seems involuntary?” — sometimes the most important thing you do all weekend is the thirty seconds you spend checking on a stranger.',

 ("bass", "TRUST ME, THIS IS LEGIT"):
  'B.A.S.S. — “A” CHECK: “Who actually has access to my financial decisions right now, and what do I actually know about where this money is going?” — if you can’t answer the second half, you don’t have an investment, you have a story.',
 ("bass", "BUYING AND SELLING SAFELY"):
  'B.A.S.S. — “A” CHECK: “Who has access to my decisions in this transaction — and do I know enough about this person to be doing this at all?” — if the answer is no, the deal isn’t worth what it’s about to cost you.',
 ("bass", "THIS ONE'S ABOUT YOU"):
  'B.A.S.S. — “B” CHECK: “What is my body — and hers — actually saying right now, separate from what I want the answer to be?” — ask out loud rather than guessing. The men who ask are the ones people want to be around.',
 ("bass", "SEE SOMETHING, DO SOMETHING"):
  'B.A.S.S. — “S” CHECK: “Is someone in my squad or nearby in a situation that doesn’t look right? What would I want someone to do if it were me?” — do that.',

 ("rave", "I'LL SHOW YOU EVERYTHING"):
  'R.A.V.E. — “V” CHECK: “Can I get to my camp, the medical tent, and the exit right now without asking him?” — if not, you’re not being guided, you’re being kept.',
 ("rave", "THIS WILL MAKE THE FESTIVAL"):
  'R.A.V.E. — “V” CHECK: “Can I get to my camp, the medical tent, and the exit right now without asking him?” — if not, slow down before the moment sweeps you somewhere you didn’t choose.',
 ("rave", "YOU'RE SAFE WITH ME"):
  'R.A.V.E. — “V” CHECK: “Does this person’s help return me to my own people and navigation — or keep me needing them for the next thing too?” — real help ends. It doesn’t renew itself.',
 ("rave", "THE OVERWHELM WINDOW"):
  'R.A.V.E. — “A” CHECK: “Am I making decisions right now with the same judgment I’d have at 2pm on a Tuesday?” — if not, this isn’t the moment to decide anything.',
 ("rave", "WELCOME TO THE FAMILY"):
  'R.A.V.E. — “E” CHECK: “Am I free to leave this camp right now, without social cost?” — if that question makes you nervous to even ask, that nervousness is the answer.',
 ("rave", "THE DIFFERENCE BETWEEN BEING FOUND AND BEING COLLECTED"):
  'R.A.V.E. — “R” CHECK: “Is this person’s warmth consistent whether I’m being compliant or independent?” — that’s the whole test.',

 ("pride", "THE ALLY WHO IS NOT"):
  'P.R.I.D.E. — “R” CHECK: “Does this person’s behavior match their stated values — or is the language the whole performance?” — vocabulary is cheap. Watch what they actually do.',
 ("pride", "IT KNEW YOU WERE LIKE ME"):
  'P.R.I.D.E. — “I” CHECK: “Am I giving this person more than I would give any other stranger because of shared identity alone?” — shared identity is not a relationship. It hasn’t been earned yet.',
 ("pride", "YOU ARE NOT QUEER ENOUGH"):
  'P.R.I.D.E. — “I” CHECK: “Is my sense of my own identity secure — or am I letting someone else’s framework define it for me?” — nobody else’s checklist gets a vote.',
 ("pride", "OUTING AS LEVERAGE"):
  'P.R.I.D.E. — “I” CHECK: “Is this person treating private information I shared with care — or as something they hold over me?” — information given in trust and then used as leverage was never really given. It was taken on credit.',
 ("pride", "RELATIONSHIP PRESSURE IN A SMALL COMMUNITY"):
  'P.R.I.D.E. — “E” CHECK: “Can I leave this dynamic freely — or does leaving come with social costs that are being used to keep me in it?” — a cost attached to leaving is the whole design.',
 ("pride", "YOUR VISIBILITY IS THEIR WEAPON"):
  'P.R.I.D.E. — “P” CHECK: “My presence and expression are mine. They do not communicate consent for anything less than what I explicitly say yes to.” — presence is not permission. Only yes means yes.',
 ("pride", "SUBSTANCE SAFETY FOR QUEER FESTIVALGOERS"):
  'P.R.I.D.E. — “D” CHECK: “Do I know what is in what I am taking — and does someone sober know what I took and when?” — if nobody sober knows, nobody can help you if it goes wrong.',
 ("pride", "REAL QUEER COMMUNITY VS BEING COLLECTED"):
  'P.R.I.D.E. — “D” CHECK: “Does this person’s warmth remain consistent whether I am being close or independent?” — that consistency is the whole test.',

 ("create", "I KNOW PEOPLE"):
  'C.R.E.A.T.E. — “C” CHECK: “Have I agreed to any representation arrangement — or is someone claiming one that was never actually agreed?” — a representative you never hired is telling you exactly who they are.',
 ("create", "SEXY ARTIST ENERGY"):
  'C.R.E.A.T.E. — “T” CHECK: “Is the appreciation of my work actually about my work — or is it cover for something else entirely?” — your art being beautiful does not make your body available.',
 ("create", "WE JUST NEED THIS ONE THING"):
  'C.R.E.A.T.E. — “C” CHECK: “Is what I’m being asked to do now what I agreed to do — and is the compensation still matching the scope?” — if the ask has grown and the fee hasn’t, that gap is the whole story.',
 ("create", "THE CAMP GAVE YOU A WALL"):
  'C.R.E.A.T.E. — “E” CHECK: “Can I walk away from this arrangement right now without losing something I shouldn’t have had to risk in the first place?” — an undefined arrangement is a contract you’re signing in paint.',
 ("create", "YOUR ART ON OUR MERCH"):
  'C.R.E.A.T.E. — “A” CHECK: “Has anyone asked me in writing for permission to reproduce this work — or did they just assume they could?” — assumption is not permission, and it never comes with a check attached.',
 ("create", "YOUR ART IS YOUR LABOR"):
  'C.R.E.A.T.E. — “R” CHECK: “Is my rate for this engagement something I decided — or something that got decided around me?” — a rate you didn’t set is a rate someone else set, on purpose, in their favor.',
 ("create", "THE REAL COLLAB"):
  'C.R.E.A.T.E. — “A” CHECK: “Is this person interested in my whole artistic practice — or just in what my hands can do for their project?” — real collaborators want your voice. The fake ones just want your output.',

 ("sound", "I CAN MAKE YOU"):
  'S.O.U.N.D. — “S” CHECK: “Is there a signed contract — or just a verbal promise and a sense that questioning it risks the whole opportunity?” — that feeling is the leverage working exactly as intended.',
 ("sound", "THE FESTIVAL WANTS YOU"):
  'S.O.U.N.D. — “S” CHECK: “Have I confirmed every material detail of this booking in writing before I announce it to my own audience?” — once you’ve announced it, the leverage in the negotiation is gone, and it’s gone in their favor.',
 ("sound", "THE SUPERFAN SITUATION"):
  'S.O.U.N.D. — “D” CHECK: “Have I documented this person’s behavior with dates, locations, and screenshots — solely so I have a record if this escalates?” — a fan’s dedication is not a reason to skip documenting once it stops feeling safe.',
 ("sound", "WE OWN THE RECORDINGS"):
  'S.O.U.N.D. — “O” CHECK: “Who owns the recordings being made of me tonight — and is that in writing before I go on stage?” — know who owns the product before you create it, not after.',
 ("sound", "THE CHECK'S COMING"):
  'S.O.U.N.D. — “D” CHECK: “Do I have documentation of everything agreed financially — so I have something to point to when the money doesn’t show up on time?” — you performed. You get paid what was agreed. This is completely enforceable.',
 ("sound", "YOUR REPUTATION OR YOUR COMPLIANCE"):
  'S.O.U.N.D. — “D” CHECK: “Have I documented the facts of this situation so I have something to point to if my version of events gets challenged later?” — the people worth working with will believe the documentation over the rumor.',
 ("sound", "YOUR STANDARD RIDER"):
  'S.O.U.N.D. — “S” CHECK: “Does my rider include recording rights language, payment terms, and all my technical requirements, spelled out in writing?” — the rider is not arrogance. It’s professionalism, and it protects both sides of the booking.',
 ("sound", "BUYING AND SELLING SAFELY ON THE CIRCUIT"):
  'S.O.U.N.D. — “U” CHECK: “Do I understand who is actually in this space and what the legal implications of this transaction actually are?” — backstage is not a legal gray zone just because it feels like one.',
 ("sound", "THE MENTAL HEALTH REALITY OF TOURING"):
  'S.O.U.N.D. — “N” CHECK: “What does my actual wellbeing need right now — not what does the tour schedule need from me?” — those are two different questions, and only one of them is actually yours to answer.',

 ("market", "BEST SPOT ON THE CIRCUIT"):
  'M.A.R.K.E.T. — “M” CHECK: “Is the placement, the attendance number, and every fee in writing — or just verbally promised by someone with every reason to over-promise?” — a great pitch that isn’t in writing is just a story.',
 ("market", "LAST MINUTE CHANGES"):
  'M.A.R.K.E.T. — “R” CHECK: “Do I have written documentation of what was originally agreed so I can actually point to it when the terms shift?” — the paper trail you build before the event is the only thing that protects you at it.',
 ("market", "WE ARE ALL FAMILY HERE"):
  'M.A.R.K.E.T. — “E” CHECK: “What would it actually cost me to leave this arrangement — and is that cost getting bigger the longer I stay quiet about it?” — an undefined cost that grows with your silence is not community. It’s a bill you didn’t agree to.',
 ("market", "I CAN GET YOU IN ANYWHERE"):
  'M.A.R.K.E.T. — “A” CHECK: “Does my business access depend on this relationship — and what does that mean for me the day this relationship ends?” — access that depends on one relationship was never really yours.',
 ("market", "BOOTH PLACEMENT AS PUNISHMENT"):
  'M.A.R.K.E.T. — “K” CHECK: “Am I staying quiet about legitimate concerns because I am afraid of what it will cost my placement next season?” — an organizer who punishes standards is telling you exactly who they are.',
 ("market", "YOUR DESIGN ON THEIR MERCH"):
  'M.A.R.K.E.T. — “R” CHECK: “Do I have timestamped documentation of my original designs that establishes my ownership before anyone else’s does?” — your designs are copyrighted the moment you create them. You get to enforce that.',
 ("market", "BUYING AND SELLING SAFELY"):
  'M.A.R.K.E.T. — “A” CHECK: “Am I proceeding with this conversation because I actually want to — or because saying no feels riskier than it is?” — no transaction at a festival is worth your freedom, and no conversation is worth your business.',
 ("market", "REAL VENDOR COMMUNITY VS EXTRACTION"):
  'M.A.R.K.E.T. — “K” CHECK: “Is this interaction genuinely mutual — or is community being invoked to extract something one direction only?” — real community runs both ways. Extraction only runs one.',

 ("hold", "THE PREDATOR KNOWS WHERE THE TENT IS"):
  'H.O.L.D. — “L” CHECK: “Have I documented the specific behaviors that are making me uncomfortable about this person in an access role, with dates and specifics?” — the team looking out for each other matters as much as the team looking out for attendees.',
 ("hold", "YOU CAN HANDLE MORE"):
  'H.O.L.D. — “H” CHECK: “Am I actually present with the people I am supporting — or am I running on empty and performing presence I don’t actually have?” — you cannot give what you do not have. Recovery is the job, not a luxury outside it.',
 ("hold", "THE PARTICIPANT WHO MANIPULATES YOUR CARE"):
  'H.O.L.D. — “O” CHECK: “Is the pattern of this person’s engagement consistent with genuine support seeking — or does it track more closely with something else entirely?” — discernment is as much a part of this role as compassion.',
 ("hold", "BURNOUT AS A CONTROL TOOL"):
  'H.O.L.D. — “H” CHECK: “Do I have the basic resources I need to do this role safely — food, sleep, breaks, a way to say when I’ve hit my limit?” — a depleted volunteer isn’t a martyr, they’re a liability to everyone they’re trying to protect.',
 ("hold", "DON'T RUIN THE VIBE OF THE EVENT"):
  'H.O.L.D. — “L” CHECK: “Have I documented this incident in writing regardless of what the organization is asking me to prioritize instead?” — reporting harm is the job. Anyone telling you otherwise is protecting the wrong thing.',
 ("hold", "THIS IS YOUR FAULT"):
  'H.O.L.D. — “L” CHECK: “Have I documented my version of events in writing immediately — before organizational framing has a chance to reshape it?” — you’re responsible for your actions, not for the systemic conditions you were placed in.',
 ("hold", "BYSTANDER ACTIVATION FOR STAFF"):
  'H.O.L.D. — “O” CHECK: “What am I observing right now, and what does my role require me to do with that observation, in this exact moment?” — your vest and your radio are the tools for this moment. Use them.',
 ("hold", "YOUR RIGHTS AS A VOLUNTEER"):
  'H.O.L.D. — “H” CHECK: “Am I being asked to do something that my training, my safety, or my basic needs require me to say no to?” — saying no to an unsafe task isn’t letting the team down. It’s doing the job correctly.',
 ("hold", "THE DEBRIEF IS PART OF THE JOB"):
  'H.O.L.D. — “D” CHECK: “Have I actually stopped and processed what I experienced today — or am I just pushing through to the next shift?” — what you process becomes wisdom. What you don’t becomes weight.',
 ("hold", "YOUR ACCESS IS NOT YOUR PERMISSION"):
  'H.O.L.D. — “H” CHECK: “Am I using my access in service of the people I am there to protect — or for my own convenience, curiosity, or gain?” — the access isn’t yours, it belongs to the role. Use it accordingly.',
 ("hold", "STAFF CULTURE THAT PROTECTS PEOPLE"):
  'H.O.L.D. — “O” CHECK: “Does the culture of this staff team make it easy or hard to raise concerns?” — that tells you a great deal about how safe this event actually is.',

 ("care", "THE PARTICIPANT WHO RUNS A PATTERN"):
  'C.A.R.E. — “R” CHECK: “Is the pattern of this person’s engagement consistent with genuine support seeking — or does it track more closely with something else entirely?” — discernment is as much a part of this role as compassion.',
 ("care", "YOU CAN HANDLE MORE"):
  'C.A.R.E. — “C” CHECK: “Am I actually present with the people I am supporting — or am I performing presence from a tank that’s already empty?” — you cannot give what you do not have, and your recovery is what makes the giving possible.',
 ("care", "WHAT YOU SAW STAYS HERE"):
  'C.A.R.E. — “A” CHECK: “Is confidentiality being applied to protect the people we serve — or to protect the organization from accountability?” — confidentiality protects participants. It was never meant to protect an organization from consequences.',
 ("care", "YOU SHOULD HAVE CAUGHT THAT"):
  'C.A.R.E. — “A” CHECK: “Have I documented my own account of events immediately — before organizational framing has a chance to reshape it?” — you’re responsible for your actions, not for the systemic conditions you were placed in.',
 ("care", "THE DEBRIEF PROTOCOL"):
  'C.A.R.E. — “E” CHECK: “Have I actually stopped and named what I am carrying from this shift — or am I just pushing it down to deal with later?” — what you name, you can put down. What you don’t, you carry.',

 ("lead", "THE PREDATOR IN YOUR CAMP"):
  'L.E.A.D. — “L” CHECK: “Am I responding to this in a way that protects the person who came to me — or the person the report is about?” — the standard you set when it’s hard is the only standard that actually matters.',
 ("lead", "THIS IS HOW WE DO THINGS HERE"):
  'L.E.A.D. — “E” CHECK: “Do my camp’s norms make it easier or harder for members to raise concerns and seek help when something has gone wrong?” — the norms you build in calm times are the ones that show up in the hard ones.',
 ("lead", "HOUSING AS LEVERAGE"):
  'L.E.A.D. — “A” CHECK: “Do the members who depend most on what I provide feel the most or least free to push back on me when something’s wrong?” — generosity that creates dependency isn’t generosity. It’s leverage that happens to be warm.',
 ("lead", "THE CAMP THAT OWNS YOU"):
  'L.E.A.D. — “L” CHECK: “Can members of my camp leave freely, talk to outsiders freely, and question decisions freely, without a cost attached to any of it?” — a community that needs control to hold together isn’t a community. It’s a structure.',
 ("lead", "THE CAMP LEAD WHO DOES THE WORK"):
  'L.E.A.D. — “D” CHECK: “When I look at my camp honestly — am I the kind of leader I would want my members to describe honestly, if they were asked?” — the best camp lead isn’t the one who never gets it wrong. It’s the one who keeps working to get it more right.',

 ("event", "THE BAIT AND SWITCH"):
  'E.V.E.N.T. — “V” CHECK: “Would I be comfortable if every vendor and artist I have worked with saw this pitch in writing, side by side with what actually happened?” — the reputation you’re building is the accurate one, not the one in your pitch.',
 ("event", "YOUR STAFF AND VOLUNTEERS"):
  'E.V.E.N.T. — “N” CHECK: “Do my staff have what they need to do their jobs safely — and do they have a clear path to raise a concern without it costing them?” — your event runs on other people’s labor. You owe them clarity, safety, and a path that actually works.',
 ("event", "THE RECORDING RIGHTS QUESTION"):
  'E.V.E.N.T. — “V” CHECK: “Are the artists whose recordings I am using being compensated fairly for the commercial use I am putting that footage to?” — the content that builds your brand was created by artists. Treat their contribution accordingly.',
 ("event", "THE ETHICAL PROMOTER TOOLKIT"):
  'E.V.E.N.T. — “T” CHECK: “Would the artists, vendors, and staff who worked my last event describe it the way I just did?” — ethical production isn’t complicated. It’s a set of choices made consistently. Make them.',

 ("safe", "FOOD, SLEEP, AND YOUR ACTUAL BODY"):
  'S.A.F.E. — “A” CHECK: “Am I making decisions right now with my full judgment — or with a significantly depleted version of it?” — rest isn’t missing the festival. It’s what makes you available to actually be in it.',
 ("safe", "TEST EVERYTHING EVERY TIME"):
  'S.A.F.E. — “A” CHECK: “Have I tested this — and does everyone in my group know what to do if something goes wrong?” — two minutes of testing is the difference between a good night and a medical emergency.',
 ("safe", "DANGEROUS COMBINATIONS"):
  'S.A.F.E. — “A” CHECK: “Do I know what I have already taken and do I actually know what I am being offered right now, specifically?” — the combination is where most of the risk lives. Know what you’re mixing before you mix it.',
 ("safe", "KNOW THESE LOCATIONS BEFORE NIGHT ONE"):
  'S.A.F.E. — “F” CHECK: “Have I physically located the medical tent, Harm Reduction tent, and Ranger station with my own feet, not just on the map?” — knowing where help is before you need it is the preparation everything else builds on.',
 ("safe", "IF SOMEONE GOES MISSING"):
  'S.A.F.E. — “E” CHECK: “Have I already checked medical and Harm Reduction tents — and do I have her photo on my phone, ready to show people?” — there’s no minimum wait time to report someone missing. Report when you’re concerned, not after.',
 ("safe", "DIFFICULT TRIPS AND PSYCHOLOGICAL CRISES"):
  'S.A.F.E. — “F” CHECK: “Do I know where the Zendo or Harm Reduction tent is — and can I get us both there calmly, without rushing them?” — a calm presence is the most powerful intervention there is, and you already have it.',
 ("safe", "THE MORNING AFTER"):
  'S.A.F.E. — “E” CHECK: “What does my body actually need right now — not what does the situation require me to perform?” — you don’t have to be okay yet. Support exists, and you deserve it.',
 ("safe", "THE BUDDY SYSTEM"):
  'S.A.F.E. — “E” CHECK: “Does everyone in my group have a buddy, and do we all have the code word and the meeting point, agreed before we split up?” — ten minutes spent on this before the festival is the preparation that matters most.',
}
