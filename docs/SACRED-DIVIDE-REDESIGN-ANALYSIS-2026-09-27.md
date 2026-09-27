# The Sacred Divide — redesign analysis

2026-09-27. Companion to `SACRED-DIVIDE-AUDIT-2026-09-27.md` and
`SACRED-DIVIDE-ULTIMATE-PROMPT.md`. Three questions:

1. Which navigation and information layout is best? (§1–§3)
2. Which missing religions can be filled to the same depth as the existing 27? (§4)
3. What sections should be added or strengthened inside every religion? (§5)

Facts marked *(verify)* are leads, not findings. The prompt tells the next
pass to confirm each one against a primary source before it goes on the page.

---

## 1. The problem, measured

A reader who picks a religion today faces:

- **18 acts with literary names** ("The forefront", "Reach", "The differential", "The mirror"). The name doesn't say what's inside.
- **No family level.** 27 flat traditions. Islam is three unconnected pages, and material overlaps between them: hijab enforcement and the 2022 death in custody appear on both Islam and Shia, and zakat is split between Islam and Sunni.
- **Material about one religion spread across ~9 other places:**
  - the apex table
  - turning points
  - the phrasebook
  - regional cards
  - the four people-volumes
  - the Disclosure Scorecard
  - documented cases
  - the Exit Atlas
  - the Error Ledger

  None of these are linked from that religion's page.
- **Five competing front doors:** a ~50-link sidebar, an 8-item dock, a 486-cell grid, search, and the Board.
- **Hardcoded counts** ("25 traditions" survived in 13 places after the book grew to 27). Every new religion will repeat this unless counts are computed from the data.

---

## 2. Six candidate layouts

| | Layout | One-line description |
|---|---|---|
| **A** | Question-first hub | Keep the flat index; each religion opens on 8 plain-question tiles ("Where does the money go?") mapped to the acts. |
| **B** | Family tree | Family → religion → act. Family hubs (Islam, Christianity, Judaism, Dharmic…) with a button per branch; branch pages hold only branch-specific material. |
| **C** | Compare-first matrix | The main view is a grid of religions × topics; a reader picks a row (one religion) or a column (one topic across religions). |
| **D** | Situation-first | Enter by your situation (staying / leaving / worried about someone / joining / protecting your faith / already left), then pick a religion inside a curated path. |
| **E** | Dossier | Each religion becomes one long page with a sticky table of contents and collapsible sections instead of 18 separate acts. |
| **F** | Hybrid: family hub + religion dossier | Family hub (B) → religion page opening with a summary card and question tiles (A) → acts in a sticky topic rail (E) → a **same-topic switcher** across the family → an auto-built "elsewhere in the book about this religion" panel. C and D remain as secondary tools (Compare, Your Track), not front doors. |

### Round 1 — weighted criteria

Weights reflect what readers came for (finding things about *their* religion)
and what the book must never lose (its argument and its safety stance).

| Criterion | Weight | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| Finding a religion-specific answer fast | 25 | 5 | 3 | 2 | 3 | 4 | **5** |
| Orientation — always know where you are | 15 | 3 | 5 | 2 | 3 | 4 | **5** |
| Family comparison / similar religions | 15 | 1 | 4 | 5 | 1 | 2 | **5** |
| Preserves the argument (pattern first, fair, **not a league table**) | 10 | 4 | 4 | 2 | 5 | 4 | 4 |
| Mobile ergonomics | 10 | 4 | 3 | 1 | 4 | 4 | 4 |
| Buildable in a single offline file, generated from data | 10 | 5 | 4 | 4 | 3 | 3 | 3 |
| Scales to 35+ religions | 10 | 2 | 5 | 3 | 3 | 4 | **5** |
| Calm: no engagement mechanics | 5 | 5 | 5 | 4 | 5 | 5 | 5 |
| **Weighted total /100** | | **72** | **79** | **55** | **62** | **73** | **92** |

C loses on its own terms: a religions × topics grid is visually a **harm
league table**, which the book's Method page explicitly refuses to build. D
is the best *on-ramp* but a poor *map*, because once inside a religion it
offers nothing new.

### Round 2 — five reader walkthroughs (taps to a complete answer)

| Reader | Question | Today | A | B | E | F |
|---|---|---|---|---|---|---|
| P1 · Sunni woman, UK | "Can my husband end the marriage without me? What is a sharia council?" | 8–9 taps, 3 separate places (Sunni differential, Women's Codex, the UK regional card under *Islam*) | 4, still misses the UK card | 5 | 4 | **3** (Islam → Sunni → "Who gets hurt most" tile; the UK card and Women's Codex rows come in via the elsewhere panel) |
| P2 · Ahmadi reader | "Is my community in here?" | Not findable: it appears only inside Islam, as a victim | same | **2** (visible as a branch button on the Islam hub, even as "coming soon") | same as today | **2** |
| P3 · Researcher | "Compare the money across the Islamic family" | 12+ taps, manual | not possible | 6 | not possible | **3** (Sunni › Money → switch to Shia › Money → "compare across family") |
| P4 · Ex-JW on a phone, in a hurry | "What does leaving cost?" | 5 | 3 | 5 | 3 | **3** |
| P5 · Parent, son at a madrasa | "Is he safe? What can I ask?" | 6+, and the Children's Codex is unlinked | 4 | 5 | 4 | **3** (Sunni → "Who gets hurt most" → children, with the Children's Codex row inline) |

F wins every scenario or ties. The gap is widest where material is spread
across the book (P1, P5) and where a family matters (P2, P3).

### Round 3 — adversarial critique of F (and fixes)

| Objection | Fix built into the spec |
|---|---|
| "Two navigation systems (tiles + acts) will confuse." | Tiles are **views onto acts**, not new content. Every tile names the acts it opens, and routes stay `#/r/<id>/<act>`, so nothing links to a new route. |
| "Family hubs duplicate branch content." | Hubs hold only **shared foundations** (written once) plus one "what's different here" sentence per branch. Branch pages link back to foundations at the top instead of repeating them. Remove the duplication already found in Islam and Shia. |
| "Build cost in a 3.3MB single file." | Everything new is **generated from existing data** (tradition ids already key the volumes, cards, cases and phrasebook). No new prose is needed to ship the structure. |
| "A same-topic switcher invites ranking." | It compares **within a family, one topic at a time**, with no scores, colours or ordering by severity. The evidence grade shown is the existing per-cell grade, not a total. |
| "Hub pages delay the reader." | A hub is one screen. If the reader came from a branch deep link it's skipped, and the saver returns them to the exact act. |

**Decision: F.** C survives as the existing Compare and Grid tools; D
survives as Your Track, which is also offered on each family hub.

---

## 3. The chosen design, specified

### 3.1 Families (proposed grouping — current 27 plus recommended additions in *italics*)

| Family hub | Branch buttons | "Related families" links |
|---|---|---|
| **Christianity** | Catholicism · Eastern Orthodoxy · *Oriental Orthodoxy* · *Anglicanism* · Protestant/Evangelical · Pentecostal & Charismatic · *Anabaptist & Plain* · *Plymouth Brethren (Exclusive)* | Restorationist & Adventist; Judaism |
| **Restorationist & Adventist** | Mormonism/LDS · Jehovah's Witnesses · Seventh-day Adventism · *Iglesia ni Cristo* · *Christian Science* | Christianity |
| **Islam** | Sunni · Shia · *Ahmadiyya* · *Sufi Orders* · *Dawoodi Bohra (Ismaili)* | Baháʼí (born from Babi Islam); Judaism |
| **Judaism** | Orthodox/Hasidic (+ room for Reform/Conservative as a healthy-structure contrast) | Christianity; Islam |
| **Dharmic** | Hinduism · Hare Krishna/ISKCON · *Guru movements* · Sikhism · Jainism | Buddhism |
| **Buddhism** | Buddhism · Tibetan Buddhism · *Soka Gakkai* · *Theravada monastic institutions* | Dharmic; East Asian |
| **East Asian** | Taoism · Confucianism · Shinto | Buddhism |
| **Persian-born** | Zoroastrianism · Baháʼí | Islam |
| **New movements & the spiritual marketplace** | Scientology · New Age · *Unification Church* · *Shincheonji* | (the Lens) |
| **Indigenous & folk** | Indigenous/Folk/Ancestral | — |

A religion that fits two families appears in its main one; the other family
hub gives it a "related" link, not a second copy.

### 3.2 Page templates

**Family hub** (one screen on mobile; `#/f/<family>`):

1. The family's name and one plain paragraph on what the branches share.
2. **Branch buttons**: name, size, and one line on "what's different here" (for example, "authority sits with a living Khalifa").
3. **Shared foundations**, written once: origin, shared money instruments (zakat/waqf/hajj for Islam), shared legal exposure (apostasy law).
4. **Compare one topic across the family**: pick Money / Structure / Leaving / Who gets hurt, then see each branch's one-line answer.
5. Related families, and "Your Track".

**Religion page** (`#/r/<id>`):

1. **At a glance**: size, who's in charge (apex row), money in one line, leaving in one line, the unanswered question, evidence mix (existing grade counts).
2. **Eight question tiles**, each showing the acts it opens:

| Tile | Opens |
|---|---|
| Who's in charge, and can they be removed? | Structure 03 + apex |
| Where does the money go? | Money 04 · Ledger 11 |
| How did it get this way? | History 02 · Genealogy 05 · turning points |
| How does the pressure work? | Reach 06 · Cycle 07 · Loops 08 |
| What they say vs. what the record shows | Say vs do 09 |
| What does leaving cost? | Cost & cover 10 (+ Exit Atlas row) |
| Who gets hurt most? | Differential 12 + Women / Children / LGBTQ+ / Medical rows |
| Is anyone changing it? What can I ask? | Precedent 14 · Objections 15 · Mirror 16 · Questions 17 |

3. **Read it straight through**: the 18 acts grouped into five chapters, each with a time and weight marker:
   - Meet it (Day, Forefront)
   - How it's built (History, Structure, Money, Genealogy)
   - How it works on people (Reach, Cycle, Loops, Say vs do)
   - What it costs and who gains (Cost, Ledger, Differential, Tiers)
   - What now (Precedent, Objections, Mirror, Questions)
4. **Elsewhere in the book about this religion**: auto-built from every record carrying this id (regional cards, phrasebook, volume rows, scorecard row, cases, turning points, Error Ledger entries).

**Act page**: unchanged content, plus:

- a breadcrumb: *Islam › Sunni › Money*
- a **same-topic switcher** across the family (Sunni › Money → Shia › Money)
- prev/next inside the chapter
- the sticky topic rail on desktop, or a bottom-sheet on mobile

### 3.3 Global navigation

- **Dock (4):** Home · Religions · Find · Your Track. Lens, Volumes and Instruments move into one "Library" sheet.
- **Sidebar:** collapses to the five districts, plus the saver toggle and "Show the introduction again".
- **Search:** a scope toggle (this religion / whole book), and results grouped by religion.
- **Counts:** every number such as "27 traditions" or "12 instruments" is **computed from the data at render time**, never typed.

### 3.4 Constraints that do not move

- Single self-contained HTML file.
- No CDN.
- Fonts and icons inline.
- Works offline (the counter simply fails silently).
- The Cloudflare counter stays (owner decision).
- The section saver stays: on-device only, switchable off.
- No streaks, badges, "% complete", notifications, or engagement mechanics of any kind.
- Dark theme, MOVEMENT labels, numbered cards.
- Reduced-motion support.
- 375px first.

---

## 4. Missing religions — can each be filled like the others?

**Fillability test.** A new religion must be able to fill the same record as
the existing 27, including:

- a composite "day"
- a dated timeline
- a named apex with a removal route
- money flows with at least one financial filing or official figure
- exit costs with a documented source
- a named roster
- the phrasebook
- middle tiers
- differential harms
- victories
- 30 mechanism entries with defenses
- a sector defense
- turning points
- compel/revise lines
- **at least two documented cases** (court, inquiry, regulator)

Grades:

- **Full** — every field can be sourced.
- **Partial** — most can; one or two acts will read thin and must say so.
- **Thin** — the institution or the record is not there; a section would have to invent structure. Recommend against.

### Priority 1 — Full, and add

| Religion | Family | Size | Why it fills | Anchor records *(verify each)* |
|---|---|---|---|---|
| **Ahmadiyya** | Islam | ~10–20M | Living Khalifa; chanda dues and the Wasiyyat bequest; national jamaat hierarchy; exit/boycott; unique legal persecution | Pakistan 2nd Amendment 1974, Ordinance XX 1984; Indonesia 2008 decree; UK charity accounts of the Ahmadiyya Muslim Jamaat |
| **Anglicanism** | Christianity | ~85M | Established church, bishops in the Lords, a large endowment, a clear apex | IICSA Anglican Church investigation (2020); Makin Review (2024) and the Archbishop's resignation; Church Commissioners' 2023 report on historic links to transatlantic slavery; current Archbishop *(verify)* |
| **Oriental Orthodoxy** | Christianity | ~60M | Distinct patriarchates; state entanglement | Eritrea's removal and house arrest of Patriarch Antonios (2006–); Ethiopian Orthodox 2023 synod crisis; 2025 Armenian government–Catholicos confrontation *(verify)* |
| **Dawoodi Bohra** | Islam | ~1M | One Daʿi; misaq oath; raza permissions; baraat excommunication | US v. Nagarwala (2017); A2 v The Queen, High Court of Australia (2019); Bombay High Court succession judgment (2024); Maharashtra social-boycott law (2016) |
| **Unification Church / Family Federation** | New movements | ~100k+ active *(verify)* | Donations, mass weddings, state finding | Japanese government dissolution request (2023) and Tokyo District Court dissolution order (2025) *(verify appeal status)*; "spiritual sales" damage judgments |
| **Plymouth Brethren Christian Church (Exclusive Brethren)** | Christianity | ~50k | Doctrine of separation; withdrawal/shunning; its own school network; political funding | UK Charity Commission / Preston Down Trust (2012–14); Australian and NZ election-campaign funding reporting; OneSchool Global |
| **Soka Gakkai** | Buddhism | ~8M households claimed (Japan) | Mass lay organization, newspaper, contributions, a political party | Komeito relationship; 1991 break with Nichiren Shoshu; Diet debates on separation of religion and state *(verify)* |

### Priority 2 — Full or Partial, add after Priority 1

| Religion | Family | Grade | Notes |
|---|---|---|---|
| **Sufi Orders** | Islam | Partial→Full | The shaykh–murid oath, pir/sajjada-nashin inheritance, shrine offerings, Pakistan's Auqaf takeover of shrines (1959–60 *(verify)*). The coercion-case record is thinner; Cost and Differential will lean on academic sources. |
| **Iglesia ni Cristo** | Restorationist | Partial | Bloc voting, expulsion, the 2015 leadership-family dispute. English sources are moderate. |
| **Anabaptist & Plain (Amish, Old Order Mennonite, Hutterite)** | Christianity | Partial | Meidung/shunning; colony property on expulsion (*Hofer v. Lakeside Colony*, Supreme Court of Canada 1992 *(verify)*); abuse-reporting investigations. |
| **Shincheonji** | New movements | Partial | The 2020 COVID cluster and prosecutions *(verify outcomes)*; a documented recruitment method. |
| **Guru movements** (BAPS, Isha, Art of Living, Sathya Sai, Rajneesh) | Dharmic | Partial | Better as **one cross-guru page** than several thin ones. BAPS 2021 US forced-labour suit *(verify status)*; the Rajneeshpuram record (1980s) is extensive. |
| **Theravada monastic institutions** (Thai Sangha, Dhammakaya) | Buddhism | Partial | The Wat Phra Dhammakaya embezzlement case and 2017 siege *(verify)*; Sangha Supreme Council under state law. |
| **Christian Science** | Restorationist | Partial (small) | Medical-neglect prosecutions (Twitchell, 1990s *(verify)*); strong on Medical, thin elsewhere. |
| **International Churches of Christ** | Christianity/Restorationist | Partial (small) | 2023 US lawsuits *(verify)*; a discipling hierarchy. |

### Recommend against a full section (Thin) — mention inside another page instead

| Religion | Why | Where it belongs instead |
|---|---|---|
| Afro-diasporic religions (Candomblé, Umbanda, Vodou, Santería) | Decentralized houses; little institutional record; high risk of repeating colonial stigma | Indigenous & folk page: a paragraph on the *persecution* record (Brazil terreiro attacks) |
| Chinese folk religion | No institution beyond state regulation | East Asian family hub |
| Rastafari, Wicca / neo-paganism | No institutional machinery | Not included; say so in "Why isn't X here?" |
| Druze, Yazidi | Closed communities; Yazidi post-genocide; the record is about harm *to* them | Islam family hub "related" note; the Regional Variants volume |
| Nation of Islam | Small, US-only | Islam family hub "related" card + US regional card |
| Cao Dai, Tenrikyo | Thin in English | Revisit if sources are found |
| Falun Gong | A heavily contested record on both sides (state persecution vs. recent reporting on its media and performing arts arms) | Only with a dedicated evidence review; otherwise leave out and say why |

**Add a public "Why isn't X here?" note** listing this table's reasoning. It
answers the obvious question and keeps the inclusion rule transparent.

**Counts after Priority 1: 27 → 34 religions.** This is why every count must be computed.

---

## 5. New or strengthened sections inside every religion

| # | Section | New / enhance | Why |
|---|---|---|---|
| 1 | **At a glance** card | New | Orientation in one screen. It's the top reason readers get lost today. |
| 2 | **What healthy looks like here** | Enhance: surface the existing `healthy` field as its own act | Fairness. Insiders need to see their tradition's best practice named, and the book's own standard (the Mirror) depends on it. |
| 3 | **Law & state here** | New | Apostasy/blasphemy statutes, religious courts, charity law, church tax, state temple boards, officeholder appointment. Currently scattered across Money, Cost, apex and regional cards, and it's the most-asked question for Islam, Hinduism (temple boards) and the state churches. |
| 4 | **Money in numbers** | New | Where a filing exists, show the figures (Church Commissioners, the LDS SEC order, Watchtower property sales, UK charity accounts). Turns "unaudited" from an assertion into a visible gap. |
| 5 | **Documented cases** (≥3 each) | Enhance | 22 cases for 27 traditions; Sunni has none. Cases are the book's strongest evidence type. |
| 6 | **Voices from inside** | New (grows out of Victories) | Reformers, scholars and survivors *from the tradition*, in their own published words. It counters the "outsider attack" reading, which matters most for Islam. |
| 7 | **Branches & variants** | New | Which branches differ on each act. It feeds the family hub's compare row. |
| 8 | **Regional variants** | Enhance: 11 → all | Law and exit costs change more by country than by doctrine. |
| 9 | **Who gets hurt most** | Enhance | Pulls this religion's rows from the Women's, Children's, LGBTQ+ and Medical volumes into one place. |
| 10 | **Leaving safely here** | New | Practical and jurisdiction-specific: legal jeopardy, custody, documents, money, quiet exits. The Exit Atlas row plus the calculator, pre-filtered. |
| 11 | **Where to get help** | New | Dated, vetted support and legal organizations per religion and region, reviewed each edition. The book currently has no resources hub, which the design standard asks for. |
| 12 | **Words used here** | Enhance | That religion's phrasebook entries inline, not only in the Language Codex. |
| 13 | **Sources for this page** | New | A per-religion bibliography with grade counts. Makes fact-checking and insider review possible. |
| 14 | **What changed on this page** | New | A per-religion slice of the Error Ledger and version notes, so insider reviewers like Abdurahman can see their corrections land. |

Priority order for building: 1, 5, 9, 3, 13, 14 (all mostly generated or
sourced from existing data), then 2, 7, 12, then the research-heavy 4, 6,
8, 10, 11.
