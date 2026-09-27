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


# ============ Receipts page: refresh quotes from the edited profiles ============
D['receiptIndex'], moved, dropped = RCPT.refresh(D, PINS, RI_ORDER)
log += [f'receipt moved: {m}' for m in moved] + [f'receipt dropped: {d!r}' for d in dropped]

# ============ reassemble ============
for n in BLOBS: spans[n][2] = B[n]
res, prev = [], 0
for n in sorted(BLOBS, key=lambda n: spans[n][0]):
    i, e, d, tail = spans[n]
    res.append(s[prev:i]); res.append(json.dumps(d, ensure_ascii=False) + tail); prev = e
res.append(s[prev:])
out_s = ''.join(res)
assert not MISS, f'{len(MISS)} mismatches'
open(out, 'w', encoding='utf-8').write(out_s)
print('\n'.join(log)); print(f'{len(log)} edits; wrote {out} ({len(out_s.encode())} bytes)')
