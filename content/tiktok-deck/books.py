# TikTok book deck v3: marketing highlights, in play order.
# Each book = cover + hook card + 4-5 highlight slides (Fractal 6).
# Every section: "h" = small label, "t" = the big headline (*italic gold*),
# then ONE body shape: "p" (list of paragraphs), "items" [(name, desc)],
# "bullets" [...], "acro" [(letter, word)], "card" {title, rows:[(label, text)]}
# or "stats" [(number, label)].
# Facts: catalogue PDF (Oct 2026), BOOKS.md, the books themselves, and the
# live Decoder v20 data (335 tactics, 32 patterns, 21 fields each).
# Rebuild: python3 content/tiktok-deck/build.py

DONATE = [("Cash App", "$shaestovell"), ("Venmo", "@noblefather")]

INTRO = [
 {"k": "Fifteen books · One practice · All free",
  "h": "Words for the things we *can't name.*",
  "p": "How people get steered, in love, in families, at work, in faith, online and at festivals, in plain words from someone who lived near it.",
  "grid": True, "sig": "Written by"},
 {"k": "Who it's for",
  "h": "If something feels wrong, *there's a book for that.*",
  "bullets": ["Women, men, kids and parents", "Believers, and people walking away",
              "Workers, festival-goers, anyone with a phone", "People who left, and people who caused harm",
              "The counsellors and advocates beside them"]},
 {"k": "What they do",
  "h": "Name it. Check it. *Act on it.*",
  "p": "Every book puts a name on the tactic, shows you how to tell it from an ordinary bad day, and hands you the next move: the script, the checklist, the safety plan, the number to call."},
 {"k": "The catch",
  "h": "There isn't one. *100% free.*",
  "bullets": ["No paywall, no account, no sign-up", "Nothing tracked, nothing sold", "Works on any phone, even offline"],
  "donate": True},
]

OUTRO = [
 {"k": "The whole library",
  "h": "Find the one *you need.*",
  "p": "Then send it to the person it would help next.",
  "big": "noblefathercreations.com",
  "donate": True},
]

ABOUT = {"p": [
 "I'm Shae Stovell. I run Noble Father Creations. I make things by hand with a small NFC chip inside, and I write free books and tools about how people get steered: in relationships, in faith communities, at work, and on their feeds.",
 "Everything in my library is written by a person who lived near what it describes."]}

BOOKS = [
# ---------------------------------------------------------------- DECODER
{
 "slug": "decoder", "title": "The Pattern Decoder", "sub": "Put a name to what's happening, before someone else names it for you.",
 "kicker": "The instrument", "url": "noblefathercreations.com/playbook",
 "cover": "covers/decoder.jpg",
 "chips": ["335 tactics", "32 patterns", "10 lines", "21 checks each"],
 "sections": [
  {"h": "What it is", "t": "For the moment you ask *\"is this normal?\"*", "p": [
   "Type what happened. Paste the sentence they said. Or answer a few gentle questions if you can't find the words yet.",
   "The Decoder searches **335 named tactics** of manipulation and control, plus **32 well-known patterns** like Gaslighting, DARVO and Trauma Bonding, and shows you what fits."]},
  {"h": "Inside every tactic", "t": "Twenty-one ways to *check it.*", "bullets": [
   "What it sounds like, and why it lands so hard",
   "Signs it's this, and signs it's something else",
   "The innocent explanation, checked first",
   "A boundary script, your options, a safety note",
   "The look-alikes, and where the books go deeper"]},
  {"h": "One entry, in miniature", "t": "This is what *an answer* looks like.", "card": {
   "title": "Account Takeover · Online line",
   "rows": [
    ("Safety first", "Changing a password can alert them. Plan your next step on a device they can't see."),
    ("It can sound like", "\"I changed it because you can't be trusted with it.\""),
    ("Signs it might be this", "You lost access without changing anything, or posts appear you didn't write."),
    ("Probably something else", "Many people report the same lockout and the provider confirms a fault.")]}},
  {"h": "Why it's different", "t": "335 tactics on *one transit map.*", "p": [
   "335 tactics across relationships, families, work, online life and whole groups, laid out like a transit map with ten colour-coded lines.",
   "It's careful both ways: every entry checks for an innocent explanation and warns you not to use the word as a weapon."]},
  {"h": "Built for someone frightened", "t": "Safe on a phone *someone else checks.*", "bullets": [
   "A green Leave button on every screen",
   "No account. Nothing stored. Nothing tracked.",
   "Calm mode, large text, works offline",
   "For anyone unsure, and the helplines, counsellors and friends sitting beside them"]},
 ]},
# ---------------------------------------------------------------- FEMININE
{
 "slug": "feminine", "title": "The Sovereign Divine Feminine", "sub": "A field guide to psychological manipulation: the tactics, their names, and your counter-moves.",
 "kicker": "For women", "url": "noblefathercreations.com/feminine",
 "cover": "covers-existing/feminine.jpg",
 "chips": ["42 chapters", "9-step framework", "30-minute rescue"],
 "sections": [
  {"h": "What it is", "t": "The playbook for *what to do next.*", "p": [
   "42 chapters for women facing manipulation in love, family, work, institutions, online and in high-control groups.",
   "How the hook gets set. How control tightens. How to interrupt it in real time, document it, and rebuild after. In crisis tonight? The **30-Minute Rescue** opens the book."]},
  {"h": "The framework", "t": "One word to carry *into every room.*", "acro": [
   ("S", "Spot"), ("O", "Orient"), ("V", "Validate"), ("E", "Establish the frame"), ("R", "Respond"),
   ("E", "Enforce"), ("I", "Invest"), ("G", "Ground"), ("N", "Navigate")]},
  {"h": "The lexicon translator", "t": "Say it so *the system has to listen.*", "card": {
   "title": "Appendix E · Plain language → HR language",
   "rows": [
    ("You'd say", "\"He dismissed me as emotional so he didn't have to address the issue.\""),
    ("HR hears", "\"During [meeting/date], my concern was redirected from the substantive issue to commentary about my tone, which prevented resolution and undermined my ability to participate.\""),
    ("The rule", "Facts, impact, request, timeline. Send once. Then stop.")]}},
  {"h": "Inside", "t": "Built for 2am, *mid-situation.*", "bullets": [
   "Love bombing, trauma bonding, DARVO, weaponised therapy-speak",
   "Medical gaslighting, PIPs, false reports, legal threats",
   "Word-for-word scripts and if-then plans",
   "Somatic tools, exit logistics, life after"]},
  {"h": "Who it's for", "t": "Power reclaimed, *with no enemy required.*", "bullets": [
   "Women in it now, or on the way out",
   "Mothers and daughters reading together",
   "Counsellors and social workers, as a teaching text",
   "Domestic-violence services",
   "Anyone who needs the words for HR, a doctor or a court"]},
 ]},
# ---------------------------------------------------------------- LONG AFTER
{
 "slug": "longafter", "title": "The Long After", "sub": "What happens once you have left.",
 "kicker": "For women, after leaving", "url": "noblefathercreations.com/longafter",
 "cover": "covers/longafter.jpg",
 "chips": ["45 chapters", "7 movements", "Years 2, 5, 10"],
 "sections": [
  {"h": "What it is", "t": "Leaving was *the middle,* not the end.", "p": [
   "For many people the abuse doesn't stop at the door. It changes channel: the kids, the money, the story told to mutual friends, the court date, the phone.",
   "This book starts where most resources stop, and picks up exactly where The Sovereign Divine Feminine ends."]},
  {"h": "Inside", "t": "The years *nobody warned you about.*", "bullets": [
   "Hoovering, surveillance, the new partner, the smear",
   "What to document, and how",
   "Family court honestly, legal aid with no money",
   "Protective orders, housing, benefits",
   "What your nervous system is doing, and why it's normal"]},
  {"h": "Why it's different", "t": "The most patient voice *in the library.*", "p": [
   "It covers years two, five and ten, where so much harm and so much recovery quietly happens.",
   "Short paragraphs. No \"by six months you should…\" timelines. Never tells you how to feel. Written to be read slowly, re-read, and opened at 2am."]},
  {"h": "Who it's for", "t": "If it *followed you out,* start here.", "bullets": [
   "Anyone who left and found it didn't end",
   "Anyone asking \"maybe I'm still the problem?\"",
   "Friends and family supporting someone after",
   "Services holding cases that \"closed\" years ago"]},
 ]},
# ---------------------------------------------------------------- CHILDREN
{
 "slug": "children", "title": "Playground Protectors", "sub": "A kids' guide to tricky people, power-ups, and building real friendships.",
 "kicker": "For kids", "url": "noblefathercreations.com/children",
 "cover": "covers-existing/children.jpg",
 "chips": ["28 missions", "4 worlds", "Ages 7-12", "Read together"],
 "sections": [
  {"h": "What it is", "t": "Give them the words *before they need them.*", "p": [
   "28 illustrated missions across four worlds for kids about 7 to 12, made to read with a grown-up.",
   "It plays like a game. Manipulation tactics are **tricks**. That funny feeling is a **Wait a Minute Feeling**. The comebacks are **Power-Ups**. Kids level up into Playground Protectors."]},
  {"h": "A mission, in miniature", "t": "The Memory *Mixer-Upper.*", "card": {
   "title": "World 1 · Mission 01 · for grown-ups: gaslighting",
   "rows": [
    ("Tricky move", "\"That didn't happen. I never said that.\""),
    ("The feeling", "Confused. The confusion isn't a sign you're wrong. It's a sign the trick is happening."),
    ("Power-Up", "The Truth Lock. Say: \"I remember it differently. My memory is that…\""),
    ("Then", "Write it down. It's very hard to Memory Mixer-Upper a piece of paper.")]}},
  {"h": "The tricks", "t": "Names a kid *will actually remember.*", "items": [
   ("The Super-Fast Best Friend", "love bombing"),
   ("The Hot-and-Cold Game", "intermittent reinforcement"),
   ("The Whisper Game", "triangulation"),
   ("The Internet Ghost", "catfishing and online safety")]},
  {"h": "Why it's different", "t": "Kids play *the hero,* never the victim.", "p": [
   "Most kids' books stop at feelings, kindness and obvious bullying. This one teaches the quiet stuff: guilt trips, the silent treatment, jealousy as control, the friend who's lovely then cruel.",
   "A traffic light keeps it simple: green and yellow they can handle, red means tell a trusted grown-up."]},
  {"h": "Who it's for", "t": "A shared language *for the whole family.*", "bullets": [
   "Kids about 7 to 12",
   "Parents and carers, reading together",
   "Parents who never had these words as kids",
   "Therapists and school counsellors",
   "Schools building a social-emotional curriculum"]},
 ]},
# ---------------------------------------------------------------- WOOK
{
 "slug": "wook", "title": "The Festie Codex", "sub": "A field manual for spotting wooks in sheep's clothing.",
 "kicker": "Wook in sheep's clothing", "url": "noblefathercreations.com/wook", "accent": "hippy-angel.png",
 "cover": "covers-existing/wook.jpg",
 "chips": ["33 chapters", "A-Z toolkit", "Zine voice"],
 "sections": [
  {"h": "What it is", "accent": True, "t": "Know the pattern. Trust your body. *Protect the magic.*", "p": [
   "A 33-chapter festival harm-reduction manual written like a zine and laid out like a setlist: Know the Pattern, Read the Room, and an Encore.",
   "Free, and made to be shared."]},
  {"h": "Inside", "t": "The stories *you'll recognise.*", "bullets": [
   "The new best friend you met at the gate",
   "The group chat that turns into a leash",
   "The dose that wasn't your choice",
   "The \"family\" that isn't, and the friend who goes missing",
   "The comedown, and getting home"]},
  {"h": "The A to Z toolkit", "t": "Pocket tools *for the field.*", "bullets": [
   "Consent and capacity quick references",
   "A bystander-interruption kit",
   "Good Samaritan law guidance",
   "A pre-event checklist and a long-exit plan",
   "A directory of safety organisations"]},
  {"h": "Why it's different", "t": "Written from the dance floor, *not the podium.*", "p": [
   "No lecture, no judgement. Peer voice reaches the people who'd bin an official leaflet.",
   "It hands you the pattern at the gate, before someone else decides who you are this weekend. Event teams and welfare crews get a vocabulary attendees already speak."]},
 ]},
# ---------------------------------------------------------------- FESTIVAL
{
 "slug": "festival", "title": "The Festie Bible", "sub": "Twenty-one field guides for the whole festival world.",
 "kicker": "The Festival Bible", "url": "noblefathercreations.com/festival",
 "cover": "covers-existing/festival.jpg",
 "chips": ["21 guides", "270 scenarios", "128,000 words"],
 "sections": [
  {"h": "What it is", "t": "The whole scene, *one safety language.*", "p": [
   "21 guides and about 270 real scenarios on staying psychologically safe across the festival world.",
   "Written for the people who go, and for everyone who makes it happen: crew, vendors, volunteers, welfare and medical teams."]},
  {"h": "Inside", "t": "Built from *what actually happens.*", "bullets": [
   "Every scenario audited against real events in its category",
   "Physical and environmental risks other guides miss, including crowd crush",
   "Short video scripts for training and outreach",
   "Guides for attendees, crew, vendors and welfare"]},
  {"h": "Why it's different", "t": "A volunteer, a vendor and a first-timer, *saying the same thing.*", "p": [
   "It turns what the scene has always known informally into something you can teach, train and hand out.",
   "Built for operators, welfare and medical teams, harm-reduction organisations and event-safety training, and readable by any attendee in a tent at 3am."]},
  {"h": "Who it's for", "t": "Everyone *inside the gates.*", "bullets": [
   "Attendees, first-timers to veterans",
   "Volunteers, vendors and crew",
   "Operators, welfare and medical teams",
   "Harm-reduction groups and safety trainers",
   "Anyone working their first festival"]},
 ]},
# ---------------------------------------------------------------- FRACTAL
{
 "slug": "fractal", "title": "The Fractal", "sub": "How one pattern runs the world.",
 "kicker": "The pattern", "url": "noblefathercreations.com/fractal",
 "cover": "covers-existing/fractal.jpg",
 "chips": ["30 sectors", "8 stages", "30 techniques", "3 scales"],
 "sections": [
  {"h": "What it is", "t": "The cycle doesn't stop *at the relationship.*", "p": [
   "Idealize, hook, devalue, confuse, isolate, extract, discard, replace. People learn this cycle from abusive relationships.",
   "The Fractal follows it into every system we've built, across thirty sectors of life. A pattern you can see is a pattern you can exit."]},
  {"h": "One cycle, eight stages", "t": "Thirty techniques, *one engine.*", "items": [
   ("Idealize · Hook", "Love bombing, future faking, hoovering"),
   ("Devalue · Confuse", "Gaslighting, moving goalposts, DARVO"),
   ("Isolate · Extract", "Triangulation, smears, trauma bonding"),
   ("Discard · Replace", "Manufactured crisis, plausible deniability")]},
  {"h": "Three scales", "t": "One person. One institution. *One civilization.*", "items": [
   ("Individual", "One person doing it to another. The damage is personal and the perpetrator has a face."),
   ("Institutional", "The pattern in a uniform, calling itself policy. The harm feels like the weather."),
   ("Civilizational", "The pattern as the air you breathe. Invisible because it's everywhere.")]},
  {"h": "One sector, in miniature", "t": "Healthcare, *read through the cycle.*", "card": {
   "title": "Sector · Healthcare & medicine",
   "rows": [
    ("What it maps", "Patient pain dismissed. \"Difficult patient\" used as a technique."),
    ("Who it helps", "Chronically ill patients, women and people of colour, healthcare workers."),
    ("Plus 29 more", "Religion, politics, media, schools, money, tech, family, dating, law, prisons, housing, food, beauty, sport…")]}},
  {"h": "Why it's different", "t": "Come in *personal.* Leave with the map.", "p": [
   "Readers arrive with \"my therapist calls it narcissistic abuse, and I keep seeing it everywhere\" and leave seeing the whole structure.",
   "The closing chapters on the body, inherited patterns, what came before and the planet keep it from ending in despair."]},
  {"h": "Who it's for", "t": "For anyone who *keeps seeing it.*", "bullets": [
   "Survivors who notice the pattern everywhere",
   "Professionals caught between their values and their system",
   "Activists who watched reform get absorbed",
   "Therapists, educators, organisers, parents"]},
 ]},
# ---------------------------------------------------------------- FRACTURE
{
 "slug": "fracture", "title": "The Fracture", "sub": "The wealth transfer, told from the public record.",
 "kicker": "The money behind it", "url": "noblefathercreations.com/fracture",
 "cover": "covers-existing/fracture.jpg",
 "chips": ["12 episodes", "195 citations", "43 years of record"],
 "sections": [
  {"h": "The numbers", "t": "The argument, *in three numbers.*", "stats": [
   ("$50T", "moved upward"), ("90%", "from the bottom 90% of earners"), ("1%", "to the top 1%")]},
  {"h": "What it is", "t": "Follow the pattern *to the money.*", "p": [
   "A documentary-style read in twelve episodes: where the money went, who received it, and how that machinery shows up in ordinary lives.",
   "The Fractal's companion. Same pattern, followed to the bank.",
   "Plus a companion story, **Sarah's Tuesday**: one ordinary day lived inside the architecture."]},
  {"h": "Inside", "t": "Twelve episodes, *zero hand-waving.*", "bullets": [
   "The ownership class and the five wealth tiers",
   "Six loops that keep it running and swallow reform",
   "What it does to the body, and who it hits hardest",
   "Every time it was broken before, and an action map"]},
  {"h": "Why it's different", "t": "195 sources. *Check every one.*", "p": [
   "Every claim comes from the public record: court filings, SEC disclosures, peer-reviewed research, government reports, congressional records and established investigative journalism. 195 numbered references.",
   "It answers three questions in order: is it real, why doesn't change come, and what can I actually do?"]},
  {"h": "Who it's for", "t": "For people *done with rhetoric.*", "bullets": [
   "Anyone who tried reform and watched it get absorbed",
   "Skeptics who need hard numbers",
   "Managers, teachers, doctors and lawyers in the middle tiers",
   "Organisers and researchers"]},
 ]},
# ---------------------------------------------------------------- FAITH
{
 "slug": "faith", "title": "The Sacred Divide", "sub": "Honor the faith. Name the machinery.",
 "kicker": "The faith book", "url": "noblefathercreations.com/faith",
 "cover": "covers-existing/faith.jpg",
 "chips": ["34 traditions", "10 families", "27 sections each"],
 "sections": [
  {"h": "What it is", "t": "Keep the faith. *See the machinery.*", "p": [
   "How institutional power works inside **34 religious traditions**, from Catholicism and Sunni Islam to Hinduism, Mormonism, Scientology and Indigenous religions.",
   "Written for believers, former believers and the people who love them. Nobody is told what to believe."]},
  {"h": "One page, in miniature", "t": "Catholicism, *at a glance.*", "card": {
   "title": "Every tradition opens with the same questions",
   "rows": [
    ("Size", "About 1.4 billion baptized (2023)"),
    ("Chosen by", "A conclave whose every elector was appointed by a previous pope"),
    ("Removable by", "Nobody. Canon law has no mechanism to remove a pope."),
    ("Leaving", "Can bring excommunication and denial of the sacraments")]}},
  {"h": "Every tradition page", "t": "Twenty-seven sections. *Same test for all.*", "bullets": [
   "History, authority, law, and who holds the money",
   "Reach into children and bodies",
   "30 control tactics, each graded by evidence",
   "Documented cases and voices from inside",
   "How to leave safely, and where to get help"]},
  {"h": "Why it's different", "t": "Its consistency *is its credential.*", "p": [
   "Same 27 sections, same evidence standard, every claim sourced, so nobody can say theirs was singled out.",
   "Believers get questions to ask inside their own tradition. People leaving get a map and a safe-exit page. One room of mixed beliefs can use it together. A quick-exit button sits on every page."]},
  {"h": "Who it's for", "t": "For every side *of the pew.*", "bullets": [
   "Believers, former believers and the people who love them",
   "People leaving high-control communities",
   "Clergy, chaplains and interfaith groups",
   "Journalists, researchers and survivors",
   "Anyone comparing two traditions side by side"]},
 ]},
# ---------------------------------------------------------------- SILENCE
{
 "slug": "silence", "title": "The Silence", "sub": "For men nobody thought to ask.",
 "kicker": "For men", "url": "noblefathercreations.com/silence",
 "cover": "covers/silence.jpg",
 "chips": ["46 chapters", "7 movements", "Beside, not instead"],
 "sections": [
  {"h": "What it is", "t": "For the man who was told *nobody would believe him.*", "p": [
   "46 chapters for men in coercive relationships: how to recognise it, what help actually exists, and what to do next.",
   "It stands beside The Sovereign Divine Feminine, never in place of it.",
   "Seven movements, from **Why Nobody Asked** to **Out and After**."]},
  {"h": "Inside", "t": "The things *you're not allowed to say.*", "bullets": [
   "The fog, being managed, money and sex as currency",
   "The kids used as leverage",
   "Being provoked into being \"the bad one\"",
   "The reversal, the police call, the violence you can't name",
   "What's really available, and life after"]},
  {"h": "Why it's different", "t": "No hero font. *A plain page he'll trust.*", "p": [
   "No flourish, no hero font, a plain ruled list. Written for a reader taught his experience isn't serious.",
   "One rule held the whole manuscript: no chapter can be quoted as an argument for cutting women's services.",
   "It even takes on the manosphere offering to help, and what you'll be accused of for reading this."]},
  {"h": "Who it's for", "t": "Support for men, *taking nothing from anyone.*", "bullets": [
   "Men in coercive relationships",
   "Men still in it, and men years out",
   "Services that want to help men without taking sides",
   "Women's services, who can trust it won't undercut them"]},
 ]},
# ---------------------------------------------------------------- REPAIR
{
 "slug": "repair", "title": "The Repair", "sub": "For the person on the other side of it.",
 "kicker": "For the person who caused harm", "url": "noblefathercreations.com/repair",
 "cover": "covers/repair.jpg",
 "chips": ["48 chapters", "7 movements", "Measured in months"],
 "sections": [
  {"h": "What it is", "t": "Measured by what changes, *over months.*", "p": [
   "48 chapters for people who have harmed someone and want to change. The densest book in the library.",
   "Success is measured as behaviour change, over months, by the people affected. Insight and remorse alone don't count."]},
  {"h": "The Thursday rule", "t": "If it won't change Thursday, *it was cut.*", "p": [
   "Any paragraph that would make you feel better without changing what you do on Thursday didn't make the book.",
   "It blocks both easy exits by name: \"I'm a monster\" and \"I'm actually fine.\"",
   "Chapters 2, 5 and 47 are deliberately uncompromising. They're what stop the book being used as a shield."]},
  {"h": "Inside", "t": "The honest inventory, *then the work.*", "bullets": [
   "What you actually did, itemised",
   "The pattern you'd spot instantly in someone else",
   "Causes, not excuses",
   "How to stop, and amends done properly",
   "Most chapters end with something concrete to try"]},
  {"h": "Who it's for", "t": "For the person who *searched at 3am.*", "bullets": [
   "Anyone who caused harm and means to change",
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
  {"h": "What it is", "t": "Bad job, or *coercive job?*", "p": [
   "47 chapters that run The Fractal's eight-stage cycle on a workplace and show you the moment one becomes the other.",
   "Written for a lunch break, or the car park before a shift.",
   "Seven movements: the frame, the moves, the machinery, who's doing it, what you're owed, your options, and the ledger."]},
  {"h": "Inside", "t": "Every line *you've heard at work.*", "bullets": [
   "\"We're a family\", and passion as a pay cut",
   "Manufactured urgency and the moving target",
   "Recognition instead of a raise",
   "The review as a weapon, the PIP that's really a firing",
   "NDAs, non-competes, arbitration, surveillance, wage theft"]},
  {"h": "Why it's different", "t": "Start the paper trail *before you need a lawyer.*", "p": [
   "It names the harm that happens with no villain, where incentives produce it on their own, without letting anyone who chooses it off the hook.",
   "Employment law changes by place, so it teaches the pattern everywhere and points you to the local specifics."]},
  {"h": "Who it's for", "t": "For anyone *dreading Monday.*", "bullets": [
   "Workers facing a review, a PIP or a quiet push out",
   "Gig workers managed by an algorithm",
   "HR leads who want to get it right",
   "Unions and workplace advocates"]},
 ]},
# ---------------------------------------------------------------- SLOW TAKE
{
 "slug": "slowtake", "title": "The Slow Take", "sub": "Elder financial exploitation, for the adult child.",
 "kicker": "For adult children", "url": "noblefathercreations.com/slowtake",
 "cover": "covers/slowtake.jpg",
 "chips": ["45 chapters", "7 movements", "Later life"],
 "sections": [
  {"h": "What it is", "t": "Your parent won't search for this. *You will.*", "p": [
   "45 chapters on coercion and financial exploitation in later life, written for the adult child.",
   "The person being isolated and drained is the least likely to look for help. Their son or daughter is the one typing the question."]},
  {"h": "Inside", "t": "The signs *hiding in plain sight.*", "bullets": [
   "The new friend, and the phone that rings at the same time every day",
   "The romance, the paperwork, the will that changed",
   "Care that became control",
   "Following the money, and power of attorney",
   "Who does it: mostly family, then carers, professionals, scammers"]},
  {"h": "Why it's different", "t": "Protect them *without taking over.*", "p": [
   "Autonomy isn't safety, and safety isn't the only value. Your parent keeps the right to make bad decisions.",
   "It's honest that guardianship gets abused too, and asks the hard question in its own chapter: \"Am I the one benefiting?\"",
   "The only book in the library set in a sans-serif face, chosen for a frightened reader scanning on a phone."]},
  {"h": "Who it's for", "t": "For the family *watching from close by.*", "bullets": [
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
  {"h": "What it is", "t": "You can't out-willpower *an optimiser.*", "p": [
   "47 chapters on algorithmic manipulation: how optimisation found whatever holds your attention, who profits from it, and what actually works against it.",
   "It closes with the ledger: what the book may have wrong, how to help someone else, and what has to change at a larger scale."]},
  {"h": "Inside", "t": "Why you *can't put it down.*", "bullets": [
   "The machine with no motive, and no villain to confront",
   "The mechanics, each tested on millions and kept because it won",
   "Who pays, who's paid, and what's really for sale",
   "The same machine pricing groceries and ranking dates",
   "What it does to belief, and to you"]},
  {"h": "Why it's different", "t": "No streaks. No badges. *Nothing tracked.*", "p": [
   "No streaks, no progress bar, no badges, nothing tracked, and it says so in its own pages.",
   "Nobody designed this; selection pressure did. That takes the shame off the person scrolling and makes it a problem with real answers."]},
  {"h": "Who it's for", "t": "For anyone *who felt the pull.*", "bullets": [
   "Anyone who opens the app without deciding to",
   "Parents and teachers",
   "Anyone helping a teenager with their phone",
   "Digital-literacy programmes"]},
 ]},
# ---------------------------------------------------------------- WEIGHING
{
 "slug": "scale", "title": "The Weighing", "sub": "How to be right about people.",
 "kicker": "Discernment", "url": "noblefathercreations.com/scale",
 "cover": "covers-existing/scale.jpg",
 "chips": ["38 chapters", "6 movements", "4 tests"],
 "sections": [
  {"h": "What it is", "t": "Is that the *best explanation?*", "p": [
   "A 38-chapter course in discernment. It moves past \"does this look like a tactic?\" to the question that matters: \"is that the best explanation for what happened?\"",
   "Six movements: why weigh at all, the instrument is you, what counts, the tests that work, the mirror, and living calibrated."]},
  {"h": "Inside", "t": "Calibrate *the instrument: you.*", "bullets": [
   "Where your own detector was set, and what bends it",
   "Evidence standards, and how a case builds itself",
   "The two riskiest sources of information you'll ever use",
   "Four tests that separate manipulation from ordinary failure",
   "Living with a conclusion, or without one"]},
  {"h": "Why it's different", "t": "A detector *with a safety catch.*", "p": [
   "Most books in this field teach detection. This one teaches judgement, with a safety gate before every test and a chapter on the book in the wrong hands.",
   "Useful to anyone who has to weigh claims about people, at the kitchen table or for a living."]},
  {"h": "Who it's for", "t": "For anyone who *weighs people* for a living.", "bullets": [
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
 "chips": ["18 steps", "1 sitting", "0 accounts"],
 "sections": [
  {"h": "What it is", "t": "One reaction. *All the way down.*", "p": [
   "A guided practice, not a book. Take one reaction that keeps getting under your skin, trace the belief underneath it and where it came from, and finish with one true thing to do about it.",
   "Along the way: a paced breathing exercise and a body map that shows where the belief lives."]},
  {"h": "How it moves", "t": "Eighteen steps, *one sitting.*", "items": [
   ("Name what surfaced", "A person, a habit, a fear, a memory, a hope"),
   ("Trace its root", "Childhood, a relationship, a culture"),
   ("Write the belief plainly", "\"I am too much\", not \"I felt bad\""),
   ("Find it in the body", "A body map, then paced breathing"),
   ("Act", "One true thing to do about it")]},
  {"h": "Why it's different", "t": "Shadow work *with a finish line.*", "p": [
   "Self-reflection usually sprawls. The Root makes it bounded and repeatable, something you can actually finish tonight.",
   "Private by design: no account, and what you write stays on your device.",
   "Come back whenever a new reaction shows up. Each run is one belief, start to finish."]},
  {"h": "Who it's for", "t": "For the reaction *you can't explain.*", "bullets": [
   "Anyone who wants to understand one reaction",
   "Therapists and coaches, between sessions",
   "Wellbeing programmes"]},
 ]},
]
