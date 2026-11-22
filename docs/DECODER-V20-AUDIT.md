# Pattern Decoder update package: audit (2026-11-09, before any change)

Package: `Playbook_Update_Package.zip` (owner upload). Nothing has been changed yet.

## Matches the live Decoder (v19, 310 tactics)
- Same 10 lines (people, wear, pressure, control, systems, blame, truth, society, online, hook) and the same 21 fields.
- All 310 live tactics are accounted for in `LIVE_ENTRY_CHANGES.csv`; none missing, none invented.
- The 174 kept + 51 renamed tactics carry the live text word for word (0 differences), none moved line.
- New list: 335 tactics, every field filled, no duplicate names. The 110 new ones are the same size and style as the
  existing ones (avg 7.9 KB vs 8.2 KB).
- Safety scan of the 110 new: 0 named companies/organisations, 0 diagnosis labels, 0 percentage claims, 0 Noble Father
  wording; "do not confront" appears only as safety advice; 86 of 110 route to emergency or specialist help. 10 mention
  children without naming a route in the safety note (review list: Forced Continuity, Initiative Churn, Deniable
  Authorization, Buried Consent, Celebration as Cover, Captive Expertise, Language Laundering, Data Onward Sharing,
  That's-Not-All, Reputation Braiding).

## Must be handled, or the update does damage
1. **Big search terms would lose their pages.** 32 tactics move to "patterns" (11 effects, 11 umbrellas, 10 built-in
   combos) and 3 are removed. They include **Gaslighting, DARVO, FOG, Trauma Bonding, Learned Helplessness, Fawning,
   Mobbing, Pig Butchering** and the Feminine book's own **"Good Woman Program"**. These are among the most searched
   words in this whole field. Fix: a Patterns section where each keeps its own page at the SAME address, with its live
   text plus "made of" links to its single tactics. No page is lost.
2. **136 addresses change** (51 renames, 50 merges, 32 patterns, 3 removed). 187 links from the books point at 43 of
   them (e.g. intermittent-reinforcement 24, trauma-bonding 5). Fix: a permanent redirect from every old address to its
   new page, then rebuild the book pages so their links use the new names directly.
3. **73 of 109 combos ("recipes") use a pattern or removed tactic** (251 references to changed names). Fix: map each
   reference through the package's alias map; a pattern step expands to its parts or stays as a pattern link.
4. **Search must still find old names.** Every old name goes into the search aliases (`standard_index.json` has them).
5. **Who owns the new writing?** The package comes from the `miakamikee1101-collab/mieee` repo and its own rules say
   "Noble Father wording must not be copied into our own lists", which reads like a separate project. The 110 new
   entries will be published under your licence (CC BY-NC-ND, © Shae Stovell). Confirm that repo is yours, or that its
   owner agrees.

## Plan once approved (v20)
1. Build from `content/playbook-data.json` + package: 335 tactics, a Patterns section (32 pages), old names searchable.
2. Redirects for all 136 old addresses; combos remapped; version note + `sites.json` changelog.
3. Two-way links: each tactic page gets "Where this shows up in the books" (generated from the same term matching the
   books already use); then rebuild the seven books' links.
4. Checks: Decoder suite, every old address resolves, axe, speed, phone/desktop screenshots, then ask before deploying.
