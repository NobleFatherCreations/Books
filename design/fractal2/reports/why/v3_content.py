"""New writing and additions for edition 3 of "Why I Wrote This". First person, the owner's voice.
Sources are named next to each block. Nothing here invents a statistic, a tactic, a combination or a quote:
figures come from design/fractal2/reports/value-and-impact.html (the Value-and-Impact report) with its cautions,
and the owner's words come from content/fractal2/owner-source/ and docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md."""
import re, json, html, pathlib
HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
VERB = (ROOT / "docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md").read_text().split("\n")
WAR = (ROOT / "content/fractal2/owner-source/B-part-III-the-war-map.md").read_text()
e = html.escape

def add(chunk, extra, before=False):
    """Add new material to a reused section: after its kicker/h2/lede when before=True, else at the end."""
    if before:
        m = re.search(r'(<p class="lede">.*?</p>|</h2>)', chunk, re.S)
        return chunk[:m.end()] + extra + chunk[m.end():]
    return chunk + '<div class="add">' + extra + "</div>"

# ---------------------------------------------------------------- movement dividers (curiosity hooks)
def parts():
    P = {
        1: ("Movement 1", "Why I wrote this", "Why would anyone spend years mapping something this painful?"),
        2: ("Movement 2", "What I saw", "What is the pattern, exactly, and why is it so hard to see from inside?"),
        3: ("Movement 3", "What I built to name it", "If the pattern is everywhere, how does one person find the exact thing that happened to them?"),
        4: ("Movement 4", "Why the order matters", "Why do smart, careful people still get caught?"),
        5: ("Movement 5", "What was there first", "If every system copies something real, what was the real thing, and is it still there?"),
        6: ("Movement 6", "How change begins", "So what do we do: in a school, a family, a sector, a country?"),
        7: ("Movement 7", "What these three works do, and how they help people", "What could happen if enough people could see it?"),
        8: ("Movement 8", "I can't do this alone", "One small thing, and then one thing I want to show you."),
        "ref": ("Reference", "Tools, lenses and limits", "For use, for checking, and for disagreeing with me."),
    }
    return {k: f'<div class="part"><i>{a}</i><h2>{b}</h2><p>{c}</p></div>' for k, (a, b, c) in P.items()}

# ---------------------------------------------------------------- contents + how to read the map
def contents(N, machine):
    groups = [("Why I wrote this", [1, 2, 3]), ("What I saw", [4, 5, 6, 7, "7b"]), ("What I built to name it", [8, 9, 10]),
              ("Why the order matters", [11, 12]), ("What was there first", [13, 14, "14b", 15]),
              ("How change begins", [16, 17, 18, "18b", 19]), ("What these three works do", [20, 21, 22, "22b", 23, 24, 25]),
              ("I can't do this alone", [26, 27]), ("Reference", ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14"])]
    inter = {1: "Before this page: The Trauma Bond Engine", 3: "Then: The Normalization Engine",
             7: "Then: The Public Shaming Ritual", 10: "Then: The Paper Child", 15: "Then: The Calling Trap"}
    rows = []
    for i, (g, ns) in enumerate(groups):
        rows.append(f'<tr class="g"><td colspan="2">{"Movement %d · " % (i + 1) if i < 8 else ""}{g}</td></tr>')
        for n in ns:
            rows.append(f'<tr><td class="n">{n}</td><td><a href="#sec{n}">{e(N[n])}</a></td></tr>')
            if n in inter: rows.append(f'<tr class="il"><td></td><td>{inter[n]}</td></tr>')
    return f'''<section class="pb" id="contents"><div class="kick">How to read this</div><h2>One story, eight movements</h2>
<p class="lede">You've just been inside one machine. This document explains why I mapped thousands of them, what the map shows, and what it could do for people.</p>
<div class="cols2"><table class="toc">{"".join(rows)}</table>
<div><h4>If you have ten minutes</h4><p class="small">The opening scene you just read, then Sections 1 and 24.</p>
<h4>If you're a parent</h4><p class="small">Sections 4, 15 and 19, and the Public Shaming Ritual interlude.</p>
<h4>If you work in a school or a clinic</h4><p class="small">All five interludes. Then Sections 16, 19 and 21, the self-audit in R1, and the limits in R3.</p>
<h4>If you want the whole argument</h4><p class="small">Straight through. Each movement opens with the question it answers. The scenes between movements are not illustrations. They are the work itself, so you can judge it directly.</p>
<h4>Three kinds of statement</h4><p class="small"><span class="tag f">Documented</span>research, history, public numbers. <span class="tag j">My synthesis</span>the map, what I see across it. <span class="tag l">My belief</span>faith and contested science, marked as mine.</p></div></div>
<h3>The whole map on one page</h3>{machine}</section>'''

# ---------------------------------------------------------------- trust, up front (Blueprint B7, Part H)
def trust():
    return '''<section class="pb" id="trust"><div class="kick">Before you read</div><h2>What you can trust here, and what you shouldn't</h2>
<p class="lede">You'll believe the rest more if you know where it is weakest. So here it is first.</p>
<div class="three"><div><b>Documented</b><p>The individual tactics have names in the clinical and research literature. The harms they describe are among the most common in human life. Where I give a number, I give its source and its caution.</p></div>
<div><b>My synthesis</b><p>That one pattern of eight stages runs through all thirty sectors, at three scales, and that the order of moves is what bonds a person. That is my map. It hasn't yet been checked by outside reviewers. I'm asking for that.</p></div>
<div><b>My belief</b><p>The spiritual reading, and some of the nervous-system and inheritance language. I hold these as faith and as my understanding, not as fact. The structure stands without them.</p></div></div>
<h3>I wasn't the first to see pieces of this</h3>
<p>Serious people reached parts of this picture by study. I reached the whole of it by living it and then looking. Two routes arriving at the same shape is a reason to take the shape seriously.</p>
<table class="small"><tr><th>Who, when</th><th>What they saw</th><th>Where it sits in my map</th></tr>
<tr><td><b>Albert Biderman</b>, 1957</td><td>Eight methods that break a person without force</td><td>The techniques: isolate, confuse, occasional kindness</td></tr>
<tr><td><b>Paulo Freire</b>, 1968</td><td>The dominated take the dominator inside and enforce his rules on themselves</td><td>The Mirror</td></tr>
<tr><td><b>Ivan Illich</b>, 1971–75</td><td>Past a certain size, schools and medicine turn a need into a product</td><td>Every need has a gate</td></tr>
<tr><td><b>Jack Forbes</b>, 1978</td><td>Wétiko: exploitation as a sickness that spreads carrier to carrier</td><td>The pattern as an organism</td></tr>
<tr><td><b>Dutton and Painter</b>, 1981, tested 1993</td><td>A trauma bond needs a power gap and good treatment alternating with bad</td><td>Why the order matters</td></tr>
<tr><td><b>Walter Wink</b>, 1984–92</td><td>Institutions have an inner spirit; the struggle is with the Powers, never with persons</td><td>Patterns, never people</td></tr>
<tr><td><b>Judith Herman</b>, 1992</td><td>Captivity in a home and in a political prison produce the same psychology</td><td>The three levels</td></tr>
<tr><td><b>Evan Stark</b>, 2007</td><td>Coercive control: liberty taken, mostly without violence</td><td>The cycle as a whole</td></tr>
<tr><td><b>Miranda Fricker</b>, 2007</td><td>A person can be wronged twice: once by the harm, again by having no words for it</td><td>Why naming matters</td></tr></table>
<p>Each of them saw one face of it. What I've tried to add is the whole of it in one map: plain language, every sector, three scales, the inner life and the family line, and a practice for each part.</p>
<div class="box plain"><h4>Three things I won't claim</h4><p><strong>That every institution is only this.</strong> Hospitals also heal. Schools also teach, sometimes in the same hour they run the cycle. The map shows you which one you're getting.<br><strong>That seeing it means leaving.</strong> Seeing is not leaving. Sometimes the safest move is to stay and get help first.<br><strong>That a map ends the cycle.</strong> No map does. What ends is the method's ability to stay hidden.</p></div></section>'''

# ---------------------------------------------------------------- 1. origin (verbatim, test-locked)
def origin():
    L = (ROOT / "content/fractal2/intro-final.md").read_text().split("\n")[274:279]
    paras = "".join(f"<p>{e(l)}</p>" for l in L if l.strip())
    return f'''<div class="sec" id="origin"><div class="kick">x</div><h2>Why I can draw this</h2>
<div class="origin">{paras}</div>
<p>That's the whole reason. Everything that follows is the work of turning one person's survival into something anyone can use.</p>
<p>I started writing about one sector, then the next. I made a video series, one sector per episode, thirty of them. Then I wrote it down as a book, then kept going. The rest of this document is what I found, what I built, and what I think it can do.</p></div>'''

def fix_why(chunk):
    """Remove the paragraph edition 2 wrote in my voice without my words (steelman miss #1). Replace with Fricker."""
    chunk = re.sub(r"<p>I didn't come to this as a researcher\..*?</p>", "", chunk, count=1, flags=re.S)
    return add(chunk, '''<p class="pull">You can be harmed twice: once by what was done, and again by having no words for it.</p>
<p>The philosopher Miranda Fricker named that second harm. Her example is Carmita Wood, who left a job because of a professor's advances, couldn't explain why on a benefits form, wrote "personal reasons," and was refused. A group of women met, compared stories, and coined a phrase: <em>sexual harassment</em>. About ten years later it was recognised in law. <span class="tag f">Documented</span></p>
<p>That's the realistic way change starts. A book rarely does it. A vocabulary does, once enough people use it. I've tried to build the vocabulary.</p>''')

# ---------------------------------------------------------------- 3. three works, four verbs, three units
def three_works():
    return '''<div class="sec" id="works"><div class="kick">x</div><h2>Three works, four verbs</h2>
<p class="lede">Everything I've made does one of four things. If you remember nothing else, remember these.</p>
<div class="verbs"><div><i>See</i><b>The Fractal</b><p>30 sectors × 30 techniques × 3 levels. It proves the pattern runs everywhere.</p><span>"It's not just me."</span></div>
<div><i>Name</i><b>The Pattern Decoder and Fractal²</b><p>Over 300 named tactics per sector, each at three scales, each in plain words.</p><span>"That's the one."</span></div>
<div><i>Break</i><b>The combinations</b><p>150+ per sector. How moves chain into a life, why the order matters, where it breaks.</p><span>"There's the exit."</span></div>
<div><i>Return</i><b>The Frequency</b><p>The real need under every copy, and one small practice to get back to it.</p><span>"It was mine all along."</span></div></div>
<p>Under all four sits one idea. Every human need was meant to be met. A pattern has learned to stand between people and their needs, copy the real thing, and charge for access.</p>
<h3>Three units</h3>
<div class="units"><div><b>The unit of harm is the sequence.</b><p>Nobody is hit by one tactic. People live through orders of moves. The combinations show the sequence.</p></div>
<div><b>The unit of healing is the pause.</b><p>The gap between the move and your response. The Frequency teaches the pause.</p></div>
<div><b>The unit of prevention is the word.</b><p>A child who has the name before the move can't be caught the same way. Playground Protectors and the Decoder give the word.</p></div></div>
<h3>Three moments</h3>
<p>Most help for manipulation reaches people <em>after</em>. My work is built for all three moments: <strong>before</strong> (the word: Playground Protectors and the Decoder), <strong>during</strong> (the sequence and its turning point: the combinations), and <strong>after</strong> (the proof it wasn't you: The Fractal).</p>
<h3>Five things this work does that almost nothing else does</h3>
<div class="five"><div><i>1</i><b>It transfers a skill you already have.</b> Millions of people learned "gaslighting" and "love bombing" the hard way, inside a relationship. The same eye that finally saw it in a partner can see it in a hospital bill, an enrolment office or a contract.</div>
<div><i>2</i><b>It teaches by repetition.</b> The same grid laid over thirty buildings. By the fifth sector you start predicting the next cell before you read it. That's when it stops persuading and starts training.</div>
<div><i>3</i><b>It doesn't need a villain.</b> A real need, a power gap and a gatekeeper are enough. That keeps it out of conspiracy thinking, and explains why replacing the person at the top so rarely fixes the building.</div>
<div><i>4</i><b>It turns inward and backward.</b> The Mirror: we run these moves on ourselves. The Chain: they were handed down. That's where it stops being about "them."</div>
<div><i>5</i><b>It ends in practice, and gives no orders.</b> Each technique is paired with the real thing it copied and one small practice. Then it refuses to tell you what to do with your life. If it did, it would be the cycle.</div></div>
<p class="small">The five come from an independent assessment of the work (the Value-and-Impact report, November 2026), which I've adopted because I think it's right.</p></div>'''

# ---------------------------------------------------------------- 8, 9 additions
def numbers_plus(chunk):
    chunk = add(chunk, '<p class="pull">By the fifth sector, you start predicting the next cell. That is why there are thirty.</p>', before=True)
    return add(chunk, '''<p class="small"><strong>A note on the count.</strong> The framework is thirty sectors and 2,700 examples. Twenty-six sector chapters are published (2,340 examples). Technology, Dating, Surveillance and Child Welfare are in production. I'd rather you hear that from me.</p>''')

def ladder_plus(chunk):
    return add(chunk, '''<h3>The change in scale</h3><table><tr><th></th><th>The Fractal</th><th>Fractal², per sector</th><th>Fractal², thirty sectors</th></tr>
<tr><td><b>Named tactics</b></td><td class="n">30</td><td class="n">335</td><td>the same 335, re-observed in each</td></tr>
<tr><td><b>Worked examples</b> (tactic × 3 levels)</td><td class="n">90 per sector · 2,700</td><td class="n">1,005</td><td class="n">30,150</td></tr>
<tr><td><b>Combinations</b></td><td>none</td><td>153 in the first sector; 203 on its master list</td><td>one set per sector</td></tr></table>
<p class="small">For scale: Biderman's chart had 8 items, the Power and Control Wheel 8, <em>A Pattern Language</em> 253, the security catalogue ATT&amp;CK about 222. Size isn't quality. The two smallest are the most widely used, which is why I also need a one-page form (Section 22).</p>''')

# ---------------------------------------------------------------- 10. one tactic through every work
def one_tactic():
    return '''<div class="sec" id="one"><div class="kick">x</div><h2>One tactic through every work</h2>
<p class="lede">This shows how the pieces fit, using one move: hot, then cold, then hot again.</p>
<p>The research name is <em>intermittent reinforcement</em>. Watch it move from a definition to words a ten-year-old can use.</p>
<div class="strip">
<div><i>1 · The Pattern Decoder</i><b>Names it</b><p>"Giving out affection, praise or kindness rarely and at unpredictable times. The few good moments then hold a person tighter than steady warmth would."</p><p class="q">It can sound like: "See, this is how it could always be, if you tried a bit harder."</p></div>
<div><i>2 · The Fractal, Education</i><b>Shows it everywhere</b><p><b>Person:</b> grades as an unpredictable reward. An A for work you barely tried on, a C for work you poured yourself into.</p><p><b>Institution:</b> honours and awards dangled just unpredictably enough to keep a student body striving.</p><p><b>Civilization:</b> the degree-to-career pipeline delivers just often enough to sustain the myth.</p></div>
<div><i>3 · Fractal², Entertainment</i><b>Finds the exact version</b><p><b>Person:</b> "Your manager calls you a genius one week and ignores your texts the next."</p><p><b>Institution:</b> playlist placements that arrive without explanation, keeping artists pitching.</p><p><b>Civilization:</b> the lottery logic that anyone could blow up overnight.</p></div>
<div><i>4 · The combinations</i><b>Shows where it sits in a life</b><p>It opens The Trauma Bond Engine: "screams at you one day, hand on your shoulder the next." It appears in 9 of the 153 Entertainment combinations, usually early: on average third of six or seven moves, in the first half of the chain in 6 of 9. It softens the ground for what follows.</p></div>
<div><i>5 · Playground Protectors</i><b>Gives a child the word</b><p>"The Hot-and-Cold Game." Week one, Furbie saves you a seat. Week two, he looks through you. Week three, he acts like nothing happened.</p><p class="q">The power-up: Steady Sunshine. "Your job is not to turn your heat up to compensate. Your job is to stay at your own steady temperature."</p></div></div>
<p class="pull">One move at five resolutions, from a research term to words a ten-year-old can use.</p>
<p>The Decoder holds the definitions. The Fractal proves the pattern crosses all thirty sectors. Fractal² applies the Decoder's tactics to one sector at three scales. The combinations put the tactics in the order a life meets them. Playground Protectors gets the word to a child before the move does.</p>
<p class="small">One honest seam: The Fractal files this move under Stage 4 (Confuse); Fractal² files it under Stage 3 (Devalue). It does both jobs. I'll make the two agree.</p></div>'''

# ---------------------------------------------------------------- 11. why the order matters, opened with the strongest argument
def order_plus(chunk):
    lines = VERB[936:946]
    notes = [l for l in lines if l.strip()]
    owner = "".join(f"<p>{e(l)}</p>" for l in notes if l.startswith(("If every", "And when you", "You've been", "This video is the")))
    lead = f'''<div class="five two"><div><i>1</i><b>Nobody is hit by one tactic.</b> People live through sequences. Almost everything written for the public describes single tactics. A person can learn thirty definitions and still not recognise their own life, because what they're inside is the order.</div>
<div><i>2</i><b>Each step removes the defence against the next.</b> The trust built at step one is what makes the paperwork at step four feel rude to question. That also means there's a weak point at every join.</div>
<div><i>3</i><b>A list explains your past. A sequence predicts your future.</b> Someone taught to distrust their own memory can still run this test: <em>the map said this would come next, and it did.</em> Gaslighting works on memory. It has little grip on a prediction made in advance and then watched coming true.</div>
<div><i>4</i><b>The defender only needs one link.</b> Security researchers describe a network attack as a chain of steps, and point out the defender only has to break one. Their free public catalogue of attacker behaviour became the shared language of their profession. Fractal² has the same structure, for coercion between people. <span class="tag f">Documented</span></div></div>
<h3>In my own words, from the combinations script</h3><div class="owner">{owner}<p>And a combo is always greater than the sum of its parts.</p></div>
<p>I wrote them in three kinds: <strong>early-stage hooks</strong> that latch before you know you've been touched, <strong>mid-stage traps</strong> that tighten while you still call it normal, and <strong>late-stage entanglements</strong>, where leaving feels like losing a piece of yourself.</p>'''
    return add(chunk, lead, before=True)

# ---------------------------------------------------------------- 13. frequency additions
def frequency_plus(chunk):
    i = VERB.index("WHAT THE FREQUENCY SOUNDS LIKE")
    s = VERB[i + 1:i + 16]
    sounds = "".join(f"<li>{e(l[len('It sounds like '):])}</li>" for l in s if l.startswith("It sounds like"))
    return add(chunk, f'''<h3>What it sounds like</h3><p class="small">From the last chapter of The Fractal, in my words:</p><ul class="sounds">{sounds}</ul>
<p class="pull">You did not get here by going up. You went down.</p>
<p>That's the shape of the whole book, and of this document. Out into the sectors. In, to the mirror and the body. Back, along the chain. Then down to the ground: the frequency. The ending is the floor under your feet, which was there before any of this.</p>
<p>The pause is where the original impulse lives. The cycle didn't stop because you named it. But you can now catch it in the instant between the move and your response. <strong>That instant is the frequency.</strong></p>''')

# ---------------------------------------------------------------- 15. your life, sector by sector
LIFE = [("Birth", "Healthcare", 5, "Healthcare", "Words for being dismissed; the right to be believed about their own body", "A check for when a \"normal\" result ends the conversation", "A measure of health restored, not activity billed"),
        ("Birth", "Child welfare", 22, "Child Welfare", "\"I was processed, not chosen\" stops being a private shame", "A test for whether a child is a case or a person", "A reason to fund belonging, not placements"),
        ("Early years", "Family", 8, "Family", "The inherited sentence, caught mid-word", "A shared vocabulary at the table (the family is the institution)", "A chain that breaks between generations"),
        ("Early years", "Food", 14, "Food", "Hunger heard as a signal, not a failure of will", "A view of what engineered craving does to trust", "Nourishment measured, not calories sold"),
        ("Childhood", "Education", 4, "Education", "Worth separated from the score", "A way to spot shame used as a tool; the self-audit in R1", "Curiosity kept as the measure of a school"),
        ("Childhood", "Sports", 16, "Sports", "Joy in movement back from the contract", "A line between demanding and degrading", "Play valued without a scoreboard"),
        ("Childhood", "Religion", 1, "Religion", "The sacred separated from the gatekeeper", "A way to welcome questions without losing the faith", "Belief without coercion"),
        ("Youth", "Beauty", 19, "Beauty", "\"Born complete\" as a counter-voice to the mirror", "Accountability for manufactured insufficiency", "A generation less sold-to about their bodies"),
        ("Youth", "Technology", 7, "Technology", "The tool put back in the hand", "A design test for attention capture", "Platforms judged by time well spent"),
        ("Youth", "Media", 3, "Media", "The ability to tell informing from inflaming", "A mirror for engagement-first editing", "A public that can name a manufactured crisis"),
        ("Youth", "Entertainment", 12, "Entertainment", "Expression that doesn't need an audience", "Contracts artists can read and leave", "Culture that isn't only product"),
        ("Youth", "Dating", 20, "Dating", "Speed recognised as a warning, not a compliment", "Apps judged by matches that leave the app", "Intimacy that isn't a market"),
        ("Adulthood", "Corporate", 10, "Corporate", "\"We're a family here\" heard correctly", "A check on whether leaving is punished", "Work measured by more than output"),
        ("Adulthood", "Finance", 6, "Finance", "Debt seen as a leash, not a character flaw", "Plain-language terms as a standard", "Enough as a legitimate goal"),
        ("Adulthood", "Housing", 15, "Housing", "Rest that doesn't have to be earned", "Housing as shelter first", "Security of the median household"),
        ("Adulthood", "Insurance", 28, "Insurance", "A denial read as a first offer", "Claims handling people can follow", "Safety that isn't sold on fear"),
        ("Adulthood", "Legal system", 9, "Legal System", "The right to ask \"what would repair look like?\"", "Restorative options beside punishment", "Justice measured by harm repaired"),
        ("Adulthood", "Politics", 2, "Politics", "Participation at the size of a room", "Promises tracked against delivery", "A vote that isn't the only voice"),
        ("Adulthood", "Military", 11, "Military", "Identity beyond the uniform", "Care that continues after service", "Protection separated from projection"),
        ("Adulthood", "Science", 17, "Science", "Permission to ask unfunded questions", "Disclosure of who paid for the answer", "Trust that is earned, not demanded"),
        ("Adulthood", "Nonprofits", 18, "Nonprofits", "Helping hand to hand", "Outcomes over stories", "Compassion that reaches the person"),
        ("Adulthood", "Wellness", 13, "Wellness", "Healing at its own pace", "A line between help and upsell", "A remedy test: does this return me to myself?"),
        ("Adulthood", "Mental health", 26, "Mental Health", "A feeling felt before it is labelled", "Care that builds self-knowledge", "Help that isn't locked behind a diagnosis"),
        ("Adulthood", "Pharmaceuticals", 27, "Pharma", "A vote for the body, alongside the prescription", "Honest alternatives in the room", "Medicine priced as need, not leverage"),
        ("Adulthood", "Surveillance", 21, "Surveillance", "A private inner life, kept on purpose", "Consent a person can actually read", "Privacy treated as a right"),
        ("Adulthood", "Transportation", 25, "Transportation", "Three miles an hour, sometimes", "Places built to be walked", "Freedom of movement without a payment"),
        ("Adulthood", "Energy & environment", 24, "Energy", "Belonging to the earth, felt in the hands", "Costs no longer pushed onto others", "Restoration as the measure"),
        ("Any age", "Incarceration", 29, "Incarceration", "Worth not set by the worst day", "A way back that is real", "Restoration over warehousing"),
        ("Any age", "Immigration", 30, "Immigration", "Belonging that doesn't wait for a document", "People treated as people, not files", "A welcome that matches the values claimed"),
        ("The end", "Aging & death", 23, "Death", "A say in how the end feels", "Comfort before billing", "Dying brought back into the home")]

def _impulses():
    out, cur = {}, None
    for l in VERB[148:281]:
        m = re.match(r"^(\d+)\. (.+)$", l)
        if m: cur = int(m.group(1)); out[cur] = {"title": m.group(2).rstrip(".")}; continue
        if cur and l.startswith("The practice:") and "practice" not in out[cur]:
            out[cur]["practice"] = " ".join(re.split(r"(?<=[.!?])\s+", l[len("The practice: "):])[:2])
    assert len(out) == 30
    return out

def _reclaim():
    t = WAR[WAR.index("| Sector | Reclamation Practice |"):WAR.index("### 4. Protect the Children")]
    return {r[0].strip(): r[1].strip() for r in (row.strip("|").split("|") for row in t.split("\n")[2:] if row.startswith("|"))}

def sector_cards():
    imp, rec = _impulses(), _reclaim()
    cards = []
    for stage, name, n, key, p, i, s in LIFE:
        cards.append(f'''<div class="sc"><div class="sch"><i>{stage}</i><b>{name}</b></div><p class="imp">{e(imp[n]["title"])}</p>
<dl><dt>Person</dt><dd>{e(p)}</dd><dt>Institution</dt><dd>{e(i)}</dd><dt>Society</dt><dd>{e(s)}</dd></dl>
<p class="start"><b>Start here</b> {e(rec[key])}</p></div>''')
    return f'''<div class="sec" id="cards"><div class="kick">x</div><h2>Your life, sector by sector</h2>
<p class="lede">Thirty sectors, in the order life meets them. For each: the real need underneath, what seeing the pattern gives a person, an institution and a society, and one place to start.</p>
<p>This is where the map turns from diagnosis into help. The three lines on each card are three different kinds of help. A person gets <strong>recognition</strong>. An institution gets a <strong>design test</strong> it can run on itself. A society gets <strong>a shared language and something better to measure</strong>. "Start here" is the reclamation practice from my war map, in my words.</p>
<div class="life"><span>Birth</span><span>Childhood</span><span>Youth</span><span>Adulthood</span><span>The end</span></div>
<div class="cards">{"".join(cards)}</div>
<p class="small">Read down your own column. Most people find five or six sectors that have touched them directly. The original impulse for each is defined in full in Section 14.</p></div>'''

# ---------------------------------------------------------------- 16. machines feed machines (school)
def machines(intro11, connect):
    pass
    return f'''<div class="sec" id="mach"><div class="kick">x</div><h2>Five machines, one school</h2>
<p class="lede">You've now met all five. They all happen inside the same building. I chose a school because that's where most of us met our first machine, before we had the language to see it.</p>
<p>The first three are from my Education scripts. The last two are composites I wrote for the people who work in schools, because the pattern runs through their hands, and on them too. Every scene is a composite. Yours may differ.</p>
<p>When I put them side by side, I saw that <strong>the machines feed each other.</strong> Each one hands its output to the next.</p>{connect}
<div class="box"><h4>Slow it down, and bring someone in</h4><p>Every chain breaker in these five restores one of two things: <strong>time</strong> (a pause, a written record, a delay before signing) or <strong>a witness</strong> (someone outside the system who can see what you can't). Look back at the breakers in each interlude. "Separate the pain from the meaning" buys time. "Ask someone outside the system" brings a witness. "Meet the child before the file" does both.</p></div>
<div class="box plain"><h4>What separates harm reduction from content about harm</h4><p>The quiet parts. Each full combination also has a <em>false-positive check</em> (the innocent explanations, taken seriously), <em>evidence to keep</em>, <em>escalation levels</em> ending at "safety first, do not confront," and <em>safer wording</em>. Those parts protect a reader from accusing someone wrongly, stop the map becoming a weapon, and are what a clinician or lawyer will look for first. Popular content about manipulation almost never has them.</p></div>
<h3>What the first sector's data shows</h3>
<p>I checked two of my own claims against the 153 Entertainment combinations instead of asserting them.</p>
<figure class="fig"><div class="bars"><div class="l">Accountability Evasion</div><div><div class="b me" style="width:100%"></div></div><div class="v">26</div><div class="l">Conditioning &amp; Behavioral Shaping</div><div><div class="b me" style="width:92%"></div></div><div class="v">24</div><div class="l">Exit Prevention &amp; Entrapment</div><div><div class="b me" style="width:65%"></div></div><div class="v">17</div><div class="l">Social Warfare</div><div><div class="b me" style="width:65%"></div></div><div class="v">17</div><div class="l">Capture &amp; Attachment</div><div><div class="b me" style="width:50%"></div></div><div class="v">13</div><div class="l">Institutional &amp; Systemic</div><div><div class="b me" style="width:50%"></div></div><div class="v">13</div><div class="l">Specialized Exploitation</div><div><div class="b me" style="width:50%"></div></div><div class="v">13</div><div class="l">Reality Distortion &amp; Perception Control</div><div><div class="b me" style="width:38%"></div></div><div class="v">10</div><div class="l">Digital &amp; Technological</div><div><div class="b me" style="width:38%"></div></div><div class="v">10</div><div class="l">Identity &amp; Psychological Destruction</div><div><div class="b me" style="width:38%"></div></div><div class="v">10</div></div><figcaption>Combinations per family, Entertainment &amp; Music (153). All ten families appear. The Corporate sector (138) is not in the repository yet, so I can't yet show whether the same mix holds there.</figcaption></figure>
<p><strong>The turning point.</strong> Each combination names its key conversion point. In a sample of ten, seven turned at the moment the person starts running the machine on themselves: the artist who posts the inflated number, the singer who says "I'll do another" without being asked. In the other three the turn was a move by the other side ("you've already signed"). So the honest claim is: most combinations turn when the target takes over the work. That's the moment to watch for.</p></div>'''

# ---------------------------------------------------------------- 18. war map, restored in the owner's words
def war_map_plus(chunk):
    def sect(title):
        a = WAR.index(title); b = WAR.find("\n### ", a + 5); c = WAR.find("\n## ", a + 5)
        b = min(x for x in (b, c, len(WAR)) if x > 0)
        return WAR[a:b]
    def md(t):
        t = re.sub(r"^### (.+)$", r"<h4>\1</h4>", t, flags=re.M)
        t = re.sub(r"^\*\*(.+)\*\*$", r"<p><b>\1</b></p>", t, flags=re.M)
        t = re.sub(r"^- (.+)$", r"<li>\1</li>", t, flags=re.M)
        t = re.sub(r"(<li>.*?</li>\n?)+", lambda m: "<ul>" + m.group(0) + "</ul>", t, flags=re.S)
        rows = []
        def tab(m):
            L = [r.strip().strip("|").split("|") for r in m.group(0).strip().split("\n") if not re.match(r"^\|[-| ]+\|$", r.strip())]
            return "<table class='small'><tr>" + "".join(f"<th>{c.strip()}</th>" for c in L[0]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c.strip()}</td>" for c in r) + "</tr>" for r in L[1:]) + "</table>"
        t = re.sub(r"(^\|.*\|$\n?)+", tab, t, flags=re.M)
        t = re.sub(r"^(?!<)(.+)$", r"<p>\1</p>", t, flags=re.M)
        return t
    f2 = WAR[WAR.index("## FRONT 2"):WAR.index("## FRONT 3")]
    f2 = f2.split("\n", 2)[2]
    keep3 = "".join(md(sect(t)) for t in ["### 1. Change the Metrics", "### 3. Change the Narratives", "### 4. Restore the Commons", "### 5. Build Intergenerational Memory", "### 6. Practice the Unmonetizable"])
    child = md(sect("### 4. Protect the Children"))
    f1 = md(sect("### 1. Learn to Detect the Cycle in Real Time")) + md(WAR[WAR.index("### 2. Build Technique Immunity"):WAR.index("### 3. Reclaim the Original Impulse")])
    return add(chunk, f'''<h3>The war map, in full, in my words</h3>
<p class="small">The summary above is the shape. Here is the detail I wrote for the series. The laws list sits in R4, labelled as one possible program; the map doesn't depend on it.</p>
<div class="wm"><h3>Front 1 · The inner war</h3>{f1}{child}<h3>Front 2 · The building war</h3>{md(f2)}<h3>Front 3 · The civilizational war</h3>{keep3}</div>''')

# ---------------------------------------------------------------- 20. who this is for
def need():
    rows = [("People psychologically abused by a partner", "61 million women · 53 million men", "United States, lifetime, CDC. About half of all adults. Nearly as many men, with far less written for them."),
            ("Women subjected to partner or sexual violence", "840 million", "Worldwide, lifetime, WHO (November 2025). Nearly one in three, barely changed since 2000."),
            ("Workers bullied at work", "about 32% · 74.8 million", "United States, 2024 Workplace Bullying Institute survey. An advocacy group's poll: indicative."),
            ("People in forced labour", "27.6 million", "Worldwide, ILO, 2021. One in five in private forced labour is held by a debt."),
            ("Losses to online fraud", "$16.6 billion", "United States, reported to the FBI in 2024. The largest category, investment fraud, runs on staged trust: a sequence."),
            ("Survivors who stayed longer because of money", "73%", "2025 study with the US National Domestic Violence Hotline.")]
    tr = "".join(f"<tr><td><b>{a}</b></td><td class='big'>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f'''<div class="sec" id="need"><div class="kick">x</div><h2>Who this is for, in numbers</h2>
<p class="lede">These are different harms, counted different ways. Don't add them together. My claim is only that the same small set of moves runs through all of them, so one literacy serves every row.</p>
<table class="need"><tr><th>Who</th><th>How many</th><th>Source and caution</th></tr>{tr}</table>
<p class="small"><span class="tag f">Documented</span>Figures and cautions as compiled in the Value-and-Impact report; sources listed there.</p>
<h3>Three groups the numbers leave out</h3>
<div class="three"><div><b>The person beside them</b><p>A parent, friend or teammate. Isolation is a stage of the cycle, so the last person still in contact is often the only way in. They need different words from the person inside.</p></div>
<div><b>The professionals</b><p>Therapists, school psychologists, advocates, teachers, chaplains, union reps. Each meets dozens or hundreds of people a year at the moment of need. One of them using the map multiplies it.</p></div>
<div><b>The carriers</b><p>If the cycle runs without a villain, most people running it don't know. Managers, parents, pastors, clinicians who'd stop if they could see it. This may be the biggest audience of all.</p></div></div></div>'''

# ---------------------------------------------------------------- 21. mechanisms + evidence
def mechanisms():
    M = [("Naming moves the blame", "Turns \"it must be me\" into \"this has a name, and it was done in an order\"", "Once \"sexual harassment\" and \"coercive control\" were named, each became speakable, then reportable, then illegal", 3, "Strong, historical"),
         ("Naming calms the body", "The cut to the name after each scene", "Putting a feeling into words lowered activity in the brain's alarm centre in a 2007 UCLA study of 30 adults; the authors called it tentative", 1, "Suggestive"),
         ("Learning the technique protects against its next use", "Teaches the move, not the particular lie", "Seven Cambridge and Bristol studies; a 90-second video shown to 5.4 million YouTube users raised recognition of manipulation techniques by about 5% a day later. It fades and needs refreshing", 3, "Strong for recognition"),
         ("Local detail matters", "Every example sits inside the reader's own sector", "The same videos worked in Poland and did almost nothing in Slovakia, where they were dubbed rather than made for that audience", 2, "Moderate"),
         ("The order creates the bond", "\"Why this order\" in every combination", "In 75 women who had left abusive partners, the power gap and alternating good and bad treatment explained more than half the variation in how attached they still felt", 2, "Moderate"),
         ("A sequence can be predicted, so tested", "The reader can see the next step coming", "Reasoned from how security defence works. Nobody has tested it for coercion between people", 1, "Reasoned, untested"),
         ("A plan lowers risk", "Evidence to keep, escalation levels, safer wording, \"do not confront\"", "Standard practice among advocates. Not yet tested in this form", 1, "Reasoned")]
    def meter(k): return '<span class="meter">' + "".join(f'<i class="{"on" if j < k else ""}"></i>' for j in range(3)) + "</span>"
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{meter(k)}<br><span class='strength'>{s}</span></td></tr>" for a, b, c, k, s in M)
    return f'''<div class="sec" id="mech"><div class="kick">x</div><h2>How it helps, and how sure I can be</h2>
<p class="lede">I believe this work helps people. This is how I think it does, and how strong the evidence is for each piece. Some of it is strong. Some of it is my reasoning.</p>
<table class="mech"><tr><th>How it helps</th><th>What the work does</th><th>What is known</th><th>Evidence</th></tr>{tr}</table>
<div class="box"><h4>The most valuable unknown</h4><p>Nobody has yet measured whether reading this work changes what happens to a person. Every row above is evidence that it should. None is evidence that it does. That question can be answered cheaply, and the answer is worth more than any praise. It's one of the things I'm asking for help with.</p></div>
<p>The research also limits my favourite phrase, "a trick explained stops working." The honest version: <strong>a named trick is harder to run, and knowing is the closest thing to immunity.</strong> Recognition fades without reminders. That's what a reference work is for. Every return visit is a booster.</p></div>'''

# ---------------------------------------------------------------- 22. precedents
def precedents():
    T = [("1957", "Biderman's Chart of Coercion", "One sociologist. A one-page table of eight methods.", "Amnesty called it the \"universal tools of torture and coercion.\" Later used to explain domestic abuse."),
         ("1970", "Our Bodies, Ourselves", "Twelve women in Boston. A 75-cent stapled booklet.", "More than 4.5 million copies in 34 languages."),
         ("1973", "Where There Is No Doctor", "David Werner, with villagers in western Mexico.", "Over 5 million copies, 85+ languages, free to download."),
         ("mid-1970s", "\"Sexual harassment\"", "Women in Ithaca, New York, comparing stories. Two words.", "Recognised in US law within about a decade."),
         ("1977", "A Pattern Language", "Christopher Alexander and colleagues. 253 linked patterns.", "Changed architecture, then software design."),
         ("1982–84", "The Power and Control Wheel", "Three advocates in Duluth and groups of women survivors. Redrawn until the women said it matched their lives.", "One page. 40+ languages. Used in shelters and courts worldwide."),
         ("2007", "Coercive Control", "Evan Stark. One book, one concept.", "A crime in England and Wales eight years later, then Scotland, Ireland and two Australian states."),
         ("2013", "ATT&amp;CK", "A small team at MITRE. A free catalogue of attacker behaviour.", "The shared language of a whole profession.")]
    tl = "".join(f'<div class="tl"><i>{y}</i><b>{n}</b><p>{w}</p><p class="out">{o}</p></div>' for y, n, w, o in T)
    return f'''<div class="sec" id="prec"><div class="kick">x</div><h2>This is how work like this has always started</h2>
<p class="lede">One person, or a small group, making a map and giving it away. That is the normal origin of this kind of work.</p>
<div class="timeline">{tl}</div>
<h3>Six things they had in common</h3>
<ol class="disc"><li><strong>They came from lived experience.</strong> Their authority came from fit: the people described looked at the map and said "yes, that's it." Scholarship came later.</li>
<li><strong>They were free or nearly free.</strong> Nothing that reached this scale sat behind a price.</li>
<li><strong>Each had a short form.</strong> One page, one wheel, two words. The long version earned the authority. The short version travelled.</li>
<li><strong>They named behaviour, never people.</strong> That's what let institutions adopt them without being sued or shamed first.</li>
<li><strong>They were checked and revised, in public,</strong> by the people they described.</li>
<li><strong>They spread through people at the moment of need:</strong> shelter workers, village health workers, analysts. Not fame.</li></ol>
<div class="ab"><div><h4>Where my work is ahead</h4><p>Scope. Sequences as well as single tactics. Three scales. Thirty sectors. The inner life and the family line. A practice for every technique.</p></div>
<div><h4>Where it is behind</h4><p>Lessons 3, 5 and 6. There's no one-page form in circulation. Nobody outside has checked it. No organisation is using it yet.</p><p><strong>Those three gaps are exactly where I need help.</strong></p></div></div></div>'''

# ---------------------------------------------------------------- 23. horizon + sixteen ways
def horizon_plus(chunk):
    G = [("Reach people earlier", [("Before, not only after", "Before you enrol, borrow, join, sign or move in. The readers who gain most are sixteen to twenty-five."),
                                   ("The person beside them", "A path for the friend or parent: what to say, what never to say, how to stay the one contact that isn't cut."),
                                   ("Men and boys", "Nearly as many men report psychological abuse by a partner, and very little is written in a voice they recognise.")]),
         ("Reach the people who carry it", [("\"Am I doing this?\"", "A page for the manager, parent, pastor or teacher who recognises their own behaviour and doesn't want to pass it on."),
                                            ("A self-check for organisations", "A school, clinic or church runs its own policy against the map. The self-audit in R1 is the first version.")]),
         ("Put it in hands at the moment of need", [("One page", "The eight rings holding every tactic, as a poster for a classroom, clinic or shelter. The main lesson of Duluth."),
                                                     ("Sheets for professionals", "One combination on one page for a therapist's or advocate's folder. Not legal advice; a shape for an account."),
                                                     ("Faith communities", "The spiritual lens opens doors secular material can't, including for people harmed inside a church.")]),
         ("Make it a commons", [("An open, citable dataset", "Stable identifiers, a licence, an archived copy. It outlives any one website or person."),
                                ("A counterexample register", "Publish the strongest objections and what changed because of them."),
                                ("\"Checked by\"", "People who work in each sector read their sector and say what's wrong. Published, with corrections."),
                                ("Measure it", "One optional question: \"Did this help you name something?\" Nothing stored about the person.")]),
         ("New ground", [("Fraud and persuasive technology", "Apps, feeds and AI companions run warmth, then unpredictable reward, then the cost of leaving. Regulators need a list to test products against."),
                         ("The same machine in another building", "The Debt Prison in music beside student loans, bail and medical debt. The fractal made visible."),
                         ("After the recognition", "A page for the hours after someone sees it: pacing, grounding, where to get help."),
                         ("Plain language, audio, translation", "The most trapped have the least time. Short spoken versions reach them. Spanish first.")])]
    k, out = 0, []
    for g, items in G:
        cs = []
        for t, d in items:
            k += 1
            cs.append(f'<div><i>{k}</i><b>{t}</b><p>{d}</p></div>')
        out.append(f'<h4>{g}</h4><div class="ways">{"".join(cs)}</div>')
    return add(chunk, f'''<h3>Sixteen ways this could help that nobody has named yet</h3>
<p>Some of these already exist in a first form. Number 5 is the self-audit in this document. The slides in R5 are a step toward number 6.</p>{"".join(out)}''')

# ---------------------------------------------------------------- 24. what these three works do (the expanded finale)
def worth():
    return '''<div class="sec" id="worth"><div class="kick">x</div><h2>What these three works do for people</h2>
<p class="lede">Everything above, gathered into one answer.</p>
<div class="worth"><div><b>To one person</b><p>A name for something they've carried without one. A reason to believe themselves. A way to see the next step before it lands. Words to say. A list of what to keep. A warning about when not to act alone. It costs nothing and asks for no sign-up. For someone inside a sequence, or about to sign into one, that can be the difference between years lost and years kept.</p></div>
<div><b>To the people who help</b><p>A shared vocabulary across fields. A school psychologist, an advocate and a union rep can each say "that's the Normalization Engine" and be understood. That hasn't existed before, and it's how separate efforts start working as one.</p></div>
<div><b>To a society</b><p>The cycle depends on three things a map can reach: <strong>namelessness</strong>, each person believing <strong>they're the only one</strong>, and <strong>deniability</strong>. A public map, with every sequence written down in advance, is witnessing at scale. The pattern keeps running. It gets more expensive to run everywhere the map has been read.</p></div></div>
<h3>Through the three levels</h3>
<table><tr><th></th><th>The Fractal (see)</th><th>Fractal² and the Decoder (name)</th><th>The combinations (break)</th><th>The Frequency (return)</th></tr>
<tr><td><b>A person</b></td><td>"It wasn't just me." The blame moves.</td><td>The exact name for the exact thing.</td><td>The next step, seen before it lands. The exit.</td><td>The pause. The need, met without the gate.</td></tr>
<tr><td><b>An institution</b></td><td>A mirror: where it runs the cycle without meaning to.</td><td>A checklist for contracts, welcomes, policies.</td><td>Where its machines hand off to each other, and where to cut.</td><td>A design standard: serve the need, don't gate it.</td></tr>
<tr><td><b>A society</b></td><td>A shared picture of one pattern across thirty buildings.</td><td>A common language, like "coercive control."</td><td>Laws and practices aimed at sequences, not single acts.</td><td>New measures: wellbeing, curiosity, security, repair.</td></tr></table>
<figure class="fig illus"><div class="ill"><div><b>100,000</b><span>readers of one sector in a year</span></div><div class="ar">→</div><div><b>1 in 50</b><span>recognise a sequence they're in or about to enter</span></div><div class="ar">→</div><div><b>2,000</b><span>people with a name, a self-check, a script and a safety note, at no cost</span></div></div>
<figcaption><strong>An illustration, not a forecast. The numbers are invented.</strong> The shape is real: the cost per person is zero, the harms are among the most common there are, and the map doesn't wear out. Thirty sectors and ten years turn that into hundreds of thousands. Then count the reader who is a therapist and passes it to forty clients a year.</figcaption></figure>
<p>That's what I mean when I say these works help people. Not that they fix the world. That they put words, warnings and a way out into the hands of people who never had them, and they keep doing it for free, for as long as anyone reads.</p>
<p>Now let me show you what I see when I imagine it landing.</p></div>'''

# ---------------------------------------------------------------- 26. ask additions
def ask_plus(chunk):
    extra = '''<p class="pull">You can see it now. That makes you one of the people this needs.</p>
<h3>Why it's free, and what it can't do</h3>
<p>The work is free for a structural reason as well as a generous one. A map of gatekeeping that sat behind a gate would contradict itself. It also passes its own test for a clean system: it's free, it shows its engineering, it says what else it could be, and it invites disagreement.</p>
<p>No map ends the cycle, and I won't tell you this one will. The record shows what a map <em>can</em> do. Two earlier names each became law in about a decade. A one-page wheel drawn by three advocates and a room of survivors reached shelters and courtrooms around the world. In each case, what ended was the method's ability to stay hidden. That was enough to change what people would tolerate.</p>
<p>The writing is largely done. What's left is less glamorous: checking it, shortening it, and putting it in the hands of people who meet others at the moment of need. That's a lifetime. I can't do it alone. <strong>Can you help me get eyes and minds on this?</strong></p>'''
    return add(chunk, extra, before=True)

# ---------------------------------------------------------------- 27. the levers, and the point
def v1_body(chunk):
    """An edition-1 section folded into another section: drop its kicker and title, keep everything else."""
    chunk = re.sub(r'<div class="kick">.*?</div>', "", chunk, count=1, flags=re.S)
    chunk = re.sub(r"<h2[^>]*>(.*?)</h2>", r"<h3>\1</h3>", chunk, count=1, flags=re.S)
    return '<div class="add">' + re.sub(r'^<div class="sec[^"]*"[^>]*>', "<div>", chunk) + "</div>"

def first_edition_note():
    return '''<div class="sec" id="fe"><div class="kick">From the first edition</div><h2>The first edition's tables, kept whole</h2>
<p class="lede">These are the tables from the first version of this document, unchanged, so nothing from it is lost.</p>
<p>Where a cell carries a dagger (†), the first edition filled it in for me, because my own wording for it wasn't in that draft. My own words for every one now appear in the body: the thirty original impulses with their full definitions and practices in Section 14, the thirty counter-practices in the war map in Section 18, and a reclamation practice for every sector on the cards in Section 15. Where they differ, the body is right.</p></div>'''

def levers(old23=""):
    L = [("Open loop", "The opening (\"what if I didn't tell you?\") and the question at the top of every movement. An unfinished question pulls you forward."),
         ("Narrative transportation", "Five full scenes in the second person. A story you're inside lowers counter-arguing."),
         ("Concrete before abstract", "The basketball coach before the theory. The body recognises first."),
         ("Self-reference", "\"You're seventeen.\" \"Read down your own column.\" Information about you is remembered better."),
         ("Two-sided message and early disclosure", "The limits and \"what I won't claim\" before the argument. Admitting weakness raises trust."),
         ("Authority by association", "Biderman, Freire, Herman, Stark, Fricker. Serious company makes a claim feel safer."),
         ("Social proof", "The maps that changed things. If others did it, it can be done."),
         ("Contrast", "Original against copy, garden against gate, on almost every page."),
         ("Repetition and the rule of three", "Three levels, three units, three moments, four verbs. Repeated structure feels true and is remembered."),
         ("Metaphor", "Notes and chords. Alphabet, dictionary, sentences. A frame decides what counts as evidence."),
         ("Prediction", "\"By the fifth sector you predict the next cell.\" Guessing right feels like your own discovery."),
         ("Identifiable victim", "Marcus, not \"students in special education.\" One face moves people more than a statistic."),
         ("Anchoring", "Big numbers early (2,700; 30,150; 840 million) set the scale for everything after."),
         ("Identity labelling", "\"You can see it now. That makes you one of the people this needs.\""),
         ("Peak-end", "The strongest scene and the hopeful picture placed near the end, so that's what you remember."),
         ("Foot in the door", "Small asks first: read one sector, try one worksheet, send it to one person."),
         ("Reciprocity", "Everything is given free before anything is asked.")]
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in L)
    return f'''<div class="sec" id="levers"><div class="kick">x</div><h2>You may have noticed</h2>
<p class="lede">If you're a psychologist, you probably caught some of these. I used them on purpose, all the way through.</p>
<table class="small lev"><tr><th>Lever</th><th>Where I used it on you</th></tr>{tr}</table>
<h3>What I did, and why I think it's fair</h3>{v1_body(old23).replace('<h3>How this document was built to persuade you</h3>', '')}
<p>I didn't use these to explain psychology to someone with far more formal training in it than me. I'd lose that contest.</p>
<p>I used them to make one point.</p>
<p class="pull">Most people who read this didn't spot the levers while they were working.</p>
<p>They're the same kind of levers. Story before argument. Warmth before the ask. A frame that decides what counts as evidence. Small steps that feel like your own choice. In this document they were used in the open, with the limits stated first, and with nothing to lose by saying no.</p>
<p>Now imagine them used in private. On a woman whose partner is running the cycle on her. The warmth came first. The future was painted next. The small reasonable requests came after that. Each step removed her defence against the next. She is intelligent and careful, and she doesn't see it, because nobody ever gave her the words or the map. The levers worked on her the same way they just worked on you, except nobody listed them at the end.</p>
<p>The levers can be identical. What separates persuasion from coercion is whether you can see them, and whether you're free to leave.</p>
<p><strong>That's why I wrote this.</strong> So that list exists for everyone, before they need it. Help me put it in front of them.</p></div>'''

# ---------------------------------------------------------------- reference additions
def lenses_plus(chunk):
    T = [("Christian", "Evil has no being of its own, only a corruption of good (Augustine, Aquinas). \"Our struggle is not against flesh and blood but against the powers.\" \"Satan disguises himself as an angel of light\": a counterfeit has to be precise.", "Very close"),
         ("Buddhist", "Māra comes in one disguise after another; each time he realises \"the Blessed One knows me\" and vanishes. Being recognised is the whole defeat. Correction: the Buddhist words are avidyā (not-seeing) and Māra; māyā is mainly Hindu.", "Very close"),
         ("Islamic", "Fitra, the sound nature every child is born with. \"The whisperer who withdraws\" retreats when remembered. Ghafla, heedlessness, is Normalization. Correction: fana is paired with baqa.", "Close"),
         ("Hindu", "The rope mistaken for a snake. Nobody kills the snake; it ends when the rope is seen. (Fits Advaita well; other schools differ.)", "Close"),
         ("Jewish", "In Luria's teaching, divine light is still present inside the broken shards: the original alive inside the corruption.", "Very close"),
         ("Indigenous", "Wétiko, an Algonquian word Jack Forbes used for exploitation as a contagious sickness of spirit. Caution: name the people a word comes from.", "Close, with care"),
         ("Gnostic", "The Secret Book of John speaks of a \"counterfeit spirit\" that binds people through forgetfulness.", "Close"),
         ("Taoist", "\"In the pursuit of learning, every day something is added. In the pursuit of the Way, every day something is dropped.\" Down, not up.", "Close"),
         ("No tradition", "Arrangements that capture a need tend to out-compete arrangements that serve it unless something stops them. Nobody has to choose that.", "Holds")]
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td class='n'>{c}</td></tr>" for a, b, c in T)
    return add(chunk, f'''<h3>Parallels I hadn't used</h3><p>Every tradition has a word for the covering and a word for what's under it. That's the claim I'll stand on. I won't say the destinations are the same; many believers reject that, and the traditions disagree about what's at the bottom.</p>
<table class="small"><tr><th>Tradition</th><th>What its own sources say</th><th>Fit</th></tr>{tr}</table>
<p class="small">That the pattern is literally a false god is a statement of my faith. It belongs inside this lens, marked as mine.</p>''')

def limits_plus(chunk):
    R = [("Unchecked content at scale", "About 400,000 words in one sector, not yet read by a working professional in that field", "Sector reviewers; a public corrections page; checking before a second sector"),
         ("A totalising reading", "\"It runs everywhere\" can slide into trusting nothing, or refusing care a person needs", "\"Seeing is not leaving.\" The same institution can serve and capture"),
         ("Use as a weapon or a manual", "Someone could use the names to accuse, or the sequences to plan", "The false-positive check; writing from the target's side. Practised manipulators already know their craft; their targets have had no curriculum"),
         ("Safety at the moment of recognition", "Confronting or leaving can be the most dangerous point", "Escalation levels and \"do not confront\"; a safety line near the top of every page"),
         ("Contested science stated as fact", "Inherited stress, nervous-system theory, the history in The Origin", "Worded as my belief"),
         ("One person", "The whole work depends on one author and one website", "A licence, an archive copy, and other people who check and carry it"),
         ("Its own size", "Thirty sectors at this depth is a library nobody reads end to end", "Entry points and short forms")]
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in R)
    return add(chunk, f'''<h3>What could hold it back, and what answers it</h3><table class="small"><tr><th>Risk</th><th>Why it matters</th><th>What answers it</th></tr>{tr}</table>
<p class="small">Two facts in the composites are still being sourced: the recommended school-psychologist ratio (about 1 to 500) and the referral disparity in The Paper Child. Treat both as approximate until cited.</p>''')

def laws():
    t = WAR[WAR.index("| Reform | What It Does |"):WAR.index("### 3. Change the Narratives")]
    L = [r.strip().strip("|").split("|") for r in t.strip().split("\n") if r.startswith("|") and not r.startswith("|---")]
    tr = "".join(f"<tr><td><b>{a.strip()}</b></td><td>{b.strip()}</td></tr>" for a, b in L[1:])
    return f'''<div class="sec" id="laws"><div class="kick">x</div><h2>The laws list from the war map</h2>
<p class="lede">One possible program. The map doesn't depend on it, and you can reject every line and still use everything else.</p>
<table class="small"><tr><th>Reform</th><th>What it does</th></tr>{tr}</table>
<p class="small">From Front 3 of my war map, as I wrote it for the series. Political judgments, not findings.</p></div>'''

def slides_plus(chunk):
    return add(chunk, '''<h3>The whole map</h3><figure class="fig full"><img src="../../art/fractal-original-1600.webp" alt="The Fractal: one pattern repeating across thirty sectors"><figcaption>The Fractal. One pattern, repeating at every scale, across all thirty sectors.</figcaption></figure>''')

# ---------------------------------------------------------------- 7b. The Origin and The Largest Body (steelman: never placed)
def origin_and_largest():
    return '''<div class="sec" id="oralb"><div class="kick">x</div><h2>Where it came from, and the largest body it runs on</h2>
<p class="lede">Two chapters of The Fractal widen the three levels in both directions: back in time, and out to the planet.</p>
<h3>The Origin: ten thousand years</h3>
<p>Halfway through the book, the reader has crossed thirteen sectors, and I wrote this for that moment:</p>
<div class="owner"><p>Something is running inside these buildings. The same something. In every building.</p></div>
<p>The Origin traces the cycle back through stored grain, writing, currency, law, armies, colonialism and industry, and argues that it is not human nature. In my words: "There was a time — a long time, a time that lasted hundreds of thousands of years longer than the time that has followed it — when the cycle was not the organizing principle of human life." The chapter treats the pattern as an organism, one that "does not require a host to understand it in order to host it." That is why it needs no villain.</p>
<p class="small"><span class="tag l">My belief</span>The road from surplus to hierarchy is argued well by some historians and disputed by others. I hold The Origin as a lens, not settled history.</p>
<h3>The Largest Body: the planet</h3>
<p>The last chapter before the frequency runs the same eight stages on the body that holds every other body. By then the reader has seen the cycle on their own body, through the institution, across the civilization, inside themselves, and down their family line. The Largest Body shows it at one more scale: extraction from the earth, sold back as scarcity. The three levels in this document are the working minimum. The book itself goes further: self, lineage, institution, civilization and the living earth.</p></div>'''
