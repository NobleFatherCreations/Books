#!/usr/bin/env python3
"""The Sacred Divide — apply fact-check pass 1 to the v4 candidate.

Input:  library/_undeployed/sacred-divide-v4-candidate.html  (output of sacred-divide-v4.py)
Output: library/_undeployed/sacred-divide-v4-factchecked.html

Every edit here comes from a "Corrections to apply in the next build" list in
content/sacred-divide/sources/*.md, where the claim, the finding and the source
are recorded. This script only applies them. Stage two of the same v4 round,
not a new version: v4 has never been deployed.

Edits are global, exact-count string replacements across every data blob;
the expected count makes a miss or a stray hit fail loudly. D.receiptIndex
(the Receipts page) quotes the profiles, so it is left out of the replacements
and instead refreshed from the edited profiles at the end
(scripts/sacred_divide_receipts.py). Paths use the notation of scripts/sacred_divide_paths.py.

Usage: python3 scripts/sacred-divide-factcheck.py <v4-candidate.html> <out.html>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sacred_divide_paths as P
import sacred_divide_receipts as RCPT

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
BLOBS = P.BLOBS
log = []
DRY = os.environ.get('FC_DRY') == '1'; MISS = []

spans = {}
for n in BLOBS:
    i = s.index(f'window.{n} = ') + len(f'window.{n} = ')
    e = s.index('</script>', i)
    raw = s[i:e]; t = raw.rstrip().rstrip(';')
    assert json.dumps(json.loads(t), ensure_ascii=False) == t, n
    spans[n] = [i, e, json.loads(t), raw[len(t):]]
B = {n: spans[n][2] for n in BLOBS}
D, V2, V3, V6, V7, V8 = (B[n] for n in ('CODEX_DATA', 'CODEX_V2', 'CODEX_V3', 'CODEX_V6', 'CODEX_V7', 'CODEX_V8'))


PINS = RCPT.pin(D)
RI_ORDER = list(D['receiptIndex'])

def _map(o, fn):
    if isinstance(o, dict): return {k: (v if k == 'receiptIndex' else _map(v, fn)) for k, v in o.items()}
    if isinstance(o, list): return [_map(v, fn) for v in o]
    if isinstance(o, str) and not o.startswith('data:'): return fn(o)
    return o

def G(old, new, n):
    """Replace `old` with `new` everywhere; exactly n occurrences must exist."""
    global B, D, V2, V3, V6, V7, V8
    found = [0]
    def count(t):
        found[0] += t.count(old); return t
    _map(B, count)
    if found[0] != n:
        msg = f'G: expected {n}x {old[:80]!r}, found {found[0]}'
        if DRY: print('MISMATCH', msg); MISS.append(msg)
        else: raise AssertionError(msg)
    B = {k: _map(v, lambda t: t.replace(old, new)) for k, v in B.items()}
    D, V2, V3, V6, V7, V8 = (B[k] for k in ('CODEX_DATA', 'CODEX_V2', 'CODEX_V3', 'CODEX_V6', 'CODEX_V7', 'CODEX_V8'))
    log.append(f'{n}x {old[:50]!r} -> {new[:50]!r}')

def SET(rid, path, new, old=None):
    """Set one value by path; `old`, when given, must be its current value."""
    o, k = P.ref(B, rid, path)
    if old is not None and o[k] != old:
        msg = f'SET {rid} {path}: unexpected {str(o[k])[:80]!r}'
        if DRY: print('MISMATCH', msg); MISS.append(msg)
        else: raise AssertionError(msg)
    o[k] = new; log.append(f'set {rid or ""} {path}')

def ADD(rid, path, item):
    """Append an item to the list at path."""
    o, k = P.ref(B, rid, path); o[k].append(item); log.append(f'append {rid or ""} {path}')


# ============ Islam (sources/islam.md) ============
SET('islam', 'apex.rows[0][2]', "Since 2012, elected by al-Azhar's Council of Senior Scholars and confirmed by presidential decree",
    old='Appointed under Egyptian state law')
SET('islam', 'apex.rows[0][3]', "Nobody — Egypt's 2014 Constitution makes the Grand Imam irremovable", old='The Egyptian state')
G("Sheikh Saleh al-Fawzan — appointed by royal decree in 2025 on the death of Abdulaziz Al ash-Sheikh (a fast-moving seat; verify)",
  "Sheikh Saleh al-Fawzan — appointed by royal order on 22 October 2025, a month after Abdulaziz Al ash-Sheikh died", 1)
G("it is the page.", "it is the page. al-Azhar is the partial exception: its independence was written into the constitution after 2011, and its budget is still a line in the state's.", 1)
G('[OFFICIAL POLICY: national penal codes; verify current list]',
  '[OFFICIAL POLICY: national penal codes — about ten states, per Humanists International]', 1)
G('[GOVERNMENT REPORT / INVESTIGATIVE REPORT — verify jurisdiction-specific cases]',
  '[GOVERNMENT REPORT: e.g., Karnataka State Minorities Commission, 2012, on waqf land]', 1)
G('~1.9–2 billion Muslims worldwide;', 'About 2 billion Muslims worldwide (Pew, 2020 data);', 1)
G('~1.9–2 billion; projected', 'About 2 billion (Pew, 2020 data); projected', 1)

# ============ Sunni Islam (sources/sunni-islam.md) ============
SET('sunni-islam', 'apex.rows[0][1]', 'Grand Imam Ahmed el-Tayeb, appointed by the president in 2010',
    old='Grand Imam Ahmed el-Tayeb, state-appointed, since 2010')
SET('sunni-islam', 'apex.rows[0][2]', 'The Council of Senior Scholars (since 2012)', old='The Egyptian state')
SET('sunni-islam', 'apex.rows[0][3]', 'Nobody — the 2014 Constitution makes the office irremovable', old='The Egyptian state')
SET('sunni-islam', 'apex.rows[2][1]', 'Safi Arpaguş, appointed by presidential decree in September 2025; the Diyanet drafts the Friday sermon read in some 90,000 mosques')
SET('sunni-islam', 'apex.tell', "Ask who accredits the scholars who decide who counts as a scholar. The trail ends at a ministry almost every time — al-Azhar, made irremovable by Egypt's 2014 constitution, is the partial exception, and its budget is still a state line.",
    old='Ask who accredits the scholars who decide who counts as a scholar. The trail ends at a ministry every time.')
G('~1.6–1.8 billion (roughly 85–90% of Muslims)', 'About 1.7–1.8 billion (roughly 87–90% of Muslims)', 1)
G('~85–90% of Muslims; authority', '~87–90% of Muslims; authority', 1)

# ============ Shia Islam (sources/shia-islam.md) ============
SET('shia-islam', 'apex.rows[0][1]', 'Ayatollah Mojtaba Khamenei, chosen in March 2026 after his father Ali Khamenei — Leader since 1989 — was killed in an air strike on 28 February 2026; constitutional authority over doctrine, courts, media, and the bonyad economies')
SET('shia-islam', 'apex.rows[0][3]', "In theory, that Assembly. In thirty-seven years and two Leaders, never — and it chose the late Leader's son",
    old='In theory, that Assembly. In thirty-six years, never')
G('~180–250 million (~10–13% of Muslims)', 'About 200–260 million (~10–13% of Muslims)', 1)
G("with Najaf backing the protesters’ right to demonstrate",
  "with Najaf backing the protesters’ right to demonstrate; in 2026 the founding generation’s Leader is killed in war and the Assembly of Experts chooses his son", 1)

# ============ Christianity (sources/christianity.md) ============
G('[INVESTIGATIVE REPORT — verify organizations and figures before publication]',
  '[INVESTIGATIVE REPORT: openDemocracy, 2020 — 28 US groups, at least $280m spent abroad, 2007–2018]', 1)
G('— unlike other charities —', '— unlike almost every other US charity —', 1)
G('— uniquely among American charities —', '— unlike almost every other American charity —', 1)  # receiptIndex keeps a truncated excerpt
G('Form 990 that every other nonprofit must file', 'Form 990 that other nonprofits must file', 1)
G('Form 990 public disclosure every other charity must file', 'Form 990 public disclosure almost every other charity must file', 1)
G('no obligation to file the public Form 990 every other charity files', 'no obligation to file the public Form 990 almost every other charity files', 1)
G('while uniquely exempt from the Form 990 disclosure every other charity files', 'while exempt from the Form 990 disclosure almost every other charity files', 1)
G('exempt from the financial disclosure that every other charity in the country must file', 'exempt from the financial disclosure that almost every other charity in the country must file', 1)
G('Catholic (~1.3B)', 'Catholic (~1.4B)', 1)
G('are now restricted in many jurisdictions. [GOVERNMENT REPORT / INVESTIGATIVE REPORT]',
  'are now restricted in many jurisdictions — though in the US the Supreme Court held in 2026 (Chiles v. Salazar) that bans on conversion talk therapy face strict First Amendment scrutiny. [GOVERNMENT REPORT / INVESTIGATIVE REPORT]', 1)
G('Sarah Mullally — confirmed January 2026,', 'Sarah Mullally — confirmed in January and installed in March 2026,', 1)

# ============ Catholicism (sources/catholicism.md) ============
RETRIAL = ' In March 2026 the Vatican’s appeals court found procedural errors and ordered a partial retrial, which began in June; the 2023 verdict stands until it ends.'
G("was the first trial of a cardinal by the Vatican's own criminal court. [COURT RECORD]",
  "was the first trial of a cardinal by the Vatican's own criminal court." + RETRIAL + ' [COURT RECORD]', 1)
G('Financial reform attempts; Cardinal Becciu convicted 2023', 'Financial reform attempts; Cardinal Becciu convicted 2023, partial retrial ordered 2026', 1)
G('Convicted by the Vatican\'s own criminal court in the London property affair',
  'Convicted by the Vatican\'s own criminal court in the London property affair (2023); a partial retrial was ordered on appeal in 2026', 1)
G("First conviction of a cardinal by the Vatican's own court. Demonstrates",
  "The first trial and conviction of a cardinal by the Vatican's own court — now being retried in part." + RETRIAL + ' Demonstrates', 1)
G("First criminal conviction of a cardinal by the Vatican's own court", "First criminal conviction of a cardinal by the Vatican's own court (now being retried in part)", 1)
G("[FINANCIAL RECORD: German Kirchensteuer, ~€6–7B/yr Catholic share; verify current figures]",
  "[FINANCIAL RECORD: German Bishops' Conference — €6.75bn in 2025]", 1)
G("[FINANCIAL RECORD: Kirchensteuer; verify current figures]", "[FINANCIAL RECORD: German Bishops' Conference — €6.75bn in 2025]", 1)
G('[FINANCIAL RECORD: Vatican financial statements, partially published since 2020]',
  '[FINANCIAL RECORD: Vatican financial statements, partially published since 2021]', 1)
G('Germany and Austria collect church tax through the state revenue system on behalf of registered religious bodies, generating billions annually.',
  'Germany collects church tax through the state revenue system on behalf of registered religious bodies, generating billions annually; Austria’s church contribution is collected by the churches themselves but enforced through the civil courts.', 1)
G("Germany and Austria collect church tax on the Church's behalf through the state revenue system — billions annually,",
  "Germany collects church tax on the Church's behalf through the state revenue system, and Austria enforces the churches' own contribution through its civil courts — billions annually,", 1)
SET('catholicism', 'regional[1].documented',
    "Independent documentary films — notably 'Tell No One' (2019), released two months after the bishops published their first abuse figures — reached tens of millions of viewers and did work no state inquiry had done.",
    old="Independent documentary films — notably 'Tell No One' (2019) — did work that no state inquiry had done, and prompted the church's own first partial disclosure of case numbers.")
G('(the Pennsylvania grand jury, 2018, and successors in roughly twenty states)',
  '(the Pennsylvania grand jury, 2018, and inquiries announced by attorneys general in at least fourteen states)', 1)
G('More than thirty US dioceses have filed for bankruptcy protection', 'Some forty US dioceses and religious orders have filed for bankruptcy protection', 1)
G('~1.3–1.4 billion baptized. [OFFICIAL POLICY: Vatican Annuarium Statisticum]', '~1.4 billion baptized (2023). [OFFICIAL POLICY: Vatican Annuarium Statisticum]', 1)
G('(~1.3–1.4 billion baptized members)', '(~1.4 billion baptized members)', 1)
G('a church of 1.3 billion does not notice', 'a church of 1.4 billion does not notice', 1)


# ============ Eastern Orthodoxy (sources/eastern-orthodoxy.md) ============
G('[INVESTIGATIVE REPORT: 1990s tobacco/alcohol import concessions; verify details before publication]',
  '[INVESTIGATIVE REPORT: duty-free tobacco and alcohol imports through the Department for External Church Relations, 1994–97]', 1)
G('[INVESTIGATIVE REPORT — verify specifics before publication]', '[INVESTIGATIVE REPORT: Moskovsky Komsomolets, 1997; OSW, 2012]', 1)
G('and has been personally sanctioned by several governments', 'and has been personally sanctioned by several governments; the EU renewed its attempt to sanction him in 2026', 1)

# ============ Protestant / Evangelical (sources/protestant-evangelical.md) ============
G('Report published in full including the list. A public database was established. The list had existed for years without being acted upon.',
  'The Executive Committee released its list of accused ministers. Messengers voted in 2022 for a public database; none was ever published, and in 2025 the Executive Committee shelved it, citing legal risk. The list had existed for years without being acted upon.', 1)
G("The SBC's Guidepost report published in full, list included, and a public database created",
  "The SBC's Guidepost report published in full, and the Executive Committee's list of accused ministers released", 1)
SET(None, 'V7.promises.rows[1][2]', 'Abandoned', old='Partial')
SET(None, 'V7.promises.rows[1][3]', 'Messengers voted for the "Ministry Check" database in 2022. No name was ever published; in February 2025 the Executive Committee said it was no longer a focus, citing legal hurdles. In 2026 survivors launched their own national database instead.')
G('[INVESTIGATIVE REPORT — verify organizations before publication]', '[INVESTIGATIVE REPORT: openDemocracy, 2020]', 1)
G('ACNC registration with published annual information statements.',
  'ACNC registration — though churches that qualify as "basic religious charities" are exempt from financial reporting.', 1)

# ============ Pentecostal / Charismatic (sources/pentecostal-charismatic.md) ============
G('Church of God in Christ Cleveland', 'Church of God (Cleveland, Tennessee)', 1)
G('is convicted of embezzlement involving church funds', 'is convicted of breach of trust involving church funds', 1)
G('for embezzlement in Seoul', 'for breach of trust in Seoul', 1)
G('the Seoul embezzlement conviction', 'the Seoul breach-of-trust conviction', 1)
G('an embezzlement conviction of a Seoul megachurch founder in 2014', 'a breach-of-trust conviction of a Seoul megachurch founder in 2014', 1)
G('Korean and Brazilian criminal courts', 'a Korean criminal court and Brazilian prosecutors', 1)
G('criminal courts in Seoul and São Paulo', 'a Korean criminal court and Brazilian prosecutors', 2)
G('Both have removal mechanisms and both have used them.',
  'Both hold real elections and revoke credentials — the Assemblies of God defrocked Jim Bakker in 1987 and Jimmy Swaggart in 1988.', 1)
G(" was fought hard by churches and its application curtailed.", " was fought hard by churches.", 1)
SET(None, 'V7.promises.rows[7][2]', 'Partial', old='Open')
SET(None, 'V7.promises.rows[7][3]', 'Two governance reviews by a former ACNC assistant commissioner, board term limits and a 40% women target, and compliance agreements with the ACNC in December 2024; the founder-era questions the reviews were asked to answer have not all been answered publicly.')

# ============ Judaism (sources/judaism.md) ============
SET('judaism', 'timeline[8][1]', "State of Israel; the Mandate's religious-court system continued, and in 1953 statute gave rabbinical courts exclusive jurisdiction over Jewish marriage and divorce",
    old='State of Israel; Chief Rabbinate given legal monopoly over personal status')
G('into Israeli statute in 1948. [OFFICIAL POLICY]', 'into Israeli statute in 1953. [OFFICIAL POLICY]', 1)
EXITS = " Israel's courts have opened three narrow exits: non-Orthodox conversions performed in Israel count for citizenship (2021), civil burial is a legal right (1996) though scarce, and online civil marriages must be registered (2023). Divorce has no exit."
G('In Israel, the Chief Rabbinate holds legal monopoly over Jewish marriage, divorce, conversion, and burial — state-enforced Orthodox gatekeeping over personal status for all Jewish citizens.',
  'In Israel, the Chief Rabbinate holds a legal monopoly over Jewish marriage and divorce, and gatekeeping over Orthodox conversion and most burial — state-enforced Orthodox control over personal status for all Jewish citizens.' + EXITS, 1)
G('Legal control of Jewish marriage, divorce, conversion, and burial for all Jewish citizens',
  'Legal control of Jewish marriage and divorce for all Jewish citizens, and gatekeeping over Orthodox conversion and most burial', 1)
G("Israel's Chief Rabbinate holds statutory monopoly over Jewish marriage, divorce, conversion, and burial.",
  "Israel's Chief Rabbinate holds a statutory monopoly over Jewish marriage and divorce, and gatekeeping over Orthodox conversion and most burial.", 1)
G('Chief Rabbinate of Israel — statutory monopoly over Jewish marriage, divorce, conversion, and burial in Israel',
  'Chief Rabbinate of Israel — statutory monopoly over Jewish marriage and divorce in Israel, and gatekeeping over Orthodox conversion and most burial', 1)
G('A secular or Reform Jew cannot legally marry in the country without Orthodox rabbinic authority.',
  'A secular or Reform Jew cannot legally marry in the country without Orthodox rabbinic authority — the one exit is a civil marriage conducted online from abroad, which the state must register (2023).', 1)
G('Rabbis have ruled internally that abuse reporting is not mesirah. [COURT RECORD]', 'Rabbis have ruled internally that abuse reporting is not mesirah. [LEADERSHIP STATEMENT]', 1)

# ============ Orthodox / Hasidic Judaism (sources/orthodox-hasidic-judaism.md) ============
SET('orthodox-hasidic-judaism', 'case weberman.outcome',
    "Conviction and a 103-year sentence, later cut to 50. Several prominent rabbis have since ruled that reporting abuse with a substantial basis is not mesirah — though Agudath Israel's rabbinical board still requires consulting a rabbi first — and in 2021–22 community leaders sought his clemency.",
    old='Conviction and lengthy sentence. Several prominent rabbis subsequently ruled that reporting abuse does not constitute mesirah; social enforcement continued regardless.')
G("The city's investigation found the overwhelming majority of examined yeshivas not providing substantially equivalent instruction.",
  "The city's investigation found 2 of 28 examined yeshivas meeting the standard (2019); its final 2023 determinations found 18 failing.", 1)
SET('orthodox-hasidic-judaism', 'victories[2].when', '2015–2023, and continuing at the state level', old='2015–present')

# ============ Hinduism (sources/hinduism.md) ============
RR = 'Gurmeet Ram Rahim Singh was convicted of rape in 2017; his two murder convictions were overturned on appeal in 2024 and 2026, the latter now before the Supreme Court. Asaram’s life sentence for raping a minor was upheld in 2026.'
G('Documented collapses (e.g., convictions of high-profile godmen for rape and murder — Ram Rahim [COURT RECORD], Asaram [COURT RECORD]) reveal internal economies of total control.',
  'Documented collapses reveal internal economies of total control: ' + RR + ' [COURT RECORD]', 1)
G('High-profile godman convictions (Ram Rahim 2017, Asaram 2018)', 'High-profile godman rape convictions (Ram Rahim 2017, Asaram 2018; upheld or pending on appeal)', 1)
G('Multiple godmen have been convicted of rape and murder while devotees insisted it was impossible.',
  'Multiple godmen have been convicted of rape while devotees insisted it was impossible.', 1)
G('Public convictions of leaders of major movements for rape and, in one case, murder conspiracy',
  'Public convictions of leaders of major movements for rape; murder convictions in one case were overturned on appeal (2024, 2026)', 1)
SET('hinduism', 'victories[0].what', 'Rape convictions of major godmen, upheld on appeal', old='Convictions of major godmen for rape and murder conspiracy')
SET('hinduism', 'victories[0].when', '2017–2026', old='2017–2019')
G('Convictions of high-profile godmen for rape and murder conspiracy, after sustained devotee denial.',
  'Rape convictions of high-profile godmen, after sustained devotee denial.', 1)
G('The convictions of Gurmeet Ram Rahim Singh and Asaram Bapu came from criminal courts',
  'The rape convictions of Gurmeet Ram Rahim Singh and Asaram Bapu came from criminal courts', 1)
G('criminal convictions of guru figures including Gurmeet Ram Rahim Singh and Asaram Bapu;',
  'rape convictions of guru figures including Gurmeet Ram Rahim Singh and Asaram Bapu;', 1)
G('was convicted of rape in 2017 and later of conspiracy to murder a journalist.',
  'was convicted of rape in 2017, and in 2019 of conspiring to murder a journalist — a conviction overturned on appeal in 2026 and now before the Supreme Court.', 1)
G('Demonstrates purity custom operating without doctrinal necessity.',
  'Demonstrates purity custom operating without doctrinal necessity. A nine-judge bench heard the wider questions in 2026 and has reserved judgment; the 2018 ruling stands meanwhile.', 1)
G('brought forced-labour and wage claims into court. UK charity filings',
  'brought forced-labour and wage claims into court. A federal criminal investigation closed without charges in 2025; the civil case continues. UK charity filings', 1)


# ============ Buddhism (sources/buddhism.md) ============
BUD = "about 324 million by Pew's 2020 count — the only major religion that shrank from 2010 to 2020; broader counts that include Chinese folk practice run near 500 million"
G('~500–520 million adherents across Theravada, Mahayana, and Vajrayana streams;',
  "About 324 million adherents by Pew's 2020 count (broader counts that include Chinese folk practice run near 500 million), across Theravada, Mahayana, and Vajrayana streams;", 1)
G('~500–520 million. [ACADEMIC SOURCE: Pew]', BUD[0].upper() + BUD[1:] + '. [ACADEMIC SOURCE: Pew, 2025]', 1)
G('Both were possible because the entities were registered charities with legal duties.',
  "Registration gave regulators a handle: the Charity Commission's statutory inquiry later found Rigpa UK's former trustees had failed to act on what they knew.", 1)
G('Charity Commission and ACNC — the reason those investigations happened at all; ordinary courts.',
  'Charity Commission and ACNC — the handle that made the findings enforceable; ordinary courts.', 1)

# ============ Tibetan Buddhism (sources/tibetan-buddhism.md) ============
SET('tibetan-buddhism', 'timeline[9][1]', 'Independent investigations find abuse by Sogyal Rinpoche (Rigpa, 2018) and sexual misconduct by Sakyong Mipham (Shambhala, 2019)',
    old='Independent investigations confirm abuse by Sogyal Rinpoche (Rigpa) and Sakyong Mipham (Shambhala)')
G('Charity regulators over Western dharma organizations — both landmark investigations became possible because the entities were registered charities with legal duties — and civil courts.',
  'Charity regulators over Western dharma organizations — registration is what gave the Charity Commission a statutory inquiry into Rigpa — and civil courts.', 1)
G('~10–20 million within the Tibetan cultural sphere,', 'Estimated ~10–20 million within the Tibetan cultural sphere,', 1)

# ============ Sikhism (sources/sikhism.md) ============
SET('sikhism', 'apex.rows[0][1]', 'Giani Kuldeep Singh Gargaj, acting Jathedar since March 2025 — installed by the SGPC after it removed two predecessors in the same year amid open political conflict')
SET(None, 'V3.compel.sikhism', "The SGPC's statutory elections — a genuine lever on paper, though the general house has not faced voters since 2011 and the rolls have halved; the Gurdwara Election Commission that must call them; and the courts that supervise gurdwara trusts abroad. The Jathedar cannot be petitioned; the body that hires him has not been voted on in fifteen years.")
DERA = 'convicted of rape in 2017; a 2019 conviction for conspiring to murder a journalist was overturned on appeal in 2026 and is now before the Supreme Court'
G("was convicted of rape and subsequently of conspiracy to murder a journalist.", 'was ' + DERA + '.', 1)
SET('sikhism', 'victories[2].what', 'Rape conviction of a dera leader with mass following and political protection',
    old='Conviction of a dera leader with mass following and political protection')
SET('sikhism', 'victories[2].when', '2017–2026', old='2017–2019')
G("(Dera Sacha Sauda's convicted leader controlled a corporate-scale operation)",
  "(Dera Sacha Sauda's leader, " + DERA + ', controlled a corporate-scale operation)', 1)
G('across a change in SGPC political control would revise the political-capture finding',
  'across a change in SGPC political control, or a general SGPC election held on schedule, would revise the political-capture finding', 1)

# ============ Jainism (sources/jainism.md) ============
SET('jainism', 'victories[1].when', '2008–present (most recently a 2026 court stay of a seven-year-old’s initiation)', old='2000s–present')

# ============ Taoism (sources/taoism.md) ============
TAO = '[OFFICIAL POLICY: 2017 directive of twelve central agencies barring investors from running temples]'
G('ticketed sacred sites with revenue flowing through state-adjacent management. [INVESTIGATIVE REPORT — verify specifics]',
  'ticketed sacred sites with revenue flowing through state-adjacent management. ' + TAO, 1)
G('Management companies and local government [INVESTIGATIVE REPORT — verify specifics]', 'Management companies and local government ' + TAO, 1)
SET('taoism', 'apex.rows[0][1]', 'The state-supervised body through which clergy registration and temple licensing run in the PRC — president Li Guangfu, re-elected in December 2025')

# ============ Confucianism (sources/confucianism.md) ============
G('Essentially uncountable as a religion: perhaps 6–8 million formal identifiers, while Confucian norms',
  'Essentially uncountable as a religion: formal identification is rare, while Confucian norms', 1)

# ============ Shinto (sources/shinto.md) ============
SET('shinto', 'apex.rows[0][1]', 'The umbrella body over roughly 80,000 shrines. The staff who questioned a 2015 property sale were dismissed; the courts voided the dismissals (final, 2022), and a rival claim to the presidency was rejected (final, 2024). President Tanaka Tsunekiyo was confirmed for a sixth term in 2025.')
SET('shinto', 'apex.rows[0][3]', 'The board — and, when it failed, the courts', old='The courts, apparently — which is itself the finding')
G("Japan's courts — where the shrine world's own governance dispute is already being heard —",
  "Japan's courts — where the shrine world's whistleblowers won their case —", 1)

# ============ Zoroastrianism (sources/zoroastrianism.md) ============
SET('zoroastrianism', 'apex.rows[0][1]', "Seven trustees elected by the city's Parsi electorate, controlling the housing trusts, the Towers of Silence, and — in effect — the boundary disputes over who is Parsi")
G("because it litigates them publicly.", "because it litigates them publicly. In 2026 the question reached a nine-judge bench of India's Supreme Court, where a judge asked why a Parsi man who marries out keeps his religious rights and a woman does not; judgment is reserved.", 1)
G('Indian courts repeatedly adjudicate who counts as Parsi and who may use community facilities',
  'Indian courts repeatedly adjudicate who counts as Parsi and who may use community facilities; heard by a nine-judge constitutional bench in 2026', 1)

# ============ Bahá'í (sources/bahai.md) ============
G('[FORMER MEMBER TESTIMONY / ACADEMIC SOURCE — document specific cases before publication]',
  '[FORMER MEMBER TESTIMONY: e.g., removals from the rolls in 1997, 2000 and 2005 after online discussion and scholarship]', 1)
SET('bahai', 'apex.rows[0][3]', 'The next election — though members are usually re-elected until they step down',
    old='The next election — though members are customarily returned until resignation or death')
G('[GOVERNMENT REPORT: UN documentation of Iranian persecution]', '[GOVERNMENT REPORT: UN Special Rapporteur on Iran, 2024]', 1)


# ============ Mormonism (sources/mormonism.md) ============
G('Presiding Bishop Gérald Caussé over temporal affairs;', 'Presiding Bishop W. Christopher Waddell over temporal affairs (since November 2025);', 1)
G('Utah abolished the clergy-penitent reporting exemption only partially and after sustained campaigning.',
  'Utah has not removed the clergy-penitent privilege; a 2024 law only protects clergy who choose to report.', 1)
G('~17 million members on the rolls;', '~17.9 million members on the rolls (2025);', 1)
G('~17.2 million on the rolls;', '~17.9 million on the rolls (2025);', 1)
G('Growth has slowed markedly; retention of youth in the U.S. has declined;',
  'Growth in the United States has slowed and youth retention has fallen; convert baptisms abroad rose sharply in 2025;', 1)

# ============ Seventh-day Adventism (sources/seventh-day-adventism.md) ============
G(' Almost nowhere else in this codex does that sentence appear. (Verify current officers before citing.)', ' Almost nowhere else in this codex does that sentence appear.', 1)
SET('seventh-day-adventism', 'apex.rows[0][1]', 'Erton Köhler, elected on 4 July 2025 at the General Conference session in succession to Ted N. C. Wilson, who had held the office since 2010')
G('Erton Köhler, elected 2025 (verify current holder)', 'Erton Köhler, elected July 2025', 1)
G('Erton Köhler, elected 2025 (verify)', 'Erton Köhler, elected July 2025', 1)
G('A global Protestant denomination of roughly 22 million members,', 'A global Protestant denomination of about 23.7 million baptized members (2024),', 1)
G('Roughly 22 million baptized members worldwide,', 'About 23.7 million baptized members worldwide (2024),', 1)

# ============ Jehovah's Witnesses (sources/jehovahs-witnesses.md) ============
BK = '[FINANCIAL RECORD: Brooklyn sales to Kushner Cos. and partners, about $1 billion]'
G('(e.g., 25–30 Columbia Heights sold for ~$340M). [FINANCIAL RECORD / INVESTIGATIVE REPORT — verify totals]', '(e.g., 25–30 Columbia Heights sold for ~$340M). ' + BK, 1)
G('[FINANCIAL RECORD — verify totals before publication]', BK, 1)
G('Decades of donated labor and funds realized as real-estate capital. [FINANCIAL RECORD — verify totals]',
  'Decades of donated labor and funds realized as real-estate capital. ' + BK, 1)
G('sold for very large sums after decades of donated work and funds. [FINANCIAL RECORD — verify totals]',
  'sold for about $1 billion after decades of donated work and funds. ' + BK, 1)
G("The organization's reserves [FINANCIAL RECORD — verify totals]", "The organization's reserves, which it does not publish [PATTERN OBSERVED: no public accounts]", 1)
G('[OFFICIAL POLICY: 2024 updates — verify details]', '[OFFICIAL POLICY: Governing Body Update, March 2024]', 1)
G('External and litigation pressure producing internal change. [OFFICIAL POLICY — verify details]',
  'External and litigation pressure producing internal change. [OFFICIAL POLICY: Governing Body Update, March 2024]', 1)
SET('jehovahs-witnesses', 'apex.rows[0][1]', "A self-perpetuating body of eleven men in Warwick, New York — among them Geoffrey Jackson, who testified before Australia's Royal Commission, David Splane, and Stephen Lett. Appointments are announced, never explained; Anthony Morris III's 2023 departure was announced in one sentence with no reason")
SET(None, 'V7.succession.rows[3].current', 'Eleven men, Warwick, New York', old='Approximately nine men, Warwick, New York')
G('initially declined to join the National Redress Scheme and joined in 2020 after sustained pressure and public naming.',
  'initially declined to join the National Redress Scheme and joined in September 2021, after the government moved to strip charity status from institutions that refused.', 1)
G('2015–16 proceedings; joined the National Redress Scheme 2020', '2015–16 proceedings; joined the National Redress Scheme in September 2021', 1)
SET('jehovahs-witnesses', 'regional[1].documented', "Norwegian authorities withdrew the organisation's registration and grants in 2022; the Supreme Court ruled in 2026 that the withdrawal was unlawful.")
SET('jehovahs-witnesses', 'regional[1].tell', "A state tried to condition religious registration on how a group treats people who leave, and its highest court said it could not do it that way. That is the finding — and it cuts against this codex's own hope for the lever.",
    old="The first case in this codex of a state conditioning religious registration on how a group treats people who leave. Whatever the final outcome, the precedent is the finding.")
G('~8.7 million active publishers worldwide;', '~9 million active publishers worldwide (2025);', 1)
G("~8.7 million active 'publishers'", "~9 million active 'publishers' (2025)", 1)
G('~20 million attend the annual Memorial.', '~20.6 million attend the annual Memorial.', 1)

# ============ Scientology (sources/scientology.md) ============
G('Australian, UK, and New Zealand censuses record numbers in the low thousands each.',
  'Census counts are small: 1,854 in England and Wales (2021), about 1,700 in Australia (2016), and 315 in New Zealand (2023).', 1)
G('arbitration clauses in membership agreements have been enforced against former members.',
  "arbitration clauses in membership agreements have been enforced against former members in federal court (2021), while California's courts refused to enforce them for claims arising after members left (2022).", 1)

# ============ Hare Krishna (sources/hare-krishna.md) ============
G('in one community murder conspiracy convictions', 'in one community murder convictions', 1)
G('in one case murder conspiracy convictions (New Vrindaban)', 'in one case murder convictions (New Vrindaban)', 1)
G('in one community, murder conspiracy convictions.', 'in one community, murder convictions.', 1)
G('the female diksha-guru question has been a major recent controversy.',
  'the female diksha-guru question has been a major recent controversy — approved by the GBC in 2019 and 2021, then paused again in 2022.', 1)

# ============ New Age (sources/new-age.md) ============
G('Children present in ceremony and plant-medicine contexts is an emerging and poorly documented risk area. [SOURCE NEEDED]',
  'This codex found no systematic data on children in ceremony and plant-medicine settings — and in a market with no licensing body, the absence of records is itself the risk.', 1)
G('Uncountable by design: roughly 20–30% of adults in Western countries report New Age beliefs (astrology, energy healing, reincarnation) while claiming no religion. [ACADEMIC SOURCE: Pew]',
  'Uncountable by design: about six in ten US adults hold at least one New Age belief — psychics, spiritual energy in objects, reincarnation, astrology — religious and non-religious alike. [ACADEMIC SOURCE: Pew, 2018]', 1)

# ============ Indigenous (sources/indigenous.md) ============
SET('indigenous', 'timeline[4][0]', '1910–1970 / 1950s–1980s', old='1950s–1970s')
SET('indigenous', 'timeline[4][1]', 'Stolen Generations (Australia) and Sixties Scoop (Canada) child removals; forced sterilization programs',
    old='Stolen Generations and Sixties Scoop child removals; forced sterilization programs')
G('Several church bodies have still not fully released records or met funding commitments — harm inflicted on these traditions from outside them.',
  'Catholic entities were released from a $25 million fundraising pledge in 2015 after raising under $4 million, and re-pledged $30 million in 2021 after public outcry — harm inflicted on these traditions from outside them.', 1)
G('[INVESTIGATIVE REPORT — verify specifics]', TAO, 1)  # Taoism roster[1]: same 2017 directive

# ============ Cross-cutting volumes (sources/_crosscutting.md) ============
G('documented jets, mansions, family boards; ended without penalty when ministries declined disclosure — the opacity itself was the finding.',
  'documented jets, mansions and family boards; only two of the six fully cooperated, and it ended without penalty — the opacity itself was the finding.', 1)
G('Gurmeet Ram Rahim Singh (rape, murder convictions), Asaram Bapu (rape conviction).',
  'Gurmeet Ram Rahim Singh (rape conviction; two murder convictions overturned on appeal, 2024 and 2026), Asaram Bapu (rape conviction).', 1)
G('lost in speculative investment.', 'lost in speculative investment — convicted December 2023; a partial retrial was ordered on appeal in 2026.', 1)
G("Germany's Kirchensteuer: the state collects roughly €12–13B annually for the churches via the tax system. [FINANCIAL RECORD — verify current figures]",
  "Germany's Kirchensteuer: the state collects about €12.8B a year for the two large churches through the tax system (2025: Catholic €6.75B, Protestant €6.09B). [FINANCIAL RECORD: DBK and EKD figures, 2026]", 1)
G("Israel's Chief Rabbinate monopoly over Jewish marriage/divorce/conversion;",
  "Israel's Chief Rabbinate monopoly over Jewish marriage and divorce (1953 law), and until 2021 over recognised conversion in Israel;", 1)
G('Hillsong/Bethel/Elevation worship-licensing revenues via CCLI — global congregational singing as royalty stream. [FINANCIAL RECORD — verify current figures]',
  'Worship-licensing via CCLI — over 250,000 churches licensed, and a handful of publishers tied to Hillsong, Bethel, Elevation and Passion controlling most of its most-sung songs: congregational singing as royalty stream. [INVESTIGATIVE REPORT: Christianity Today, 2023]', 1)
G("Every tradition's section 17–19 in this codex:", "Every tradition's Acts 06, 10 and 12 in this codex:", 1)
G('Officeholders are stated as of early 2026 and offices outlast holders — verify the name before citing it.',
  'Officeholders were last checked on 27 September 2026, and offices outlast holders — check the name before citing it.', 1)
G("One hundred and sixty-seven of this codex's 750 graded intersections name a specific document.",
  "One hundred and ninety-four of this codex's 810 graded intersections name a specific document.", 1)
assert D['sourcedN'] == 194 and len(D['graded']) == 810
G('and Justice Douglas said so in dissent', 'and Justice Douglas said so in partial dissent', 1)
G('A number of US states retain statutory language shielding parents from neglect prosecution where treatment was withheld on religious grounds.',
  'Most US states — thirty-four and the District of Columbia, by one 2025 count — retain statutory language giving parents a religious defence where treatment was withheld.', 1)
G('The head of the bishops\' conference publicly disputed a core finding within days.',
  'Within days the head of the bishops\' conference said the seal of confession was "stronger than the laws of the Republic", rejecting its central reporting recommendation, and was summoned by the interior minister.', 1)
G('handled under the pontifical secret — sent to bishops, not published.', 'handled under the secret of the Holy Office — sent to bishops, not published.', 1)
G('Tens of thousands of minors were married in the US in recent decades under exceptions.',
  'Nearly 300,000 minors were married in the US between 2000 and 2018 under exceptions.', 1)
G('testing whether religious volunteer framing displaces labour law.',
  'testing whether religious volunteer framing displaces labour law. The Justice Department closed its criminal investigation in 2025 without charges; the civil case continues.', 1)
G('The worst are Sunni Islam, Taoism, Judaism, Shia Islam, Sikhism, and Jainism.',
  "The worst are Sunni Islam and Taoism, then Judaism, then seven tied: Shia Islam, Sikhism, Jainism, Shinto, Zoroastrianism, Bahá'í and Hare Krishna.", 1)
G('The Instruments (11) · Your Track (4 paths)', 'The Instruments (12) · Your Track (6 paths)', 1)


# ============ Notes that promised "verify" flags, and the reader-facing change log ============
G("Every structural grade carries its authored basis and is open to dispute; every 'verify' flag marks a figure awaiting a primary source.",
  'Every structural grade carries its authored basis and is open to dispute.', 1)
SET(None, 'D.changeMind.log[4][1]', 'Every figure once marked for checking has now been checked against a primary source. Claims still open are listed in the Gap Register.',
    old="Figures marked 'verify before publication' throughout are not yet confirmed against primary sources and should be read as provisional.")
assert D['changeMind']['log'][0][0] == 'v4 — 2026-09-27'
D['changeMind']['log'][0][1] += (' Fact-checked every tradition and every cross-cutting volume against primary sources: updated leaders who have changed,'
    ' convictions since overturned or sent for retrial, membership figures and several dates, and resolved every note'
    ' that said a figure still needed checking.')
log.append('changeMind v4 entry: + fact-check sentence')


# ============ Receipts page: refresh quotes from the edited profiles ============
D['receiptIndex'], moved, dropped = RCPT.refresh(D, PINS, RI_ORDER)
log += [f'receipt moved: {m}' for m in moved] + [f'receipt dropped: {d!r}' for d in dropped]

# ============ reassemble ============
for n in BLOBS: spans[n][2] = B[n]
# markup: the Gap Register counted every occurrence of the word "verify" as a flag, so prose
# ("a lineage you cannot verify") showed up as unchecked figures; count bracketed flags only
MK = [("const vf = (s.match(/verify/gi)||[]).length;",
       "const vf = (s.match(/[\\[(][^\\])]*\\bverify\\b[^\\])]*[\\])]/gi)||[]).length;", 1)]
res, prev = [], 0
for n in sorted(BLOBS, key=lambda n: spans[n][0]):
    i, e, d, tail = spans[n]
    res.append(s[prev:i]); res.append(json.dumps(d, ensure_ascii=False) + tail); prev = e
res.append(s[prev:])
markup_idx = list(range(0, len(res), 2))  # even slots are markup, odd slots are data
for old_m, new_m, n in MK:
    c = sum(res[k].count(old_m) for k in markup_idx)
    assert c == n, f'markup: expected {n}x {old_m!r}, found {c}'
    for k in markup_idx: res[k] = res[k].replace(old_m, new_m)
    log.append(f'markup: {old_m[:50]!r}')
out_s = ''.join(res)
assert not MISS, f'{len(MISS)} mismatches'
open(out, 'w', encoding='utf-8').write(out_s)
print('\n'.join(log)); print(f'{len(log)} edits; wrote {out} ({len(out_s.encode())} bytes)')
