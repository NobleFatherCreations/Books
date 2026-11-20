# TikTok book deck v2: book descriptions / highlights, in play order.
# Each book = cover slide + hook card + 4-5 highlight slides (Fractal gets 6).
# Facts come from the catalogue PDF (Oct 2026), BOOKS.md and, for the
# Decoder, the live v20 data (335 tactics, 32 patterns, 21 fields each).
# Edit here, then: python3 content/tiktok-deck/build.py
#
# Section shapes: {"h", "p": [...]} prose | {"h", "items": [(name, desc)]}
# | {"h", "bullets": [...]} | {"h", "acro": [(letter, word)]}
# Every section is written to fit ONE slide; render.mjs warns if one spills.

DONATE = [("Cash App", "$shaestovell"), ("Venmo", "@noblefather")]

INTRO = [
 {"k": "Noble Father Creations · Shae Stovell",
  "h": "Words for the things we *can't name*",
  "p": "Fifteen books and one guided practice about how people get steered: in love, in families, at school, at work, in faith, online, at festivals, and by the systems we all live inside."},
 {"k": "One library, many doors",
  "h": "Something feels wrong. *Here's the word for it.*",
  "bullets": ["Women, men and kids", "Parents, carers and adult children", "Believers and people leaving faith",
              "Workers, festival-goers and anyone online", "People who have left, and people who caused harm",
              "Counsellors, teachers, advocates and the people who train them"]},
 {"k": "How they help",
  "h": "Name it. Check it. *Know what to do next.*",
  "p": "Each book names the tactic, shows how to tell it apart from an ordinary bad day, and gives real next steps: scripts, checklists, safety plans and where to get help. Written by a person, in plain words."},
 {"k": "Free. Really.",
  "h": "100% free. *Always.*",
  "bullets": ["No paywall, no account, no sign-up", "Nothing tracked, nothing sold", "Works on any phone, even offline",
              "Donations welcome, never required"],
  "donate": True},
]

OUTRO = [
 {"k": "The whole library",
  "h": "Find the one *you need.*",
  "p": "Every book and the Root are free to read today. If one helped, send it to the person it would help next.",
  "big": "noblefathercreations.com",
  "donate": True},
]

BOOKS = [
# ---------------------------------------------------------------- DECODER
{
 "slug": "decoder", "title": "The Pattern Decoder", "sub": "335 manipulation tactics, named in plain words, so you can trust what you're seeing.",
 "kicker": "The instrument", "url": "noblefathercreations.com/playbook",
 "cover": "covers/decoder.jpg",
 "chips": ["335 tactics", "32 patterns", "10 lines", "Private"],
 "sections": [
  {"h": "What it is", "p": [
   "A free lookup tool for the moment you ask yourself *is this normal?*",
   "It names **335 tactics** of manipulation and control, plus **32 well-known patterns** like Gaslighting, DARVO and Trauma Bonding, and shows what each is built from.",
   "Type what happened, paste a phrase you were told, or answer a few gentle questions, and it shows you what it might be."]},
  {"h": "Inside every tactic", "bullets": [
   "What it is, what it sounds like, and why it hurts",
   "Signs it might be this, and signs it's probably something else",
   "Innocent explanations and common false alarms, checked first",
   "Questions to ask yourself, and what makes it more or less concerning",
   "What to do: response options, a boundary script and a safety note",
   "Look-alike tactics, and where it shows up in the other books"]},
  {"h": "Ten lines, one map", "p": [
   "The tactics are laid out like a transit map: ten colour-coded lines, from **Twisting what is real** and **Love that hooks you** to **Work, school and systems** and **Groups, cults and propaganda**.",
   "\"Change here\" links connect tactics that look alike, so you can compare two side by side and tick the signs that fit."]},
  {"h": "What makes it different", "p": [
   "Most guides give you ten famous words. This is a full map of 335, across relationships, families, work, online life and whole groups, every one written to the same standard.",
   "It's careful in both directions: each entry checks for an innocent explanation first and warns against using the word as a weapon. Safety comes first on the riskiest entries."]},
  {"h": "Built for someone frightened", "bullets": [
   "A green Leave button, always in reach",
   "No account, nothing stored, safe on a shared or watched phone",
   "Calm mode, larger text, works offline",
   "Every tactic has its own page, so a search finds the answer",
   "For anyone unsure, and for the helplines, advocates, counsellors and friends sitting beside them"]},
 ]},
# ---------------------------------------------------------------- FEMININE
{
 "slug": "feminine", "title": "The Sovereign Divine Feminine", "sub": "A field guide to psychological manipulation: tactics, names, and counter-moves.",
 "kicker": "For women", "url": "noblefathercreations.com/feminine",
 "cover": "covers-existing/feminine.jpg",
 "chips": ["42 chapters", "30-minute rescue", "Scripts for HR, medical, legal"],
 "sections": [
  {"h": "What it is", "p": [
   "A 42-chapter manual for women facing manipulation in love, family, work, institutions, online and in high-control groups.",
   "It covers the whole arc: how the hook is set, how control tightens, how to interrupt it in real time, how to document it, and how to rebuild after. If you're in crisis, a **30-Minute Rescue** opens the book."]},
  {"h": "The SOVEREIGN framework", "acro": [
   ("S", "Spot"), ("O", "Orient"), ("V", "Validate"), ("E", "Establish the frame"), ("R", "Respond"),
   ("E", "Enforce"), ("I", "Invest"), ("G", "Ground"), ("N", "Navigate")]},
  {"h": "Inside", "bullets": [
   "Love bombing, trauma bonding, DARVO, weaponised therapy-speak, medical gaslighting, PIPs and false reports",
   "Word-for-word scripts and if-then plans for each tactic",
   "A searchable script library and decision trees",
   "Somatic tools for a nervous system on high alert",
   "Exit logistics, and a life-design section for after"]},
  {"h": "What makes it different", "p": [
   "It gives you language that works. Its **lexicon translator** turns \"he dismissed my pain\" into words HR, doctors and courts actually respond to.",
   "It's specific enough to use mid-situation, at 2am, when you're working out what to send. And it reclaims feminine power without making men the enemy."]},
  {"h": "Who it's for", "bullets": [
   "Women in it right now, or trying to get out",
   "Mothers and daughters reading together",
   "Counsellors and social workers, as a teaching text",
   "Domestic-violence services"]},
 ]},
# ---------------------------------------------------------------- LONG AFTER
{
 "slug": "longafter", "title": "The Long After", "sub": "What happens once you have left.",
 "kicker": "For women, after leaving", "url": "noblefathercreations.com/longafter",
 "cover": "covers/longafter.jpg",
 "chips": ["45 chapters", "7 movements", "Years 2, 5 and 10"],
 "sections": [
  {"h": "What it is", "p": [
   "For many people, leaving doesn't end the abuse. It changes the channel: the children, the money, the story told to friends, the court, the phone.",
   "This 45-chapter guide starts where most resources stop, at the door, and picks up where The Sovereign Divine Feminine ends."]},
  {"h": "Inside", "bullets": [
   "Post-separation abuse: hoovering, surveillance, the new partner, the smear campaign",
   "What to document, and how",
   "Family court honestly, legal aid with no money, protective orders, housing and benefits",
   "What your nervous system is doing, and why it's normal",
   "Rebuilding: people, money, a life of your own"]},
  {"h": "What makes it different", "p": [
   "It covers years two, five and ten, where so much harm and so much recovery quietly happens.",
   "It's the most patient voice in the library: short paragraphs, no \"by six months you should…\" timelines, and never telling you how to feel. Built to be read slowly and opened at 2am."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who left and found it followed them",
   "Anyone wondering \"maybe I'm still the problem\"",
   "Friends and family supporting someone after",
   "Support services holding cases that \"closed\" years ago"]},
 ]},
# ---------------------------------------------------------------- CHILDREN
{
 "slug": "children", "title": "Playground Protectors", "sub": "A kids' guide to tricky people, power-ups, and building real friendships.",
 "kicker": "For kids", "url": "noblefathercreations.com/children",
 "cover": "covers-existing/children.jpg",
 "chips": ["28 missions", "4 worlds", "Ages 7 to 12", "Read together"],
 "sections": [
  {"h": "What it is", "p": [
   "An illustrated book of 28 missions across four worlds, made for kids about 7 to 12 to read with a grown-up.",
   "It's a game: manipulation tactics are **tricks**, that funny feeling is a **Wait a Minute Feeling**, and the responses are **Power-Ups**. Kids level up into Playground Protectors."]},
  {"h": "The tricks kids learn to spot", "items": [
   ("The Memory Mixer-Upper", "gaslighting"),
   ("The Super-Fast Best Friend", "love bombing"),
   ("The Hot-and-Cold Game", "intermittent reinforcement"),
   ("The Whisper Game", "triangulation"),
   ("The Group-Up", "social exclusion"),
   ("The Internet Ghost", "catfishing and online safety")]},
  {"h": "How every mission works", "bullets": [
   "A story, then the feeling it causes, then how the trick works",
   "Moves and counter-moves, with real words to say",
   "Accident or on purpose? How to tell the difference",
   "A traffic light: green and yellow kids can handle, red means tell a trusted grown-up",
   "A mission to try for real"]},
  {"h": "What makes it different", "p": [
   "Most kids' books cover feelings, kindness or obvious bullying. This one teaches the quieter stuff: guilt trips, silent treatment, jealousy as control, the friend who's lovely then cruel.",
   "Kids become the hero, not the victim, so there's no shame in it. And reading together gives the family a shared language for hurts that are hard to explain."]},
  {"h": "Who it's for", "bullets": [
   "Kids about 7 to 12",
   "Parents and carers, reading together",
   "Parents who never had these words as kids",
   "Therapists and school counsellors"]},
 ]},
# ---------------------------------------------------------------- WOOK
{
 "slug": "wook", "title": "The Festie Codex", "sub": "A field manual for spotting wooks in sheep's clothing.",
 "kicker": "Wook in sheep's clothing", "url": "noblefathercreations.com/wook",
 "cover": "covers-existing/wook.jpg",
 "chips": ["33 chapters", "Appendices A to Z", "Zine voice"],
 "sections": [
  {"h": "What it is", "p": [
   "A 33-chapter festival harm-reduction manual written like a zine, laid out like a setlist: Know the Pattern, Read the Room, and an Encore.",
   "Three rules carry through it: *Know the pattern. Trust your body. Protect the magic.*"]},
  {"h": "Inside", "bullets": [
   "The person who befriends you at the gate",
   "The group chat that becomes a leash",
   "A dosing that wasn't your choice",
   "The \"family\" that isn't, and the missing friend",
   "The comedown, and getting home"]},
  {"h": "The A to Z toolkit", "bullets": [
   "Consent and capacity quick references",
   "A bystander-interruption kit",
   "Good Samaritan law guidance",
   "A pre-event checklist and a long-exit plan",
   "A directory of safety organisations"]},
  {"h": "What makes it different", "p": [
   "It's written by someone from the scene, not handed down from above. No lecturing, no judging, so it reaches the people who'd bin an official leaflet.",
   "The goal: hand you the pattern at the gate, before someone else decides who you are this weekend."]},
  {"h": "Who it's for", "bullets": [
   "Festival-goers, first-timers to veterans",
   "Friends looking out for each other",
   "Event teams, welfare and harm-reduction crews"]},
 ]},
# ---------------------------------------------------------------- FESTIVAL
{
 "slug": "festival", "title": "The Festie Bible", "sub": "Twenty-one field guides for the whole festival world.",
 "kicker": "The Festival Bible", "url": "noblefathercreations.com/festival",
 "cover": "covers-existing/festival.jpg",
 "chips": ["21 guides", "About 270 scenarios", "Video scripts"],
 "sections": [
  {"h": "What it is", "p": [
   "A scenario-based reference of 21 guides, about 270 real situations and roughly 128,000 words on staying psychologically safe across the whole festival world.",
   "It's written for the people who go, and for the people who make it happen."]},
  {"h": "Inside", "bullets": [
   "Scenarios checked against what actually happens in each part of the scene",
   "Physical and environmental risks most guides miss, including crowd crush",
   "Short video scripts for training and outreach",
   "Guides for attendees, crew, vendors, volunteers and welfare teams"]},
  {"h": "What makes it different", "p": [
   "It gives a whole community one shared language for safety, so a volunteer, a vendor and a first-timer can say the same thing in the same moment.",
   "It turns what the scene has always known informally into something that can be taught."]},
  {"h": "Who it's for", "bullets": [
   "Attendees",
   "Volunteers, vendors and crew",
   "Festival operators",
   "Welfare and medical teams",
   "Harm-reduction groups and event-safety trainers"]},
 ]},
# ---------------------------------------------------------------- FRACTAL
{
 "slug": "fractal", "title": "The Fractal", "sub": "How one pattern runs the world.",
 "kicker": "The pattern", "url": "noblefathercreations.com/fractal",
 "cover": "covers-existing/fractal.jpg",
 "chips": ["30 sectors", "8 stages", "30 techniques", "3 scales"],
 "sections": [
  {"h": "What it is", "p": [
   "The cycle people learn about in abusive relationships doesn't stop at the edge of the relationship. It scales into every system we've built.",
   "The Fractal maps one eight-stage cycle across thirty sectors of life. The aim isn't to fight it. It's to see it, because a pattern you can see is a pattern you can exit."]},
  {"h": "One cycle, eight stages", "items": [
   ("Idealize · Hook", "Love bombing, weaponized generosity, future faking, hoovering"),
   ("Devalue · Confuse", "Gaslighting, double binds, moving goalposts, DARVO"),
   ("Isolate · Extract", "Triangulation, smear campaigns, trauma bonding, financial control"),
   ("Discard · Replace", "Manufactured crisis, replacement, plausible deniability")]},
  {"h": "Thirty sectors, three scales", "p": [
   "Religion, politics, media, education, healthcare, finance, tech, family, dating, law, prisons, the military, housing, food, beauty, sport and more.",
   "Each is read at three scales: **one person** doing it to another, an **institution** calling it policy, and a **civilization** where it's so normal it's invisible."]},
  {"h": "Beyond the map", "p": [
   "Closing chapters keep it from ending in despair: **The Origin** (how the pattern was installed, and why it wasn't inevitable), **The Spiritual Lens**, **The Somatic** (what it does to the body), **The Epigenetic** (how it passes down), **The Original Frequency** (what came before) and **The Earth**."]},
  {"h": "What makes it different", "p": [
   "It's a bridge. Readers arrive from something personal, \"my therapist calls it narcissistic abuse, and I keep seeing it everywhere\", and leave with a map of the whole structure.",
   "Every sector speaks to its own people, from survivors of religious abuse to burned-out nurses, dismissed patients, tech workers and immigrants."]},
  {"h": "Who it's for", "bullets": [
   "Abuse survivors who keep seeing the pattern everywhere",
   "Professionals feeling the gap between their values and their systems",
   "Activists who watched reform get absorbed",
   "Young people working out what they're inheriting",
   "Therapists, educators, organisers and parents"]},
 ]},
# ---------------------------------------------------------------- FRACTURE
{
 "slug": "fracture", "title": "The Fracture", "sub": "The wealth transfer, told from the public record. 195 citations.",
 "kicker": "The money behind it", "url": "noblefathercreations.com/fracture",
 "cover": "covers-existing/fracture.jpg",
 "chips": ["12 episodes", "195 citations", "$50 trillion"],
 "sections": [
  {"h": "What it is", "p": [
   "A documentary-style read in twelve episodes about a documented **$50 trillion** wealth transfer: where the money went, who received it, and how that machinery shows up in ordinary lives.",
   "It's The Fractal's companion: one pattern, followed to the money."]},
  {"h": "Inside the twelve episodes", "bullets": [
   "The ownership class and the five wealth tiers",
   "The six loops that keep extraction running and absorb reform",
   "The official language, read against the record",
   "Why replacing the person in charge changes nothing",
   "What it does to the body, and who it hits hardest",
   "Times it was broken before, and an action map for every scale"]},
  {"h": "What makes it different", "p": [
   "Every factual claim comes from the public record: court filings, SEC disclosures, peer-reviewed research, government reports, congressional records and established investigative journalism, across 43 years.",
   "It doesn't ask you to believe a conspiracy. It asks you to check a structure."]},
  {"h": "It answers three questions", "items": [
   ("Is it real?", "With data."),
   ("Why doesn't change come?", "With structure."),
   ("What can I do?", "With leverage points, not promises.")]},
  {"h": "Who it's for", "bullets": [
   "People who tried reform and want to know why it was absorbed",
   "Data-minded skeptics who need proof",
   "Middle-tier professionals: managers, teachers, doctors, lawyers",
   "Organisers and researchers"]},
 ]},
# ---------------------------------------------------------------- FAITH
{
 "slug": "faith", "title": "The Sacred Divide", "sub": "Honor the faith. Name the machinery.",
 "kicker": "The faith book", "url": "noblefathercreations.com/faith",
 "cover": "covers-existing/faith.jpg",
 "chips": ["34 traditions", "10 families", "27 sections each"],
 "sections": [
  {"h": "What it is", "p": [
   "A reference to how institutional power works inside **34 religious traditions**, from Catholicism and Sunni Islam to Hinduism, Mormonism, Scientology and Indigenous religions.",
   "It isn't written against faith. It separates faith from the coercive machinery that can grow around it, and holds every tradition to the same test."]},
  {"h": "Every tradition page", "bullets": [
   "At a glance: who's in charge, who chose them, who can remove them, where the money comes from, what leaving costs",
   "History, authority, law and reach into children and bodies",
   "30 documented control tactics, each graded by evidence",
   "Documented cases and voices from inside",
   "How to leave safely, and where to get help"]},
  {"h": "One example: Catholicism", "items": [
   ("Chosen by", "A conclave whose every elector was appointed by a previous pope"),
   ("Removable by", "Nobody. Canon law has no mechanism to remove a pope"),
   ("Leaving", "Can bring excommunication and the denial of the sacraments")]},
  {"h": "What makes it different", "p": [
   "Its consistency is its credential. Same 27 sections, same evidence standard, every claim sourced, so no one can say theirs was singled out.",
   "Believers get questions to ask inside their own tradition. People leaving get a map and a safe-exit page. Nobody is told what to believe. A quick-exit button is on every page."]},
  {"h": "Who it's for", "bullets": [
   "Believers, former believers and the people who love them",
   "People leaving high-control communities",
   "Clergy, chaplains and interfaith groups",
   "Journalists, researchers and survivors"]},
 ]},
# ---------------------------------------------------------------- SILENCE
{
 "slug": "silence", "title": "The Silence", "sub": "For men nobody thought to ask.",
 "kicker": "For men", "url": "noblefathercreations.com/silence",
 "cover": "covers/silence.jpg",
 "chips": ["46 chapters", "7 movements", "Beside, not instead"],
 "sections": [
  {"h": "What it is", "p": [
   "A 46-chapter guide for men in coercive relationships: how to recognise it, what help actually exists, and what to do next.",
   "It sits beside The Sovereign Divine Feminine, never instead of it."]},
  {"h": "Inside", "bullets": [
   "The fog, being managed, money and sex as currency",
   "Children used as leverage, and being provoked into being \"the bad one\"",
   "The reversal, the police call, violence you're not allowed to name",
   "Why you haven't said anything",
   "What's actually available, and life out and after"]},
  {"h": "What makes it different", "p": [
   "It's written to be believed by a reader who's been told his experience isn't serious. Plain, direct, deliberately less literary.",
   "It was built on one rule: no chapter can be quoted as an argument for cutting women's services. Men get the same quality of language and help other survivors get, without turning it into a grievance."]},
  {"h": "Who it's for", "bullets": [
   "Men in coercive relationships",
   "Men told no one would believe them",
   "Services that want to support men without taking sides",
   "Women's services, who can trust it won't undercut their work"]},
 ]},
# ---------------------------------------------------------------- REPAIR
{
 "slug": "repair", "title": "The Repair", "sub": "For the person on the other side of it.",
 "kicker": "For the person who caused harm", "url": "noblefathercreations.com/repair",
 "cover": "covers/repair.jpg",
 "chips": ["48 chapters", "7 movements", "Behaviour change"],
 "sections": [
  {"h": "What it is", "p": [
   "A 48-chapter book for people who have harmed someone and want to change. It's the densest in the library.",
   "Its measure of success is behaviour change, judged over months by the people affected. Insight and remorse don't count on their own."]},
  {"h": "Inside", "bullets": [
   "The honest inventory: what you actually did",
   "The pattern you'd spot instantly in someone else",
   "Causes, not excuses",
   "The people you did it to, and how to stop",
   "Amends done properly, and the rest of your life",
   "Most chapters end with a concrete thing to try"]},
  {"h": "What makes it different", "p": [
   "It blocks both easy exits by name: \"I'm a monster\" and \"I'm actually fine.\"",
   "Its rule: if a paragraph would make you feel better without changing what you do on Thursday, it was cut. No warmth that reads as absolution, and no condemnation that makes you defensive."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who has caused harm and wants to change",
   "The person who looked it up at 3am",
   "Programmes working with people who cause harm",
   "Survivors' advocates, who can read it without wincing"]},
 ]},
# ---------------------------------------------------------------- AT WILL
{
 "slug": "atwill", "title": "At Will", "sub": "The coercive workplace.",
 "kicker": "For workers", "url": "noblefathercreations.com/atwill",
 "cover": "covers/atwill.jpg",
 "chips": ["47 chapters", "7 movements", "Your job"],
 "sections": [
  {"h": "What it is", "p": [
   "A 47-chapter guide that runs The Fractal's eight-stage cycle on a job, and shows when a bad job has become a coercive one.",
   "Written for a lunch break, or the car park before a shift."]},
  {"h": "Inside", "bullets": [
   "\"We're a family\", and passion as a pay cut",
   "Manufactured urgency, the moving target, recognition instead of pay",
   "The review used as a weapon, and the improvement plan that's really a firing",
   "NDAs, non-competes, arbitration, gig classification, surveillance, wage theft",
   "What you're actually owed, and your real options"]},
  {"h": "What makes it different", "p": [
   "It names the harm that happens with no villain, where incentives produce it on their own, without excusing the people who do choose it.",
   "It builds a record-keeping habit before you need a lawyer. Employment law varies by place, so it teaches the pattern everywhere and points you to local specifics."]},
  {"h": "Who it's for", "bullets": [
   "Anyone dreading Monday and not sure why",
   "Workers facing a review, a PIP or a quiet push out",
   "HR leads who want to do it right",
   "Unions and workplace advocates"]},
 ]},
# ---------------------------------------------------------------- SLOW TAKE
{
 "slug": "slowtake", "title": "The Slow Take", "sub": "Elder financial exploitation, for the adult child.",
 "kicker": "For adult children", "url": "noblefathercreations.com/slowtake",
 "cover": "covers/slowtake.jpg",
 "chips": ["45 chapters", "7 movements", "Later life"],
 "sections": [
  {"h": "What it is", "p": [
   "A 45-chapter guide to coercion and financial exploitation in later life, written for the adult child.",
   "An older person being isolated and drained is the least likely to search for help. Their son or daughter is the one who searches."]},
  {"h": "Inside", "bullets": [
   "The new friend, the isolating sibling, the phone that rings at the same time every day",
   "Romance late in life, paperwork that appeared, the will that changed",
   "Care that became control, and exhaustion that isn't malice",
   "Following the money, and power of attorney",
   "Who does it: family, carers, professionals, scammers, institutions"]},
  {"h": "What makes it different", "p": [
   "It refuses to pick a side. Autonomy isn't safety, and safety isn't the only value: your parent keeps the right to make bad decisions.",
   "It's honest that guardianship can be abused too, and includes a chapter called \"Am I the one benefiting?\" Set for a frightened reader scanning on a phone."]},
  {"h": "Who it's for", "bullets": [
   "Adult children worried about a parent",
   "Adult-protective services and elder-law practices",
   "Banks' vulnerable-customer teams",
   "Carers and carers' charities"]},
 ]},
# ---------------------------------------------------------------- LOOP
{
 "slug": "loop", "title": "The Loop", "sub": "The machine that learns you.",
 "kicker": "Algorithms", "url": "noblefathercreations.com/loop",
 "cover": "covers-existing/loop.jpg",
 "chips": ["47 chapters", "8 movements", "Your feed"],
 "sections": [
  {"h": "What it is", "p": [
   "A 47-chapter book on algorithmic manipulation: how optimisation found whatever holds your attention, who profits, and what actually works against it."]},
  {"h": "Inside", "bullets": [
   "The machine with no motive: why there's no villain to confront",
   "The mechanics, each part tested on millions and kept because it won",
   "Who pays, who's paid, and what's really being sold",
   "The same machine scheduling shifts, pricing groceries and ranking dates",
   "What it does to belief, and to you",
   "What works, starting with: you can't out-willpower an optimiser"]},
  {"h": "What makes it different", "p": [
   "It takes the shame off the person scrolling. Nobody designed this; selection pressure did. That makes it a structural problem with structural answers.",
   "It's a book about attention that refuses to take any: no streaks, no progress bar, no badges, nothing tracked. And it's honest where the research is still argued over."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who feels the scroll pulling at them",
   "Parents and teachers",
   "Digital-literacy programmes"]},
 ]},
# ---------------------------------------------------------------- WEIGHING
{
 "slug": "scale", "title": "The Weighing", "sub": "How to be right about people.",
 "kicker": "Discernment", "url": "noblefathercreations.com/scale",
 "cover": "covers-existing/scale.jpg",
 "chips": ["38 chapters", "6 movements", "Discernment"],
 "sections": [
  {"h": "What it is", "p": [
   "A 38-chapter course in discernment. It moves past \"does this look like a tactic?\" to the harder question: \"is that the best explanation for what happened?\""]},
  {"h": "Inside", "bullets": [
   "Where your own detector was calibrated, and what distorts it",
   "Evidence standards, and how a case quietly builds itself",
   "The two riskiest sources of information you'll ever use",
   "Four tests that separate manipulation from ordinary human failure",
   "Living with a conclusion, or without one, and trusting again"]},
  {"h": "What makes it different", "p": [
   "Most books in this field teach you to detect. This one teaches judgement, and protects you from both failures: being fooled, and wrongly deciding someone is a manipulator.",
   "It even has a chapter on the book in the wrong hands."]},
  {"h": "Who it's for", "bullets": [
   "Anyone afraid of being fooled, or of getting it wrong",
   "Journalists and investigators",
   "HR, mediators and juries",
   "Teachers of critical thinking"]},
 ]},
# ---------------------------------------------------------------- ROOT
{
 "slug": "root", "title": "The Root", "sub": "A shadow-work practice in 18 guided steps.",
 "kicker": "The practice", "url": "noblefathercreations.com/shadowroot",
 "cover": "covers/root.jpg",
 "chips": ["18 guided steps", "One sitting", "Private"],
 "sections": [
  {"h": "What it is", "p": [
   "A guided practice rather than a book. Take one reaction that's been bothering you, trace the belief underneath it and where it came from, and finish with one true thing to do about it."]},
  {"h": "How it moves", "items": [
   ("Name what surfaced", "A person, a habit, a fear, a memory or a hope"),
   ("Trace its root", "Childhood, a relationship, or a culture you grew up in"),
   ("Write the belief plainly", "As a rule: \"I am too much\", not \"I felt bad\""),
   ("Find it in the body", "With a body map, then paced breathing"),
   ("Act", "One true thing to do about it")]},
  {"h": "What makes it different", "p": [
   "It turns self-reflection into something bounded and repeatable, that you can finish in one sitting.",
   "It's private: no account, and what you write stays on your device."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who wants to understand one reaction",
   "Therapists and coaches, between sessions",
   "Wellbeing programmes"]},
 ]},
]
