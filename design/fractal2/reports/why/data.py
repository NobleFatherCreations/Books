# Source tables for "Why I Wrote This". Every row comes from the author's own text:
#   originals  -> The Fractal, "The Frequency" (30 counter-practice headings)
#   faculties  -> The Fractal, "The Spiritual Lens" (True Source Faculty table)
#   sectors    -> "The Spiritual Lens" (dominion + 30 gardens tables) and "The Frequency" (30 original impulses)
FAM = {
    "sed": ("Seduction", "draws you in", "#B97F00", "Idealize · Hook"),
    "des": ("Destabilization", "breaks your footing", "#2A6FC9", "Devalue · Confuse"),
    "iso": ("Isolation", "removes your witnesses", "#D4502F", "Isolate"),
    "ext": ("Extraction", "takes what you have", "#0F8F84", "Extract"),
    "dis": ("Disposal", "ends the cycle on you and resets it", "#9A46C4", "Discard · Replace"),
}

# name, family, the original it imitates, sacred faculty, how the copy works, the practice
TECH = [
 ("Love bombing","sed","Genuine welcome","Unconditional love","Warmth delivered faster than trust can be earned. The speed is the technique.","Slow trust. Match your own pace, not theirs: “I'm going to sit with this for a few days.”"),
 ("Weaponized generosity","sed","Clean giving","Generosity","A gift recorded on a ledger you never signed, produced when you try to leave.","Ask: “Am I free not to return this?” Give one thing this week and release the tracking."),
 ("Future faking","sed","Present inhabiting","Promise","A future vivid enough to keep you paying now, designed never to arrive.","Feet on the floor: “What is real right now?” Compare the brochure to the receipt."),
 ("Hoovering","sed","Completed exits","Welcome","The pull back in, timed to the moment you start to leave.","The pull is a reunion response, not information. Ask what has changed besides the words."),
 ("Devaluation","des","Inherent worth","Worth","Praise slowly converted into conditions, so you work harder to earn back what was free.","Write down what is true about you that no score, review or verdict can change."),
 ("Gaslighting","des","Self-trust","Genuine knowing","Your experience is denied until the system becomes your only source of truth.","Keep a written record. Your body is a record too: if it tensed, something happened."),
 ("Double bind","des","The third option","Choice","Two choices, both of which serve the system. Every door leads to the same room.","Name it aloud: “Both options serve the system.” Then look for the third."),
 ("Intermittent reinforcement","des","Steady presence","Stability","Reward on an unpredictable schedule. The nervous system bonds to the uncertainty.","Name the variable reward. Then value what is steady over what is intense."),
 ("Moving the goalposts","des","Arrival","Trust","The standard changes each time you meet it, so you never arrive.","Write your own finish line. When you reach it, stop and let yourself arrive."),
 ("Strategic ambiguity","des","Plain speech","Honest communication","Language clear enough to inspire and vague enough never to commit.","Ask for specifics, in writing. Ambiguity dissolves under a direct question."),
 ("Projection","des","Ownership","Accountability","The system accuses you of the very thing it is doing.","Ask: “Is this truer of the accuser than of me?” Then own only what is yours."),
 ("DARVO","des","Holding the naming","Justice","Deny, attack, reverse victim and offender. You raise the harm and leave feeling guilty.","Keep the timeline. You don't have to win the argument to keep hold of what happened."),
 ("Normalization","des","Recalibration","Presence","Harm raised in steps too small to trigger alarm, until it is the background hum.","The newcomer's test: would someone seeing this for the first time call it acceptable?"),
 ("Isolation","iso","Chosen solitude and genuine connection","Authentic belonging","Outside voices are removed until the system is the only world.","Keep at least one relationship the system doesn't own, and keep solitude that is chosen."),
 ("Triangulation","iso","Direct relationship","Relationship","A third party is inserted so people compete instead of comparing notes.","Talk to the other person directly. Cut out the middleman."),
 ("Flying monkeys","iso","Your own voice","Allies","People you love carry the system's message, so refusing it costs the relationship.","The messenger usually believes the message. Answer the source, in your own words."),
 ("Smear campaign","iso","Your own narrative","Witness","Your credibility is damaged in advance, so your account arrives already doubted.","Tell your account plainly and consistently. Don't chase every version of the story."),
 ("Silent treatment","iso","Responsive presence","Dialogue","Your concern is not argued with. It is simply not acknowledged.","Don't chase the silence. State your position once, in writing, and hold it."),
 ("Manufactured consent","iso","Genuine choice","Truth","An agreement made under conditions where refusal was impossible, later cited as proof you chose.","Ask what the alternative is. No alternative means compliance, not consent."),
 ("Trauma bonding","ext","Safe attachment","Attachment","The source of the hurt becomes the source of the relief, and the swing feels like devotion.","Ask: “Is this good for me, or have pain and relief become a loop?” Build one steady bond."),
 ("Learned helplessness","ext","One completed action","Empowerment","Every attempt to act is punished until the body stops trying and calls it peace.","Finish one small action today. The body needs evidence that effort still works."),
 ("Benevolent control","ext","Self-governance","Protection","Restriction and monitoring delivered in the language of care.","Ask who the protection serves. If it stops you leaving, it isn't protection."),
 ("Infantilization","ext","Self-trust in capability","Growth","You are positioned as incapable, and the dependency is called expertise.","Make one decision today without asking permission. Then another."),
 ("Identity erosion","ext","The original self","Wholeness","You walk in with a name and walk out with a label.","Keep one practice that belongs to who you were before the label."),
 ("Spiritual bypassing","ext","Honest reckoning","Transcendence","Sacred or therapeutic language used to skip the pain and avoid accountability.","If a teaching soothes you but changes nothing, it's a bypass. Feel it, then reckon with it."),
 ("Financial control","ext","Sovereign provision","Security","Money and debt used as a leash that makes leaving unaffordable.","Add up the cost of staying as well as leaving. Build even a small reserve: options are freedom."),
 ("Manufactured crisis","dis","Deliberate response","Urgency","An emergency created or inflated so you decide before you think.","When urgency appears, slow down: “If I wait 24 hours, will anyone be harmed?”"),
 ("Discard","dis","Self-retrieval","Dignity","Dropped without a conversation the moment you cost more than you produce.","Grieve the illusion, then call back the parts of yourself you gave away to stay."),
 ("Replacement","dis","Irreplaceability","Renewal","Your seat is filled before it cools: proof the warmth was for the position.","A function can be replaced. A person cannot. You were never the function."),
 ("Plausible deniability","dis","Witnessing","Freedom","Harm structured so that no one can be shown to have decided it.","Document, date and save. Deniability depends on there being no witness. Be the witness."),
]

# name, our relationship with, original impulse, garden, the gate ("flaming sword"), practice
SECT = [
 ("Religion","the divine","The impulse toward the sacred","The Sacred","A man who stands between you and God and calls himself necessary","Sit in silence for ten minutes, with no app and no script."),
 ("Politics","power","The impulse to organize together for the common good","Self-governance","The highest bidder","Go to the smallest local meeting, where your voice is a voice in a room."),
 ("Media","reality","The impulse to share truth and bear witness","Shared reality","The algorithm that decides what you see","Tell one person the truth about something you saw, in person, with no agenda."),
 ("Education","our own mind","The child's impulse to ask why","Curiosity","A grade, a ranking, a student loan","Learn something that will never appear on a résumé."),
 ("Healthcare","our own body","The body's knowledge of how to heal itself","Healing","A billing department","Ask your body what it is telling you, and bring that into the appointment."),
 ("Finance","survival","The impulse to exchange, sustain and provide","Enough","A number the system assigned to you","Give or lend something without tracking it."),
 ("Technology","attention and identity","The impulse to extend our ability through tools","Connection","The screen that watches you back","Pick the device up, use it for the task, put it down."),
 ("Family","love","The need for unconditional love","Love","Conditions where none were supposed to exist","Love one person today without a condition or a ledger."),
 ("Legal system","freedom and fairness","The impulse toward fairness and the repair of harm","Justice","A priced courtroom","When harm happens, ask: “What would repair look like?”"),
 ("Corporate work","our labour","The impulse to create, contribute and collaborate","Meaningful work","A performance review","Make something no one will pay you for."),
 ("Military","our sovereignty","The impulse to protect the vulnerable","Protection","A gun pointed outward while the threat is inward","Protect someone who can't repay you, with no audience."),
 ("Entertainment","being seen","The desire to express and be witnessed","Expression","An industry that turns expression into product","Create something and don't post it."),
 ("Wellness","our wound","The wound's natural movement toward healing","The wound","A price tag on the journey inward","Let something heal at its own pace, without a program."),
 ("Food","nourishment","The body's need for nourishment from the living earth","Nourishment","A price tag on what the ground grew for free","Eat one thing your great-grandmother would recognize, slowly."),
 ("Housing","rest","The body's need for rest and safe shelter","Shelter","A mortgage","Rest today without earning it first."),
 ("Sports","our physical self","The joy of the body in motion","Joy of movement","A contract where play was supposed to be","Move without measuring."),
 ("Science","truth and inquiry","The need to understand reality through honest inquiry","Truth","A funding source with an agenda","Ask a question you aren't “qualified” to ask, and follow it."),
 ("Nonprofits","compassion","The impulse to help the suffering","Compassion","An overhead budget","Help one person directly, hand to hand."),
 ("Beauty","self-acceptance","The body born complete and whole","Bodily wholeness","The mirror replaced by a magnifying glass","Look in the mirror for what is there, not what is missing."),
 ("Dating","intimacy","The ache to be truly known by another","Being known","A screen between you and every face","Tell one trusted person something real and uncurated."),
 ("Surveillance","privacy and autonomy","The right to a private inner life","Privacy","A camera called safety","Keep something to yourself. Phone in another room for an hour."),
 ("Child welfare","innocence","The child's need to be held and chosen","Innocence","A case file where a name was supposed to be","Hold a child with both arms and your full attention."),
 ("Aging and death","mortality","The body's right to complete its arc in peace","The passage","A final bill","Tell someone you love how you want the end to feel."),
 ("Energy and environment","the living earth","The communion between the human and the living earth","The living earth","A drill in the body of the planet","Put your hands in soil or your bare feet on grass."),
 ("Transportation","movement and access","The freedom to move through the world under your own power","Movement","A world you can't walk through","Walk somewhere you would normally drive."),
 ("Mental health","our inner world","The sovereignty of the inner world","The inner world","A diagnosis where a witness was supposed to be","Sit with a feeling for ten minutes before you name it."),
 ("Pharmaceuticals","what enters our body","The body's right to decide what enters it","Relief","A patent on the molecule","Give your body a vote, and ask about alternatives. Never stop a medicine without your clinician."),
 ("Insurance","risk and safety","The feeling of safety that requires no purchase","Shared risk","A denied claim","Sit somewhere you feel safe and notice that the feeling is free."),
 ("Incarceration","confinement","The right to freedom and restoration even after a mistake","Freedom","A cage called corrections, charged per night","Loosen one grudge. Forgiveness opens your own door."),
 ("Immigration","belonging and displacement","The right to belong wherever you stand on the earth","Belonging","A border and a document","Stand still and feel the ground hold you, as it holds everyone."),
]

# stage, what it looks like, what it actually is, what it sounds like, real need, spiritual principle, checklist question
STAGE = [
 ("Idealize","The system finds your exact hunger and offers itself as the only thing that can fill it.","Not generosity but reconnaissance: mapping what you lack.","“You're special. We've been waiting for you.”","To be seen and chosen","Election: chosen before performing","Is this warmth unconditional, or aimed at my specific hunger?"),
 ("Hook","You give time, identity, money and trust, and each gift becomes a thread that ties you in.","The moment leaving becomes too expensive.","“Plant your roots here. Sign for four years.”","Secure commitment","Covenant: unbreakable from the source's side","What am I being asked to invest, and what would leaving cost?"),
 ("Devalue","Unconditional warmth becomes conditional. The bar rises. You can never quite earn it back.","Your worth stops being something you carry and becomes something they assign.","“You've changed. You're not applying yourself.”","Worth that needn't be earned","Inherent worth: “fearfully and wonderfully made”","Has the warmth become conditional? Am I being told I'm not enough?"),
 ("Confuse","Contradiction by design. What was true yesterday is false today.","A person who trusts their own perception can leave. Confusion removes that.","“That never happened. You misunderstood.”","Trust in what you see and feel","Truth and discernment: the still, small voice","Am I doubting my own perception? Is the information contradictory?"),
 ("Isolate","Every outside source of reality is removed, one closed door at a time.","No prison is needed. Every other room is made to look uninhabitable.","“Those people don't understand us.”","Connection and witnesses","Community: “not good to be alone”","Am I losing outside perspectives? Are other connections discouraged?"),
 ("Extract","The operational phase. The system takes what it came for.","By now there is no compass, no exit and no ally.","No sound. A feeling: tired in a way sleep doesn't fix.","Fair exchange; enough","Abundance: giving from overflow","What is being taken: energy, money, time, health, identity?"),
 ("Discard","When you cost more than you produce, you are dropped with administrative indifference.","Timed, not random. You were an operation, not a relationship.","“We wish you well in your future endeavours.”","Someone who stays","Unfailing presence: “I am with you always”","Am I being treated as disposable now that I've slowed down?"),
 ("Replace","Your seat is filled before it cools. The newcomer gets the same words.","The words were written for the position, and the position is always open.","The system hums exactly as it did before you came.","To be irreplaceable","Known by name: the shepherd leaves the 99 for the 1","Is the same cycle already running on someone new?"),
]
STAGE_COL = ["#B97F00","#B97F00","#2A6FC9","#2A6FC9","#D4502F","#0F8F84","#9A46C4","#9A46C4"]
