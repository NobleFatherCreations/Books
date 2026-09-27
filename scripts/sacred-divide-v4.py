#!/usr/bin/env python3
"""Build The Sacred Divide v4 candidate from the live v3 file.

Input:  the live page, fetched with curl from https://noblefathercreations.com/faith
        (byte-identical to https://thenobledivide.netlify.app/ on 2026-09-27).
Output: library/_undeployed/sacred-divide-v4-candidate.html

Every data edit goes through the embedded window.CODEX_* JSON blobs, which
round-trip byte-exactly through json.loads/json.dumps(ensure_ascii=False).
Every replacement asserts it matched, so a stale input fails loudly.

Usage: python3 scripts/sacred-divide-v4.py <live.html> <out.html>
"""
import json, re, sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
BLOBS = ['CODEX_DATA', 'CODEX_V8', 'CODEX_V7', 'CODEX_V6', 'CODEX_V3', 'CODEX_V2']
log = []

def sub1(text, old, new, n=1, where='markup'):
    c = text.count(old)
    assert c == n, f'{where}: expected {n}x {old[:70]!r}, found {c}'
    log.append(f'{where}: {old[:60]!r} -> {new[:60]!r} ({n}x)')
    return text.replace(old, new)

# ---------- 1. markup / JS strings ----------
M = [
    ('<title>The Coercive Control Codex</title>', '<title>The Sacred Divide</title>', 1),
    ('navigation layer for the Coercive Control Codex.', 'navigation layer for The Sacred Divide.', 1),
    ("'From The Coercive Control Codex.", "'From The Sacred Divide.", 1),
    ('The Coercive Control Codex &middot;', 'The Sacred Divide &middot;', 3),
    ('<h1 class="display board-t">The Coercive Control Codex</h1>', '<h1 class="display board-t">The Sacred Divide</h1>', 1),
    ('<div class="mh-cap">The Coercive Control Codex</div>', '<div class="mh-cap">The Sacred Divide</div>', 1),
    ("document.title='Coercive Control Codex — '", "document.title='The Sacred Divide — '", 1),
    ('>The Coercive Control <span class="rule-word">Codex</span></a>', '>The Sacred <span class="rule-word">Divide</span></a>', 1),
    ('through twenty-five religious traditions.', 'through twenty-seven religious traditions.', 1),
    ('>Index of 25 traditions<', '>Index of 27 traditions<', 1),
    ('>The 25 × 30 matrix<', '>The 27 × 30 matrix<', 1),
    ('Twenty-five Tuesdays, one per tradition', 'Twenty-seven Tuesdays, one per tradition', 1),
    ('The Twenty-Five Traditions</h1>', 'The Twenty-Seven Traditions</h1>', 1),
    ('The twenty-five traditions &rarr;', 'The twenty-seven traditions &rarr;', 1),
    ('twenty-five defender attacks', 'twenty-seven defender attacks', 1),
    ('eleven accountability instruments.</p>', 'twelve accountability instruments.</p>', 1),
    ('Four readers, four different needs.', 'Six readers, six different needs.', 2),
]
# the analytics beacon contradicts the page's own "nothing is tracked" promise
BEACON = re.compile(r"<!-- Cloudflare Web Analytics -->.*?<!-- End Cloudflare Web Analytics -->", re.S)
assert len(BEACON.findall(s)) == 1
s = BEACON.sub('', s); log.append('markup: removed Cloudflare Web Analytics beacon')

# split out blobs so markup edits cannot touch data
parts, pos, spans = [], 0, {}
for n in BLOBS:
    i = s.index(f'window.{n} = ') + len(f'window.{n} = ')
    e = s.index('</script>', i)
    raw = s[i:e]; t = raw.rstrip().rstrip(';')
    assert json.dumps(json.loads(t), ensure_ascii=False) == t, n
    spans[n] = (i, e, json.loads(t), raw[len(t):])
order = sorted(spans, key=lambda n: spans[n][0])
chunks, prev = [], 0
for n in order:
    i, e, _, _ = spans[n]; chunks.append(s[prev:i]); chunks.append(n); prev = e
chunks.append(s[prev:])
markup = '\x00'.join(c for c in chunks if c not in BLOBS)
for old, new, n in M:
    markup = sub1(markup, old, new, n)
mk = markup.split('\x00')

D, V8, V7, V6, V3, V2 = (spans[n][2] for n in BLOBS)
REL = {r['id']: r for r in D['religions']}
IDX = {r['id']: str(k) for k, r in enumerate(D['religions'], 1)}
TAC = {t['name']: t for t in D['tactics']}

def rep(obj, key, old, new, where):
    assert old in obj[key], f'{where}: {old[:60]!r} not found'
    obj[key] = obj[key].replace(old, new); log.append(f'{where}: {old[:60]!r} -> {new[:60]!r}')

def setv(obj, key, old, new, where):
    assert obj[key] == old, f'{where}: unexpected {obj[key][:80]!r}'
    obj[key] = new; log.append(f'{where}: rewritten')

# ---------- 2. stale counts inside data ----------
rep(D['entry'], 'close', 'Twenty-five traditions.', 'Twenty-seven traditions.', 'entry.close')
rep(D['entry2'], 'howlong', 'Twenty-five traditions.', 'Twenty-seven traditions.', 'entry2.howlong')
rep(D['legal']['sections'][0], 1, 'across twenty-five religious traditions', 'across twenty-seven religious traditions', 'legal.0')
rep(V3['about']['roadmap'], 3, 'the twenty-five Tuesdays', 'the twenty-seven Tuesdays', 'about.roadmap')
rep(V3, 'antiweapon', 'all twenty-five traditions', 'all twenty-seven traditions', 'antiweapon')
rep(V3['asking']['rules'], 2, 'twenty-five offices', 'twenty-seven offices', 'asking.rules')
rep(V3['asking'], 'close', 'expands to all twenty-five,', 'expands to all twenty-seven,', 'asking.close')
walk0 = [st for st in D['walk']['steps'] if 'eleven accountability' in st.get('quiet', '')]
assert len(walk0) == 1
rep(walk0[0], 'quiet', 'eleven accountability instruments', 'twelve accountability instruments', 'walk.quiet')
g = json.dumps(V8, ensure_ascii=False)
assert g.count('Four readers, four needs') == 1 and g.count('four readers, four needs') == 1
V8 = json.loads(g.replace('Four readers, four needs', 'Six readers, six needs').replace('four readers, four needs', 'six readers, six needs'))
spans['CODEX_V8'] = spans['CODEX_V8'][:2] + (V8,) + spans['CODEX_V8'][3:]
log.append('V8 guide: four readers -> six readers (2x)')

# ---------- 3. leaked drafting notes ("your file ...") ----------
def intro(name, old, new):
    t = TAC[name]; i = [k for k, x in enumerate(t['intro']) if old in x]; assert len(i) == 1
    t['intro'][i[0]] = t['intro'][i[0]].replace(old, new).rstrip(); log.append(f'intro {name}: leak removed')
intro('WEAPONIZED GENEROSITY', ' Your file defines it as “giving help that installs unspoken obligation” where “the gift creates a debt you didn’t agree to”.',
      ' Put simply: help that installs an unspoken obligation — a gift that creates a debt you never agreed to.')
intro('FUTURE FAKING', ' Your file defines it as “promising a future that keeps you invested but never has to arrive”.',
      ' Put simply: a promised future that keeps you invested but never has to arrive.')
intro('HOOVERING', ' Your file defines it as “pulling someone back after they’ve started to leave through guilt, love, or fear”.', '')
intro('DEVALUATION', ' Your file defines this tactic as “reducing your sense of worth so you become dependent on the institution for identity”.', '')

def ex(name, rid, frag, new):
    xs = TAC[name]['entries'][IDX[rid]]['examples']; i = [k for k, x in enumerate(xs) if frag in x]
    assert len(i) == 1, (name, rid, frag); xs[i[0]] = new; log.append(f'{name}/{rid}: leak rewritten')
ex('WEAPONIZED GENEROSITY', 'scientology', 'The file describes',
   'The pattern begins with free or low-cost introductory auditing and courses, followed by steeply rising costs for advancement.')
ex('FUTURE FAKING', 'scientology', 'The file specifically names',
   'The promised future is built as a ladder — “Going Clear,” then the Operating Thetan levels — with always one more level to purchase.')
ex('HOOVERING', 'islam', 'your file notes',
   'In some contexts, apostasy is not only social but legally dangerous, which makes the “return” pressure far more than emotional.')
ex('HOOVERING', 'orthodox-hasidic-judaism', 'Your file specifically',
   'A common hoovering line: “You’re breaking the chain. Your ancestors died for this.”')
ex('HOOVERING', 'mormonism', 'your file lists',
   'The emotional hook is family eternity: “Your eternal family is at stake.”')
ex('HOOVERING', 'jehovahs-witnesses', 'Your file names',
   'When a Witness drifts, elders may visit, call, write letters, or request a shepherding call; family guilt and the line “Jehovah is waiting for your return” carry the rest.')
ex('DEVALUATION', 'christianity', 'The file’s example',
   'Christianity often begins by telling the person they are a sinner before God, sometimes this bluntly: “You are a sinner. The heart is deceitful. Without God you are nothing.”')
ex('DEVALUATION', 'protestant-evangelical', 'the file names',
   'Calvinist forms intensify this with total depravity: the teaching that “you cannot even choose good without God choosing you first” can function as devaluation.')
ex('DEVALUATION', 'islam', 'Your file gives',
   'Institutional Islam can devalue by emphasizing human weakness, forgetfulness, ingratitude, and need for divine guidance. Verses such as “man was created weak” (Qur’an 4:28) and “man is ungrateful to his Lord” (100:6) are scripture; the institutional move is to use them as a standing verdict on the believer rather than a call to humility.')
ex('DEVALUATION', 'hinduism', 'The file names caste',
   'Caste is the starkest institutional example: a person can be “born into a caste they can never leave,” with the condition explained as cosmic justice.')
ex('DEVALUATION', 'buddhism', 'The file gives',
   'Institutional Buddhism can devalue by defining ordinary desire as the root of suffering, in a form like: “You are trapped in samsara. Your desires are the disease.”')
ex('DEVALUATION', 'jehovahs-witnesses', 'your file explicitly',
   'Members are taught to distrust independent thinking; Watchtower literature has warned against “independent thinking” as a trait Satan promotes.')
ex('DEVALUATION', 'scientology', 'Your file gives',
   'The framing can be blunt: “You are a reactive mind. Your engrams control you. Without auditing, you are broken.”')

# Jainism normalization: four Taoism examples and pasted chat text were filed into it
jx = TAC['NORMALIZATION / DESENSITIZATION']['entries'][IDX['jainism']]['examples']
assert len(jx) == 13 and jx[9] == 'Got it' and 'qi' in jx[4]
del jx[4:]; log.append('NORMALIZATION/jainism: removed 4 misfiled Taoism examples + 5 lines of pasted chat')
g = TAC['LOVE BOMBING']['entries'][IDX['islam']]['counters']
rep(g, 0, 'as long as they becomes', 'as long as they become', 'LOVE BOMBING/islam grammar')

# ---------- 4. Islamic sections: corrections ----------
I, SU, SH = REL['islam'], REL['sunni-islam'], REL['shia-islam']
setv(I['timeline'][4], 1, 'Sufi orders, universities, vast waqf endowments', 'Sufi orders, madrasas, vast waqf endowments', 'islam.timeline 900–1500')
setv(I['demographics'], 'branches',
     I['demographics']['branches'],
     'Sunni (~85–90%), Shia (~10–13%, mostly Twelver, with Ismaili and Zaydi branches), plus Ibadi (Oman), Ahmadi (persecuted, and excluded by several states from the legal category of Muslim), Turkey’s Alevis, and Sufi orders crossing all of these lines.',
     'islam.branches')
rep(I['info'], 1, "[GOVERNMENT REPORT: e.g., Pakistan's blasphemy prosecutions]",
    "[OFFICIAL POLICY / COURT JUDGMENT: e.g., Pakistan Penal Code §295-C; the Supreme Court of Pakistan's 2018 acquittal of a Christian woman after eight years on death row]", 'islam.info')
setv(I['loopHere'], '1', I['loopHere']['1'],
     'Zakat and khums are fixed obligations, administered by boards and offices whose accounts a payer can rarely audit, funding the institutions that teach the obligation.', 'islam.loop1')
setv(I['language'][3], 'do', I['language'][3]['do'],
     'Where the state collects it, distribution is at official discretion, and published criteria rarely let a payer trace where their own zakat went.', 'islam.language zakat')
rep(I['whoPays'], 3, 'Ahmadis and other groups legally excluded from their own religious identity.',
    'Ahmadis — declared non-Muslim by Pakistan’s 1974 Second Amendment and criminalized for “posing as Muslims” by Ordinance XX (1984) — and other groups legally excluded from their own religious identity. [OFFICIAL POLICY]', 'islam.whoPays')
rep(I['differential'][3], 'how', 'Legally excluded from their own religious identity in some states',
    'Legally excluded from their own religious identity (Pakistan: Constitution, Second Amendment 1974; Ordinance XX 1984; Indonesia: 2008 joint ministerial decree restricting Ahmadi activity)', 'islam.differential ahmadi')
I['victories'] += [
    {'what': 'Morocco’s family code (Moudawana) reform: marriage age raised to 18, polygamy restricted, divorce opened to wives, the family placed under joint responsibility of both spouses',
     'who': 'Moroccan women’s movement, argued in Islamic legal terms, enacted by the monarchy', 'when': '2004', 'cost': 'Two decades of campaigning; judges still grant underage-marriage exemptions'},
    {'what': 'India’s Supreme Court strikes down instant triple talaq (Shayara Bano v. Union of India)', 'who': 'Muslim women petitioners and women’s groups', 'when': '2017', 'cost': 'Years of litigation and public opposition within their own communities'},
    {'what': 'Tunisia withdraws the 1973 ban on Muslim women marrying non-Muslim men', 'who': 'Tunisian civil society and the presidency', 'when': '2017', 'cost': 'Condemnation from religious establishments abroad'},
]
log.append('islam.victories: +3 (Morocco 2004, India 2017, Tunisia 2017)')
I['healthy'].append('Qur’an 2:256 — “there is no compulsion in religion” — is the tradition’s own standard, and it is the one this page measures the institutions against.')
log.append('islam.healthy: +1')

# Sunni
setv(SU['timeline'][1], 0, '700–850', '700–950', 'sunni.timeline schools date')
setv(SU['timeline'][1], 1, "Four legal schools crystallize (Hanafi, Maliki, Shafi'i, Hanbali)",
     "Four legal schools form around founders active c. 700–855 (Hanafi, Maliki, Shafi'i, Hanbali) and consolidate over the following century", 'sunni.timeline schools')
setv(SU['timeline'][2], 1, 'Hadith canon compiled; theology (kalam) debates; Sufi orders form',
     'Canonical hadith collections compiled (al-Bukhari, Muslim); theology (kalam) debates; Sufi mysticism spreads — organized Sufi orders (tariqas) follow in the 12th–13th centuries', 'sunni.timeline hadith/sufi')
rep(SU['genealogy'][2], 'origin', '[OFFICIAL POLICY]', '[ACADEMIC SOURCE]', 'sunni.genealogy wali receipt')
setv(SU['hardQuestions'], 3, SU['hardQuestions'][3],
     'Scholars across the schools condemn honor killing as murder. Yet until 2016 Pakistani law let a victim’s heirs pardon the killer — and when the killer is family, the heirs are the family. Why did closing that route take until 2016, and why does it still depend on a court classifying the killing as “honor”?', 'sunni.hardQuestions honor')
setv(SU['language'][2], 'do', SU['language'][2]['do'],
     'Correct, and many scholars say so plainly. The mechanism is legal, not doctrinal: where qisas-and-diyat law lets a victim’s heirs pardon a killer, a family that kills one of its own can also forgive itself. Pakistan narrowed this only in 2016.', 'sunni.language honor')
setv(SU['language'][2], 'receipt', '[PATTERN OBSERVED]',
     '[OFFICIAL POLICY: Criminal Law (Amendment) (Offences in the Name or Pretext of Honour) Act 2016, Pakistan]', 'sunni.language receipt')
rep(SU['demographics'], 'regions', 'Turkey, Morocco,', 'Turkey, Malaysia, Morocco,', 'sunni.regions')
SU['healthy'].append('Indonesia’s Nahdlatul Ulama and Muhammadiyah — mass-membership organizations with genuinely contested leadership elections, together representing well over a hundred million people — show that accountable Sunni institutions exist at scale.')
SU['roster'].append({'entity': 'Majelis Ulama Indonesia (MUI)', 'type': 'Semi-official scholarly council',
    'holder': 'Council leadership drawn from the major Islamic organizations, state-funded',
    'holds': 'Nationally influential fatwas — including a 2005 fatwa declaring Ahmadiyya outside Islam and ruling against pluralism and liberalism — and a continuing role in halal certification',
    'sector': 'Whether a minority mosque in your district is tolerated, and who certifies your food', 'receipt': '[OFFICIAL POLICY / ACADEMIC SOURCE]'})
SU['victories'].append({'what': 'Indonesia raises the minimum marriage age to 19 for both sexes', 'who': 'Child-marriage survivors whose petition won a 2018 Constitutional Court ruling',
    'when': '2019', 'cost': 'Religious courts’ dispensations for underage marriage rose sharply in the years that followed'})
log.append('sunni: +healthy (NU/Muhammadiyah), +roster (MUI), +victory (Indonesia 2019)')

# Shia
setv(SH['timeline'][2], 0, '874', '874–941', 'shia.timeline occultation date')
setv(SH['timeline'][2], 1, 'Occultation of the Twelfth Imam begins',
     'Minor Occultation: four named deputies act for the Twelfth Imam; from 941 the Major Occultation leaves no named deputy', 'shia.timeline occultation')
setv(SH['timeline'][2], 2, 'Authority passes to scholars as deputies — creating the clerical class that still governs.',
     'Over the following centuries jurists claim a general deputyship — the clerical class that still governs.', 'shia.timeline occultation reading')
setv(SH['timeline'][9], 1, 'Mass protests in Iran and Iraq against clerical governance, including by believers',
     'Mass protests — in Iran against clerical governance, including by believers; in Iraq (2019) against a sectarian political class and militia power, with Najaf backing the protesters’ right to demonstrate', 'shia.timeline protests')
setv(SH['money'], 0, SH['money'][0],
     'Khums: a 20% levy on annual surplus income. Half (sahm-e Imam) goes to the marjaʿ’s office as the Imam’s deputy; the other half (sahm-e sadat) is owed to needy descendants of the Prophet and is often routed through the same offices. No audited public accounting is required. [OFFICIAL POLICY: fiqh manuals]', 'shia.money khums')
rep(SH['children'], 0, 'in some contexts children participate in self-flagellation practices that senior clerics themselves have discouraged.',
    'in some contexts children participate in self-flagellation, including tatbir (blade cutting), which senior clerics themselves have prohibited or discouraged.', 'shia.children tatbir')
setv(SH['victories'][1], 'what', 'Senior clerical discouragement of self-flagellation practices involving children',
     'Rulings by senior clerics — including a 1994 fatwa by Ayatollah Khamenei and rulings by Grand Ayatollah Fadlallah — prohibiting or discouraging tatbir (blade self-cutting)', 'shia.victory tatbir')
setv(SH['victories'][1], 'when', '20th century onward', '1990s onward', 'shia.victory tatbir date')
rep(SH['differential'][4], 'how', 'offices that publish no accounts', 'offices that publish no audited accounts', 'shia.differential khums')
SH['cycle'][5]['shows'] = SH['cycle'][5]['shows'].replace('an office that publishes no ledger', 'an office that publishes no audited ledger'); log.append('shia.cycle extract: softened')
lang = V6['language']['per']['shia-islam']; k = [i for i, x in enumerate(lang) if x[0] == 'Khums']; assert len(k) == 1
setv(lang[k[0]], 2, 'A religious obligation with no published accounts anywhere in the system.',
     'A religious obligation with no audited public accounts required anywhere in the system. Where a marjaʿ’s network runs a registered charity abroad, that charity files accounts — proof the audit is possible.', 'V6 language khums')
rep(SH['demographics'], 'branches', 'Twelver (vast majority), Ismaili (including Nizari under the Aga Khan), Zaydi;',
    'Twelver (vast majority); Ismaili — Nizari under the Aga Khan, and Mustaʿli, chiefly the Dawoodi Bohras (~1 million) under the Daʿi al-Mutlaq; Zaydi (including the Houthi movement’s base in Yemen);', 'shia.branches')
SH['whoPays'].append('Shia minorities elsewhere — Hazara in Pakistan and Afghanistan, Shia citizens of Saudi Arabia’s Eastern Province and of Bahrain, where the state’s own 2011 Independent Commission of Inquiry documented torture and mass dismissals of protesters. [GOVERNMENT REPORT]')
SH['leverage'].append('In Lebanon, Hezbollah’s social network — schools, hospitals, and the Al-Qard Al-Hassan lending association, designated by the US Treasury in 2007 — delivers real services and binds communities to a party with an armed wing. [REGULATORY FILING: US Treasury designation]')
SH['roster'].append({'entity': 'Popular Mobilization Forces (Iraq)', 'type': 'State-funded armed network',
    'holder': 'A commission under the Iraqi prime minister; factions keep their own leaderships, several aligned with Iran',
    'holds': 'A state salary line created after Grand Ayatollah Sistani’s 2014 call to arms against ISIS and formalized in law in 2016; factions documented by UN and human-rights investigators committing abuses',
    'sector': 'Who holds guns in your city, and on whose religious call they first mobilized', 'receipt': '[GOVERNMENT REPORT: UN reporting; Iraqi PMF law 2016]'})
SH['differential'].append({'who': 'Girls in the Dawoodi Bohra community',
    'how': 'Khatna (female genital cutting), documented in criminal courts — the first US federal FGM prosecution (Detroit, 2017) and convictions reinstated by Australia’s High Court (2019)',
    'compounds': 'With social boycott available against families who refuse — a practice Maharashtra outlawed generally in 2016'})
log.append('shia: +whoPays (minorities/BICI), +leverage (Hezbollah/AQAH), +roster (PMF), +differential (Bohra khatna)')

# officeholder dates: the Saudi appointment month is not something this build can verify
for obj, key in ((V2['apex']['islam']['rows'][1], 1), (V2['apex']['sunni-islam']['rows'][1], 1)):
    obj[key] = obj[key].replace('in September 2025', 'in 2025').replace('since September 2025', 'since 2025')
log.append('V2 apex: Saudi Grand Mufti appointment month -> year only')

# ---------- 5. stray spaces before punctuation (stripped-citation residue) ----------
SP = re.compile(r'(\S) ([.,;:])(?=\s|$|[”"’)])')
nsp = 0
def clean(o):
    global nsp
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list): return [clean(v) for v in o]
    if isinstance(o, str) and not o.startswith('data:'):
        new, c = SP.subn(r'\1\2', o); nsp += c; return new
    return o
for n in BLOBS:
    i, e, d, tail = spans[n]; spans[n] = (i, e, clean(d if n != 'CODEX_V8' else V8), tail)
log.append(f'data: {nsp} stray spaces before punctuation removed')

# ---------- reassemble ----------
res, mi = [], 0
for c in chunks:
    if c in BLOBS: res.append(json.dumps(spans[c][2], ensure_ascii=False) + spans[c][3])
    else: res.append(mk[mi]); mi += 1
out_s = ''.join(res)
for bad in ('Coercive Control Codex', 'Coercive Control <span', 'Your file', 'your file', 'cloudflareinsights', 'Got it', '25-list'):
    assert bad not in out_s, bad
open(out, 'w', encoding='utf-8').write(out_s)
print('\n'.join(log)); print(f'wrote {out} ({len(out_s.encode())} bytes)')
