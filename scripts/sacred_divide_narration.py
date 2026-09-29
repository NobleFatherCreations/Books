"""The Sacred Divide — reader narration, shared by the expanded PDFs and the redesigned site.

Three layers for every religion page, none of them addressed to a named person:

  intro(rid, slug)    "Before you read" — what this section is built to show, in one short paragraph.
  foryou(rid, slug)   "Why this matters to you" — a caption placed AFTER the section. It points at the
                      part of the section that lands on an ordinary reader (a member, a donor, a parent,
                      someone thinking of leaving, a voter, an outsider forming an opinion) and asks them
                      something: a rhetorical question, a check on a bias, a fact they probably didn't know.
  questions(rid)      For section 23: each of the page's hard questions expanded into {why, example}.

Where a caption states a fact, the fact comes from the religion's own page (its glance table,
scorecard, regional cards, help table) — pulled here at build time, never retyped — or from one of
a handful of well-known, citable research findings named inline (e.g. Arkes & Blumer 1985 on sunk
cost). Hand-written text lives in content/sacred-divide/narration/<id>.md and overrides the
data-driven default for any section it covers; every question expansion is hand-written there.

File format (content/sacred-divide/narration/<id>.md):

    ## for-you money
    Paragraph(s)…

    ## intro structure          (optional; overrides the generic intro)
    Paragraph(s)…

    ## q1
    why: One paragraph.
    example: One paragraph.
"""
import os
import re
import sacred_divide_edits as EDITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'content/sacred-divide/religions')
NARR = os.path.join(ROOT, 'content/sacred-divide/narration')

INTRO_LABEL = 'Before you read'
FORYOU_LABEL = 'Why this matters to you'


# ---------------------------------------------------------------- facts pulled from the page itself
def _section(body, slug):
    m = re.search(r'^## \d+\. .+? \{#' + re.escape(slug) + r'\}\s*\n(.*?)(?=^## \d+\. |\Z)', body, re.S | re.M)
    return m.group(1) if m else ''


def _clean(t):
    t = re.sub(r'\[(?:[A-Z][A-Z /]+)(?::[^\]]*)?\]', '', t)          # receipts
    t = re.sub(r'\s*\[\d+\](?:\[\d+\])*', '', t)                      # numbered cites
    t = re.sub(r'\*\*?', '', t)
    return re.sub(r'\s+', ' ', t).strip().rstrip('.')


_FACTS = {}


def facts(rid):
    if rid in _FACTS:
        return _FACTS[rid]
    raw = open(os.path.join(SRC, f'{rid}.md'), encoding='utf-8').read()
    title = re.search(r'^title:\s*"?(.*?)"?\s*$', raw, re.M).group(1)
    g = _section(raw, 'at-a-glance')
    glance = {k: _clean(v) for k, v in re.findall(r'^\| ([^|]+?) \| (.*?) \|\s*$', g, re.M) if k.strip() not in ('', '---')}
    score = {}
    sm = re.search(r'^\| Accounts \| Pay \| Safeguarding \| External first \| Removal \| Reply \|\n\|[-| ]+\|\n(\|.*\|)', raw, re.M)
    if sm:
        cells = [c.strip() for c in sm.group(1).strip('|').split('|')]
        for k, c in zip(['Accounts', 'Pay', 'Safeguarding', 'External first', 'Removal', 'Reply'], cells):
            score[k] = c[:1] if c[:1] in 'YPN?' else '?'
    regions = [re.sub(r'\s*\{#.*', '', r) for r in re.findall(r'^### (.+)$', _section(raw, 'regional'), re.M)]
    help_orgs = re.findall(r'^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|', _section(raw, 'help'), re.M)
    cases = re.findall(r'^### (.+)$', _section(raw, 'cases'), re.M) or re.findall(r'^\d+\. \*\*(.+?)\*\*', _section(raw, 'cases'), re.M)
    fam = re.search(r'^family:\s*"?(.*?)"?\s*$', raw, re.M)
    f = {'title': title, 'glance': glance, 'score': score, 'regions': regions, 'help': help_orgs,
         'cases': [_clean(c) for c in cases], 'family': fam.group(1) if fam else ''}
    _FACTS[rid] = f
    return f


# ---------------------------------------------------------------- hand-written overrides
_OVR = {}


def overrides(rid):
    if rid in _OVR:
        return _OVR[rid]
    path = os.path.join(NARR, f'{rid}.md')
    o = {'for-you': {}, 'intro': {}, 'q': {}}
    if os.path.exists(path):
        text = open(path, encoding='utf-8').read()
        for head, body in re.findall(r'^## (.+?)\s*\n(.*?)(?=^## |\Z)', text, re.S | re.M):
            body = body.strip()
            kind, _, slug = head.partition(' ')
            if kind in ('for-you', 'intro'):
                o[kind][slug.strip()] = body
            elif re.fullmatch(r'q\d+', kind):
                why = re.search(r'^why:\s*(.*?)(?=^example:|\Z)', body, re.S | re.M)
                ex = re.search(r'^example:\s*(.*)', body, re.S | re.M)
                o['q'][int(kind[1:])] = {'why': why.group(1).strip() if why else '', 'example': ex.group(1).strip() if ex else ''}
    _OVR[rid] = o
    return o


# ---------------------------------------------------------------- "Before you read" — generic, unpersonalized
INTROS = {
    'at-a-glance': "The whole page on one screen: how big {name} is, who sits at the top, how that person is chosen and whether anyone can remove them, where the money comes from, and what leaving costs. The disclosure scorecard underneath asks six yes-or-no questions any charity or public company would be expected to answer. Every later section expands one of these rows.",
    'a-day-inside': "One ordinary day, told from inside. The person is a composite built from documented patterns, not a real individual. The point is to make the structure visible at human scale: phrases like \"removal mechanism\" or \"giving record\" are easy to read past, but a Tuesday organized around them is not.",
    'forefront': "The page's thesis in one place. First, the single question the documented record could not answer. Then the widest gap between what the institution says and what the record shows, one cost of leaving set beside how it is officially denied, and the strongest objection to this whole page, answered rather than dismissed.",
    'healthy': "What genuinely works in {name}, stated first and separately from any critique. That is a standing rule of this book: no tradition is reduced to its worst documented moments. Anything criticized later is measured against the best of what is described here.",
    'history': "A dated timeline and a few moments where the direction changed. Dates matter because they show that most rules had a beginning. A rule that began in a particular year, for a particular reason, is a rule that can be examined, and sometimes retired.",
    'branches': "{name} is not one bloc. This section maps the main branches and variants, so that nothing documented about one community is read as true of all of them.",
    'structure': "The organizational chart: how many people and institutions there are, where authority sits, who holds the top office, and who holds what beneath it. The question to keep in mind is simple: if the person at the top got something badly wrong, what written procedure exists to correct or remove them?",
    'law': "What states actually do. That includes how they fund, protect, regulate or enforce the tradition, and which outside body, if any, can compel an answer from it. For most readers, this is where the institution meets their own passport.",
    'money': "Where the money comes from, how each flow is justified, how it can be used to control, and who benefits. Read it the way you would read any organization you give to: what is disclosed, what is not, and who decides.",
    'genealogy': "Rules with a history. Each card asks the same three questions: what was this rule originally for, has that reason expired, and who benefits from the rule continuing anyway?",
    'reach': "How far the institution's authority extends into three private areas: what members may read and hear, how children are raised and schooled, and decisions about their own bodies.",
    'techniques': "A fixed checklist of thirty influence and control patterns from research on coercive control and social psychology, applied here to institutions rather than to individual people. Every entry carries an evidence grade. The grade matters more than the name of the technique: Codified or Documented means there is a paper trail; Contested means the claim is disputed.",
    'loops': "How the techniques connect into cycles. A single practice can look harmless on its own. The loops show how one step feeds the next, so that, for example, a newcomer's welcome turns into an obligation.",
    'say-do': "Direct, checkable comparisons: a public statement on one side, the documented record on the other, and the receipt that links them. This is the most falsifiable section on the page, because each row either matches its source or it doesn't.",
    'cost': "What leaving actually costs here, in family, work, housing, money and legal status, and how each of those costs is officially denied. Where the cost is low, the page says so plainly.",
    'ledger': "The balance sheet. It shows who benefits, who pays, and what leverage flows back to the institution in return for what it gives.",
    'who-gets-hurt': "Where the weight lands hardest, and what it compounds with: poverty, childhood, gender, a lack of civil alternatives. This is the human stakes stated plainly.",
    'tiers': "The people in the middle: local clergy, teachers, officials and volunteers who apply rules they did not write. The section exists so that an institution is not collapsed into a monolith, and so that people in the middle can see their own position in it.",
    'cases': "Named, dated, sourced incidents: court records, government inquiries, regulators' findings and on-the-record reporting. Read the outcome lines in particular. They show what actually changed, if anything.",
    'precedent': "What has already been broken once, somewhere, and what would count as real change here. It is a benchmark, not a prediction.",
    'voices': "People from inside {name} who raised the hard question publicly, often at real cost. They answer the objection that criticism only ever comes from outsiders.",
    'regional': "The same tradition under different governments. What a member can say, leave, marry or inherit depends heavily on the state, and these cards show how differently it plays out.",
    'questions': "The six questions the documented record could not resolve. Each is expanded below: why it is being asked, and a concrete example already on this page that it points back to.",
    'leaving': "Practical, non-theological guidance for someone who needs to step back or step away safely. It is a safety document, not an argument.",
    'help': "Organizations that can help, each checked directly against its own site, with the date of the check. Nothing here is endorsed beyond that check.",
    'sources': "Every numbered citation on this page, with a named, checkable source. Spot-check a few before trusting the rest; that is the honest way to read any page in this book, including this one.",
    'changed': "A dated log of corrections to this page. Mistakes are logged publicly rather than quietly edited away.",
}

SCORE_WORDS = {
    'Accounts': ('publishes accounts anyone can read', 'accounts'),
    'Pay': ('publishes what its leaders are paid', 'leaders\' pay'),
    'Safeguarding': ('has a public safeguarding policy', 'a public safeguarding policy'),
    'External first': ('sends abuse allegations to outside authorities first', 'allegations going to police first'),
    'Removal': ('has a written way to remove its top leader', 'a written removal procedure'),
    'Reply': ('answers questions on the record', 'on-the-record replies'),
}


def _score_sentence(sc):
    if not sc or all(v == '?' for v in sc.values()):
        return ''
    no = [SCORE_WORDS[k][1] for k, v in sc.items() if v == 'N']
    yes = [SCORE_WORDS[k][1] for k, v in sc.items() if v == 'Y']
    s = ''
    if no:
        s += f"The scorecard finds no public evidence of {_join(no)}."
    if yes:
        s += (" It does find " if no else "The scorecard finds ") + f"{_join_and(yes)}, and that deserves credit."
    return s.strip()


def _join(xs):
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' or ' + xs[-1] if xs else ''


def _join_and(xs):
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1] if xs else ''


# ---------------------------------------------------------------- "Why this matters to you" — data-driven defaults
def _default_foryou(rid, slug):
    f = facts(rid)
    name, g, sc = f['title'], f['glance'], f['score']
    uq = g.get('The unanswered question', '')
    money = g.get('Money in one line', '')
    leave = g.get('Leaving in one line', '')
    chosen_raw = g.get('Chosen by / removable by', '')
    cb, _, rb = chosen_raw.partition(' / ')
    cb, rb = cb.strip().rstrip('.'), rb.strip().rstrip('.')
    # quote the table's own cells rather than re-parse them into a sentence: they are free text
    chosen = (f"answer to who chooses the top office is \"{cb}\", and to who can remove its holder, \"{rb}\"" if cb and rb and rb.strip('— ') else
              (f"answer to who chooses the top office is \"{cb}\"" if cb else ''))
    D = {
        'at-a-glance': (
            (f"There is no single office at the top here. The glance table's {chosen}. That can protect people from a distant hierarchy. It can also mean there is no one to appeal to when the people closest to you are wrong. If that happened to you, who would you go to?"
             if chosen and sc and all(v == '?' for v in sc.values()) else
             (f"The glance table's {chosen}. Read that as though it described the board of a pension fund holding your savings. Would you accept the arrangement there? " if chosen else
              "Read the top of this table as though it described a pension fund holding your savings: who runs it, and who could remove them? ")
             + (_score_sentence(sc) + (" Each \"No\" is something the institution could publish tomorrow. Ask yourself why it hasn't." if 'N' in sc.values() else "") if _score_sentence(sc) else
                "Where the scorecard cannot be filled in, that is itself the finding: there is no single office to ask."))),
        'a-day-inside': (
            "Did any moment in that day feel familiar: a cost nobody questions, a door nobody can see how to open? The section of this page that explains that moment is the one to read first. "
            "If nothing felt familiar, ask whether that's because it isn't your life, or because the patterns have become normal to you."),
        'forefront': (
            (f"Try answering the unanswered question yourself: *{uq}* " if uq else "Try answering the unanswered question above yourself. ")
            + "If you can't, who could, and would asking them be welcome? How an institution reacts to a fair question often tells you more than the answer does."),
        'healthy': (
            "A bias check before the critique. People tend to read criticism of their own group as an attack and criticism of other groups as simply true. Social psychologists call this in-group bias; it shows up even when the groups are assigned at random (Tajfel's \"minimal group\" experiments, 1971). "
            "If you belong here, did this section feel fair? If you don't, did anything in it surprise you? The surprise is a rough measure of what you had assumed."),
        'history': (
            "Pick one rule that shapes your week and look for it on the timeline. If it has a start date, it was decided by people at a particular moment, for reasons of that moment. "
            "Were you taught it as timeless? What would it mean for you if it turned out to be younger than your grandparents' grandparents?"),
        'branches': (
            f"If you know one community of {name}, you know one community. Most bad generalizations about a religion, and most unfair defenses of it, come from treating one branch as the whole. "
            "Which branch is the one you picture when you hear the name? Is that picture yours, or one you were given by news coverage or by the community itself?"),
        'structure': (
            (f"This page's {chosen}. " if chosen else "The practical question for you is who chooses the top office, and who could remove its holder. ")
            + "If the person at the top made a serious mistake that affected your family, where exactly would you take the complaint, and who has the power to act on it? If the answer is \"nobody\", then the rest of this page is about what happens in that gap."),
        'law': (
            "Your rights inside this tradition depend partly on which passport you hold. The same question, whether you can leave, marry or speak freely, gets different answers in different states. "
            "Find your country in this section. Who, in your country, can compel this institution to answer a question it would rather not?"),
        'money': (
            (f"In one line: {money}. " if money else "")
            + (_score_sentence(sc) + " " if _score_sentence(sc) else "")
            + "If you give, you are funding this structure. Ask one question before your next gift: could you, as a donor, read where last year's money went? A charity that must file public accounts would have to show you. Does this one?"),
        'genealogy': (
            "The expired-reason test works on any rule. Take one you follow or enforce, name what it was originally for, and ask whether that reason still exists. "
            "If it doesn't, and the rule survives anyway, the section's last question is the one that matters to you: who benefits from it continuing?"),
        'reach': (
            "If you are a parent, this is the section about your children: what they may read, what they are taught about their bodies, and who else has a say in their schooling. "
            "Ask what your child would need to do at sixteen to hear the strongest case against what they were taught. Would they be allowed? Would they know it existed?"),
        'techniques': (
            "Count grades, not names. A long list of Contested entries says something very different from a short list of Codified ones. "
            "A bias to watch for in yourself: people rate the same pressure as \"normal\" when their own group applies it and as \"manipulation\" when another group does. Before you judge an entry, try imagining it applied by a group you distrust. Does it look different?"),
        'loops': (
            "The loops explain why good people stay in arrangements they would never sign up for from scratch. The more you have already put in, the harder it is to walk away. Researchers call this the sunk-cost effect (Arkes & Blumer, 1985), and it works on time, money and relationships alike. "
            "Ask yourself: if you were starting today, knowing what you know, would you join?"),
        'say-do': (
            "Test one row yourself. Pick a \"they say\" line you have actually heard said in person, then read the receipt. "
            "If the record matches the statement, this page is wrong about that row, and you should tell us. If it doesn't, what does it mean that you had never seen the receipt?"),
        'cost': (
            (f"In one line: {leave}. " if leave else "")
            + "Even if you never intend to leave, the cost of leaving shapes everyone who stays, because it sets the price of disagreeing. "
            "If you have a brother, a daughter or a friend who doubts, this is what their doubt costs them. Who, in your community, would stand with them?"),
        'ledger': (
            "Find yourself in this table. Are you among those who benefit, those who pay, or both? Most readers are both. "
            "The question is whether the exchange was ever explained to you in these terms, and whether you would agree to it if it had been."),
        'who-gets-hurt': (
            "Read this table with a particular person in mind: a daughter, a son, a mother, a friend, or yourself as a child. "
            "Harm in institutions rarely lands evenly. It concentrates on whoever has the fewest alternatives. Who in your life has the fewest alternatives?"),
        'tiers': (
            "If you are a local leader, a teacher or a volunteer, this section is about you. It is not an accusation: most of the people who carry out a rule did not write it. "
            "But the middle tier is also where a rule is most often quietly softened, or quietly enforced. Which do you do, and what would happen to you if you chose differently?"),
        'cases': (
            (f"These are not hypotheticals. {len(f['cases'])} documented case{'s' if len(f['cases']) != 1 else ''} on this page carry a court, regulator or inquiry record. " if f['cases'] else
             "Cases are where \"it could never happen here\" meets a court record. ")
            + "The most common reaction to documented cases is \"that was them, not us.\" "
            "Before settling on that, read the outcome lines. Did anything change in the structure that allowed each case to happen, or did one person leave while the structure stayed?"),
        'precedent': (
            "Every change described here was once called impossible by someone inside the tradition. "
            "When you are told something \"can't change\", it is fair to ask: can't, or won't? And who decided?"),
        'voices': (
            "Were these people traitors, or the most loyal members their tradition had? Most were treated as the first at the time, and some are honored as the second now. "
            "If someone in your community raised one of these questions tomorrow, how would they be treated, and by you?"),
        'regional': (
            (f"This page covers {_join_and(f['regions'])}. " if f['regions'] else "")
            + "Your country changes what this tradition can do to you, and what you can do about it. "
            "If you live somewhere not listed, ask which of these cards your country most resembles. If you are a voter, note that each of these arrangements was chosen by a government."),
        'questions': (
            "Choose one question and ask it this month, out loud, to a real person who could answer it. Then write down what happened. "
            "Were you answered, redirected, or told that asking was the problem? Whichever it was, the response is information."),
        'leaving': (
            "Even if this section is not for you, it may be for someone you know. Most people who leave a high-demand community say that the first person who listened without trying to argue them back mattered more than anything else. "
            "Could that person be you?"),
        'help': (
            (f"Save one contact now, before anyone needs it: **{f['help'][0][0]}** ({f['help'][0][1].lower()}; {f['help'][0][2]}). " if f['help'] else "Save one contact now, before anyone needs it. ")
            + "People in crisis rarely have the energy to research options. Having a name ready is one of the most useful things you can do for someone else."),
        'sources': (
            "Don't take this page's word for anything either. People tend to believe a claim more the more often they have heard it, whether or not it is true; this is the \"illusory truth effect\" (Hasher, Goldstein & Toppino, 1977). "
            "Spot-check three citations at random. If any fails, tell us, and it will be corrected and logged."),
        'changed': (
            "This page keeps a public log of its own mistakes. "
            "Does the institution you belong to, give to, or were raised in keep one like it? If not, how would you know what it got wrong, and when?"),
    }
    return D.get(slug, '')


# ---------------------------------------------------------------- public API
def intro(rid, slug):
    o = overrides(rid)['intro']
    t = o[slug] if slug in o else INTROS.get(slug, '').replace('{name}', facts(rid)['title'])
    return EDITS.apply(t, rid, 'narration') if t else t


def foryou(rid, slug):
    o = overrides(rid)['for-you']
    t = o[slug] if slug in o else _default_foryou(rid, slug)
    return EDITS.apply(t, rid, 'narration') if t else t


def questions(rid):
    """{n: {'why', 'example'}} — hand-written; missing ones fall back to a pointer to the page."""
    return {n: {k: EDITS.apply(v, rid, 'narration') for k, v in q.items()} for n, q in overrides(rid)['q'].items()}


def coverage():
    rows = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md':
            continue
        rid = fn[:-3]
        o = overrides(rid)
        rows.append((rid, len(o['for-you']), len(o['q'])))
    return rows


if __name__ == '__main__':
    for rid, fy, q in coverage():
        print(f'{rid:26} hand-written for-you: {fy:2}  question expansions: {q}')
