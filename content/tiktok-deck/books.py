# TikTok book deck: slide content, in play order.
# Text is taken verbatim from the "Noble Father Creations" catalogue PDF
# (Oct 2026), with the partner-specific (Theria) material removed.
# "Who it's for" sections are assembled from the audience sentences in the
# same PDF. Edit here, then re-run build.py.
#
# Section shapes:
#   {"h": heading, "p": [paragraph, ...]}            prose, split by sentence
#   {"h": heading, "items": [(name, desc), ...]}     list, split by item
#   {"h": heading, "bullets": [text, ...]}           simple bullets

BOOKS = [
# ---------------------------------------------------------------- DECODER
{
 "slug": "decoder", "title": "The Pattern Decoder", "sub": "310 tactics, ten lines, five parts each",
 "kicker": "The instrument", "url": "noblefathercreations.com/playbook",
 "cover": "covers/decoder.jpg",
 "chips": ["310 tactics", "10 lines", "5 parts each", "Private"],
 "sections": [
  {"h": "What it is", "p": [
   "A lookup tool for the moment someone asks *is this normal?* It holds **310 named tactics** of manipulation and control, each explained in plain words, so a person who is hurting and unsure can put a name to what is happening without having to prove anything first.",
   "It is not a book to read in order. It is built like a transit map: ten colour-coded lines, each a family of tactics, with stations on every line and \"change here\" links where one tactic looks like another."]},
  {"h": "The ten lines", "items": [
   ("Twisting what is real", "Lies, denial and confusion that leave you unsure of your own memory or judgment."),
   ("Guilt, pressure and fear", "Pushing you to say yes through guilt, obligation, urgency or threat."),
   ("Control over your life", "Rules, monitoring and limits on your time, money, body or choices."),
   ("Love that hooks you", "Affection, attention and promises used to pull you in and keep you there."),
   ("Put-downs that wear you down", "Insults, contempt and slow erosion of how you see yourself."),
   ("Dodging blame", "Ways a person avoids responsibility, or turns it back on you."),
   ("Turning people against you", "Isolating you, using other people, and controlling who hears what."),
   ("Work, school and systems", "When an organization, its rules or its paperwork become the weapon."),
   ("Online and technology", "Fake accounts, deepfakes, tracking, scams and pressure through screens."),
   ("Groups, cults and propaganda", "Influence over whole groups: high-control groups, propaganda and influence operations.")]},
  {"h": "Every entry, in five parts", "items": [
   ("1 · In short", "The tactic in one plain sentence, with what it can sound like."),
   ("2 · Understand it", "What it is, how it works, and what it is often mistaken for."),
   ("3 · Is this it?", "Signs it might be this, and signs it is probably something else, so the reader can check without being told what happened."),
   ("4 · What you can do", "Practical next steps, in plain words. About a third of entries (105) open with a safety-first note before anything else."),
   ("5 · Go deeper", "Look-alikes, related tactics and where the pattern shows up in the other books.")]},
  {"h": "Four ways in", "items": [
   ("Type or paste", "A reader types what happened, or pastes a phrase they were told, and the tool narrows what it might be."),
   ("Narrow it down", "A guided path through six situations and thirty-five feelings, for someone who cannot name what is wrong."),
   ("Browse the map", "Ten colour-coded lines, each a family of tactics, with stations and \"change here\" links between look-alikes."),
   ("Compare and save", "Put look-alike tactics side by side, tick what fits, and save a private trail. Nothing leaves the device.")]},
  {"h": "One entry in miniature", "items": [
   ("Entry", "Account Takeover: station 21 of 25 on the Online and technology line"),
   ("Safety first", "Changing a password can alert the person. Work out your next step before you change anything, on a device they cannot see."),
   ("It can sound like", "\"I changed it because you can't be trusted with it. I'll give it back when we've sorted this out.\""),
   ("Signs it might be this", "You lost access without changing anything, or content appears in your accounts that you did not create."),
   ("Signs it is probably something else", "Many people report the same lockout at once and the provider confirms a fault.")]},
  {"h": "Built for someone frightened", "p": [
   "A green **Leave** button is always in reach. Safety-sensitive entries put safety first and red is used only for danger. It stores nothing, tracks nothing and asks for no account, so a reader can look things up on a shared or watched phone.",
   "There is a Calm mode and an optional reading pause, no points or streaks, and text that can be enlarged. It works offline. Every tactic also has its own plain page that a search engine or an AI assistant can find, so the answer is there when someone types the question into a search box."]},
  {"h": "The intent", "p": [
   "To give a name to the thing before it has been named by someone else. Many people live inside a pattern for years because they have no word for it, and the word is often what lets them ask for help, set a boundary, or simply trust their own memory."]},
  {"h": "What makes it unique", "p": [
   "Lookup tools for manipulation usually give a short list of famous terms. This one is a full map of 310 tactics across relationships, work, online life and whole groups, with the same five-part structure for every entry and a safety-first design for the hardest ones.",
   "A helpline, advocate, counsellor, teacher or friend can use it with someone, and the person can use it alone. Its vocabulary also unlocks the rest of the library: each tactic connects back to the books that go deepest on it."]},
  {"h": "Who it's for", "bullets": [
   "Anyone hurting and unsure, asking *is this normal?*",
   "Someone looking things up on a shared or watched phone",
   "Helplines, advocates and counsellors working with someone",
   "Teachers and friends who want the right words",
   "Readers of the other books, looking up a tactic by name"]},
 ]},
# ---------------------------------------------------------------- FEMININE
{
 "slug": "feminine", "title": "The Sovereign Divine Feminine", "sub": "A Field Guide to Psychological Manipulation: Tactics, Names, and Counter-Moves",
 "kicker": "For women", "url": "noblefathercreations.com/feminine",
 "cover": "covers-existing/feminine.jpg",
 "chips": ["42 chapters", "30-minute rescue", "SOVEREIGN framework", "Scripts for HR, medical and legal"],
 "sections": [
  {"h": "What it is", "p": [
   "A 42-chapter operational manual for women navigating psychological manipulation in romantic relationships, families, workplaces, institutions, digital spaces and high-control groups. It is built around the SOVEREIGN acronym as a portable internal operating system.",
   "It covers not just what manipulation looks like but how to interrupt it in real time, document it for institutional contexts, and rebuild after it.",
   "The back matter includes appendices on somatic tools for nervous-system regulation, exit logistics, a full manipulation index with decision trees, a searchable script library, and a lexicon translator that converts plain emotional language into the HR, medical and legal language that systems actually respond to."]},
  {"h": "The SOVEREIGN framework", "acro": [
   ("S", "Spot"), ("O", "Orient"), ("V", "Validate"), ("E", "Establish the frame"), ("R", "Respond"),
   ("E", "Enforce"), ("I", "Invest"), ("G", "Ground"), ("N", "Navigate")]},
  {"h": "The content", "p": [
   "Forty-two chapters cover the full arc: capture (love bombing, manufactured intimacy, reciprocity traps); conditioning (trauma bonding, FOG scripts, the cognitive cage); and control (tone policing, weaponised therapy-speak, conversational fog, DARVO).",
   "They continue into social warfare, institutional and administrative control, digital terrain, high-control systems, family and motherhood scripts, and finally recovery: discernment repair, repair templates, the Sovereign Playbook, and life design after survival.",
   "Each chapter uses a recurring structure: Mirror Scene, Fracture Point, Core Concept, the SOVEREIGN framework applied to the specific tactic, scripts, if-then plans, identity repair, and a Love-Centered Mandate closing. A \"30-Minute Rescue\" opens the book for anyone in crisis."]},
  {"h": "The intent", "p": [
   "To give women what psychological insight alone cannot: language that works. Not just \"this is gaslighting,\" but here is the exact sentence to say to HR, here is what to write in your chart note, here is how to translate \"he dismissed my pain\" into something a legal record can hold.",
   "The book treats women as capable of handling precision, and it refuses to soften the mechanics of how they are being harmed. The framing of \"sovereign\" deliberately reclaims feminine power without framing men as the enemy; patriarchy is named as a cultural operating system, not a person."]},
  {"h": "What makes it unique", "p": [
   "The crowded self-help space for women tends toward either the deeply personal (memoir, emotional processing) or the broadly conceptual (naming abuse patterns). This book is operationally specific enough to be used mid-situation, with scripts you can reach at 2am when you're trying to work out what to send your HR department.",
   "The lexicon translator alone, which turns lived experience into the language institutions respond to, is a practical tool that is rare elsewhere. The coverage of digital manipulation, medical gaslighting and administrative warfare (PIPs, legal threats, false reports) reflects the full modern landscape of control.",
   "It can function as a self-help book, a classroom text for counsellors and social workers, a resource for domestic-violence organisations, and a co-reading guide for mothers and daughters. The SOVEREIGN framework is portable enough to become cultural shorthand, the way DARVO and love bombing have become common vocabulary."]},
  {"h": "Who it's for", "bullets": [
   "Women navigating manipulation in relationships, families, work, institutions, online and in high-control groups",
   "Anyone in crisis: the 30-Minute Rescue opens the book",
   "Counsellors and social workers, as a classroom text",
   "Domestic-violence organisations",
   "Mothers and daughters reading together"]},
 ]},
# ---------------------------------------------------------------- LONG AFTER
{
 "slug": "longafter", "title": "The Long After", "sub": "What happens once you have left",
 "kicker": "For women, after leaving", "url": "noblefathercreations.com/longafter",
 "cover": "covers/longafter.jpg",
 "chips": ["45 chapters", "7 movements", "After leaving"],
 "sections": [
  {"h": "What it is", "p": [
   "A 45-chapter, seven-movement guide to post-separation abuse: the well-documented fact that for many people, leaving does not end the coercion, it changes the channel.",
   "It sits after The Sovereign Divine Feminine, which ends at the door, and it begins where most resources stop."]},
  {"h": "The content", "p": [
   "Movements run from The Thing Nobody Warned You About (leaving was the middle, not the end; the grief nobody will let you have) through Post-Separation Abuse (children, money and the narrative campaign as channels; surveillance and technology; the new partner; hoovering; mutual friends and family) to The Systems (systems abuse, what to document and how, legal aid with no money, family court honestly, police and protective orders, housing and benefits).",
   "It then covers The Body and the Mind (what the nervous system is doing), The People, Rebuilding, and The Ledger. Chapters that touch acute material carry a heavier safety review."]},
  {"h": "The intent", "p": [
   "That a reader who has left can recognise post-separation abuse for what it is rather than mistaking it for \"it just doesn't fully end\" or \"maybe I'm still the problem.\"",
   "They should know the practical systems available, understand what is happening in their body without pathologising normal responses, and have a realistic, patient route through the years after."]},
  {"h": "What makes it unique", "p": [
   "Most material on leaving abuse stops at the exit, as though the story ends there. This book covers years two, five and ten, where a large amount of under-discussed harm and recovery happens.",
   "It is the most patient voice in the library: short paragraphs, no universal timelines (\"by six months you should…\"), and never prescriptive about feelings. It is built to be read slowly, re-read, and opened at 2am. For support organisations, it is a ready reference for the long tail of cases that officially \"closed\" years ago."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who has left, and found the coercion followed them",
   "Readers in years two, five and ten after leaving",
   "Readers of The Sovereign Divine Feminine, picking up at the door",
   "Support organisations holding cases that officially \"closed\" years ago"]},
 ]},
# ---------------------------------------------------------------- CHILDREN
{
 "slug": "children", "title": "Playground Protectors", "sub": "A Kids' Guide to Tricky People, Power-Ups, and Building Real Friendships",
 "kicker": "For kids", "url": "noblefathercreations.com/children",
 "cover": "covers-existing/children.jpg",
 "chips": ["28 missions", "4 worlds", "Ages 7 to 12", "Read together"],
 "sections": [
  {"h": "What it is", "p": [
   "An illustrated children's book of 28 missions across four worlds, calibrated for roughly ages 7 to 12, with a deliberate dual-audience design for parent-child co-reading. It teaches psychological-manipulation tactics through the lens of a game.",
   "Manipulation tactics are named as \"tricks,\" recognition skills are \"Wait a Minute Feelings,\" responses are \"Power-Ups,\" and children are positioned as Playground Protectors levelling up through the book.",
   "The subject matter (gaslighting, love bombing, intermittent reinforcement, triangulation, social exclusion, blame-shifting, peer pressure, fear-based coercion) is made age-appropriate not by simplifying it into uselessness but by finding the exact childhood contexts where these patterns occur and naming them there."]},
  {"h": "The tricks it names", "items": [
   ("The Memory Mixer-Upper", "gaslighting"),
   ("The Super-Fast Best Friend", "love bombing and premature enmeshment"),
   ("The Whisper Game", "triangulation"),
   ("The Hot-and-Cold Game", "intermittent reinforcement"),
   ("The Body Copycat", "mirroring as manipulation"),
   ("The Secret Whisperer", "secret-keeping as coercion"),
   ("The Blame Game", ""),
   ("The Group-Up", "social exclusion and mob dynamics"),
   ("The Best Friend Trap", "idealise/devalue"),
   ("The Internet Ghost", "catfishing and online safety"),
   ("The Unfair Clubhouse", "high-control group dynamics"),
   ("The Mean Voice in Your Head", "internalised criticism")]},
  {"h": "The content", "p": [
   "It also has chapters on guilt manipulation, the silent treatment, jealousy as control, comparison traps and compliment manipulation. It also covers defensive skills, friendship architecture, forgiveness with boundaries, social-media safety, and quiet heroism.",
   "Each chapter follows a consistent structure: narrative scenario, emotional recognition, the mechanic explained, moves and counter-moves with actual scripts, a differentiation between accidental and intentional versions, a playground story where a character uses their Power-Ups, and a mission the child can act on.",
   "A traffic-light system keeps responses simple: green and yellow a child can handle; red means tell a trusted grown-up."]},
  {"h": "The intent", "p": [
   "To give children the specific vocabulary for what is happening to them before they have to figure it out alone at thirty-five. Most children encounter gaslighting, social exclusion, guilt manipulation and intermittent reward cycles well before they have language for it; they just know something feels wrong.",
   "The parent-child co-reading design is structural: when a child reads this with a parent, it opens a shared vocabulary that turns abstract hurt into something that can be discussed and navigated together."]},
  {"h": "What makes it unique", "p": [
   "Children's social-emotional learning material typically covers emotions, kindness and basic conflict resolution. Anti-bullying literature typically addresses physical bullying or obvious exclusion. This book sits in the gap between both, teaching the mechanics of relational and psychological manipulation at the age when children first meet it systematically.",
   "Books on consent, body safety or stranger danger each address one topic; this addresses an architecture of social manipulation across home, school, sports, online and peer contexts.",
   "Therapists can use it as a therapeutic tool, school counsellors can build curricula around it, and parents who were themselves manipulated as children can use it to process their own experience alongside their child's. The gamification removes shame and adds agency: children become the hero rather than the victim, which is the posture from which resilience is built."]},
  {"h": "Who it's for", "bullets": [
   "Kids roughly ages 7 to 12",
   "Parents reading together with their child",
   "Parents who were manipulated as children themselves",
   "Therapists, as a therapeutic tool",
   "School counsellors building curricula"]},
 ]},
# ---------------------------------------------------------------- WOOK
{
 "slug": "wook", "title": "The Festie Codex", "sub": "A field manual for spotting wooks in sheep's clothing",
 "kicker": "Wook in sheep's clothing", "url": "noblefathercreations.com/wook",
 "cover": "covers-existing/wook.jpg",
 "chips": ["33 chapters", "Appendices A to Z", "Zine voice", "Free"],
 "sections": [
  {"h": "What it is", "p": [
   "A 33-chapter field manual for festival and field harm reduction, in a zine voice: *Know the pattern. Trust your body. Protect the magic.*",
   "It is structured as a setlist: Know the Pattern, Read the Room, and an Encore, with a lettered archive of appendices A to Z."]},
  {"h": "The content", "p": [
   "Story-led chapters on real situations: the person who befriends you at the gate, a group chat that becomes a leash, a dosing that wasn't your choice, the \"family\" that isn't, the missing friend, the comedown and re-entry.",
   "The appendices hold the practical tools: consent and capacity quick references, a bystander-interruption kit, Good Samaritan law guidance, a pre-event checklist, a long-exit protocol, a community accountability compact template, and a directory of safety organisations."]},
  {"h": "The intent", "p": [
   "To hand people the pattern at the gate, before the gap closes between who they are and who someone else needs them to be."]},
  {"h": "What makes it unique", "p": [
   "It is peer-voiced and unpreachy, so it reaches people who would ignore an official leaflet. The zine aesthetic is deliberate.",
   "For event teams, welfare services and harm-reduction groups, it offers a field-tested vocabulary that attendees already recognise."]},
  {"h": "Who it's for", "bullets": [
   "Festival-goers, from the gate to the comedown",
   "People who would ignore an official leaflet",
   "Event teams and welfare services",
   "Harm-reduction groups"]},
 ]},
# ---------------------------------------------------------------- FESTIVAL
{
 "slug": "festival", "title": "The Festie Bible", "sub": "Twenty-one field guides for the whole festival world",
 "kicker": "Festival Bible", "url": "noblefathercreations.com/festival",
 "cover": "covers-existing/festival.jpg",
 "chips": ["21 guides", "About 270 scenarios", "Video scripts", "Free"],
 "sections": [
  {"h": "What it is", "p": [
   "A scenario-based reference of 21 guides, about 270 scenarios and roughly 128,000 words, covering psychological safety across the festival ecosystem, for attendees and for the people who work it."]},
  {"h": "The content", "p": [
   "The book was built from a full source and then audited against what actually happens in each category. That audit added scenarios for the physical and environmental risks that interpersonal-focused guides often miss, including crowd crush.",
   "Short video scripts accompany the scenarios for training and outreach."]},
  {"h": "The intent", "p": [
   "To give an entire community the same shared language for safety, so a volunteer, a vendor and a first-time attendee can say the same thing in the same moment."]},
  {"h": "What makes it unique", "p": [
   "It is built for operators, welfare and medical teams, harm-reduction organisations and event-safety training. It turns a large scene's informal knowledge into something that can be taught."]},
  {"h": "Who it's for", "bullets": [
   "Attendees, from first-timers to veterans",
   "Volunteers and vendors",
   "Festival operators",
   "Welfare and medical teams",
   "Harm-reduction organisations and event-safety trainers"]},
 ]},
# ---------------------------------------------------------------- FRACTAL
{
 "slug": "fractal", "title": "The Fractal", "sub": "How one pattern runs the world",
 "kicker": "The pattern", "url": "noblefathercreations.com/fractal",
 "cover": "covers-existing/fractal.jpg",
 "chips": ["30 sectors", "8 stages", "30 techniques", "3 scales"],
 "sections": [
  {"h": "What it is", "p": [
   "A book mapping one eight-stage cycle (idealize, hook, devalue, confuse, isolate, extract, discard, replace) across thirty sectors of human life, at three scales.",
   "The argument is that the cycle people learn about in abusive relationships does not stop at the edge of the relationship: it scales into every system humanity has built. The aim is not to fight it but to see it. A pattern you can see is a pattern you can exit."]},
  {"h": "The eight stages and thirty techniques", "items": [
   ("1 · Idealize", "Love Bombing · Weaponized Generosity"),
   ("2 · Hook", "Future Faking · Hoovering"),
   ("3 · Devalue", "Devaluation · Gaslighting · Double Bind"),
   ("4 · Confuse", "Intermittent Reinforcement · Moving the Goalposts · Strategic Ambiguity · Projection · DARVO · Normalization"),
   ("5 · Isolate", "Isolation · Triangulation"),
   ("6 · Extract", "Flying Monkeys · Smear Campaign · Silent Treatment · Manufactured Consent · Trauma Bonding · Learned Helplessness · Benevolent Control · Infantilization · Identity Erosion · Spiritual Bypassing · Financial Control"),
   ("7 · Discard", "Manufactured Crisis · Discard"),
   ("8 · Replace", "Replacement · Plausible Deniability")]},
  {"h": "The thirty sectors", "items": [
   ("Belief and information · 6", "Religion and organised spirituality · Politics and government · Media and information · Education · Science and academia · New age and wellness"),
   ("Body and health · 6", "Healthcare and medicine · Mental health and therapy · The pharmaceutical industry · Insurance · Food and agriculture · Ageing, death and end-of-life care"),
   ("Money and work · 5", "Finance and economics · Corporate and workplace · Housing and real estate · The non-profit and NGO sector · Technology"),
   ("Home, heart and image · 6", "Family and relationships · Dating, sexuality and romance · Child welfare, foster care and adoption · Beauty, fashion and body image · Entertainment and culture · Sports and athletics"),
   ("Law, force and borders · 5", "Legal and justice · Incarceration and the prison industry · Military and security · Intelligence and surveillance · Immigration and borders"),
   ("Land and movement · 2", "Energy, environment and natural resources · Transportation and mobility")]},
  {"h": "The three scales", "p": [
   "Every sector is read at three levels. **Individual:** one person doing it to another, where the damage is personal and the perpetrator has a face. **Institutional:** the pattern in a uniform, calling itself policy, where the harm feels environmental, not intentional. **Civilizational:** the pattern as the air you breathe, invisible because it is everything.",
   "Each technique is tinted by the stage of the cycle it belongs to, so the pattern can be read at a glance."]},
  {"h": "Interludes and closings", "p": [
   "The Origin traces ten thousand years of how the pattern was installed, and shows it was not inevitable. The Spiritual Lens restates the cycle in sacred language for readers whom psychological language does not reach. The Somatic shows what the cycle does to the body.",
   "The Epigenetic shows how it travels across generations. The Original Frequency names what existed before the pattern. The Earth closes at planetary scale."]},
  {"h": "Sector by sector", "items": [
   ("Religion & organised spirituality", "Doctrine idealised, doubt devalued, dissenters discarded. Helps: religious-abuse survivors, people leaving faith, pastoral counsellors, seminary educators"),
   ("Politics & government", "Candidates idealised, promises broken, populations discarded. Helps: disillusioned voters and organisers, civics teachers, journalists"),
   ("Media & information", "Trusted outlets, algorithmic bubbles, attention as the product. Helps: journalists, media-literacy educators, fact-checkers, people lied to by trusted sources"),
   ("Education", "Curiosity extracted, \"failures\" discarded, compliance trained. Helps: students who blame themselves, teachers, homeschoolers, adult learners"),
   ("Healthcare & medicine", "Patient pain dismissed, \"difficult patient\" as technique. Helps: chronically ill patients, women and people of colour, healthcare workers"),
   ("Finance & economics", "Credit as love bombing, complexity as a weapon, debt as isolation. Helps: people in debt, low-wage workers, financial educators"),
   ("Technology", "Free platforms, privacy devalued, users sold. Helps: parents, tech workers, privacy advocates, people leaving social media"),
   ("Family & relationships", "Love bombing, sudden withdrawal, generational transmission. Helps: survivors, therapists, family-law advocates; often the entry episode"),
   ("Legal & justice", "Plea deals as coercion, complexity as obfuscation. Helps: defendants, legal-aid lawyers, reform advocates, families"),
   ("Corporate & workplace", "Impossible standards, manufactured crises, layoffs. Helps: burned-out workers, middle managers, gig workers, HR"),
   ("Military & security", "Recruitment as love bombing, veterans discarded. Helps: veterans, military families, conscientious objectors"),
   ("Entertainment & culture", "Parasocial relationships, manufactured drama. Helps: fans, creators, entertainment workers"),
   ("New age & wellness", "Healing commodified, \"raise your vibration\" as bypass. Helps: survivors of spiritual abuse, practitioners, people who feel betrayed after spending"),
   ("Food & agriculture", "Food engineered to be addictive, farmland consolidated. Helps: farmers, food-justice advocates, people with disordered eating"),
   ("Housing & real estate", "Shelter turned into speculation, eviction as control. Helps: renters, people facing eviction, housing advocates"),
   ("Sports & athletics", "Young bodies extracted, injured athletes discarded. Helps: athletes, parents of young athletes, coaches"),
   ("Science & academia", "Publish-or-perish, funding as control. Helps: graduate students, researchers, science communicators"),
   ("Non-profit & NGO sector", "Radical movements absorbed, below-market labour. Helps: non-profit staff, activists, funders"),
   ("Beauty, fashion & body image", "Shame manufactured, then sold back. Helps: people with eating disorders, young women, ageing people"),
   ("Dating & sexuality", "Romance as ideology, apps commodifying intimacy. Helps: people in or leaving abusive relationships, survivors of coercion"),
   ("Intelligence & surveillance", "Privacy devalued, whistleblowers isolated. Helps: activists, whistleblowers, journalists, targeted communities"),
   ("Child welfare & foster care", "Poverty punished, children extracted. Helps: parents in poverty, foster youth, caseworkers, adoptees"),
   ("Ageing, death & end-of-life", "Wealth extracted from the dying, isolation in facilities. Helps: elderly people, family carers, hospice workers"),
   ("Energy & environment", "\"Development\" promised, damage discarded. Helps: frontline communities, Indigenous peoples, climate advocates"),
   ("Transport & mobility", "Car dependence as freedom, public transit defunded. Helps: people trapped without a car, disabled people, urbanists"),
   ("Mental health & therapy", "Structural problems turned into individual diagnoses. Helps: clients, therapists, people questioning a diagnosis"),
   ("Pharmaceutical industry", "Disease definition, marketing as education. Helps: people on long-term medication, doctors, researchers"),
   ("Insurance", "Denial as business model. Helps: under-insured patients, healthcare workers, advocates"),
   ("Incarceration", "Rehabilitation rhetoric, labour extracted, no support on release. Helps: incarcerated and formerly incarcerated people, families, re-entry workers"),
   ("Immigration & borders", "Welcome promised, undocumented labour as a design feature. Helps: migrants, refugees, immigration advocates, border communities")]},
  {"h": "The intent", "p": [
   "The cycle people learn about in abusive relationships does not stop at the edge of the relationship. It scales into every system humanity has built. The aim is not to fight it but to see it: a pattern you can see is a pattern you can exit."]},
  {"h": "What makes it unique", "p": [
   "It is a bridge for people who recognise the pattern in one place and then keep seeing it elsewhere. Each sector gives different groups what they need: religious-abuse survivors, burned-out professionals, activists whose reforms were absorbed, patients dismissed by doctors, tech workers, immigrants.",
   "It works as an entry point either way: readers arrive from the personal (\"my therapist calls it narcissistic abuse, and I keep seeing it everywhere\") and leave with a structural map. It also gives therapists, educators and organisers a shared framework for systemic understanding.",
   "The closing chapters (the body, inherited patterns, what was here before, and the planet) keep it from ending in despair."]},
  {"h": "Who it's for", "p": [
   "The Fractal serves abuse survivors, professionals feeling the gap between their values and their systems, activists who watched reform get absorbed, young people trying to understand what they are inheriting, therapists, body-based practitioners, the spiritually minded, and parents.",
   "Its entry point: \"My therapist calls it narcissistic abuse, and I keep seeing it everywhere.\""]},
 ]},
# ---------------------------------------------------------------- FRACTURE
{
 "slug": "fracture", "title": "The Fracture", "sub": "The wealth transfer · 195 citations",
 "kicker": "The money behind it", "url": "noblefathercreations.com/fracture",
 "cover": "covers-existing/fracture.jpg",
 "chips": ["12 episodes", "195 citations", "$50 trillion", "Public record"],
 "sections": [
  {"h": "What it is", "p": [
   "A documentary-style reading in twelve episodes, built on the public record, of a documented fifty-trillion-dollar wealth transfer: where the money went, who received it, and how the architecture of that transfer lives in ordinary people.",
   "The cover numbers are the argument in short: **$50 trillion** transferred, **90%** the share of the bottom, **1%** the share of the beneficiary."]},
  {"h": "The twelve episodes", "items": [
   ("I · Fifty Trillion Dollars", "The scale of the transfer, the names behind it, and the proof that extraction is documented structure, not accident."),
   ("II · The Ownership Class", "Every name, every sector, and the five wealth tiers: who sits in each and what each costs those below."),
   ("III · Thirty Pipelines, One Destination", "All thirty sectors of The Fractal mapped as routes of extraction, and why single-sector reform fails."),
   ("IV · The Six Loops", "Six self-sustaining mechanisms that keep extraction running without central coordination, and why they absorb reform."),
   ("V · The Official Language", "What corporations, politicians and media say, read directly against the documented record."),
   ("VI · The Chair, Not the Sitter", "Why replacing the person in power leaves the structure, and its outcomes, unchanged."),
   ("VII · The Enforcer", "How the middle tiers (lawyers, managers, police, teachers, doctors) deliver harm they did not design."),
   ("VIII · The Body", "What the architecture does to the physical body: chronic stress, illness, exhaustion."),
   ("* · Sarah's Tuesday", "A companion story: one ordinary day inside the architecture."),
   ("IX · The Middle Tiers", "The defection Tier One fears most, and the bind of being both exploited and complicit."),
   ("X · The Differential", "Where the extraction lands hardest, by class, race, gender, disability and place."),
   ("XI · It Has Been Broken Before", "Documented moments when the loops were broken, and what it took."),
   ("XII · What Changes at Every Scale", "The action map: leverage points for individuals, communities and movements.")]},
  {"h": "Who each episode helps", "items": [
   ("1 · The Architecture", "Skeptics who need hard numbers"),
   ("2 · The Tiers", "People placing themselves in the hierarchy"),
   ("3 · The Pipelines", "People who understand one sector and want to see how it connects"),
   ("4 · The Six Loops", "Organisers whose reforms were absorbed"),
   ("5 · The Official Language", "Media critics, communicators, anyone exhausted by rhetoric"),
   ("6 · The Chair and the Sitter", "Voters and activists moving from reform to systemic work"),
   ("7 · The Enforcer", "Lawyers, doctors, teachers, managers, police"),
   ("8 · The Body", "People with chronic illness, healthcare workers"),
   ("9 · The Middle Tiers", "Managers, administrators, institutional workers"),
   ("10 · The Differential", "Communities carrying the most, and people with privilege"),
   ("11 · It Has Been Broken Before", "Activists, young people, anyone needing evidence-based hope"),
   ("12 · The Action Map", "People asking \"what do I do with this knowledge?\"")]},
  {"h": "What it draws on", "p": [
   "Every factual claim comes from the public record: court filings, SEC and other regulatory disclosures, peer-reviewed research, government reports, congressional records and investigative journalism by established outlets, over a 43-year period. 195 numbered references close the book.",
   "An editorial and legal notice states that the series is analysis and pattern recognition drawn from published sources, and that no claim is presented as the creator's personal knowledge."]},
  {"h": "The intent", "p": [
   "To answer \"is it real?\" with data, then answer \"why doesn't change come?\" with structure, then answer \"what can I do?\" with leverage points rather than promises."]},
  {"h": "What makes it unique", "p": [
   "Every factual claim is drawn from public records: court filings, regulatory disclosures, peer-reviewed research, government reports and investigative journalism. It does not ask readers to believe a conspiracy; it asks them to check a structure.",
   "It serves people who tried reform and need to understand why it was absorbed, middle-tier professionals recognising their own position, and organisers who need hard numbers and strategic leverage."]},
  {"h": "Who it's for", "p": [
   "The Fracture serves politically aware people who need an explanation for why change failed, data-minded people who need proof, middle-tier professionals, organisers, communities carrying differential extraction, researchers, and people in specific sectors who want to see where they fit.",
   "Its entry point: \"Something is extracting from me systemically, and I need to know what and why.\" Together with The Fractal, it offers a complete map from \"something is wrong\" to \"here is what's wrong, here is where it comes from, here is how it works, here is what I can do about it.\""]},
 ]},
# ---------------------------------------------------------------- FAITH
{
 "slug": "faith", "title": "The Sacred Divide", "sub": "Honor the faith. Name the machinery.",
 "kicker": "The faith book", "url": "noblefathercreations.com/faith",
 "cover": "covers-existing/faith.jpg",
 "chips": ["34 traditions", "10 families", "27 sections each", "A PDF for every tradition"],
 "sections": [
  {"h": "What it is", "p": [
   "A reference to how institutional power works inside 34 religious traditions, grouped into ten families. Every tradition has its own page, built on the same 27 sections, held to one evidence standard, with every claim sourced.",
   "It is written for believers, former believers and the people who love them. It is not written against faith: the title is the method, honor the faith, name the machinery. Each tradition can be read on its own, compared with any other section by section, or downloaded as a full PDF."]},
  {"h": "The religions it covers", "items": [
   ("Christianity · 8", "Christianity as a whole · Catholicism · Eastern Orthodoxy · Oriental Orthodoxy · Anglicanism · Protestant and Evangelical · Pentecostal and Charismatic · Plymouth Brethren (Exclusive Brethren)"),
   ("Islam · 5", "Islam · Sunni Islam · Shia Islam · Ahmadiyya · Dawoodi Bohra"),
   ("Judaism · 2", "Judaism · Orthodox and Hasidic Judaism"),
   ("Dharmic traditions · 4", "Hinduism · Sikhism · Jainism · Hare Krishna (ISKCON)"),
   ("Buddhism · 3", "Buddhism · Tibetan Buddhism · Soka Gakkai"),
   ("East Asian traditions · 3", "Confucianism · Taoism · Shinto"),
   ("Persian-born faiths · 2", "Zoroastrianism · Baháʼí Faith"),
   ("Restorationist and Adventist · 3", "Jehovah's Witnesses · Mormonism (LDS) · Seventh-day Adventism"),
   ("Indigenous and folk · 1", "Indigenous, folk and ancestral religions"),
   ("New movements and the spiritual marketplace · 3", "New Age and spiritual-but-organized movements · Scientology · Unification Church (Family Federation)")]},
  {"h": "What every tradition page holds", "items": [
   ("Orientation", "An at-a-glance panel (who is in charge, who chose them, who can remove them, where the money comes from, what leaving costs), a day inside, the unanswered question, the widest gap between word and record, the strongest objection answered, and what a healthy version looks like."),
   ("Structure", "History and timeline, branches and variants, how authority and law work, money and who holds what, genealogy, and reach into information, children and bodies."),
   ("The 30 techniques", "Thirty documented tactics of control across eight stages, each with how it shows up, the strongest defence of it, the counter, and an evidence grade: Codified, Documented, Cultural or Reformed."),
   ("The people", "Who gets hurt most, the middle tiers, documented cases, precedent, voices from inside, regional variants and the hard questions."),
   ("Help", "How to leave safely, where to get help, and every source. A disclosure scorecard grades how open each institution is.")]},
  {"h": "The 30 techniques", "items": [
   ("1 · Idealize", "Love Bombing · Weaponized Generosity"),
   ("2 · Hook", "Future Faking · Hoovering"),
   ("3 · Devalue", "Devaluation · Gaslighting · Double Bind"),
   ("4 · Confuse", "Intermittent Reinforcement · Moving the Goalposts · Strategic Ambiguity · Projection · DARVO · Normalization"),
   ("5 · Isolate", "Isolation · Triangulation"),
   ("6 · Extract", "Flying Monkeys · Smear Campaign · Silent Treatment · Manufactured Consent · Trauma Bonding · Learned Helplessness · Benevolent Control · Infantilization · Identity Erosion · Spiritual Bypassing · Financial Control"),
   ("7 · Discard", "Manufactured Crisis · Discard"),
   ("8 · Replace", "Replacement · Plausible Deniability")]},
  {"h": "One page in miniature: Catholicism", "items": [
   ("Size", "About 1.4 billion baptized (2023)"),
   ("Chosen by", "A conclave whose every elector was appointed by a previous pope"),
   ("Removable by", "Nobody. Canon law provides no mechanism to remove a pope"),
   ("Leaving", "Can bring excommunication and the denial of the sacraments"),
   ("Evidence", "4 of 30 techniques sourced to a named document. Grades: Codified 18, Documented 6, Cultural 5, Reformed 1")]},
  {"h": "The intent", "p": [
   "To separate faith from the coercive machinery that can grow around it, and to apply the same test to every tradition so that no one can say theirs was singled out.",
   "Believers get the questions to ask and the points of leverage inside their own tradition. People leaving high-control communities get a map, a safe-exit page and a list of help. Neither group is told what to believe."]},
  {"h": "What makes it unique", "p": [
   "Its consistency is its credential. Because every tradition is measured on the same 27 sections with sources, clergy, chaplains, interfaith groups, journalists, researchers and survivors can use it without suspecting a bias.",
   "Each section opens with a note before it and closes with a \"why this matters to you\" caption, source pop-ups sit one tap away, and a quick-exit button is on every page. It can hold a room of mixed beliefs in a single conversation, which almost nothing else in this field can."]},
  {"h": "Who it's for", "bullets": [
   "Believers, former believers and the people who love them",
   "People leaving high-control communities",
   "Clergy, chaplains and interfaith groups",
   "Journalists and researchers",
   "Survivors"]},
 ]},
# ---------------------------------------------------------------- SILENCE
{
 "slug": "silence", "title": "The Silence", "sub": "For men nobody thought to ask",
 "kicker": "For men", "url": "noblefathercreations.com/silence",
 "cover": "covers/silence.jpg",
 "chips": ["46 chapters", "7 movements", "Beside, not instead"],
 "sections": [
  {"h": "What it is", "p": [
   "A 46-chapter guide for men in coercive relationships: recognition, what help actually exists, and what to do next. It sits beside The Sovereign Divine Feminine, explicitly not instead of it."]},
  {"h": "The seven movements", "items": [
   ("Why Nobody Asked", "The numbers, honestly; why this sits beside the book for women, not instead of it; the three doors that were closed; what you will be accused of for reading this; the manosphere offering to help"),
   ("What It Looks Like When It's You", "The fog, being managed, money, sex as currency, children as leverage, being provoked into being the bad one"),
   ("The Machinery", "The reversal, threats about the children, the police call, violence you're not allowed to name, immigration and status"),
   ("Why You Haven't Said Anything", ""),
   ("What Is Actually Available", ""),
   ("The Mirror", ""),
   ("Out and After", "")]},
  {"h": "The intent", "p": [
   "To give men who have been told that no one will believe them the same quality of language and routing that is offered to other survivors, without turning that into a grievance against anyone else.",
   "The manuscript was tested against a standing rule: no chapter may be quotable as an argument for cutting women's services. The only place the position is stated outright is chapter 3, which is licensed to state it once."]},
  {"h": "What makes it unique", "p": [
   "It addresses a reader who has often been taught that their experience is unserious, and it is designed to be believed by that reader. The design argument is subtraction: no italic hero, no cards, a plain ruled list, a tighter measure. It is deliberately less literary.",
   "For services that want to support men without being accused of taking sides, it offers a carefully balanced reference. For women's services, it offers reassurance that the book was built not to undercut their work."]},
  {"h": "Who it's for", "bullets": [
   "Men in coercive relationships",
   "Men who have been told no one will believe them",
   "Services that want to support men without taking sides",
   "Women's services, reassured it was built not to undercut their work"]},
 ]},
# ---------------------------------------------------------------- REPAIR
{
 "slug": "repair", "title": "The Repair", "sub": "For the person on the other side of it",
 "kicker": "For the person who caused harm", "url": "noblefathercreations.com/repair",
 "cover": "covers/repair.jpg",
 "chips": ["48 chapters", "7 movements", "Behaviour change"],
 "sections": [
  {"h": "What it is", "p": [
   "A 48-chapter, seven-movement book (the densest in the library) for people who have harmed someone and want to change. Its standard of success is behaviour change measured over months by the people affected. Insight and remorse do not count."]},
  {"h": "The seven movements", "items": [
   ("Before You Decide What You Are", "This book will not call you a monster; the two performances; the honesty floor; who this is not for"),
   ("What You Actually Did", "The inventory, the pattern you'd name instantly in someone else, your own file, what your apologies have actually been for"),
   ("Why: Causes, Not Excuses", ""),
   ("The People You Did It To", ""),
   ("Stopping", ""),
   ("Amends, Properly", ""),
   ("The Rest of Your Life", "")]},
  {"h": "The content", "p": [
   "Roughly 58% of chapters end in a concrete \"try.\""]},
  {"h": "The intent", "p": [
   "To block both easy exits by name: \"I'm a monster\" and \"I'm actually fine.\"",
   "The book's standing rule is: if a paragraph would make the reader feel better about themselves without changing what they will do on Thursday, cut it. Chapters 2, 5 and 47 are deliberately uncompromising because they are what stop the book being used as a shield."]},
  {"h": "What makes it unique", "p": [
   "Honest, free material for people who cause harm is rare. Most of it either condemns the reader into defensiveness or comforts them into complacency. This one is built like a ledger, with hairline rules, squared-off corners, and no warmth that could read as absolution.",
   "For programmes working with people who cause harm, it offers a text that survivors' advocates can read without wincing. For the person who looked it up at 3am, it offers something real to do the next day."]},
  {"h": "Who it's for", "bullets": [
   "People who have harmed someone and want to change",
   "The person who looked it up at 3am",
   "Programmes working with people who cause harm",
   "Survivors' advocates, who can read it without wincing"]},
 ]},
# ---------------------------------------------------------------- AT WILL
{
 "slug": "atwill", "title": "At Will", "sub": "The coercive workplace",
 "kicker": "For workers", "url": "noblefathercreations.com/atwill",
 "cover": "covers/atwill.jpg",
 "chips": ["47 chapters", "7 movements", "The workplace"],
 "sections": [
  {"h": "What it is", "p": [
   "A 47-chapter, seven-movement guide that runs The Fractal's eight-stage cycle on a job, the way The Loop did for platforms. It teaches the pattern universally and routes the specifics, because employment law varies by country and often by region."]},
  {"h": "The seven movements", "items": [
   ("The Frame", "\"We're a family\"; where the power sits; passion as a wage discount; a bad job versus a coercive one"),
   ("The Moves", "The moving target, manufactured urgency, recognition instead of pay, isolation, the performance review as an instrument, the improvement plan that is a termination"),
   ("The Machinery", "HR is not your friend, NDAs, non-competes, arbitration clauses, gig classification, algorithmic management, surveillance, wage theft"),
   ("Who Is Doing It", ""),
   ("What You're Actually Owed", ""),
   ("Your Options", ""),
   ("The Ledger", "")]},
  {"h": "The intent", "p": [
   "To name the cases where nobody is choosing the harm, where an incentive structure produces it with no villain required, without letting that excuse anyone who is choosing.",
   "It is written for a lunch break, or a car in the car park before a shift."]},
  {"h": "What makes it unique", "p": [
   "It gives employees language and a record-keeping habit before they need a lawyer, and it gives HR leads, unions and advocates a shared vocabulary for what a \"bad job\" turns into when it becomes coercive.",
   "The page is set like a working file: a rule under the masthead like a form header, chapters as filed rows."]},
  {"h": "Who it's for", "bullets": [
   "Employees, on a lunch break or in the car before a shift",
   "Anyone wondering if it's a bad job or a coercive one",
   "HR leads",
   "Unions and workplace advocates"]},
 ]},
# ---------------------------------------------------------------- SLOW TAKE
{
 "slug": "slowtake", "title": "The Slow Take", "sub": "Elder financial exploitation, for the adult child",
 "kicker": "For adult children", "url": "noblefathercreations.com/slowtake",
 "cover": "covers/slowtake.jpg",
 "chips": ["45 chapters", "7 movements", "Later life"],
 "sections": [
  {"h": "What it is", "p": [
   "A 45-chapter, seven-movement guide to coercion and financial exploitation in later life, written for the adult child rather than for the older person."]},
  {"h": "The seven movements", "items": [
   ("The Setup", "Capacity and the fight over it; autonomy is not safety"),
   ("What It Looks Like", "The new friend, the isolating child, the phone that rings at the same time every day, romance later in life, the paperwork that appeared, the will that changed, care that became control, neglect, and exhaustion that is not malice"),
   ("Who Does It", "Family, which is most of it; the carer; the professional; the stranger with a script; the institution"),
   ("The Money", "Following it; power of attorney"),
   ("The Systems", ""),
   ("Acting", ""),
   ("The Ledger", "")]},
  {"h": "The intent", "p": [
   "An older adult being isolated and exploited is the least likely person to search for a book about it; their adult child is the one who searches.",
   "The book holds a tension and does not resolve it: autonomy is not safety, and safety is not the only value. An older adult keeps the right to make bad decisions. Guardianship removes legal personhood and is itself frequently abused. Chapter 42 (\"Am I the one benefiting?\") exists because an adult child who is themselves the exploiter would read this."]},
  {"h": "What makes it unique", "p": [
   "A book that picks a side produces either readers who steamroll a competent adult or readers who watch and call it choice. This one does neither.",
   "It is the only book in the library set in a sans-serif face, chosen for a frightened reader scanning on a phone, and chapters hang off a continuous vertical thread because the record it asks you to build is built entry by entry over months.",
   "It is a ready reference for adult-protective services, elder-law practices, banks' vulnerable-customer teams and carers' charities."]},
  {"h": "Who it's for", "bullets": [
   "Adult children worried about an ageing parent",
   "Adult-protective services",
   "Elder-law practices",
   "Banks' vulnerable-customer teams",
   "Carers' charities"]},
 ]},
# ---------------------------------------------------------------- LOOP
{
 "slug": "loop", "title": "The Loop", "sub": "The machine that learns you",
 "kicker": "Algorithms", "url": "noblefathercreations.com/loop",
 "cover": "covers-existing/loop.jpg",
 "chips": ["47 chapters", "8 movements", "Algorithms"],
 "sections": [
  {"h": "What it is", "p": [
   "A 47-chapter, eight-movement book on algorithmic manipulation: how optimisation found the things that hold human attention, who profits, and what actually works against it."]},
  {"h": "The eight movements", "items": [
   ("The machine that has no motive", "Why there is no villain to confront"),
   ("The mechanics", "The specific machinery, each part tested on millions of people and kept because it won"),
   ("The economy", "Who pays, who is paid, what is actually being sold"),
   ("The machine in other rooms", "The same machinery schedules shifts, prices groceries and ranks dates"),
   ("What it does to belief", ""),
   ("What it does to you", ""),
   ("The counter", "What works, starting from the admission that you cannot out-willpower an optimiser"),
   ("The ledger", "What the book may have wrong, how to help someone else, what has to happen at a larger scale")]},
  {"h": "The intent", "p": [
   "To remove the shame from the person scrolling. The book's central idea is that nobody designed this; selection pressure did. That makes it a structural problem with structural answers, not a character flaw."]},
  {"h": "What makes it unique", "p": [
   "It is a book about attention that refuses to harvest any: no streaks, no progress bar, no badges, no stored reading position, and it says so in its own text.",
   "It gives teachers, parents and digital-literacy programmes a vocabulary for what is happening without moralising, and it is honest about where the research is contested."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who feels the scroll pulling at them",
   "Teachers",
   "Parents",
   "Digital-literacy programmes"]},
 ]},
# ---------------------------------------------------------------- WEIGHING
{
 "slug": "scale", "title": "The Weighing", "sub": "How to be right about people",
 "kicker": "Discernment", "url": "noblefathercreations.com/scale",
 "cover": "covers-existing/scale.jpg",
 "chips": ["38 chapters", "6 movements", "Discernment"],
 "sections": [
  {"h": "What it is", "p": [
   "A 38-chapter, six-movement course in discernment. It moves past \"does this look like a tactic?\" to \"is that the best explanation for what happened?\""]},
  {"h": "The six movements", "items": [
   ("Why weigh at all", "Including a chapter on the book in the wrong hands"),
   ("The instrument is you", "Where your own detector was calibrated and what distorts it"),
   ("What counts", "Evidence standards, how a case builds itself, the two riskiest sources of information you will ever use"),
   ("The tests that work", "Four discriminators that separate manipulation from ordinary human failure, with a safety gate before all of them"),
   ("The mirror", ""),
   ("Living calibrated", "What to do with a conclusion, how to survive not having one, how to get back to trusting people")]},
  {"h": "The intent", "p": [
   "To protect readers from both failures: being fooled, and wrongly concluding that someone is a manipulator."]},
  {"h": "What makes it unique", "p": [
   "Most material in this field teaches detection. This one teaches judgement and builds in its own safeguard against misuse.",
   "That makes it useful to anyone who has to weigh claims about people for a living: journalists, investigators, HR, juries, mediators, and teachers of critical thinking."]},
  {"h": "Who it's for", "bullets": [
   "Anyone afraid of being fooled, or of wrongly accusing someone",
   "Journalists and investigators",
   "HR, juries and mediators",
   "Teachers of critical thinking"]},
 ]},
# ---------------------------------------------------------------- ROOT
{
 "slug": "root", "title": "The Root", "sub": "A shadow-work practice, in 18 guided steps",
 "kicker": "The practice", "url": "noblefathercreations.com/shadowroot",
 "cover": "covers/root.jpg",
 "chips": ["18 guided steps", "Private", "No account"],
 "sections": [
  {"h": "What it is", "p": [
   "A single guided practice rather than a book: take one reaction, trace the belief under it and where it came from, and finish with one true thing to do about it. It includes a paced breathing exercise and a body-map interaction."]},
  {"h": "How the practice moves", "items": [
   ("Name what surfaced", "A specific person, a pattern or habit, a fear, a memory, or a desire or hope."),
   ("Notice where it came from", "Already on your mind, running in the background, or seemingly from nowhere. \"From nowhere usually means from deep storage.\""),
   ("Trace its root", "Childhood, a specific relationship, or an institution or culture."),
   ("Write the belief plainly", "As a rule, not a feeling: \"I am too much\" rather than \"I felt bad.\""),
   ("Find it in the body", "Beliefs live in the body before they live in language. \"Hard to locate\" is a real, complete answer."),
   ("Breathe, then act", "A paced breathing exercise, then one true thing to do about it.")]},
  {"h": "What makes it unique", "p": [
   "It turns self-reflection into a bounded, repeatable exercise that can be done in a sitting.",
   "It is private and needs no account: what you write stays on your device."]},
  {"h": "Who it's for", "bullets": [
   "Anyone who wants to understand one reaction, in one sitting",
   "Therapists and coaches, between sessions",
   "Wellbeing programmes, as a structured individual practice"]},
 ]},
]
