#!/usr/bin/env python3
"""The Sacred Divide — expanded reviewer editions.

Builds three expanded PDFs (Sunni Islam, Judaism, Catholicism) from the same source .md files
the site uses, reusing scripts/sacred-divide-pdf.py's rendering engine. Adds, on top of the
standard page:

  - A one-page preface explaining what this copy is and why the reader has it.
  - A personal-note box at the top of every one of the 27 sections: what the section is for,
    and — wherever the source material actually forks from a Quranic principle — a plain
    comparison, offered respectfully, not as a claim about any individual reader's own practice.
  - On the Sunni Islam copy only: a "Salafi/Sunni methodology point" box on the sections where a
    salaf-centred, evidence-over-taqlid reading sharpens the question (branches, structure, law,
    genealogy, techniques, regional).
  - The six "hard questions" each expanded into a card: the question, why it is asked, and a
    concrete example already documented on the page. The Sunni Islam copy adds a seventh,
    Salafi-lens question.
  - Larger, bolder, truer-black type, generous spacing, and new accent colours for the two box
    kinds (tools/pdf/sacred-divide-personal.css, loaded after the base stylesheet). Boxes are
    allowed to break across a page rather than jump whole, so pages fill instead of leaving gaps.

The Sunni Islam and Judaism copies are addressed by name to Abdurahman Afia (see RECIPIENT
below). The Catholicism copy is a generic reviewer edition — no name, no personal biography —
because it goes to a different reader.

Usage: python3 scripts/sacred-divide-pdf-abdurahman.py
Output: library/_undeployed/sacred-divide-pdf/personal/<id>-for-abdurahman.pdf (named copies)
        library/_undeployed/sacred-divide-pdf/personal/catholicism-review-copy.pdf (generic)
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, 'tools/pdf')
OUTDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-pdf/personal')
SITE = 'noblefathercreations.com/faith'

# ---------------------------------------------------------------- load the base renderer
spec = importlib.util.spec_from_file_location('sdp', os.path.join(HERE, 'sacred-divide-pdf.py'))
sdp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdp)
e, inline, md_to_html = sdp.e, sdp.inline, sdp.md_to_html
front_matter, sources_ids, score_cells, grade_bar = sdp.front_matter, sdp.sources_ids, sdp.score_cells, sdp.grade_bar
SRC = sdp.SRC

# Per-copy recipient. Catholicism goes to a different reader — no name, no personal biography.
RECIPIENT = {'sunni-islam': "Abdurahman Afia", 'judaism': "Abdurahman Afia", 'catholicism': None}
NOTE_LABEL = {'sunni-islam': "A note to Abdurahman", 'judaism': "A note to Abdurahman", 'catholicism': "A note for the reviewer"}

# ================================================================== reviewer content
# One "note to Abdurahman" per section (27), one Salafi box on selected sections (Sunni copy
# only), and expansions ("why this is asked" / "example") for the six hard questions, in order.

PREFACE = {
    'sunni-islam': """This copy is built for you specifically, from the same page that will eventually sit behind a "Download the full record" button on the finished site — nothing has been added that isn't already sourced on the page itself; what's added here is *framing*, addressed to you, section by section, plus a Salafi/Sunni methodology lens on six of the sections and a seventh question at the end.

You'll recognise the shape of the argument the Quran itself makes about earlier communities: that revelation is one thing and what people, scholars, and states do with it over centuries is another — that the message can be sound while the men entrusted with it are not (Quran 2:75–79, 9:34). This page applies exactly that distinction to the Sunni world as it is documented and practiced today: not "is Islam true," which this page never touches, but "where has what a ruler, a ministry, or a family calls Islam actually forked from what the text and the earliest generation said." That is a question the salaf themselves asked constantly, of their own rulers, and it is the question every note in this copy is trying to sharpen for you.

You built a public life on the claim that the Quran corrects rather than merely repeats — that it holds earlier revelation to account. Held to its own standard, it holds the institutions built in its name to account too. That is the spirit this copy is offered in, and the request behind it: read it as a brother would want a hard page about his own tradition read — for what's true, what's overstated, and what a Sunni/Salafi eye sees that a purely academic one might miss.""",
    'judaism': """This is the same Judaism page that will sit behind the site's download button, built to the identical 27-section standard as every other tradition in the book — nothing added here is unsourced; what's added is a note before each section, addressed to you, and the six hard questions expanded into full cards.

You are not being asked to review this as a Jewish reader would. You're being asked for what you actually bring: a convert's outsider clarity, a Quran-formed sense of where revelation and institution can part ways, and 25 years of watching how religious authority behaves under state power in the Gulf — which turns out to be directly useful here, since a state-run rabbinate is one of this page's central subjects. The Quran affirms Musa (peace be upon him) and the Torah he brought (2:87, 5:44) while also naming specific moments where communities that received it are said to have altered or obscured parts of what they were given (2:75, 4:46) — again, a claim about transmission and human institutions, not a verdict on individual people. That is the only lens this copy uses, applied consistently, the same way it's applied to the Islamic pages elsewhere in the project.

Where the page shows a rabbinic court, a state monopoly, or a communal rule that has drifted from what even the tradition's own reformers say the Torah requires, the note says so plainly and invites your comparison — because a fair, accurate treatment of another Abrahamic tradition is also, on your own terms, a form of honoring the God you both ultimately answer to.""",
    'catholicism': """This is the Catholicism page in the same 27-section standard as the rest of the project, with nothing added that isn't sourced on the page itself — what's new here is a note before each section explaining what that section is doing, and the six hard questions expanded into full cards with a worked example under each.

The ask of a reviewer here is straightforward: not agreement, and not a defense of the institution or a case against it — just an honest check on whether the page is accurate and fair. A great deal of what this page documents is the gap between a flattened caricature of Catholicism (uniformly corrupt, or uniformly innocent) and the actual, sourced record: real reform, real courage, real cover-up, held together in the same institution across the same centuries. Getting that balance right — naming what works before naming what doesn't, and never asserting a claim the page can't point to a source for — is the whole discipline of this project, applied here the same way it's applied to every other tradition in the book.

Where the page shows a monopoly, a secrecy rule, or a celibacy discipline the Church's own historians trace to a property question rather than a spiritual one, the note names the comparison plainly, in the same voice used throughout — because getting this page right matters to the Catholics who will read it too.""",
}

# ---- per-section notes -------------------------------------------------------------------
SECTIONS_SUNNI = {
'at-a-glance': """This table is the whole page compressed to one screen — what you'd want to know before agreeing to anything. Read the "Who's in charge" and "Chosen by / removable by" rows first: al-Azhar's Grand Imam is presidentially appointed and, since Egypt's 2014 constitution, irremovable. That single fact does more work than any paragraph — it tells you the "unanswerable" question up front. **Salafi note:** al-Azhar is one seat of learning among many the page treats as "Sunni," not the salaf's own method; keep that distinction in mind through everything that follows.""",
'a-day-inside': """This section exists to stop the page being abstract. It follows one ordinary day through an ordinary institution, because "87% of Muslims" and "state-salaried scholars" are easy to read past — a single day's schedule of duties, permissions asked, and money handled is not. Read it the way you'd read a case study in your own leadership work: the system reveals itself in the small, procedural moments, not the dramatic ones.""",
'forefront': """This is the page's thesis, stated once directly: the single unanswered question, the widest gap between what is said and what the record shows, one real cost of leaving, and the strongest counter-argument — answered fairly, not strawmanned. Read the "strongest objection, answered" subsection closely; a page that only wins against weak objections isn't worth your time, and this project tries not to be that page.""",
'healthy': """Every tradition in this book gets a section naming what actually works — the project's rule against writing only indictments. For Sunni Islam this includes real things: waqf-funded scholarship's historical independence, the ijaza chain, communities that still function exactly as intended. Read this section as the baseline the rest of the page measures departures against — you can't see the fork in the road if you don't know what the road looked like.""",
'history': """The timeline exists so nothing in later sections floats free of a date. Watch specifically for the Ottoman-to-colonial-to-postcolonial handoff of religious authority into state ministries — it's the hinge the whole "genealogy" section turns on, and it's a purely historical, checkable claim, not a theological one.""",
'branches': """This section is thinner than it should be on the page as written, and it's worth you knowing why: "Sunni" in Western reference material collapses Ash'ari kalam theology, Sufi tariqas, madhhab-bound traditionalism, and Salafi/Athari method into one 87% bucket. You will feel that flattening more than most readers will, because it erases a distinction central to how you were taught. Say so plainly if you review this — it's a real gap, not a stylistic choice.""",
'structure': """This is the organizational chart: who holds the top office, who appointed them, who — on paper — could remove them. The "Who holds what" table is the one to sit with; it's where a state ministry's fingerprints on "religious" authority are laid out plainly rather than asserted.""",
'law': """Every tradition gets one honest answer to "who can actually make this institution answer for itself" — courts, regulators, an election, or, often, nobody. For Sunni Islam the honest answer is thin, and the section says so rather than inventing an accountability mechanism that doesn't exist. That thinness is itself the finding.""",
'money': """Follow the money exactly the way you'd follow it in a corporate audit: not "is charity wrong" but "where does this specific flow go, who discloses it, and what does the absence of disclosure let happen." Gulf endowment money and celebrity-preacher media economies both appear here — worth reading with your Gulf-based, 25-year vantage point specifically in mind.""",
'genealogy': """This is the section built exactly for the comparison you asked for. Each card runs the same four-part test: what a rule was originally *for*, why that reason has expired, and who benefits from it persisting anyway. It's the clearest place on the page where a practice that once served a real purpose (a wali protecting a woman with no legal standing) now serves a different one (a father's veto over an adult with full legal standing) — read it as the page's answer to "how did this fork," worked four separate times.""",
'reach': """This section maps how deep institutional reach goes into information, children, and organizational bodies — not accusation, just documentation of scope. It's the section most readers skip and shouldn't; scope is what turns an individual grievance into a pattern worth a whole book.""",
'techniques': """This is the analytical spine of the entire project: thirty documented influence and control techniques, drawn from domestic-abuse and social-psychology research, applied here with a named evidence grade for every one — Documented, Taught, Cultural, Contested, or Reformed. Nothing here claims Islam teaches manipulation; it claims specific documented behaviors, in specific institutions, match a known pattern, and grades how solid that match is case by case. Read the grade column as carefully as the technique itself.""",
'loops': """The eight-stage cycle (idealize → hook → devalue → confuse → isolate → extract → discard → replace) is the same cycle domestic-abuse researchers use for coercive relationships, applied to an institution instead of a person. The point of showing it as a loop rather than a list is that no single stage looks alarming in isolation — the pattern is only visible once you see it repeat.""",
'say-do': """This section is a straight two-column exercise: the official statement, then what the documented record actually shows. It's the most falsifiable section on the page — every claim here either matches its citation or it doesn't, which is exactly why it's worth your closest scrutiny as a reviewer.""",
'cost': """What leaving actually costs, denominated honestly — marriage prospects, family standing, in diaspora communities sometimes the entire social base. The "how the cost is denied" subsection matters most: institutions that say "no one is forced to stay" while the social machinery makes leaving ruinous are describing a technical freedom, not a real one.""",
'ledger': """Who benefits, who pays, and what leverage flows back once the money has flowed out — the accounting question underneath the theology. Read "who pays" as the section's real center of gravity; it names the people (usually women, usually the economically dependent) who bear the cost of arrangements that benefit someone else entirely.""",
'who-gets-hurt': """A direct statement of where the weight lands hardest — not evenly distributed, and the page says so. This is the section to read if you want the human stakes in one place before returning to the more analytical sections around it.""",
'tiers': """Local imams, teachers, and community elders — the people who implement rules they didn't write and often can't change. This section exists so the page doesn't collapse "the institution" into a monolith; most of the people carrying out a policy had no hand in setting it, and the page tries to hold both facts at once.""",
'cases': """Six fully-documented cases, each with a named record — court filings, government reports, on-the-record reporting. This is the section where the page stops making a general argument and shows its work case by case. Read each one's "outcome" line specifically; it's where the page is most honest about what actually changed and what didn't.""",
'precedent': """What has already been broken, once, by someone inside the tradition — and what would have to happen for that to become the norm rather than the exception. This section exists so the page isn't read as claiming nothing ever changes; it claims specific things haven't changed yet, and names what would count as evidence that they had.""",
'voices': """Named people, from inside the tradition, who said the hard thing publicly and paid a cost for it. This section is the page's answer to "isn't this all outsiders talking" — it isn't; read the names.""",
'regional': """Eight country cards, including the UAE and Saudi Arabia specifically — read those two first, given where you've built your life and work. The point of the regional breakdown is that "Sunni Islam" is not administered identically anywhere; the same theology produces very different institutional arrangements depending on the state it sits inside.""",
'questions': """Six questions the page could not resolve from the documented record, expanded below into full cards — why each one is asked, and a concrete example already on this page it's pointing back to. A seventh, Salafi-lens question has been added for this copy.""",
'leaving': """Practical, non-legal guidance for anyone actually trying to leave a specific arrangement safely — not a theological argument, a safety document. Worth reading even if you never need it yourself, because it tells you what the institution's actual exit friction looks like in practice.""",
'help': """Vetted contact information, checked directly against each organization's own site rather than copied from a list. If you ever refer someone to this page, this is the section that has to be right, and it's the one checked most recently.""",
'sources': """Every numbered citation in the page traces back to an entry here — court records, government reports, named journalism, academic sources. This is the section to spot-check first if you're deciding whether to trust the rest; pull three or four citations at random and follow them.""",
'changed': """A running log of what was corrected and when, kept deliberately visible rather than quietly edited away. If your review changes something on this page, that correction belongs here too, dated and attributed the same way every other correction is.""",
}

SALAFI_SUNNI = {
'branches': """A Salafi/Athari reading doesn't recognise "Sunni" as one branch among four the way the page's family list implies — it holds that adherence to the Quran and authenticated Sunnah, understood as the salaf (the first three generations) understood them, *is* what "Sunni" originally meant, before centuries of kalam theology and strict madhhab taqlid layered on top of it. Where this page treats Ash'ari scholasticism, Sufi tariqa structures, and rigid four-madhhab taqlid as simply "Sunni Islam," a Salafi reader will want those distinguished — because several of the accountability failures documented later in this page (a scholar bound by loyalty to a school or an order rather than to the daleel, the evidence, directly) are precisely what the Salafi manhaj was a historical reaction against.""",
'structure': """The classical Salafi position on religious authority is that a scholar's legitimacy rests on his adherence to daleel — Quran and authentic hadith, as understood by the salaf — not on his position in a hierarchy or his government appointment. Ibn Taymiyyah himself, a foundational reference for the Salafi method, was imprisoned repeatedly by the very rulers whose religious establishment he refused to simply endorse. Measured against that standard, an appointed, constitutionally-irremovable Grand Imam is not obviously more authoritative than a scholar with no government post at all — a point this page's own "Structure" table makes without naming it.""",
'law': """This is exactly where Salafi methodology and this page's findings converge most directly, and it's worth being honest about that rather than softening it: the classical position — stated plainly by Ibn Taymiyyah and reaffirmed by Salafi scholars across the 20th century — is that obedience to any ruler or scholar stops the moment they command disobedience to Allah ("la ta'ata li-makhluqin fi ma'siyati al-Khaliq," no obedience to a created being in disobeying the Creator). A scholar whose paycheck depends on a ministry's continued approval is in a structurally harder position to apply that principle than a scholar who isn't — which is a governance observation, not an accusation against any individual.""",
'genealogy': """Every one of this section's four cards is, in Salafi terms, a bid'ah question: does this practice trace to the Quran and the authenticated Sunnah as the salaf understood it, or did it accrete later for reasons that have since expired? The Salafi method's whole project is running exactly that test — the page has effectively run it for you on marriage guardianship, honor-code enforcement, and state religious payroll, and reached conclusions a consistent Salafi reader would likely recognise as familiar, even where the page's vocabulary differs from a fiqh vocabulary.""",
'techniques': """Salafi communities have their own well-documented internal literature — sometimes sharper than outside academic critique — warning against exactly several of the thirty techniques catalogued here: blind taqlid of a single teacher (tactic 6, Gaslighting's cousin, epistemic dependency), takfir used as a social weapon against fellow Muslims (tactic 12, DARVO-adjacent), and the isolation of new converts from family (tactic 14). Reading this section as "outsiders' critique of Islam" would miss that several of its sharpest points already exist, in different language, inside Salafi self-criticism.""",
'regional': """Salafi da'wah is historically associated with Saudi religious institutions, which makes the Saudi Arabia card the one to read most carefully rather than most defensively. The internal Salafi debate over the proper relationship between scholars and the state — voiced publicly by figures within the Sahwa current from the 1990s onward — is itself a documented example of Salafi Muslims applying the "law: who can compel an answer" test to their own tradition's institutions, which is the same test this whole page runs.""",
}

QUESTIONS_SUNNI = [
    {'why': "This question exists because the page can find no scholar, anywhere in the documented record, whose government salary was ever shown to have zero effect on which fatwas got issued and which didn't — and \"no evidence either way\" is not the same as \"proven independent.\" It's the load-bearing question of the whole page: every other finding about state-controlled religious authority rests on this one being real.",
     'example': "al-Azhar's Grand Imam is appointed by Egypt's president and, under the 2014 constitution, cannot be removed by any religious body — only the appointing power installed him, which means only that power, in practice, decides who holds the seat next."},
    {'why': "Asked because \"free\" religious education that produces graduates with no employable skill outside religious institutions isn't free in the way it's marketed — it's a closed labor market with one employer. The question is deliberately structural, not a claim about any single school's intent.",
     'example': "The page's own genealogy section traces this directly: madrasas that teach hifz (memorization) without literacy, numeracy, or a transferable credential produce graduates who are economically dependent on religious employment for life — a documented pattern, not a hypothetical one."},
    {'why': "This one is asked precisely because it's answerable from inside the fiqh tradition itself, which makes the gap harder to explain away as \"just how Islam is\" — if one recognised school permits it, the practice elsewhere is a communal choice, not a textual requirement.",
     'example': "The Hanafi madhhab explicitly permits an adult woman to contract her own marriage. Communities that still require a wali's consent regardless are following a specific school's ruling, not an undisputed consensus — which is exactly the kind of distinction Salafi methodology, with its emphasis on evidence over blind school-loyalty, would want made explicit rather than blurred."},
    {'why': "Asked because a fifteen-year gap between \"scholars across the schools condemn honor killing as murder\" and a law closing the pardon loophole is itself data — it measures how much of the practice was ever really about religious law versus tribal custom wearing religious language.",
     'example': "Pakistani law allowed a victim's heirs to pardon the killer until 2016 — and when the killer is a family member, the heirs are frequently the same family, which made the \"pardon\" provision a structural exit for honor killings specifically, closed only after sustained campaigning, not by scholarly consensus alone."},
    {'why': "This is the page's version of a compliance question, not a theological one: reporting obligations for child abuse exist in every jurisdiction this page covers, and the question is simply whether religious institutions were treated as exempt from them in practice.",
     'example': "Cases documented elsewhere in this project — across multiple traditions, not only this one — show religious schools and institutions moving an accused figure rather than reporting to police. The page asks the same question of every tradition it covers; this is Sunni Islam's version of it."},
    {'why': "This closing question is aimed at the silencing mechanism itself, not at any specific claim — because a rule that says \"raising X helps the enemies of the faith\" forecloses the question before any evidence gets examined, which is a control technique this page catalogues directly (tactic 17, in the Reach section).",
     'example': "You experienced a milder version of this dynamic yourself, from the opposite direction — a father who framed leaving atheism for Islam as a betrayal of the family rather than engaging the claims of the two years of inquiry that produced it. The mechanism (foreclose the question by naming who it serves) is the same one; only the direction points the other way."},
]
EXTRA_QUESTION_SUNNI = {
    'q': "If the salaf's own method was to test every ruling against Quran and authenticated Sunnah rather than defer to a scholar's position or a ruler's preference, what changed — and who benefits from a modern reader deferring instead of testing?",
    'why': "This is the question the rest of this page's findings converge on for a Salafi reader specifically. Everything documented here — state-salaried scholarship, taqlid-bound marriage guardianship, honor-code enforcement dressed in religious language — is a case of an institution asking for deference where the classical Salafi method asks for evidence instead.",
    'example': "Ibn Taymiyyah, cited across Salafi scholarship as a primary reference, was imprisoned multiple times by the religious and political establishment of his own era for refusing exactly this kind of deference — a documented historical precedent, inside the tradition itself, for testing an institution's claims against the text rather than the institution's authority.",
}

SECTIONS_JUDAISM = {
'at-a-glance': """This table is the whole page in one screen. Read "Who's in charge" carefully: a Chief Rabbinate with a statutory monopoly over Jewish marriage and divorce in a sovereign state, on state salary, chosen by a 150-member body weighted toward rabbinic insiders. That's a state-backed religious monopoly — a structure this project also documents inside several Islamic institutions — which is exactly the kind of parallel worth drawing rather than avoiding.""",
'a-day-inside': """Follows one ordinary day through the system this page documents, for the same reason every tradition in the book gets one: abstractions like "150-member electoral body" are easy to read past; a single day of what a get-seeking woman or a would-be convert actually has to do is not.""",
'forefront': """The page's thesis in one place: the central unanswered question — why the power to free a chained wife (an agunah) was never made an obligation rather than a discretion — plus the widest gap between word and record, and the strongest counter-argument, answered rather than strawmanned. Read that last part closely; a fair page has to survive its own best objection.""",
'healthy': """What genuinely works, stated first and separately from the critique — the project's standing rule. For Judaism this includes real things: a tradition that canonized dissent, preserved minority legal opinions for two thousand years, and produced the reformers documented later in this same page. The Quran's own affirmation of the Torah (5:44) sits comfortably next to naming what its custodians got right.""",
'history': """The timeline anchors everything that follows in real dates — watch specifically for 1953, when Ottoman millet arrangements carried through the British Mandate became Israeli statute, converting communal self-governance (a real minority protection under empire) into a state-enforced monopoly inside a sovereign nation. That single year is the hinge the "genealogy" section turns on.""",
'branches': """Orthodox, Conservative, Reform, Reconstructionist — the page's branch table exists so "Judaism" isn't read as one bloc any more than "Sunni Islam" should be. Worth reading with your own experience in mind: your two-year search briefly included practicing Judaism before you found the Quran's answer more logically complete — this section is where that internal variety, which you encountered firsthand, gets laid out formally.""",
'structure': """The organizational chart: the Chief Rabbinate's top office, how it's filled, and — the table's real finding — that "removable by" resolves to "the state that created the monopoly, which has not." Read "Who holds what" as the place where state and religious authority are shown, not asserted, to be entangled.""",
'law': """Every tradition gets one honest answer to who can actually compel accountability. For Israeli Orthodox institutions specifically, civil courts have real power the page documents plainly — this is one of the stronger accountability sections in the whole project, worth noting precisely because it shows the mechanism can exist when a state chooses to build it.""",
'money': """Follow the flows the way you'd audit any organization: synagogue dues, day-school tuition, kosher certification fees, and — the line worth sitting with — how heavily communal costs land at the exact emotional moments (High Holidays) when walking away is hardest. That's a structural observation about pricing, not an accusation.""",
'genealogy': """Built for direct comparison. Each card runs the same test the rest of this project runs everywhere: what a rule was originally *for*, why that reason has expired, who benefits from it persisting anyway. The mesirah card is the sharpest example on the page — a rule built to protect Jews from medieval blood-libel tribunals, still applied by some communities to a modern child-abuse allegation, protecting the accused instead of the child it was never designed to fail.""",
'reach': """Maps institutional reach into information, children, and organizational bodies. Read it as scope-mapping, not accusation — the same section exists, in the same form, on every tradition's page in this project, including the Islamic ones.""",
'techniques': """The same thirty-technique, evidence-graded framework applied consistently across every tradition in the book — nothing here claims Judaism teaches manipulation; it grades specific documented institutional behaviors against a known pattern from domestic-abuse and social-psychology research. Read the grade column, not just the technique name.""",
'loops': """The same eight-stage cycle used throughout this project, applied here. The point of the loop framing, again, is that no single stage looks alarming alone — a synagogue's High Holiday pricing looks like ordinary fundraising until you see it sit inside a cycle with isolation and extraction stages elsewhere.""",
'say-do': """A direct, falsifiable comparison: official statement versus documented record. This is the section most worth spot-checking as a reviewer, because every line either matches its citation or it doesn't.""",
'cost': """What leaving actually costs, honestly denominated — for Orthodox and Hasidic communities specifically, family standing and social base; for liberal communities, the page says plainly, the cost is low. That contrast is itself one of the page's more careful findings.""",
'ledger': """Who benefits, who pays, what leverage flows back. The agunah dynamic is the clearest example this section returns to: a husband who withholds a get acquires indefinite leverage over a woman's entire future, at zero cost to himself under current rabbinic-court practice.""",
'who-gets-hurt': """States plainly where the weight lands hardest — disproportionately on women in get disputes, and on children and reporters in mesirah-affected abuse cases. Read this before the more analytical sections if you want the human stakes first.""",
'tiers': """The local rabbis, teachers, and communal officials implementing rules a state monopoly or a communal custom set, not something they personally authored. Same purpose as everywhere else in the book: don't collapse an institution into a monolith.""",
'cases': """Three fully-documented cases with named records — a UK school admissions ruling, an Israeli conversion-recognition case, an online-marriage recognition case. Read the outcome lines specifically for what actually changed.""",
'precedent': """What has already been broken once, and what would have to happen for it to become normal. The page names concretely what would count as evidence of real change here — worth reading as a benchmark, not a prediction.""",
'voices': """Named people from inside Jewish institutional life who raised the hard question publicly. The page's answer to "isn't this outsiders talking" — it isn't; the agunah advocates and abuse-reporting reformers named here are doing what the tradition's own history of canonized dissent trained them to do.""",
'regional': """Three country cards: Israel, the United States, the United Kingdom. Israel is the one to read first — it's the only place in this section where a religious monopoly runs on state authority inside a sovereign nation, which is the single most direct parallel to material documented elsewhere in this project's Islamic pages.""",
'questions': """Six questions the documented record could not resolve, expanded below into full cards — why each is asked, and a concrete example already on this page it points back to.""",
'leaving': """Practical, non-theological safety guidance for someone actually navigating a specific exit — a get, a communal break, a conversion dispute. Worth reading as a safety document, not an argument.""",
'help': """Vetted contact information, checked directly rather than copied from a list. The section to get exactly right if you ever point someone toward this page.""",
'sources': """Every citation traces to a named entry here — court records, rabbinic statements, academic sources, government reports. Spot-check a handful before trusting the rest of the page; that's the honest way to review any of these.""",
'changed': """A visible, dated log of corrections — the project's standing commitment not to quietly edit mistakes away. If your review changes something, it belongs here too.""",
}

SECTIONS_CATHOLIC = {
'at-a-glance': """The whole page in one table. Read "Chosen by / removable by" closely: a conclave whose every elector was appointed by a previous pope, and — the structural finding — no removal mechanism exists at all; even resignation must be the pope's own free act. That absence of any removal path is the single fact the rest of the page keeps returning to.""",
'a-day-inside': """Follows one ordinary day through the institution for the reason this section exists on every religion's page: "1.4 billion baptized" is abstract; a diocesan office's actual daily handling of a complaint, a transfer request, or a donation is not.""",
'forefront': """The page's thesis stated once: the central unanswered question — every national inquiry found the files existed and were kept; no one above the rank of bishop has ever lost office for keeping them sealed — plus the widest gap between statement and record, and the strongest counter-argument, answered fairly rather than dismissed.""",
'healthy': """What genuinely works, named first and separately, per the project's rule. For Catholicism this includes real institutional courage: the survivor networks, the bishops' conferences that broke from Rome's preferred silence, the reformers this same page names later. The Quran's own affirmation of 'Isa and the Injil (3:3) sits alongside naming what the tradition's own reformers got right.""",
'history': """The timeline anchors everything that follows in checkable dates. Watch specifically for the 11th–12th century Gregorian reforms that made clerical celibacy mandatory in the Latin Church — the genealogy section traces that requirement to an inheritance-and-property question, not a spiritual one, and the timeline is where that claim first becomes dateable.""",
'branches': """Latin Church, Eastern Catholic churches (which ordain married priests), and various reform and traditionalist currents — the branch table matters most for one specific fact it sets up: Eastern Catholic married priests are in full communion with Rome, which is the single strongest piece of internal evidence that celibacy is discipline, not doctrine.""",
'structure': """The organizational chart: the papal office, how it's filled, and the table's real finding — a chain of command with no external check at any level above the parish. Read "Who holds what" for how completely sacramental access concentrates in one office with no alternative provider.""",
'law': """Every tradition gets an honest answer to who can compel accountability. For the Catholic Church the record is mixed and instructive: real state-level prosecutions and government inquiries exist (documented in the cases section), while canon law's own internal mechanisms remain, on the record, largely untested against bishops specifically. Both facts are true at once.""",
'money': """Follow the flows the way you'd audit any large organization: Peter's Pence, diocesan appeals, one of the largest real-estate and institutional portfolios on earth. The "money in numbers" subsection is where the scale becomes concrete rather than rhetorical — worth reading with your own executive-advisory eye for where disclosure is thin.""",
'genealogy': """Built for exactly the comparison you asked for. Each of the four cards runs the same test used throughout this project: what a rule was for, why that reason expired, who benefits from it persisting. The clerical-celibacy card is the sharpest: traced to an 11th-12th century inheritance question (unmarried priests produce no heirs to claim Church land), a property rationale settled by modern corporate law centuries ago — yet the discipline remains, now serving a different function the page names directly.""",
'reach': """Maps institutional reach into information, children, and organizational bodies. Given the scale of Catholic school and hospital networks specifically, this section carries more real-world weight here than on most pages in the project — worth reading slowly.""",
'techniques': """The same thirty-technique, evidence-graded framework used across every tradition in this book. Catholicism scores among the more heavily-documented pages in the project on this measure — 11 of 30 techniques sourced to a named document, more than most — which the page states as a finding about documentation density, not severity.""",
'loops': """The same eight-stage cycle (idealize through replace) applied here. Read it alongside the cases section — the clerical-transfer pattern documented there maps almost exactly onto the "discard, then replace" stages of the cycle, worked out at institutional scale across decades.""",
'say-do': """A direct, checkable comparison between official statement and documented record — the most falsifiable section on the page, and the one worth your closest scrutiny as a reviewer.""",
'cost': """What leaving costs, honestly stated: for the devout, excommunication and denial of sacraments framed as risking eternal loss. The page treats that framing seriously rather than dismissing it, because taking a tradition's own stakes seriously is what makes documenting the institutional side of those stakes credible.""",
'ledger': """Who benefits, who pays, what leverage flows back. The annulment-tribunal card from the genealogy section is the throughline here: a panel of celibate men adjudicating whether a second marriage is spiritually real is a very specific kind of leverage over the most intimate decisions in a person's life.""",
'who-gets-hurt': """States plainly where the weight lands hardest — survivors of clerical abuse first, but also divorced Catholics denied communion while the institutions that enabled their abusers' transfers went largely unpunished. Read this section before the more analytical ones if you want the human stakes first.""",
'tiers': """Parish priests and diocesan staff implementing policies set well above them — the same purpose this section serves on every page in the book: don't collapse a global institution of 1.4 billion into a monolith of intent.""",
'cases': """Three fully-documented cases: the CIASE report on abuse in the French Church, Cardinal Becciu's conviction, and state-collected church tax. Read the outcome lines specifically — this is where the page shows, rather than asserts, both real accountability (a cardinal actually convicted) and its limits (no bishop convicted for concealment).""",
'precedent': """What has already been broken once, plus a "promises on the record" subsection tracking specific commitments against what actually happened. Read that subsection as the page's most direct answer to the question "hasn't this already been fixed?" """,
'voices': """Named Catholics — survivors, reformers, sometimes bishops themselves — who said the hard thing publicly. The page's direct answer to "isn't this all secular critique"; it isn't.""",
'regional': """Four country cards: Ireland, Poland, the United States, the Philippines — chosen because each shows a different accountability mechanism (a state commission, a concordat, grand juries, an annulment-dependent divorce-free legal system). Read them as four different experiments in the same underlying question.""",
'questions': """Six questions the documented record could not resolve, expanded below into full cards — why each is asked, and a concrete example already on this page it points back to.""",
'leaving': """Practical, non-theological guidance for someone navigating a specific exit safely. A safety document, not an argument — worth reading as such even if you never need it.""",
'help': """Vetted contact information, checked directly against each organization's own site. The section to get exactly right if this page is ever handed to someone who needs it.""",
'sources': """Every citation traces to a named entry: church records, court filings, government inquiries, named journalism. Spot-check several before trusting the rest — the honest way to review any page in this project.""",
'changed': """A visible, dated log of what was corrected and when. If your review changes anything here, it belongs in this same log, dated and attributed the same way.""",
}

QUESTIONS_JUDAISM = [
    {'why': "Asked because six years is not an edge case — it's long enough to demonstrate that \"discretion\" and \"no real remedy\" function identically in practice when no authority is willing to name a specific husband's conduct a violation with a real consequence attached.",
     'example': "The agunah pattern documented in the genealogy section: a woman chained to a marriage for years by a spiteful husband, while rabbinic courts describe themselves as procedurally unable to act — the same structural shape as a state-salaried scholar's fatwa never quite contradicting the government paying him, examined elsewhere in this project."},
    {'why': "Asked because if the rule genuinely doesn't apply to abuse, and rabbis have said so publicly, then families who still lose standing for calling police are being punished for something the rule no longer prohibits — which means the enforcement is doing different work than the stated rule.",
     'example': "The mesirah card in the genealogy section traces exactly this: a medieval protection against blood-libel tribunals, reapplied by some communities to a modern abuse report, protecting the institution's reputation rather than the child the original rule was never designed to fail."},
    {'why': "This question is aimed at the state-religion entanglement directly — a monopoly that made sense under empire, when communal self-governance was the only autonomy available, functions very differently inside a sovereign democracy with its own courts and legislature.",
     'example': "Israel's Chief Rabbinate holds statutory authority over Jewish marriage and divorce, on state salary, chosen by a 150-member body weighted toward rabbinic insiders rather than the general electorate — a state-backed religious monopoly with no secular civil-marriage alternative inside the country."},
    {'why': "Asked because a status that changes at a border reveals the authority in question is jurisdictional, not doctrinal — which matters enormously to anyone whose personal status (who they can marry, whether their children are recognized) depends on which country's religious authority is asking.",
     'example': "A conversion recognized in one country for immigration purposes can be treated as void by another country's religious authorities for marriage purposes — the same person, the same conversion, two different answers depending entirely on which institution is asked."},
    {'why': "This is a straightforward transparency test, not an accusation: institutions with genuinely adequate policies rarely take long to produce them in writing, and the delay itself is measurable data.",
     'example': "The page documents, across multiple traditions including this one, a consistent pattern where a written abuse-reporting policy either doesn't exist, exists but isn't public, or takes unusual effort to obtain — worth testing directly rather than assuming."},
    {'why': "The closing question targets the silencing mechanism itself: a rule that frames internal criticism as external aid to antisemites forecloses examination before any specific claim gets tested — a control pattern this page catalogues directly elsewhere as a named technique.",
     'example': "The same mechanism appears, differently worded, in every tradition this project covers, including in your own experience: criticism reframed as betrayal or aid to enemies, deployed to end a conversation rather than answer it."},
]

QUESTIONS_CATHOLIC = [
    {'why': "Asked because \"nothing to hide\" and \"a government had to subpoena the documents\" cannot both be true — an institution with genuinely nothing to hide does not require secular state power to produce its own internal records.",
     'example': "France's CIASE report, Australia's Royal Commission, and multiple US grand juries each obtained internal Church documents only through state authority — not one of them was produced by a synod or a papal inquiry acting first, on its own initiative."},
    {'why': "This is the page's sharpest accountability question because it isolates one specific, documented, repeated administrative decision — reassignment instead of reporting — and asks why the officials who made that decision, repeatedly, across decades and dioceses, have not lost their positions for having made it.",
     'example': "The genealogy section's canonical-secrecy card traces this directly: internal confidentiality norms built for a medieval world without functioning police were, per every national inquiry examined, used in the modern era to move accused priests between parishes rather than to protect anyone."},
    {'why': "Asked because the Becciu conviction proves the institutional capacity exists — a functioning criminal court, inside the Vatican, capable of convicting a cardinal — which makes its non-use on cover-up specifically a choice about priorities, not a limit of institutional power.",
     'example': "Cardinal Becciu was convicted of financial crimes by the Vatican's own tribunal — real, working accountability machinery. No bishop has been convicted by that same machinery, or an equivalent one, for concealing child abuse, despite the documentation multiple government inquiries produced."},
    {'why': "This question pairs two outcomes deliberately to expose an inconsistency in how the same institution applies consequence — a private, personal choice (remarriage after divorce) draws a sacramental penalty; a public, institutional choice (moving a known abuser) has not, in the documented cases, drawn an equivalent one.",
     'example': "Canon law bars a divorced-and-remarried Catholic from communion without an annulment. No comparable sacramental consequence is documented, on this page's own record, for the bishops who made the parish-transfer decisions traced in the cases and genealogy sections."},
    {'why': "This is a logic test applied to a stated doctrine, in the same spirit as the Salafi/Sunni test of daleel over custom used elsewhere in this project: if a rule is spiritually necessary, no valid exception should exist; if valid exceptions exist, the rule is a discipline, which is a different — and more honest — thing to call it.",
     'example': "Eastern Catholic churches, in full communion with Rome, ordain married men as priests. Their sacraments are recognized as fully valid by the Latin Church. That single fact settles the logic of the question on the record already, whatever any individual reader concludes from it."},
    {'why': "The closing question targets the fusion of institution and God themselves — a rule that equates criticizing the former with betraying the latter forecloses examination of the institution specifically by raising the cost of asking to the maximum possible level.",
     'example': "The same fusion appears in slightly different form in every tradition this project documents: a family or a community frames leaving one specific institution's version of faith as leaving faith itself, rather than as the narrower, separable choice it actually is."},
]


def build_personal_notes(rid):
    sections = {'sunni-islam': SECTIONS_SUNNI, 'judaism': SECTIONS_JUDAISM, 'catholicism': SECTIONS_CATHOLIC}[rid]
    salafi = SALAFI_SUNNI if rid == 'sunni-islam' else {}
    questions = {'sunni-islam': QUESTIONS_SUNNI, 'judaism': QUESTIONS_JUDAISM, 'catholicism': QUESTIONS_CATHOLIC}[rid]
    extra = EXTRA_QUESTION_SUNNI if rid == 'sunni-islam' else None
    return sections, salafi, questions, extra


# ================================================================== rendering
def note_box(md_text, kind, label):
    return f'<div class="box {kind}"><span class="lbl">{e(label)}</span>' + md_to_html(md_text) + '</div>'


def render_hardq_section(content, expansions, extra=None):
    """Replace the numbered hard-questions list with expanded cards; leave '### In closing' onward as markdown."""
    m = re.search(r'^\s*1\.\s.*?(?=\n### )', content, re.S)
    list_block = m.group(0)
    rest = content[m.end():]
    items = [it.strip().replace('\n', ' ') for it in re.findall(r'^\d+\.\s+(.*?)(?=^\d+\.\s|\Z)', list_block, re.M | re.S)]
    n_total = len(items) + (1 if extra else 0)
    cards = []
    # .qhead (label + question) is its own break-inside:avoid unit so a page break can only ever
    # land inside the why/example prose, never orphan the label above an empty rest-of-page.
    for i, (qtext, exp) in enumerate(zip(items, expansions), 1):
        cards.append(f'<div class="box hardq"><div class="qhead"><div class="qn">Question {i} of {n_total}</div>'
                      f'<div class="qtext">{inline(e(qtext))}</div></div>'
                      f'<h4>Why this is asked</h4><p>{inline(e(exp["why"]))}</p>'
                      f'<h4 class="ex">Example already on this page</h4><p>{inline(e(exp["example"]))}</p></div>')
    if extra:
        cards.append(f'<div class="box hardq"><div class="qhead"><div class="qn">Question {n_total} of {n_total} · Salafi/Sunni lens, added for this copy</div>'
                      f'<div class="qtext">{inline(e(extra["q"]))}</div></div>'
                      f'<h4>Why this is asked</h4><p>{inline(e(extra["why"]))}</p>'
                      f'<h4 class="ex">Example already on this page</h4><p>{inline(e(extra["example"]))}</p></div>')
    return ''.join(cards) + md_to_html(rest)


def build_html_personal(rid):
    sdp.VALID = None  # reset; set below exactly as the base module does
    raw = open(os.path.join(SRC, f'{rid}.md'), encoding='utf-8').read()
    meta, body = front_matter(raw)
    name = meta.get('title', rid)
    src_part = re.search(r'^## \d+\. Sources \{#sources\}\n(.*?)(?=^## \d+\.)', body, re.S | re.M)
    sdp.VALID = {int(n) for n in re.findall(r'^\s*(\d+)\.\s', src_part.group(1), re.M)} if src_part else set()
    sdp.TACTIC_NAMES = {int(n): re.sub(r'\s*\{#.*', '', t) for n, t in re.findall(r'^#### (\d+) · (.+)$', body, re.M)}

    notes, salafi, questions, extra = build_personal_notes(rid)

    parts = re.split(r'^## (\d+)\. (.+?) \{#([\w-]+)\}\s*$', body, flags=re.M)
    sections = [(parts[i], parts[i + 1], parts[i + 2], parts[i + 3]) for i in range(1, len(parts), 4)]
    toc, secs = [], []
    for num, title, slug, content in sections:
        if slug == 'questions':
            h = render_hardq_section(content, questions, extra)
        else:
            h = md_to_html(content)
        if slug == 'sources': h = sources_ids(h)
        if slug == 'cases':
            h = re.sub(r'(<strong>tactics:</strong>)\s*([\d, ]+)', lambda m: m.group(1) + ' ' + ', '.join(
                f'<a class="tlink" href="#t-{n.strip()}">{n.strip()} · {sdp.TACTIC_NAMES.get(int(n), "")}</a>' for n in m.group(2).split(',') if n.strip()), h)
            h = re.sub(r'(<strong>grade:</strong>)\s*(\w+)', lambda m: f'{m.group(1)} <span class="chip g-{m.group(2).lower()}">{m.group(2)}</span>', h)
        if slug == 'at-a-glance': h = score_cells(h)
        if slug == 'techniques':
            grades = re.findall(r'<span class="chip g-(\w+)">', h)
            counts = {}
            for g in grades: counts[g.title()] = counts.get(g.title(), 0) + 1
            index = re.findall(r'<h4 id="t-(\d+)">\d+ · (.+?)</h4>', h)
            grade_of = dict(re.findall(r'id="t-(\d+)">.*?<span class="chip g-(\w+)">', h, re.S))
            grid = ''.join(f'<a href="#t-{n}"><span class="n">{n}</span><span class="nm">{nm}</span>'
                           f'<span class="chip g-{grade_of.get(n, "ungraded")}">{grade_of.get(n, "ungraded").title()}</span></a>' for n, nm in index)
            lead = (grade_bar(counts) if counts else '') + (f'<h3 id="techniques-index">All thirty at a glance</h3><div class="tgrid">{grid}</div>' if grid else '')
            h = re.sub(r'(</p>)', r'\1' + lead.replace('\\', '\\\\'), h, count=1) if lead else h

        # -------- reviewer layer: a personal note, then (Sunni copy only) a Salafi point
        extra_html = ''
        if slug in notes:
            extra_html += note_box(notes[slug], 'note-a', NOTE_LABEL[rid])
        if slug in salafi:
            extra_html += note_box(salafi[slug], 'salafi', "A Salafi/Sunni methodology point")
        h = extra_html + h

        subs = re.findall(r'<h3 id="([\w-]+)">(.*?)</h3>', h)
        if slug != 'techniques':
            k = [0]
            def add_id(m):
                k[0] += 1
                return f'<h3 id="{slug}-{k[0]}">{m.group(1)}</h3>'
            h = re.sub(r'<h3>(.*?)</h3>', add_id, h)
            subs = re.findall(r'<h3 id="([\w-]+)">(.*?)</h3>', h)
        toc.append((num, title, slug, subs))
        secs.append(f'<section class="sec" id="sec-{slug}"><h2 id="{slug}"><span class="num">Section {int(num):02d}</span><span class="t">{e(title)}</span></h2>{h}</section>')

    howto = md_to_html(open(os.path.join(SRC, '_how-to-read.md'), encoding='utf-8').read())
    def toc_item(num, title, slug, subs):
        sub_links = ''.join('<a href="#%s">%s</a>' % (sid, re.sub(r'<[^>]+>', '', st)) for sid, st in subs[:14])
        return (f'<li><a class="sec" href="#{slug}"><span class="n">{int(num):02d}</span><span class="t">{e(title)}</span>'
                f'<span class="dots"></span></a>' + (f'<div class="subs">{sub_links}</div>' if subs else '') + '</li>')
    toc_html = '<ol>' + ''.join(toc_item(*t) for t in toc) + '</ol>'
    lede = re.search(r'<div class="box lede">\s*<p>(.*?)</p>', secs[3], re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else ''
    if len(blurb) > 260: blurb = blurb[:257].rsplit(' ', 1)[0] + '…'

    preface_html = md_to_html(PREFACE[rid])
    recipient = RECIPIENT[rid]
    for_line = f'<div class="for">Prepared for <b>{e(recipient)}</b> — for his review</div>' if recipient else ''
    cover = (f'<div class="cover"><div class="band"></div><img class="mark" src="mark.png" alt="">'
             f'<div class="eyebrow">The Sacred Divide</div>'
             f'{for_line}'
             f'<h1>{e(name)}</h1>'
             f'<div class="family">{e(meta.get("family", ""))} family</div><div class="rule"></div>'
             f'<div class="tagline">Honor the faith · Name the machinery</div><div class="blurb">{e(blurb)}</div>'
             f'<div class="meta"><span>{e(meta.get("version", ""))} · checked {e(meta.get("checked", ""))}</span><span>{SITE}</span></div></div>')
    preface = (f'<div class="front preface"><h1 id="preface">A note before you read</h1>{preface_html}</div>')
    title_suffix = f' — for {e(recipient)}' if recipient else ' — expanded review copy'
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(name)}{title_suffix} — The Sacred Divide</title>
<meta name="author" content="Noble Father Creations"><meta name="subject" content="{e(name)}: expanded review copy{' prepared for ' + e(recipient) if recipient else ''}">
<link rel="stylesheet" href="sacred-divide.css">
<link rel="stylesheet" href="sacred-divide-personal.css">
<script>window.PagedConfig = {{ auto: true, after: () => {{ window.__paged = true; }} }};</script>
<script src="paged.polyfill.js"></script></head><body>
{cover}
{preface}
<div class="front toc"><h1 id="contents">Contents</h1>{toc_html}</div>
<div class="front howto">{howto}</div>
{"".join(secs)}
</body></html>'''
    return doc, name, meta


def render_personal(rid):
    os.makedirs(OUTDIR, exist_ok=True)
    doc, name, meta = build_html_personal(rid)
    recipient = RECIPIENT[rid]
    slug = 'for-abdurahman' if recipient else 'review-copy'
    page = os.path.join(TOOLS, f'.build-abd-{rid}.html')
    open(page, 'w', encoding='utf-8').write(doc)
    out_pdf = os.path.join(OUTDIR, f'{rid}-{slug}.pdf')
    subprocess.run(['node', os.path.join(TOOLS, 'print.js'), page, out_pdf, name], check=True)
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(out_pdf)
    w = PdfWriter(clone_from=r)
    w.add_metadata({'/Title': f'{name} — expanded review copy' + (f' for {recipient}' if recipient else '') + ' — The Sacred Divide',
                    '/Author': 'Noble Father Creations',
                    '/Subject': f'{name}: full record' + (f', with a note to {recipient} before every section' if recipient else ', with a note before every section') + ' and expanded hard questions.',
                    '/Keywords': f'The Sacred Divide; {name}; {meta.get("family", "")}' + (f'; for {recipient}' if recipient else '')})
    marks = json.load(open(out_pdf.replace('.pdf', '.marks.json')))
    os.remove(out_pdf.replace('.pdf', '.marks.json'))
    w._root_object.pop('/Outlines', None)
    parent = {}
    for m in marks:
        if not m['page']: continue
        pg, text = m['page'] - 1, m['text']
        sec = re.match(r'^SECTION (\d+)\s*(.*)$', text, re.I)
        if m['level'] == 1:
            parent[1] = parent[2] = w.add_outline_item(text, pg); parent[3] = None
        elif sec:
            parent[2] = w.add_outline_item(f'{int(sec.group(1)):02d} · {sec.group(2)}', pg); parent[3] = None
        elif m['level'] == 2 and parent.get(1) is not None:
            w.add_outline_item(text, pg, parent=parent[1])
        elif m['level'] == 3 and parent.get(2) is not None:
            parent[3] = w.add_outline_item(text, pg, parent=parent[2])
        elif m['level'] == 4 and (parent.get(3) or parent.get(2)) is not None:
            w.add_outline_item(text, pg, parent=parent.get(3) or parent[2])
    w.page_mode = '/UseOutlines'
    with open(out_pdf, 'wb') as f: w.write(f)
    r = PdfReader(out_pdf)
    links = sum(1 for p in r.pages for a in (p.get('/Annots') or []) if a.get_object().get('/Subtype') == '/Link')
    def count(o):
        return sum(count(x) if isinstance(x, list) else 1 for x in o)
    print(f'{out_pdf}: {len(r.pages)} pages, {links} links, {count(r.outline)} bookmarks')
    os.remove(page)
    return out_pdf


if __name__ == '__main__':
    ids = sys.argv[1:] or ['sunni-islam', 'judaism', 'catholicism']
    for rid in ids:
        render_personal(rid)
