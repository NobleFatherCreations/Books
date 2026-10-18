# The Sacred Divide — discrepancy audit, Islamic-sections review, navigation plan

2026-09-27. Audited against the **live** file (`noblefathercreations.com/faith`,
byte-identical to `thenobledivide.netlify.app`). All fixes are in
`library/_undeployed/sacred-divide-v4-candidate.html`, built by
`scripts/sacred-divide-v4.py` from the live file. **Nothing is deployed.**

**Naming rule from now on:** the book is **The Sacred Divide**. Not "The
Coercive Control Codex", not "Coercive Control Index". The lowercase word
"codex" still appears in the book's own prose ("this codex") and in the
volume names (The Children's Codex, the Counter-Codex). Those were left
alone because they are part of the writing, not the title. Changing them is
a separate decision.

---

## 1. Discrepancies found across the whole book

| # | What was wrong | Where | Status |
|---|---|---|---|
| 1 | Title shown as "The Coercive Control Codex" in the browser tab, sidebar brand, board heading, masthead, footer, the Middle-Tier Field Kit and the page-title script | page markup | **Fixed** → The Sacred Divide |
| 2 | "Index of 25 traditions", "The 25 × 30 matrix", "The Twenty-Five Traditions", "Twenty-five Tuesdays", "twenty-five defender attacks", meta description | page markup | **Fixed** → 27 |
| 3 | "Twenty-five traditions" on the entry close screen, in "how long", in the legal notice, the anti-weaponisation note, the audio roadmap and the Annual Asking (×2) | data | **Fixed** → twenty-seven |
| 4 | "eleven accountability instruments": the Instruments district actually lists 12 | intro screen, markup + data | **Fixed** → twelve |
| 5 | "Four readers, four different needs": Your Track lists **six** | district header ×2, guide ×2 | **Fixed** → six |
| 6 | **17 leaked drafting notes** ("Your file defines it as…", "The file gives the example…") in the public tactic text: 4 shared tactic definitions (Weaponized Generosity, Future Faking, Hoovering, Devaluation), plus examples for Scientology ×3, Islam ×2, JW ×2, Orthodox/Hasidic Judaism, Mormonism, Christianity, Protestant, Hinduism, Buddhism | data | **Fixed**: rewritten as plain text, keeping the quoted material |
| 7 | **Pasted chat text in the Jainism entry** under Normalization: "Got it", "I'll interpret this as:", "1. Continue 13. NORMALIZATION … through the end of the 25-list", plus 4 Taoism examples (qi, "inner-door" teachings) misfiled into Jainism | data | **Fixed**: removed. Taoism's own entry was already complete |
| 8 | 27 stray spaces before punctuation ("technique” .") left behind by stripped citations | data | **Fixed** |
| 9 | Grammar: "as long as they becomes" | Islam / Love Bombing | **Fixed** |
| 10 | **Cloudflare analytics beacon** on a page whose first screen says "Nothing here is tracked… no way for anyone to know you were here" | end of page | **Removed from the candidate.** It is also on the Netlify origin, so it isn't Cloudflare adding it. It's either in the uploaded file or Netlify snippet injection (the connector can't show which). **Check Netlify → Site config → Snippet injection before redeploying.** |
| 11 | The repo's `library/faith/index.html` is **not** what's live. It's the older 4.7MB lineage. The 2026-08-31 audit's "it matches live" was wrong | repo | **Resolved in `sites.json`** (byte proof). Swapping the files is left for you (see §6) |
| 12 | The Weighing (scale) and The Loop call this book "The Coercive Control Codex" in their text and menus | `library/scale`, `library/loop` | **Fixed in source**, not deployed |
| 13 | Roster tables break words mid-word at desktop width ("foundatio/ns", "SEMI-OFFICI/AL") because the first column is too narrow | every tradition's Structure act | **Not fixed** (design pass, see §5) |

Left on purpose: "85 across 26 traditions" in the Language Codex is **correct**
(Indigenous has no phrasebook entries). "27 country cards across 11
traditions" is also correct. Hare Krishna's "twenty-five years of labor" is
a duration, not a count of traditions.

---

## 2. Islamic sections: what was fixed, added, and still recommended

The three entries are **Islam** (umbrella), **Sunni Islam** and **Shia Islam**.
Overall they are strong, fair-minded and well-framed. Every section concedes
the outside hostility Muslims face before making its case, and every
section's closing grounds the critique in the tradition's own standards.
Most problems were **overstated absolutes** (a reviewer from inside the
tradition would catch them at once) and **geographic narrowness**:
Sunni was written as Middle East/South Asia only, and Shia as almost
entirely Iran.

### Fixed (factual or overstated)

- **Sunni: the honor-killing question was the most damaging line in the section.** It said no scholar ever names honor killing as murder from the minbar. That's false: scholars across the schools condemn it. It now points at the real, documented mechanism instead. Under qisas-and-diyat law a victim's heirs can pardon the killer, and when the killer is family, the heirs are the family. Pakistan narrowed this only in 2016 (Criminal Law (Amendment) (Offences in the Name or Pretext of Honour) Act 2016). The receipt went from "[PATTERN OBSERVED]" to that statute.
- **Sunni timeline:** "Sufi orders form 850–1100" was wrong. Sufi *mysticism* spreads then, but the organized orders (tariqas) come in the 12th–13th centuries. The four schools' dates were widened to show founders active c. 700–855, with the schools consolidating afterward.
- **Sunni:** the wali (marriage guardian) genealogy was tagged [OFFICIAL POLICY] for a classical-law claim. Corrected to [ACADEMIC SOURCE].
- **Shia timeline:** "874: authority passes to scholars as deputies" compressed three centuries into one line. It now reads: Minor Occultation 874–941 with four named deputies, then the Major Occultation, and jurists claim general deputyship gradually over the following centuries.
- **Shia:** "Iran and Iraq protests against clerical governance" misdescribed Iraq. Iraq's 2019 protests targeted a sectarian political class and militia power, and Najaf *backed* the protesters' right to demonstrate.
- **Khums:** the section said offices publish "no ledger" and have "no published accounts anywhere." That's too absolute: marjaʿ networks that run registered charities abroad do file accounts. Now worded as "no audited public accounting is required," with the sharper point that where charities do file, the audit is proven possible. The sahm-e sadat half of khums, which was missing, was added.
- **Tatbir:** the "victory" of clerics discouraging child self-flagellation was vague. Now specific: Khamenei's 1994 fatwa and Fadlallah's rulings prohibiting or discouraging tatbir (blade cutting).
- **Islam:** "universities" (900–1500) changed to "madrasas". The zakat claims "publish nothing" and "criteria are unpublished" were softened to what's defensible: some state zakat bodies (Malaysia's, for example) do publish criteria, but a payer can rarely trace their own zakat.
- **Islam / Devaluation:** the example quoted "Man is weak. Man forgets. Man is ungrateful" as if it were institutional speech. It now cites the actual verses (4:28, 100:6) and names the institutional move precisely: turning scripture that calls for humility into a standing verdict on the believer.
- **Saudi Grand Mufti:** "appointed September 2025" changed to "2025", because the month couldn't be verified here. The page already tells readers to verify fast-moving seats.

### Added (gaps filled, same data shapes the page already renders)

- **Ahmadis, named precisely:** Pakistan's 1974 Second Amendment and Ordinance XX (1984), and Indonesia's 2008 joint ministerial decree. Before, they appeared only as "groups legally excluded."
- **Blasphemy receipt:** Pakistan Penal Code §295-C, and the Supreme Court's 2018 acquittal of a Christian woman after eight years on death row.
- **Branches, now complete:** Ibadi, Ahmadi, Turkey's Alevis, Sufi orders (Islam); Nizari and Dawoodi Bohra Ismailis, and Zaydis including the Houthi base (Shia).
- **Islam, "what has changed" (3 new, all by Muslims):** Morocco's 2004 Moudawana family code, India's 2017 triple-talaq ruling (Shayara Bano), Tunisia's 2017 repeal of the interfaith-marriage ban. Also added Qur'an 2:256 as the explicit standard the page measures against.
- **Sunni, Southeast Asia** (the world's largest Muslim country was nearly absent):
  - Nahdlatul Ulama and Muhammadiyah as proof that accountable Sunni institutions exist at scale.
  - Majelis Ulama Indonesia in the roster (its 2005 Ahmadiyya and anti-pluralism fatwas, and its halal role).
  - Indonesia's 2019 marriage-age reform, and the surge in court exemptions afterward.
  - Malaysia added to the regions list.
- **Shia outside Iran:**
  - Minorities (Hazara; Saudi Eastern Province; Bahrain, whose own 2011 Independent Commission of Inquiry documented torture and mass dismissals).
  - Hezbollah's welfare network and Al-Qard Al-Hassan (US Treasury designation, 2007).
  - Iraq's Popular Mobilization Forces: born of Sistani's 2014 call to arms, put on the state payroll by a 2016 law, with documented abuses.
- **Dawoodi Bohra girls and khatna (FGM/C):** the first US federal FGM prosecution (Detroit, 2017) and Australia's first FGM prosecution (2015 convictions later quashed; High Court clarified the law in 2019; charges dropped 2020 — **corrected 2026-09-27: an earlier version of this note wrongly said the High Court reinstated the convictions**), and social boycott (Maharashtra outlawed social boycott in 2016).

### Recommended, not done (needs format or wording decisions)

1. **Documented cases:** there is exactly one Islamic case among 22 (the 2022 death in custody), and none for Sunni. Draft three, in the page's existing case format:
   - *Blasphemy death sentence overturned* (islam; Pakistan Supreme Court 2018; the Punjab governor who defended her was assassinated in 2011; §295-C still in force).
   - *The Siddiqui review of sharia councils* (islam; UK Home Office independent review, 2018; recommended civil registration of Islamic marriages; the government declined to regulate the councils).
   - *Honor-killing pardon* (sunni-islam; a 2016 killing; the brother was convicted in 2019 and acquitted on appeal in 2022 after the parents pardoned him; this shows the qisas/diyat route).

   I didn't add these because I couldn't confirm the case list and its counters recount automatically. Add them to `D.cases` once that's checked.
2. **Error Ledger:** the page's own policy says corrections are recorded there with dates. Items 6–7 in §1 and the honor-killing line belong in it. I didn't write them in, because I couldn't confirm the render format for `V7.errors.corrections`.
3. **Day-in-the-life name:** the Islam composite is "Aliyah". That spelling is most strongly associated with the Hebrew word for immigration to Israel. "Aaliyah" or "Aliya" is the usual Arabic transliteration. It's a small thing, but an inside reader will notice it.
4. **Hajj "monopoly":** it's really a quota-and-licensing system (country quotas, licensed agents, the Nusuk platform). "Monopoly" overstates it. Suggest "priced through quotas and licensed agents".
5. **Salafism** runs through the Sunni entry but has no explicit treatment of its own institutions: Saudi-funded universities (the Islamic University of Madinah), translation houses, and online "approved scholar" lists. A dedicated block inside Sunni would help.
6. **Ask Abdurahman specifically** about the Sunni honor-killing framing, the "state capture of religion is the norm" line, and whether the Islam umbrella page duplicates too much of Sunni.

---

## 3. Should anything folded into the Islamic sections be its own section?

Test used: does the group have **its own offices, its own money, and its own
exit costs**, distinct from its parent? The book is about machinery, so
belief alone doesn't justify a section.

| Group | Size | Own machinery? | Verdict |
|---|---|---|---|
| **Ahmadiyya** | ~10–20M | **Yes, strongly.** A living Khalifa with global authority; formal membership; compulsory chanda (monthly dues) and the Wasiyyat bequest; a national jamaat hierarchy; its own exit and social-boycott dynamics. Also the most legally persecuted Muslim community on earth. | **Separate section — top priority.** Right now it appears only as a victim of other Muslims' machinery. That is half the picture, and the half a sceptic of the book would call selective. |
| **Sufi orders (tariqas)** | tens of millions of affiliates; crosses Sunni/Shia | **Yes.** The shaykh–disciple oath (bayʿa) is the purest obedience structure in Islam. Hereditary shrine custodians (pir, sajjada nashin), offerings (nazrana), festival economies, and Pakistan's state takeover of shrines through its Auqaf departments. | **Separate section — second priority.** Currently Sufis appear only as *targets* of purists. A cross-branch section is the natural home, just as Tibetan Buddhism sits beside Buddhism. |
| **Dawoodi Bohra** | ~1M | **Yes, and the best-documented in court of any Islamic group.** A single Daʿi al-Mutlaq; the misaq oath; permission (raza) required for life events; excommunication (baraat); khatna cases in US and Australian courts; the Bombay High Court succession case (decided 2024). | **Separate section on evidence**, on the same logic that justifies Scientology and JW. The alternative is an "Ismaili Islam" section with Nizari and Bohra as sub-parts. **Don't let Bohra evidence stand for Nizari Ismailis**; their machinery is very different. |
| Nizari Ismaili | ~12–15M | Yes (hereditary living Imam, councils, dasond tithe, AKDN) but thinly documented as coercion. | Keep inside Shia for now, or as part of an Ismaili section. |
| Salafism / Wahhabism | large | It's a current inside Sunni, not a separate body. | **Keep inside Sunni**, as a dedicated block (§2 rec 5). |
| Alevis | ~10–20M (Turkey) | Mostly on the *receiving* end of the Diyanet (the European Court of Human Rights ruled against Turkey in 2014 and 2016). | Keep as a minority row under Islam. Added. |
| Nation of Islam | tens of thousands | Distinct, but small and US-only. | Not a section. A Convert's Guide or US regional-card entry. |
| Zaydi / Houthi | ~10M | Governance plus armed movement. The documentation is mostly war reporting. | Keep inside Shia. Added to branches. |

**Recommendation:** Islam becomes a **family of five pages**: Islam (shared
foundations), Sunni, Shia, **Ahmadiyya**, **Sufi Orders**, with Dawoodi Bohra
as a sixth if you accept the evidence-over-size logic. That takes the book
from 27 to 29 or 30 traditions. Build each through the existing 33-field
record, plus its apex, turning points, sector defense and phrasebook entries.
Grade the 30 mechanisms before publishing. Have an insider reader for each:
Ahmadi and Sufi readers will be much more sensitive to framing than Sunni
or Shia readers.

---

## 4. Religions missing from the book entirely

The same test: large enough, **and** with institutional machinery that has a
documentary record. The book already bends the size rule for Scientology,
JW and Hare Krishna on record grounds, so both routes are listed.

**Strong candidates (size + record)**

1. **Anglicanism / Church of England** (~85M in the Anglican Communion). There's only one passing mention now. The record is exceptional: IICSA's Anglican investigation (2020), and the Makin review (2024) that led to the Archbishop of Canterbury's resignation. Established church, bishops in the House of Lords, Church Commissioners' endowment. It doesn't fit under "Protestant/Evangelical" without flattening both.
2. **Oriental Orthodoxy** (~60M: Coptic, Ethiopian Tewahedo, Eritrean, Armenian, Syriac, Malankara). Almost absent. Distinct hierarchies from Eastern Orthodoxy. Eritrea deposed and detained its own patriarch (2006), a state capture as clean as any in the book.
3. **Soka Gakkai** (~8M households claimed in Japan; ~12M claimed worldwide). Absent. A lay mass organization with its own publishing, contributions, and a political party (Komeito). It has large, distinct machinery.

**Candidates on record rather than size**

4. **Unification Church / Family Federation.** Only one mention now. Japan's government sought its dissolution after mass donation-harm findings, and the Tokyo District Court issued a dissolution order in 2025. That's one of the clearest state findings against a religious body anywhere.
5. **Iglesia ni Cristo** (~3M, Philippines). Bloc voting, expulsion practice, and the 2015 leadership-family dispute.
6. **Shincheonji** (South Korea). Court records from the 2020 COVID cluster, and a heavily documented recruitment method.

**Consider, lower priority:** African Initiated Churches (the Zion Christian
Church, Kimbanguism); Afro-diasporic religions (Candomblé, Vodou, Santería;
large but decentralized, with a thin coercion record); Chinese folk religion
(very large, but largely covered by the Indigenous/Folk, Taoism and
Confucianism pages); Hindu guru organizations such as BAPS Swaminarayan (a
2021 US forced-labor lawsuit) as a cross-cutting "guru movements" page;
Druze and Yazidi (small, closed, persecuted, and mostly on the receiving end).

---

## 5. Navigation: why readers get lost, and the redesign

### What loses people inside a religion

1. **Eighteen acts with literary names.** "The forefront", "Genealogy", "Reach", "The differential", "The mirror" don't tell a reader what's inside. Someone asking "what happens if I leave?" has to know that's act 10, "Cost and cover".
2. **The Islamic family is three unconnected pages with overlap.** Hijab enforcement and the 2022 death in custody appear on both Islam and Shia. Zakat is split between Islam and Sunni. A Sunni reader has to jump to the umbrella page for the history before 661 and back again, with nothing saying which page holds what.
3. **Tradition material is scattered outside the tradition.** Sunni content lives in at least eight other places: the apex table, turning points, phrasebook, regional cards (Indonesia/UK/Saudi), the Women's, Children's, Medical and LGBTQ+ volumes, the scorecard, and documented cases. None of it is linked from the Sunni page.
4. **Too many front doors.** A ~50-link sidebar, an 8-item bottom bar, a 486-cell grid, search, and the Board.
5. **Layout:** roster tables break words at desktop width. They need a wider first column or a stacked card layout like the one used at 375px.

### The redesign

**A. One tradition, one home: the "religion page".** Each tradition opens on
a single page with four parts, top to bottom:

1. **A one-screen summary.** Size, who's in charge (the apex row), where the money goes (one line), what leaving costs (one line), the one unanswered question.
2. **"What do you want to know?"** Eight plain-language question tiles that map to the existing acts. The literary act name becomes the subtitle:

| Question tile | Acts it opens |
|---|---|
| Who's in charge, and can they be removed? | Structure (03) + apex |
| Where does the money go? | Money (04), The ledger (11) |
| How did it get this way? | History (02), Genealogy (05), turning points |
| How does the pressure actually work? | The cycle (07), The loops (08), Reach (06) |
| What they say vs. what the record shows | Say versus do (09) |
| What does leaving cost? | Cost and cover (10) |
| Who gets hurt most — women, children, LGBTQ+? | The differential (12) + that tradition's rows from each volume |
| Is anyone changing it? What can I ask? | Precedent (14), Your objections (15), The mirror (16), The questions (17) |

3. **"Read it straight through":** the 18 acts, but grouped into five chapters, each marked with length and weight:
   - Meet it (Day, Forefront)
   - How it's built (History, Structure, Money, Genealogy)
   - How it works on people (Reach, Cycle, Loops, Say vs do)
   - What it costs and who gains (Cost, Ledger, Differential, Tiers)
   - What now (Precedent, Objections, Mirror, Questions)
4. **"Also about this tradition elsewhere in the book":** an auto-built panel of every regional card, phrasebook term, volume row, scorecard row and documented case tagged with this tradition's id. The data is already keyed by tradition id, so this is generated, not hand-kept, which matches the "generate from the data" rule in CLAUDE.md.

**B. Families, not flat lists.** In the traditions index, group by family
(Abrahamic → Islam → Sunni / Shia / Ahmadiyya / Sufi Orders). The Islam page
becomes the **family hub**: the shared foundations once (Qur'an, the
succession question, zakat/waqf/hajj, apostasy law), then one card per
branch saying in a sentence what's different there. Branch pages carry only
branch-specific material and link "shared foundations → Islam" at the top.
The same pattern works for Christianity, Judaism and Buddhism, which already
have umbrella-plus-branch pages.

**C. Keep your place when switching.** A breadcrumb (*Islam › Sunni ›
Money*) and a branch switcher that **keeps the act**: Sunni › Money switches
to Shia › Money, not to Shia's front page. The existing cross-compare can
open straight from here as "compare this act across the family".

**D. Fewer doors.**
- Bottom bar: Home · Traditions · Find · Your Track. Lens, Volumes and Instruments move into one "Library" sheet.
- The sidebar collapses to the five districts, with each district's links inside it.
- Search gets a scope toggle: this tradition / whole book.

**E. What not to change.** The book deliberately refuses tracking and
engagement mechanics. So no "continue reading", no progress memory, and no
read markers. "Keep your place" works through the URL only, which the hash
routes already do.

Suggested build order: A.2 and A.4 first (biggest gain, all generated from
existing data). Then B for the Islam family, alongside the new Ahmadiyya
and Sufi sections. Then C and D.

---

## 6. Waiting on you

1. **Deploy v4?** It's built and browser-checked at 375px and 1440px, with and without reduced motion: no page errors, no horizontal overflow, nothing stuck invisible, and every new addition renders. Per the project rules, deploying bumps `sites.json` to v4 and adds the matching on-page entry in the same commit. Before deploying, check Netlify snippet injection so the beacon doesn't come back.
2. **Make the live lineage the repo's canonical file.** Replace `library/faith/index.html` (old, not live) with the v4 candidate, and archive the old file under `_undeployed/`. I was stopped from moving or deleting tracked files, so this needs your go-ahead.
3. **Redeploy The Loop and The Weighing** so their menus and text use the new name. The source is already fixed.
4. Decide on the new sections (§3) and missing religions (§4).
