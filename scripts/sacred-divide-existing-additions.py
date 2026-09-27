#!/usr/bin/env python3
"""Generate content/sacred-divide/existing-traditions-additions.md.

The inventory part of each entry (what the religion's page already has,
and what it lacks) is read from the live book's embedded data, so it cannot
drift from the page. The research leads are hand-written below and are
drafts: every one must pass the fact-check phase before import.

Usage: python3 scripts/sacred-divide-existing-additions.py <live.html> <out.md>
"""
import json, sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def blob(n):
    i = s.index(f'window.{n} = ') + len(f'window.{n} = '); e = s.index('</script>', i)
    return json.loads(s[i:e].rstrip().rstrip(';'))
D, V2, V3, V6, V7 = (blob(n) for n in ('CODEX_DATA', 'CODEX_V2', 'CODEX_V3', 'CODEX_V6', 'CODEX_V7'))
cases = {}
for c in D['cases']: cases.setdefault(c['tradition'], []).append(c['title'])
regions = V6['regions']['cards']; lang = V6['language']['per']

FAMILY = {
 'christianity':'Christianity (umbrella)','catholicism':'Christianity','eastern-orthodoxy':'Christianity','protestant-evangelical':'Christianity',
 'pentecostal-charismatic':'Christianity','islam':'Islam (umbrella)','sunni-islam':'Islam','shia-islam':'Islam','judaism':'Judaism (umbrella)',
 'orthodox-hasidic-judaism':'Judaism','hinduism':'Dharmic','buddhism':'Buddhism (umbrella)','tibetan-buddhism':'Buddhism','sikhism':'Dharmic',
 'jainism':'Dharmic','taoism':'East Asian','confucianism':'East Asian','shinto':'East Asian','zoroastrianism':'Persian-born','bahai':'Persian-born',
 'mormonism':'Restorationist & Adventist','seventh-day-adventism':'Restorationist & Adventist','jehovahs-witnesses':'Restorationist & Adventist',
 'scientology':'New movements','hare-krishna':'Dharmic','new-age':'New movements','indigenous':'Indigenous & folk'}

# Hand-written research leads. (verify) = confirm against a primary source before import.
L = {
'christianity': dict(
  law=['Church taxes collected by the state (Germany, Austria, Switzerland, Nordic countries) — the umbrella page should summarize and link to the Catholic and Protestant pages.',
       'Established churches (England, Denmark, Norway until 2012 *(verify)*, Greece) and state clergy salaries.'],
  money=['Umbrella page should hold no figures of its own; link to branch pages (avoid duplication found in the audit).'],
  cases=[],
  voices=['Ecumenical reform voices are better placed on branch pages.'],
  help=['Link to each branch page\'s help section rather than listing here.'],
  other=['Decide the umbrella page\'s role for the family hub: shared foundations only (origin, creeds, sacraments, tithing history). Move any branch-specific rows to the branch.']),
'catholicism': dict(
  law=['Concordats (e.g. Italy 1929/1984, Spain 1979) and state funding — *(verify)* specifics.', 'The seal of confession versus mandatory-reporting laws (Australian states legislated after the Royal Commission; Washington State 2025 *(verify)*).', 'Canon law\'s 2019 *Vos estis lux mundi* and the 2021 revision of Book VI (penal law).'],
  money=['Vatican Bank (IOR) has published annual reports since 2013; APSA reports since 2021 *(verify)*.', 'US diocesan bankruptcies and settlement totals (40+ dioceses *(verify count)*).'],
  cases=['Pennsylvania grand jury report (2018). [GOVERNMENT REPORT]', 'Ireland: Ryan Report and Murphy Report (both 2009). [GOVERNMENT REPORT]', 'Australian Royal Commission — Catholic Church final report volume (2017). [GOVERNMENT REPORT]'],
  voices=['Survivor-founded organizations (e.g. SNAP in the US) and reform movements inside the church (e.g. lay councils, Voice of the Faithful *(verify)*).'],
  help=['Survivor networks (SNAP — US; One in Four — Ireland *(verify)*); national independent redress schemes where they exist.'],
  other=['Sub-pages or rows for Opus Dei and the Legion of Christ (the Vatican\'s 2010 findings on the founder of the Legion *(verify)*).']),
'eastern-orthodoxy': dict(
  law=['Greece: clergy salaries paid by the state *(verify current arrangement)*.', 'Russia: the Moscow Patriarchate\'s alignment with the state and the war in Ukraine; UK sanctions on the Patriarch (2022) *(verify)*.', 'Ukraine: 2024 law restricting Moscow-affiliated religious organizations *(verify)*.'],
  money=['Church property restitution and state funding figures by country *(research)*.'],
  cases=['Court proceedings under Ukraine\'s 2024 law *(verify)*.', 'Sanctions listings as regulatory records *(verify)*.'],
  voices=['Orthodox clergy and theologians who publicly opposed "Russian World" ideology (e.g. the 2022 declaration by Orthodox theologians *(verify)*).'],
  help=['Research needed.'],
  other=['Russian Orthodox Church vs. Ecumenical Patriarchate schism (2018) as a turning point.']),
'protestant-evangelical': dict(
  law=['US tax exemption for churches (no filing requirement, IRS Form 990 exemption) — the single largest transparency gap; the Johnson Amendment and its 2025 IRS reinterpretation *(verify)*.'],
  money=['ECFA members publish financial data; most US churches publish nothing — show the gap.'],
  cases=['Independent investigation of RZIM (2021). [INVESTIGATIVE REPORT]', 'Willow Creek Independent Advisory Group report (2019) *(verify)*. [INVESTIGATIVE REPORT]'],
  voices=['Survivor-advocates inside evangelicalism (e.g. those who pressed the SBC Guidepost report).'],
  help=['Religious-trauma and survivor support organizations *(research and vet)*.'],
  other=['IBLP/Gothard and purity culture as a documented sub-network *(verify sources)*.']),
'pentecostal-charismatic': dict(
  law=['Nigeria and Kenya church-registration debates, including Kenya after Shakahola (2023) *(verify)*.'],
  money=['Megachurch finances: Australian charity filings (e.g. Hillsong via ACNC) *(verify)*.'],
  cases=['Kenya — Shakahola forest deaths (2023) and prosecutions *(verify; classify carefully — independent church)*. [COURT RECORD / GOVERNMENT REPORT]', 'BBC investigation into the Synagogue Church of All Nations (2024) *(verify)*. [INVESTIGATIVE REPORT]', 'Hillsong: NSW prosecution of the founder for concealment (acquitted 2023) — record the acquittal *(verify)*. [COURT RECORD]'],
  voices=['Pentecostal scholars critical of the prosperity gospel.'],
  help=['Research needed by region (Africa, Latin America, US).'],
  other=['Prosperity gospel as a separate money row with the US Senate (Grassley) inquiry already cited.']),
'islam': dict(
  law=['Consolidated table: states with apostasy and blasphemy laws, and penalties (sources: USCIRF, Pew *(verify latest)*).', 'Religious personal-status courts by country; UK sharia councils (the Siddiqui review).'],
  money=['Hajj quotas and costs by country *(verify)*; state zakat bodies that publish accounts (e.g. Malaysia) versus those that don\'t.'],
  cases=['Blasphemy death sentence overturned — Supreme Court of Pakistan (2018). [COURT RECORD]', 'The Siddiqui independent review into sharia councils (UK Home Office, 2018). [GOVERNMENT REPORT]'],
  voices=['Musawah (the global movement for equality in Muslim family law); Muslim feminist scholars; Sisters in Islam (Malaysia).'],
  help=['Muslim Women\'s Network UK helpline; Karma Nirvana (forced marriage, UK); Faith to Faithless (UK); Ex-Muslims of North America *(verify all)*.'],
  other=['Remove duplication with Shia (the 2022 death in custody) and Sunni (zakat): the umbrella holds shared foundations only.', 'Add related-family cards: Ahmadiyya, Sufi Orders, Dawoodi Bohra, Nation of Islam (card only), Alevis (row).']),
'sunni-islam': dict(
  law=['Saudi Arabia, Egypt, Pakistan, Indonesia, Malaysia: who appoints muftis, who runs religious courts, and how apostasy is treated.'],
  money=['Diyanet budget (published in Turkey\'s state budget) *(verify figure)*; Al-Azhar budget.'],
  cases=['Honor-killing pardon under qisas/diyat law — a 2016 killing; conviction in 2019; acquittal in 2022 after the parents\' pardon *(verify)*. [COURT RECORD]', 'Saudi detention of clerics who declined to endorse state positions (2017) *(verify)*. [GOVERNMENT REPORT / INVESTIGATIVE REPORT]'],
  voices=['Nahdlatul Ulama and Muhammadiyah reformers; traditionalist scholars who teach madhhab diversity.'],
  help=['As for Islam, plus regional helplines *(research)*.'],
  other=['A dedicated Salafism block (Saudi-funded universities, translation houses, approved-scholar lists).', 'Regional cards: Malaysia, Egypt, Pakistan, Nigeria.']),
'shia-islam': dict(
  law=['Iran\'s constitution and the Guardian Council; Iraq\'s personal-status law amendments (2024–25) enabling sect-based family law *(verify)*.'],
  money=['Astan Quds Razavi and bonyad holdings as reported *(verify figures)*; UK charity filings of khums-receiving foundations.'],
  cases=['The 2022 death in custody (already present).', 'Bahrain Independent Commission of Inquiry (2011). [GOVERNMENT REPORT]', 'UN Fact-Finding Mission on Iran (2023–24) *(verify)*. [GOVERNMENT REPORT]'],
  voices=['Najaf quietist scholars; Iranian reformist clerics; women\'s rights activists (e.g. the Nobel Peace Prize 2023 laureate) *(verify)*.'],
  help=['Research needed (Iranian diaspora legal aid; Iraqi women\'s organizations).'],
  other=['Ismaili (Nizari) row; a Dawoodi Bohra link card; Zaydi/Houthi row.']),
'judaism': dict(
  law=['Israel: the Chief Rabbinate\'s monopoly over Jewish marriage and divorce; no civil marriage; get refusal and agunot.', 'UK: the Board of Deputies\' role; kashrut certification.'],
  money=['Kashrut certification fees; Israeli state funding of religious councils *(verify)*.'],
  cases=['Israeli rabbinical-court and state sanctions on get refusal *(verify examples)*. [COURT RECORD]'],
  voices=['Orthodox feminists and agunah advocates; Reform and Conservative movements as governance contrasts.'],
  help=['ORA — Organization for the Resolution of Agunot *(verify)*; Mavoi Satum (Israel) *(verify)*.'],
  other=['Add Reform/Conservative as a healthy-structure contrast row.']),
'orthodox-hasidic-judaism': dict(
  law=['New York State "substantial equivalency" regulations for yeshivas (2022) and litigation *(verify)*.', 'The UK Department for Education and unregistered schools.'],
  money=['Public funding to Hasidic-run schools (NYT 2022 investigation) *(verify)*.'],
  cases=['Extradition from Israel and conviction in Victoria of a former Melbourne school principal (2021–23) *(verify)*. [COURT RECORD]'],
  voices=['Footsteps alumni; YAFFED (education advocacy) *(verify)*.'],
  help=['Footsteps (US); Mavar (UK) *(verify)*.'],
  other=['Regional cards: New York, London (Stamford Hill), Israel (Bnei Brak), Melbourne.']),
'hinduism': dict(
  law=['State control of temples in India (e.g. Tamil Nadu HR&CE Department; Tirumala Tirupati Devasthanams) — board appointments by governments.', 'Caste-discrimination law (India\'s SC/ST Act; the US debate over caste in anti-discrimination law, e.g. California SB 403, vetoed 2023) *(verify)*.'],
  money=['TTD annual budget (published) *(verify figure)* — "Money in numbers" example.'],
  cases=['Conviction of a self-styled godman for rape (Jodhpur, 2018) *(verify; may belong on a Guru movements page)*. [COURT RECORD]'],
  voices=['Anti-caste reformers within Hinduism; temple-entry movements.'],
  help=['Research needed (Dalit rights organizations; caste-discrimination legal aid).'],
  other=['A cross-guru page (see the analysis doc) instead of loading guru cases onto Hinduism.']),
'buddhism': dict(
  law=['Thailand\'s Sangha Act and state control of monastic governance; Myanmar\'s state-sangha relations.'],
  money=['Temple donations; the Dhammakaya case *(verify)*.'],
  cases=['Wat Phra Dhammakaya embezzlement investigation and 2017 siege *(verify)*. [GOVERNMENT REPORT]', 'UN Independent International Fact-Finding Mission on Myanmar (2018): the role of nationalist monastic movements *(verify framing)*. [GOVERNMENT REPORT]'],
  voices=['Engaged Buddhist reformers; bhikkhuni ordination advocates.'],
  help=['Research needed.'],
  other=['Add a Soka Gakkai branch (new file) and a Theravada monastic institutions row.']),
'tibetan-buddhism': dict(
  law=['PRC State Religious Affairs Bureau Order No. 5 (2007) on reincarnation approval; the Panchen Lama case (1995).'],
  money=['Western dharma-center charity filings (Rigpa UK, Shambhala) *(verify)*.'],
  cases=['Present: Rigpa, Shambhala, Order No. 5.', 'Add: Charity Commission action on Rigpa UK (2019) *(verify)*.'],
  voices=['Survivor letters from Rigpa students (2017); teachers who called for accountability.'],
  help=['Research needed.'],
  other=['A Dalai Lama succession row in the Succession Watch.']),
'sikhism': dict(
  law=['The SGPC is elected under the Sikh Gurdwaras Act 1925 (a statutory electoral body) — record as a governance strength; elections delayed for years *(verify)*.'],
  money=['SGPC annual budget published *(verify figure)*.'],
  cases=['Present: the dera case.', 'Add: Akal Takht excommunication (tankhaiya) edicts against political figures *(verify examples)*. [OFFICIAL POLICY]'],
  voices=['Sikh women\'s equality advocates (e.g. kirtan at the Golden Temple).'],
  help=['Research needed.'],
  other=['Regional cards: Punjab, UK, Canada.']),
'jainism': dict(
  law=['Santhara (ritual fasting to death): the Rajasthan High Court (2015) classed it as suicide; the Supreme Court stayed the ruling *(verify)*.'],
  money=['Temple trusts; dana. Research needed.'],
  cases=['Rajasthan High Court santhara ruling (2015) and Supreme Court stay *(verify)*. [COURT RECORD]', 'Child diksha (initiation of minors as monastics) — petitions and child-rights commission interventions *(verify)*. [GOVERNMENT REPORT]'],
  voices=['Jain scholars debating santhara consent.'],
  help=['Research needed.'],
  other=['Fix: the Normalization entry had Taoism content and pasted chat (fixed in v4).']),
'taoism': dict(
  law=['PRC State Administration for Religious Affairs; the China Taoist Association; Taiwan\'s temple regulations.'],
  money=['Taiwan temple economies and pilgrimage finance (Mazu) *(verify)*.'],
  cases=['Research needed.'],
  voices=['Research needed.'], help=['Research needed.'],
  other=['A regional card for Taiwan.']),
'confucianism': dict(
  law=['Filial piety in law: Singapore\'s Maintenance of Parents Act (1995); China\'s elderly-rights law requiring visits (2013) *(verify)*.'],
  money=['—'],
  cases=['Parents\' maintenance tribunal cases (Singapore) *(verify)*. [COURT RECORD]'],
  voices=['Research needed.'], help=['Research needed.'],
  other=['Korean regional card (ancestral rites, family-register law history).']),
'shinto': dict(
  law=['Separation of religion and state lawsuits: the Ehime tamagushi-ryō case (Supreme Court of Japan, 1997) ruled public offerings unconstitutional *(verify)*.'],
  money=['Jinja Honchō (Association of Shinto Shrines) and neighborhood levies.'],
  cases=['Ehime tamagushi-ryō case (1997). [COURT RECORD]'],
  voices=['Research needed.'], help=['Research needed.'],
  other=['Shinto Seiji Renmei (the political league) as a roster row *(verify)*.']),
'zoroastrianism': dict(
  law=['Indian Supreme Court case on Parsi women married outside the community and access to fire temples and towers of silence (from 2017) *(verify status)*.'],
  money=['Bombay Parsi Punchayet trust assets and housing allocation.'],
  cases=['Present: BPP case.', 'Add the Supreme Court interfaith-marriage case *(verify)*. [COURT RECORD]'],
  voices=['Reformist Parsi advocates for inclusion.'],
  help=['Research needed.'], other=['—']),
'bahai': dict(
  law=['Iran: systematic persecution (the Yaran imprisonments; university exclusion) — the page\'s first fact.'],
  money=['Huqúqu\'lláh (19% of surplus wealth) — a codified obligation; research how it is accounted for.'],
  cases=['UN Special Rapporteur reports on Baháʼís in Iran *(verify)*. [GOVERNMENT REPORT]'],
  voices=['Research needed.'], help=['Research needed.'],
  other=['An internal-machinery row: "covenant-breaker" designation and shunning (documented in Baháʼí texts) *(verify framing with an insider)*.']),
'mormonism': dict(
  law=['US tax status; the SEC order already present.'],
  money=['Ensign Peak Advisors portfolio figures from SEC 13F filings *(verify latest)* — the strongest "Money in numbers" example in the book.'],
  cases=['Present: SEC Ensign; the "quit Mormon" case.', 'Add: Arizona and West Virginia clergy-reporting civil cases *(verify)*. [COURT RECORD]'],
  voices=['Members who publicly pressed for financial transparency.'],
  help=['Research and vet support communities.'], other=['—']),
'seventh-day-adventism': dict(
  law=['—'],
  money=['AdventHealth and Adventist Health system revenues (published) *(verify)*.'],
  cases=['General Conference votes on women\'s ordination (2015) *(verify)*. [OFFICIAL POLICY]'],
  voices=['Advocates for women\'s ordination within the church.'],
  help=['Research needed.'],
  other=['Keep the page\'s strong-governance framing; add "What healthy looks like here" as a model for other pages.']),
'jehovahs-witnesses': dict(
  law=['Norway: loss of state grants and registration, and litigation (2022–25) *(verify outcomes)*.', 'Russia: the 2017 ban (persecution — record first).'],
  money=['Brooklyn property sales (present); UK Charity Commission inquiry into Watch Tower Bible and Tract Society of Britain *(verify dates and outcome)*.'],
  cases=['Present: Australian Royal Commission Case Study 29.', 'Add the UK Charity Commission inquiry *(verify)*. [REGULATORY FILING]', 'Add the Norwegian court rulings *(verify)*. [COURT RECORD]'],
  voices=['Former members who testified to the Royal Commission.'],
  help=['Research and vet support organizations.'], other=['—']),
'scientology': dict(
  law=['Germany: monitoring by the domestic intelligence service *(verify current)*; US IRS exemption (1993).'],
  money=['—'],
  cases=['Present: Operation Snow White.', 'Add: French conviction of Scientology entities for organized fraud (2009), upheld by the Cour de cassation (2013) *(verify)*. [COURT RECORD]'],
  voices=['Former senior members who have testified publicly.'],
  help=['Research and vet.'], other=['—']),
'hare-krishna': dict(
  law=['—'],
  money=['—'],
  cases=['Present: the Turley case.', 'Add: ISKCON Child Protection Office (founded 1990s) as a victory *(verify)*.'],
  voices=['Former gurukula students who led the litigation and the 1998 ISKCON Communications Journal article *(verify)*.'],
  help=['Research needed.'], other=['—']),
'new-age': dict(
  law=['Consumer-protection and medical-advertising regulation of wellness claims *(research by jurisdiction)*.'],
  money=['—'],
  cases=['Present: Ray; NXIVM.', 'Add, or move to a Guru movements page: Rajneeshpuram and the 1984 Oregon salmonella attack (convictions) *(verify)*. [COURT RECORD]'],
  voices=['Research needed.'], help=['Research needed.'], other=['—']),
'indigenous': dict(
  law=['Church-run residential and boarding schools: Canada TRC (present); Australia\'s *Bringing Them Home* (1997); the US Federal Indian Boarding School Initiative reports (2022, 2024) *(verify)*.'],
  money=['—'],
  cases=['Add *Bringing Them Home* (1997). [GOVERNMENT REPORT]', 'Add the US boarding-school reports *(verify)*. [GOVERNMENT REPORT]'],
  voices=['Indigenous-led truth and reconciliation bodies.'],
  help=['Research needed by country.'],
  other=['Clarify framing: the documented machinery on this page is mostly *Christian missions acting on Indigenous peoples*. Decide whether those cases belong here or on the Christian branch pages, with a cross-link.']),
}

lines = ['# The Sacred Divide — additions for the 27 existing religions', '',
 '**Status: DRAFT, pre-fact-check.** Generated by `scripts/sacred-divide-existing-additions.py`.',
 'The **Has now** lines are read from the live book and are exact. The **Add** lines are research leads;',
 'anything marked *(verify)* was compiled from memory and must be confirmed first.', '',
 '## Sections every religion gets (from the redesign analysis, §5)', '',
 '| # | Section | Source |', '|---|---|---|',
 '| 1 | At a glance | Generated from existing data (see each entry\'s draft card below) |',
 '| 2 | What healthy looks like here | Existing `healthy` field, promoted to its own act |',
 '| 3 | Law & state here | New research (leads below) |',
 '| 4 | Money in numbers | New research (leads below) |',
 '| 5 | Documented cases (target ≥3) | Existing cases + leads below |',
 '| 6 | Voices from inside | Existing `victories` + leads below |',
 '| 7 | Branches & variants | From family hub design |',
 '| 8 | Regional variants (target: all) | Existing cards + new |',
 '| 9 | Who gets hurt most | Pulls this religion\'s rows from the four people-volumes |',
 '| 10 | Leaving safely here | Exit Atlas row + calculator |',
 '| 11 | Where to get help | New research (leads below) — vet every organization |',
 '| 12 | Words used here | Existing phrasebook entries |',
 '| 13 | Sources for this page | Generated from receipt tags |',
 '| 14 | What changed on this page | Error Ledger + version notes |', '']
lines += ['## Coverage summary (from the live data)', '', '| Religion | Family | Cases | Regional card | Phrasebook terms | Healthy items |', '|---|---|---|---|---|---|']
for r in D['religions']:
    rid = r['id']
    lines.append(f"| {r['name']} | {FAMILY[rid]} | {len(cases.get(rid, []))} | {'yes' if rid in regions else '**no**'} | {len(lang.get(rid, []))} | {len(r.get('healthy', []))} |")
lines += ['', '**Religions with zero documented cases:** ' + ', '.join(r['name'] for r in D['religions'] if not cases.get(r['id'])) + '.', '']
for r in D['religions']:
    rid = r['id']; l = L[rid]; ap = V2.get('apex', {}).get(rid, {})
    lines += ['---', '', f"## {r['name']}  ·  `{rid}`  ·  family: {FAMILY[rid]}", '']
    lines += ['**Draft "At a glance" card (from existing data):**', '']
    lines.append(f"- **Size:** {r['demographics'].get('adherents','—')}")
    if ap.get('rows'):
        lines.append(f"- **Who's in charge:** {ap['rows'][0][0]} — {ap['rows'][0][1]}")
    lines.append(f"- **Money:** {r['money'][0] if r.get('money') else '—'}")
    lines.append(f"- **Leaving:** {r['exit'][0] if r.get('exit') else '—'}")
    if V2.get('unanswered', {}).get(rid): lines.append(f"- **The unanswered question:** {V2['unanswered'][rid]}")
    lines.append('')
    lines.append(f"**Has now:** {len(cases.get(rid, []))} documented case(s)" + (f" ({'; '.join(cases[rid])})" if cases.get(rid) else '') +
                 f"; regional card: {'yes' if rid in regions else 'no'}; phrasebook terms: {len(lang.get(rid, []))}; healthy items: {len(r.get('healthy', []))}.")
    lines.append('')
    for key, title in (('law','Law & state here'),('money','Money in numbers'),('cases','New documented cases'),('voices','Voices from inside'),('help','Where to get help'),('other','Other additions and fixes')):
        items = [x for x in l.get(key, []) if x and x != '—']
        if items:
            lines.append(f"**{title}:**"); lines += [f"- {x}" for x in items]; lines.append('')
open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote', out)
