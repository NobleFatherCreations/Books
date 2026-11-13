#!/usr/bin/env python3
"""Final woven edition of "Why I Wrote This". Reuses every section of build.py unchanged (split by id),
reorders them into six movements, and adds the new material. Usage: final.py master|foil -> final-<ed>.html"""
import sys, re, html, textwrap, pathlib
HERE = pathlib.Path(__file__).parent
ED = sys.argv[1] if len(sys.argv) > 1 else "master"
src = (HERE / "build.py").read_text()
ns = {"__file__": str(HERE / "build.py")}
sys.argv = ["build.py", "foil"]
exec(src[:src.index("CSS = (HERE")], ns)
foil_html = ns["body"]()
ns["ED"] = "master"; ns["_f"][0] = 0
old = ns["body"]()
tx, wrapt, box, arrow, svg, fld, d_chain, FAM, SECT, E = (ns[k] for k in "tx wrapt box arrow svg fld d_chain FAM SECT E".split())
INK, INK2, INK3, LINE, PAPER2, GOLD, WASH = "#16171B", "#45443F", "#6B6860", "#D6CDBD", "#F6F1E7", "#8A5E00", "#F6EBD0"

# ---- split the first draft into its sections
chunks = re.split(r'(?=<div class="sec)', old[old.index('<div class="sec" id="s1">'):])
S, cur = {}, None
for c in chunks:
    m = re.match(r'<div class="sec(?: pb)?" id="(\w+)"', c)
    if m: cur = m.group(1)
    S[cur] = S.get(cur, "") + c
S["s13"] = S["s13"] + S.pop("rubric")
S["s16"] = re.sub(r'</section>\s*$', '', S["s16"])
MAP = {1: 1, 2: 6, 3: 20, 4: 2, 5: 3, 6: 5, 7: 7, 8: 8, 9: 10, 10: 12, 11: 13, 12: 14, 13: 19, 14: 15, 15: 16, 16: 21}
def renum(t):
    t = re.sub(r'(Sections? )((?:\d+(?:, | and |, and )?)+)', lambda m: m.group(1) + re.sub(r'\d+', lambda n: str(MAP.get(int(n.group()), int(n.group()))), m.group(2)), t)
    return re.sub(r'<div class="kick">(\d+) · ', lambda m: '<div class="kick">%d · ' % MAP[int(m.group(1))], t)
S = {k: renum(v).replace('class="sec pb"', 'class="sec"') for k, v in S.items()}
S["s10"] = S["s10"]  # connections (extended below)
# the old Trauma Bond chain moves to the new combinations section
S["s9"] = re.sub(r'<figure class="fig chain">.*?</figure>', '', S["s9"], count=1, flags=re.S)
S["s9"] = S["s9"].replace('<figure class="fig chain">', '<p>The same engineering shows up outside schools. Here is one from my Entertainment sector, and one I drew from the Education chapter.</p><figure class="fig chain">', 1)

IMP = [("The sacred", "Before the building and the doctrine there was the encounter itself: the edge of the ocean, the silence in the forest, a newborn's eyes. It needs only your attention."),
 ("Deciding together", "Before the party there was the circle where everyone spoke. The impulse to govern is not the impulse to control. It is the impulse to take part."),
 ("Bearing witness", "Before the feed there was the person who saw something and said so. Not content. Testimony."),
 ("Asking why", "The child on the floor staring at a bug. The curiosity was never for something. The curiosity was the thing."),
 ("The body healing itself", "The body grew itself from one cell and has repaired itself ever since. The ache, the tiredness and the craving are messages."),
 ("Exchange and enough", "The fisherman who traded fish for bread. The system was having enough, not wanting more."),
 ("Tools", "The hand that picked up a stick to reach the fruit. A tool extends you without replacing you. The tool is for you; you are not for the tool."),
 ("Unconditional love", "The infant's need to be held. Not because of anything done. Because I am here."),
 ("Fairness and repair", "The child who says “that's not fair” is speaking it. When harm happens, the answer should repair, not only punish."),
 ("Making", "Waking up and moving something from imagination into the world, for the making itself."),
 ("Protecting the vulnerable", "Stepping between the harm and the harmed. Not the weapon or the flag. The willingness."),
 ("Expression", "The song that wasn't written for a label. Making the inside visible. The audience was always optional."),
 ("The wound healing", "A wound moves toward closing the way water moves toward the sea, at its own pace."),
 ("Nourishment", "The body said “I need” and the earth said “here.” Food as a relationship, not a product."),
 ("Rest", "Rest was never a reward. It is as non-negotiable as a heartbeat. The body doesn't earn the right to beat."),
 ("Joy in motion", "The child running in circles for no reason. Moving means: I am alive."),
 ("Understanding", "Looking at the sky and asking why it's blue. The willingness to not know is the door every real answer came through."),
 ("Helping", "The neighbour whose house burned got the spare room. Help as a reflex, hand to hand."),
 ("Wholeness", "The body arrived complete. It was never the “before” in a before-and-after."),
 ("Being known", "Not seen. Known. Someone entering the room you don't show anyone, and staying."),
 ("A private inner life", "The right to think without being watched. The last sovereign territory."),
 ("Being held and chosen", "Every child needs to be chosen as a person, not processed as a case."),
 ("A peaceful ending", "Dying is the body completing its work, the way an exhale completes a breath."),
 ("The living earth", "We are made of it. The relationship was a conversation: here, take this; thank you, I will tend it."),
 ("Moving freely", "Walking is the first freedom the body chooses for itself. Three miles an hour is the human speed."),
 ("The inner world", "The landscape inside you that no one else has seen. It was yours to read before anyone offered to read it for you."),
 ("Deciding what enters your body", "The body has its own pharmacy and gets the first vote. Not anti-medicine. Pro-sovereignty."),
 ("Safety", "The felt sense of “I am okay right now.” The shoulders dropping. It is free."),
 ("Freedom after a mistake", "People make mistakes. The answer is restoration: accountability, repair, and a way back."),
 ("Belonging where you stand", "The earth holds every body with the same gravity. It doesn't check documents.")]

def part(n, title, q):
    return f'<div class="part{" first" if n == 1 else ""}"><i>Movement {n}</i><h2>{title}</h2><p>{q}</p></div>'
def stop(q, h=13):
    return f'<div class="stop keep"><b>Stop and notice</b><p>{q}</p>{fld(h)}</div>'

def d_ladder():
    b = ""
    steps = [("THE FRACTAL", "30", "techniques per sector", "The alphabet", "“It's not just me.”", 96),
             ("FRACTAL²  ·  TACTICS", "300+", "named tactics per sector", "The dictionary", "“That's the one.”", 150),
             ("FRACTAL²  ·  COMBINATIONS", "150+", "ordered sequences per sector", "Sentences", "“That's my life. And there's the exit.”", 204)]
    for i, (k, n, u, like, says, h) in enumerate(steps):
        x = 10 + i * 224; y = 230 - h
        b += box(x, y, 212, h, WASH if i == 2 else PAPER2, GOLD, 4, 1.8 if i == 2 else 1.1)
        b += tx(x + 106, y + 20, k, 8.6, 700, GOLD, "middle", 1.3)
        b += tx(x + 106, y + 56, n, 30, 500, INK) + tx(x + 106, y + 72, u, 9, 400, INK2)
        if h > 110: b += tx(x + 106, y + 98, "× 3 scales", 9, 600, INK3) + tx(x + 106, y + 112, "person · institution · society", 8.4, 400, INK3)
        if h > 170: b += tx(x + 106, y + 138, "each one a scene from a life,", 8.8, 400, INK2) + tx(x + 106, y + 150, "the order, and the way out", 8.8, 400, INK2)
        b += tx(x + 106, 248, like, 11, 700, INK) + tx(x + 106, 264, says, 9.4, 400, INK2, "middle", 0, 'font-style="italic"')
        if i < 2: b += arrow(x + 212, 214, x + 224, 214, INK3, 1.4)
    return svg(680, 272, b)

def d_school():
    b = ""
    b += tx(340, 14, "ONE SCHOOL, FIVE MACHINES", 9.4, 700, INK, "middle", 1.5)
    n = [(20, 40, "The teacher", "The Normalization Engine", "34 students, no break, “welcome to teaching”", "des"),
         (250, 40, "The classroom", "The Public Shaming Ritual", "a name on the board, a boy in the hall", "iso"),
         (480, 40, "The meeting", "The Paper Child", "eleven adults, one mother, one signature", "ext"),
         (480, 150, "The psychologist", "The Calling Trap", "four buildings, ninety minutes per child", "dis"),
         (20, 150, "The gym", "The Trauma Bond Engine", "“he made me who I am”", "sed")]
    for x, y, who, name, d, k in n:
        c = FAM[k][2]
        b += box(x, y, 180, 70, "#fff", c, 4, 1.8) + tx(x + 90, y + 18, who.upper(), 8.4, 700, c, "middle", 1.2) + tx(x + 90, y + 35, name, 10.4, 700) + wrapt(x + 90, y + 50, d, 38, 8.4)
    b += arrow(200, 75, 250, 75, INK3, 1.6) + arrow(430, 75, 480, 75, INK3, 1.6) + arrow(570, 150, 570, 110, INK3, 1.6)
    b += tx(225, 67, "produces", 7.8, 400, INK3) + tx(455, 67, "produces", 7.8, 400, INK3) + tx(600, 134, "feeds", 7.8, 400, INK3, "start")
    b += box(250, 150, 180, 70, WASH, GOLD, 4, 1.8) + tx(340, 172, "THE CHILD", 8.6, 700, GOLD, "middle", 1.3) + wrapt(340, 188, "leaves with a sentence about themselves that someone else wrote", 36, 8.8, 500, INK)
    b += arrow(200, 185, 250, 185, INK3, 1.6) + arrow(480, 185, 430, 185, INK3, 1.6) + arrow(340, 110, 340, 150, INK3, 1.6)
    b += tx(340, 240, "Nobody in this picture is a villain. Each adult is inside a machine of their own, and each machine hands its output to the next.", 9, 600, INK2)
    return svg(680, 248, b)

def d_ripple():
    rows = [("A PERSON", "sees the move while it is happening, and pauses", 150), ("A HOME", "the old sentence stops halfway out of a parent's mouth", 250),
            ("A SCHOOL, A CLINIC, A WORKPLACE", "people use the same plain words for the same thing", 370), ("AN INSTITUTION", "is asked eight questions before a policy goes live", 500),
            ("A CULTURE", "can no longer be told “that's just how it is”", 650)]
    b = ""
    for i, (t, d, w) in enumerate(rows):
        y = 6 + i * 44; x = 340 - w / 2
        b += box(x, y, w, 36, WASH if i == 0 else PAPER2, GOLD, 18, 1.4)
        b += tx(340, y + 15, t, 8.6, 700, GOLD, "middle", 1.3) + tx(340, y + 28, d if w > 240 else "", 9, 400, INK2)
        if w <= 240: b += tx(340, y + 28, "sees it, and pauses", 9, 400, INK2)
    return svg(680, 230, b)

def combo(n, name, tag, scene, cut, chain, why, inst, civ, cues, breakers, q):
    return f'''<div class="combo"><div class="ckick">Combination {n}</div><h3 class="cname">{name}</h3><p class="ctag">{tag}</p>
<div class="scene">{scene}</div><p class="cut">{cut}</p>
<figure class="fig chain">{chain}</figure>
<div class="cols"><div><h4>Why this order</h4>{why}</div><div><h4>The same machine, larger</h4><p class="small"><b>In an institution.</b> {inst}</p><p class="small"><b>Across a society.</b> {civ}</p></div></div>
<div class="cols"><div class="box plain"><h4>How to tell you're inside it</h4>{cues}</div><div class="box"><h4>What breaks the chain</h4>{breakers}</div></div>
<p class="cq">{q}</p></div>'''

C1 = combo(1, "The Trauma Bond Engine", "The pain becomes the proof of love.",
 '''<p>You're seventeen and your travel basketball coach is the reason you're still playing. He told you that you had D1 potential when your school coach barely played you. He believed in you.</p>
<p>But his practices are humiliating. He screams at you in front of the team. He's benched you for whole tournaments over one bad play. After one game he told you, in front of your parents, that you “don't have the mental toughness to play at the next level.” You cried the whole way home. You told your mom you wanted to quit. She said, “He's hard on you because he sees something in you.”</p>
<p>The next day he pulled you aside. Quiet voice. Hand on your shoulder. “I was tough yesterday because I refuse to let you waste what you have. I don't do that for players I don't believe in. You know that, right?”</p>
<p>Two years later you're injured, burned out, and playing for a college you didn't choose. When someone asks if you love the game, you hesitate. When someone asks if you'd be here without him, you say, without thinking: “He made me who I am.”</p>
<p><b>You're not wrong. That's the problem.</b></p>''',
 "Seven tactics that fuse a person to the source of their pain. Each round of harm is followed by just enough warmth to deepen the bond.",
 d_chain("The Trauma Bond Engine", [("Intermittent reinforcement", "screams one day, hand on your shoulder the next", "des"), ("Trauma bonding", "relief after pain becomes the strongest feeling in the cycle", "ext"), ("Relief bait", "“I don't do that for players I don't believe in”", "sed"),
  ("Push-pull", "benched, then “D1 potential”", "des"), ("Fear, obligation, guilt", "leaving feels like moral failure", "iso"), ("Hoovering", "the quiet voice, just as you pull away", "sed"), ("Conditional love", "belief in you, only when you comply", "ext")],
  "the pain is reframed as investment, and you accept it, because the alternative is unbearable.", [(1, "“It hurt me.” Full stop"), (4, "Ask an outsider what they see"), (5, "Trace the fear, the debt and the guilt to who installed them")], "From my Education combination script."),
 '''<p class="small">Harm without kindness doesn't bond anyone. It produces hatred, or flight. The unpredictable kindness has to come <b>first</b>, because randomness is what keeps a nervous system scanning.</p>
<p class="small">Skip the relief bait and the pain stays pain, and the person eventually leaves. Try to pull someone back before the fear, obligation and guilt are in place, and they can simply go.</p>
<p class="small">This is what makes it harder to break than ordinary dependence: you aren't only hooked on the cycle. You've been convinced <em>the cycle is the relationship.</em></p>''',
 "A university with a brutal culture. You cry every finals week. Then the professor who failed half the class gives you a B+. When you try to leave, the dean emails personally. At the reunion you tell new students: “It's brutal. But it made me who I am.”",
 "“School is hard. That's the point.” Every generation suffers through it and tells the next: we went through it, you can too. The engine needs no operator. Every graduate becomes its advocate.",
 '''<ul class="small"><li><b>The “made me who I am” test.</b> Did it make you, or did you survive it?</li><li><b>The defence reflex.</b> You don't defend what served you. You defend what you're bonded to.</li><li><b>The FOG scan.</b> What was I afraid of? What did I feel I owed? What would I have felt guilty about?</li></ul>''',
 '''<ol class="small"><li><b>Separate the pain from the meaning.</b> Rewrite the sentence without the silver lining. “It hurt me.”</li><li><b>Borrow outside eyes.</b> “Tell me what this looks like from where you're standing.”</li><li><b>Ask who installed the fear,</b> the debt and the guilt. It is usually whoever is causing the harm.</li></ol>''',
 "What is something you endured that you still call “growth”? Have you ever considered that it was pain you were never given permission to name?")

C2 = combo(2, "The Normalization Engine", "One degree at a time, until you stop feeling the heat.",
 '''<p>You're in your third year of teaching. Year one, you were appalled that your class had thirty-four students and no aide. You wrote emails. Your mentor said, “It's always been like that. You get used to it.”</p>
<p>Year two, a student told you they hadn't eaten since lunch the day before. The counsellor said, “We know. There's a waitlist.” You bought the kid breakfast. By the end of the year you were buying three kids breakfast every morning. You didn't report it anymore. You just handled it.</p>
<p>Year three, the district removed your planning period. Six straight periods. Lunch in four minutes. You haven't used the bathroom during school hours in weeks. You mentioned it to a colleague. She laughed and said, “Welcome to teaching.”</p>
<p>You haven't changed your values. The gap between your values and your reality has been closed, not by the system improving, but by your tolerance expanding.</p>
<p><b>You didn't accept these conditions. You were trained to absorb them.</b></p>''',
 "Seven tactics that worsen conditions slowly while training people to treat each step as the new baseline.",
 d_chain("The Normalization Engine", [("Gradual escalation", "30 becomes 32 becomes 34", "des"), ("Repetition as truth", "“it's always been this way”", "des"), ("Social proof", "nobody else is reacting", "iso"), ("“That's just how it is”", "a stop sign for thinking", "des"),
  ("Anchoring", "your first year sets the scale", "des"), ("Gaslighting", "“you're just new”", "des"), ("Window shifting", "the unthinkable arrives as a small change", "dis")],
  "the day you stop reporting it and just handle it.", [(1, "Describe your day to a stranger"), (4, "Compare to a standard, not to last year"), (6, "Let fresh eyes be your mirror")], "From my Education combination script."),
 '''<p class="small">Social proof only works after the escalation has begun: “no one else seems alarmed, so maybe I'm overreacting.” The stop-sign phrase only works after months of repetition have made it sound like a law of nature.</p>
<p class="small">Gaslighting is what separates a person from their own alarm. Once healthy outrage has been relabelled as inexperience, they will walk through any fire the system sets.</p>
<p class="small">The engine runs on our greatest survival skill. <em>Humans adapt.</em> It feeds us harm in doses small enough to absorb.</p>''',
 "Each year class sizes rise slightly and support falls slightly. New hires have no reference point, and the veterans who could testify to the change have been normalized into silence. The speed is one budget cycle at a time.",
 "Testing began as a diagnostic tool and became the centre. Recess shrank, arts were cut, counsellor ratios worsened. Each change was small and “reasonable.” A society looks at boiling water and says: that's just how it is.",
 '''<ul class="small"><li><b>The outrage audit.</b> What shocked you in your first year that doesn't now?</li><li><b>The time-lapse test.</b> Describe your day to an outsider and watch their face.</li></ul>''',
 '''<ol class="small"><li><b>Write the conditions down</b> as if for someone who has never seen them. Read it aloud.</li><li><b>Compare to a standard, not a trend.</b> What does the research recommend?</li><li><b>Say it to someone new.</b> Borrowed eyes are sometimes the only way to see.</li></ol>''',
 "What did you once find unacceptable that you now call normal? When did you stop noticing the change?")

C3 = combo(3, "The Public Shaming Ritual", "Five minutes on a whiteboard. A lifetime in the head.",
 '''<p>You're eleven. You forgot your homework, and not for the first time. Your parents are getting divorced, you sleep at a different house every other night, and your backpack is the one thing that's supposed to hold everything together. It doesn't.</p>
<p>Your teacher doesn't pull you aside. She walks the rows. No homework? She writes your name on the board under a header: <b>NOT PREPARED.</b> She says, “This is the third time. I'm very disappointed. I expected more from you.” Twenty-six kids are looking at you. You don't cry, because crying would make it worse.</p>
<p>At recess a kid says, “Hey, NOT PREPARED.” It isn't mean, exactly. The board gave him the word, and the word gave him permission.</p>
<p>The next morning you hand in the assignment, done at midnight at your mom's kitchen table. Your name stays on the board.</p>
<p><b>The punishment was public. The correction is invisible. The shame stays on the wall.</b></p>''',
 "Six tactics that turn the room into the punishment, until the child carries the audience inside.",
 d_chain("The Public Shaming Ritual", [("Public identification", "a name on the board", "iso"), ("Moral framing", "“I expected more from you”", "des"), ("Audience activation", "26 witnesses who could be next", "iso"),
  ("Social licence", "“Hey, NOT PREPARED”", "iso"), ("Correction invisibility", "the fix is never shown", "dis"), ("Internalized surveillance", "the board moves inside", "ext")],
  "the child begins to check, and re-check, with nobody watching.", [(1, "Give feedback in private"), (4, "Make the recovery the visible moment"), (5, "“That was their system, not my worth”")], "From my Education combination script."),
 '''<p class="small">Without the audience, the same words are private feedback. Without the moral language, a missing paper is just a missing paper. “Disappointed” is what turns a list into a verdict.</p>
<p class="small">The engine is the asymmetry: failure is displayed, recovery is hidden. If the board said “PREPARED today,” the story would balance. It doesn't, because shame is the point.</p>
<p class="small">The teacher did not know about the two houses. <em>The moral frame made them irrelevant.</em></p>''',
 "A district publishes a school report card: scores, attendance, discipline. It shows outcomes without inputs: no funding per student, no counsellor ratios, no poverty rate. A red F appears beside a school's name, families leave, resources follow them, and the rating drops again.",
 "The dunce cap, the corner, the red ink, the dashboard. The tools modernized. The architecture didn't. The children who internalize it most deeply, who can't sleep before a test, are not the system's success stories. They are its most perfectly shamed products.",
 '''<ul class="small"><li><b>The audience test.</b> Could it have been said privately?</li><li><b>The asymmetry test.</b> Is failure visible and recovery invisible?</li><li><b>The legacy test.</b> How old were you? Can you still feel it?</li></ul>''',
 '''<ol class="small"><li><b>Parents:</b> ask that performance not be displayed publicly. A boundary, not an accusation.</li><li><b>Teachers:</b> track missing work privately. Make the comeback the public moment.</li><li><b>Students:</b> “You are not the name on the board. You are the kid who did it at midnight.”</li></ol>''',
 "Think of a time you were shamed in front of a class. How old were you? How old are you now? If you can still feel it, the ritual is still running.")

C4 = combo(4, "The Paper Child", "The file speaks before the child does.",
 '''<p>You're the school psychologist. You cover four buildings. Today you have ninety minutes for a boy named Marcus.</p>
<p>You met his file before you met him. Fourteen pages. Eleven office referrals since October. “Defiant.” “Disruptive.” “Threw a chair.” Nowhere in fourteen pages does it say what he is good at.</p>
<p>He's nine. He comes in with his hood up. He's quick, quicker than the file said. Around the forty-minute mark he asks if you have any food. You find a granola bar. He eats half and puts the other half in his pocket. You ask who it's for. “My sister.” They've been staying at his aunt's since his dad left. The baby cries all night, and he's the one who gets up.</p>
<p>It isn't on any form. There's no box for it.</p>
<p>Thursday is the meeting. Eleven adults. One mother, straight from a night shift, still in her work shirt. Someone says “emotional disturbance.” Someone slides a paper toward her and says, kindly, “This is how we get him help.” She looks at you. She signs.</p>
<p>Three years later, in a middle school you also cover, a teacher you've never met nods at a tall boy outside the office. “That's Marcus. He's one of our ED kids. I read his file.” He hears her. He doesn't look up.</p>
<p><b>He already knows what he is.</b></p>''',
 "Eight tactics that replace a child with a document. Nobody in it intends harm. Everyone follows procedure.",
 d_chain("The Paper Child", [("Deficit framing", "“what's wrong with him?”", "des"), ("Selective records", "incidents written down, kindness not", "des"), ("Routine referral", "the only relief valve a teacher has", "des"), ("Expert intimidation", "eleven professionals, one parent", "ext"),
  ("Manufactured consent", "“this is how we get him help”", "iso"), ("Benevolent control", "help only through the label", "ext"), ("Identity erosion", "“I'm a behaviour kid”", "ext"), ("The file arrives first", "discredited in advance", "dis")],
  "a mother signs while overwhelmed, and later a teacher decides who he is before he speaks.", [(1, "Meet the child before the file"), (2, "Write what happened to him first"), (4, "Ten minutes alone with the parent"), (7, "A review date on the label")], "A composite I wrote for people who work in schools. It describes a design, not anyone's intent."),
 '''<p class="small">If the documentation weren't selective, the file would hold the aunt's house, the baby and the half granola bar, and the meeting would be about a tired nine-year-old.</p>
<p class="small">If consent came before the outnumbering, his mother could ask about alternatives. After forty minutes of scores she can't find the question.</p>
<p class="small">If help weren't locked behind the label, nobody would need him to qualify. <em>The gate creates the pressure to find something wrong.</em></p>''',
 "One psychologist for four buildings, where the profession's own guidance is roughly one per five hundred students. The role shrinks from understanding children to testing and placing them. Funding follows eligibility, so the only door to help has a label on it.",
 "A society that will pay for a diagnosis but not for a quiet place to sleep keeps producing diagnoses. Boys, poor children and children of colour are sent through this door more often for the same behaviour, and the numbers are then read as facts about the children, not about the door.",
 '''<ul class="small"><li><b>The first-good-thing test.</b> How many pages before a strength?</li><li><b>The verb test.</b> Does the file say what he <em>did</em>, or what he <em>is</em>?</li><li><b>The table count.</b> Who spoke most, and who spoke last?</li><li><b>The stranger test.</b> What would you think if you met him first?</li></ul>''',
 '''<ol class="small"><li><b>Meet the child before the file.</b></li><li><b>Open the report with what happened to him,</b> above the scores.</li><li><b>A strength before a deficit.</b> “Did,” not “is.”</li><li><b>Ten minutes alone with the parent</b> first. Seat her beside you.</li><li><b>Tell the child:</b> “This paper is about how to help you. It is not who you are.”</li></ol>''',
 "Whose file did you read before you met them? What did you never find out, because the paper had already told you who they were?")

C5 = combo(5, "The Calling Trap", "The people who care most are the easiest to take from.",
 '''<p>You became a school psychologist because of one kid. Everyone in this work has one.</p>
<p>At the interview they said, “The children here really need someone like you.” It was true. That's why it worked.</p>
<p>Year one you had two buildings. A colleague left and wasn't replaced. “Just until we hire.” Now you have four. You eat in the car between them. Your evaluations have legal deadlines and your conversations with children don't, so the conversations are what get cut.</p>
<p>In March you ask for help. The director is kind. She says, “I know. If you don't do it, these kids get nothing.” You drive home feeling selfish for asking. That week an email arrives from the district: <em>Wellness Wednesday — remember to practise self-care.</em></p>
<p>In May you sign a report on a girl you met for fifty minutes. You never saw her classroom. You never called her home. The report is accurate. It is also not the work you trained for, and you know it as you sign.</p>
<p>You tell yourself it's temporary. You've told yourself that for three years. A friend asks why you don't leave. You say, “Who would they have?”</p>
<p><b>Your conscience has become the leash.</b></p>''',
 "Eight tactics that turn a vocation into a supply. It doesn't need a bad director. It needs a good person and a budget.",
 d_chain("The Calling Trap", [("Love bombing", "“the kids need someone like you”", "sed"), ("Weaponized vocation", "“if you don't, they get nothing”", "sed"), ("Gradual escalation", "two buildings, then four", "des"), ("Moving the goalposts", "deadlines outrank children", "des"),
  ("Isolation", "the only one in the district", "iso"), ("Spiritual bypassing", "the self-care email", "ext"), ("Learned helplessness", "“it's temporary,” year three", "ext"), ("Replacement", "the post is filled, or contracted out", "dis")],
  "you sign work you know is thinner than the child deserves, and call it realism.", [(2, "“The shortage is not my debt”"), (3, "Say the ratio out loud"), (5, "Find your peers in other districts"), (7, "One case a month, done properly")], "A composite I wrote for people who work in schools. It describes a design, not anyone's intent."),
 '''<p class="small">The welcome has to come first. Guilt only works on someone who has already been told they are needed. Tell a stranger “these kids get nothing without you” and they shrug. Tell someone who came for the kids, and they stay late.</p>
<p class="small">Isolation is what stops the comparison. A psychologist with peers learns that four buildings isn't normal. A psychologist alone decides they must be slow.</p>
<p class="small">The self-care email arrives last because it moves the problem <em>inside the person.</em> The caseload is structural. The remedy offered is a bath.</p>''',
 "A district saves a salary every year a post stays empty, and the remaining staff cover it out of conscience. The better they cope, the less urgent the hire. Their coping is what hides the gap.",
 "Teachers, nurses, social workers, carers. A society that underfunds care can keep doing it as long as the people who care refuse to walk away from those in front of them. The shortfall is paid in their evenings, their health and their marriages.",
 '''<ul class="small"><li><b>The “who would they have” test.</b> If your reason for staying is guilt, name whose shortfall you're covering.</li><li><b>The thin-work test.</b> When did you last do a case the way you were trained to?</li><li><b>The ratio test.</b> Say your caseload to someone outside. Watch their face.</li></ul>''',
 '''<ol class="small"><li><b>Say the number out loud,</b> in writing, to the people who set it.</li><li><b>Return the debt.</b> “The shortage is real. It is not mine to pay alone.”</li><li><b>Find peers</b> outside your district. Compare notes.</li><li><b>One case a month done properly,</b> as proof to yourself of what the work is.</li><li><b>Write down what you'd do with half the caseload.</b> That is the argument for the hire.</li></ol>''',
 "What are you covering for, with your own evenings, that was never yours to carry? And who taught you that leaving it uncovered would make you a bad person?")

NEWCONN = '''<h3>Seven more, from the combinations</h3><ol class="disc" start="9">
<li><strong>Thirty lenses are how the invisible becomes visible.</strong> A fish can't see water from inside one tank. Put thirty tanks side by side and the water is the only thing they share. Writing the same cycle through every sector isn't repetition. It is the method. One sector can be explained away as “that's just how schools are.” Thirty can't.</li>
<li><strong>The combination families travel.</strong> My Entertainment sector has 153 combinations and Corporate has 138, and both sort into the same ten families. The costume changes. The skeleton doesn't. A person who learns one family in one sector can spot it in a sector they've never studied. That transfer is the real reason to finish all thirty.</li>
<li><strong>Every combination has the same kind of turning point.</strong> It is the moment a person acts before they've thought: signs while attached, stops reporting and just handles it, checks the homework at midnight with nobody watching. Before it, the control is outside them. After it, the control is inside. One question works in every sector: <em>am I still choosing this, or has the choosing stopped?</em></li>
<li><strong>Machines hand their output to each other.</strong> The teacher worn down by one combination writes the name on the board in another, and makes the referral in a third. Harm moves through people who are themselves being harmed. This is why blame doesn't fix it, and why relief for the adult is often the fastest help for the child.</li>
<li><strong>Read the thirty backwards and you have a curriculum.</strong> Each technique is a virtue reversed: generosity reversed, promise reversed, justice reversed. Turn the list around and it is thirty things worth teaching a child: welcome, clean giving, plain speech, ownership, repair. The map of harm is also a map of character. That is how this enters a school without frightening anyone.</li>
<li><strong>The work serves three moments, and most resources serve one.</strong> <em>Before</em> (a child, a new employee): recognition as prevention. <em>During</em> (someone inside it now): the turning-point question and the chain breakers. <em>After</em> (a survivor): the name, the order, and grief with a direction.</li>
<li><strong>The thing to measure is time-to-recognition.</strong> People commonly spend years inside a pattern before they can name it. Shared words shorten that. If this work is ever studied, that is the number: how long from first contact to “I know what this is.”</li></ol>'''

def build():
    foil = ED == "foil"; P = []; a = P.append
    a(f'''<section class="cover"><img src="../../art/fractal-original-1600.webp" alt=""><div class="t"><div class="k">The Fractal and Fractal² · the map, and what it is for</div><h1>Why I Wrote This</h1>
<p>How one pattern became visible to me, how far it reaches, what it looks like inside one life, and what could change if enough people could see it.</p>
<div class="m">Shae Stovell · Noble Father Creations · November 2026{"<br>Personal edition for Von “Foil” Saunders" if foil else ""}</div></div></section>''')
    if foil:
        m = renum(re.search(r'<section class="letter pb">.*?</section>', foil_html, re.S).group(0))
        m = re.sub(r'<p>Start with the map on the next page.*?</p>', '<p>If you read only three things, read Combinations 4 and 5 in Section 11 (I wrote both with your work in mind), Section 15 on children and schools, and the self-audit in Section 19.</p>', m, flags=re.S)
        a(m)
    a('''<section class="hook pb"><p class="h1">If I told you someone was love-bombing you, you'd probably catch it.</p>
<p class="h1">If I told you someone was gaslighting you, you'd probably push back.</p>
<p class="h1">If I told you your boundaries were being tested, slowly, on purpose, you'd probably hold your line.</p>
<p class="h2">Probably.</p><p class="h2">But what if I didn't tell you?</p>
<p class="h3">What if the warmth came first, so generous that your guard didn't lower, it dissolved? And while you were still glowing from being seen for the first time in years, a picture of the future slid in, so beautiful you'd do anything to protect it. And only then did the testing begin. So small. So reasonable. So wrapped in the language of the love you'd already accepted that you never felt your line move.</p>
<p class="h2">You wouldn't catch it. Nobody does.</p>
<p class="h4">Because that's not three tactics.<br>That's one machine.</p>
<p class="h5">This document is about that machine: where I found it, how big it turned out to be, what it looks like in a single life, and how it stops.</p></section>''')
    idx = [("Movement 1 · How it started", [(1, "s1", "Why these books exist")]),
           ("Movement 2 · What I noticed", [(2, "s4", "The cycle, and the garden and the gate"), (3, "s5", "Originals and inversions: the thirty techniques"), (4, "n4", "The thirty original impulses"), (5, "s6", "The thirty sectors and our relationship to each need")]),
           ("Movement 3 · How it expanded", [(6, "s2", "What I built, in numbers"), (7, "s7", "The fractal: three levels, and how it passes on"), (8, "s8", "The frequency: why it feels familiar"), (9, "n9", "From the map to the life: the step into Fractal²")]),
           ("Movement 4 · What I see now", [(10, "s9", "Why the order matters"), (11, "n11", "Five machines, one school"), (12, "s10", "What the whole map shows")]),
           ("Movement 5 · What this could do", [(13, "s11", "What a clean system looks like"), (14, "s12", "The war map: how this turns into change"), (15, "s14", "Children and schools"), (16, "s15", "What this can become"), (17, "n17", "The world that saw it")]),
           ("Movement 6 · I need help", [(18, "n18", "What I'm asking for")]),
           ("Reference", [(19, "s13", "Tools: trace it, interrupt it, audit your own system"), (20, "s3", "Three lenses, one shape"), (21, "s16", "What this is and is not"), (22, "n22", "From the series: the thirty inversions"), (23, "n23", "How this document was built to persuade you")])]
    rows = "".join(f'<tr><td colspan="2" class="mv">{mv}</td></tr>' + "".join(f'<tr><td class="n">{n}</td><td><a href="#{k}">{t}</a></td></tr>' for n, k, t in its) for mv, its in idx)
    a(f'''<section class="pb" id="qs"><div class="kick">Where everything is</div><h2>One story, six movements</h2>
<p class="lede">This is written to be read in order, like a story. It is also built so you can jump to what you need.</p>
<div class="cols"><div><table class="toc">{rows}</table></div>
<div><div class="box plain"><h4>If you have ten minutes</h4><p class="small">Read the page before this one, then <a href="#n11">one combination in Section 11</a>. Choose the one that sounds like someone you know.</p></div>
<div class="box plain"><h4>If you're a parent</h4><p class="small"><a href="#s4">2</a>, <a href="#n11">11</a> (Combination 3), <a href="#s14">15</a>.</p></div>
<div class="box plain"><h4>If you work in a school or a clinic</h4><p class="small"><a href="#n11">11</a> (Combinations 2, 4 and 5), <a href="#s14">15</a>, the <a href="#s13">self-audit in 19</a>, and the <a href="#s16">limits in 21</a>.</p></div>
<div class="box plain"><h4>If you want the whole argument</h4><p class="small">Straight through. Blue columns show the original need. Purple columns are my spiritual reading; skip them and the structure still holds. The boxes marked “Stop and notice” can be typed into.</p></div></div></div>
<figure class="fig">{renum(ns["d_machine"]())}<figcaption>The whole machine on one page. Read it from the bottom up.</figcaption></figure></section><section>''')

    a(part(1, "How it started", "Why would anyone spend years mapping this?"))
    a(S["s1"].replace('<div class="pull">', '''<p><strong>I didn't come to this as a researcher.</strong> I came to it as someone it happened to. The things that altered the course of my life, the ones I'm still unwinding years later, were never single acts. They were sequences so seamless that I experienced them as my life: as love, as loyalty, as growth. I learned to read the blueprint that had been drawn around me before I knew there was a page. Everything here comes from that, and from wanting my daughter to have the words before she needs them.</p><div class="pull">''', 1))

    a(part(2, "What I noticed", "What is the pattern, exactly, and why is it so hard to see?"))
    a(S["s4"]); a(stop("Think of one place that welcomed you warmly and later made that warmth conditional. Which stage are you in there now?"))
    a(S["s5"])
    cards = "".join(f'<div class="imp"><i>{i + 1}</i><b>{t}</b><p>{d}</p><span>Captured by: {SECT[i][0]}</span></div>' for i, (t, d) in enumerate(IMP))
    a(f'''<div class="sec" id="n4"><div class="kick">4 · What was there first</div><h2>The thirty original impulses</h2>
<p class="lede">Before the cycle there was something else. Every sector I've written began with a real human impulse: born into every body, needing no permission, and not for sale. The cycle didn't create any of them. It found each one, built a system around it, and became the gatekeeper.</p>
<p>Read these slowly. Not as information. As recognition. Your body will tell you which ones it remembers.</p>
<div class="imps">{cards}</div>
<div class="pull">They are not thirty things. They are one thing, a human being alive, seen through thirty windows.</div>
<p>The cycle can capture an impulse. It cannot kill it. It can only make you forget, and the forgetting is its only real power. A person who forgets what they are will accept the cycle's version of what they are, and the cycle's version is always: not enough.</p></div>''')
    a(stop("Which of the thirty did your chest answer to? Which one did you lose the longest ago?"))
    a(S["s6"])

    a(part(3, "How it expanded", "How big is this, and why didn't thirty turn out to be enough?"))
    a(S["s2"]); a(S["s7"]); a(S["s8"])
    a(f'''<div class="sec" id="n9"><div class="kick">9 · The step into Fractal²</div><h2>From the map to the life</h2>
<p class="lede">When I finished the thirtieth sector I thought the map was done. Then I noticed what it couldn't do.</p>
<h3>Thirty was the alphabet</h3>
<p>The Fractal can prove the pattern exists. It can't tell one specific person what was done to them. “Gaslighting” is a category. What happened to you was narrower than that. It had a particular sentence, a particular look across a room. A person can read the word and still not recognize the thing that is happening to them on a Tuesday.</p>
<p>Thirty techniques are an alphabet. You need the alphabet. But nobody is harmed by a letter.</p>
<h3>Fractal²: the dictionary</h3>
<p>So I went back into my own Pattern Decoder, where I had already catalogued more than three hundred named tactics, and began the map again at full resolution. <strong>The Fractal shows 30 techniques in each sector. Fractal² shows 300+ tactics in each sector,</strong> each at the same three scales: on a person, through an institution, across a society.</p>
<p>The first finished sector has 335 tactics. That is about a thousand examples in one sector, where Book 1 had ninety. When all thirty sectors are done the map will hold about thirty thousand. The number isn't the point. At this resolution people find their own experience. Not something like it. The thing itself, with a name.</p>
<h3>The combinations: sentences</h3>
<p>Then I saw the part that changed how I understand all of it. The tactics that altered my life were never the individual ones. Not the guilt trip by itself. Not the silent treatment by itself. Those were ingredients. What lands on a person is the combination: specific tactics, stacked in a specific order, where each one softens the ground for the next, and the next changes the meaning of the last.</p>
<p>If every tactic is a single note, a combination is a chord. Most of us have been hearing this music our whole lives without being handed the sheet music.</p>
<figure class="fig">{d_ladder()}<figcaption>Three resolutions of one map. Each step is what the one before it made possible.</figcaption></figure>
<p>So for every sector I'm writing the combinations: 150 or more. Entertainment has 153. Corporate and Consulting has 138. That is 291 so far, and every one is a scene from a life, not a general example.</p>
<div class="pull">Book 1 shows how the pattern works in general. The combinations show how it lands in someone's life. Proof convinces the mind. Recognition is what frees a person.</div>
<h3>Why I decided to publish the blueprint</h3>
<p>To show why the order matters, I have to show the engineering. I went back and forth on that for a long time. Someone could read it to build, not to heal.</p>
<p>Where I landed: more people will use this to protect themselves than will ever use it to harm. And anyone who tries will be walking into rooms full of people who recognize each move before it lands. <strong>The best defence against weaponized knowledge has never been ignorance. It has always been literacy.</strong> So every combination I write opens with a safety note, says what else the situation could be, and ends with the way out.</p></div>''')

    a(part(4, "What I see now", "What does it look like when it lands on one person?"))
    a(S["s9"])
    a(f'''<div class="sec" id="n11"><div class="kick">11 · Combinations in full</div><h2>Five machines, one school</h2>
<p class="lede">These five all happen inside the same building. I chose a school because that's where most of us met our first machine, before we had the language to see it.</p>
<p>The first three are from my Education scripts. The last two are composites I wrote for the people who work in schools, because the pattern runs through their hands, and on them too. Every scene is a composite. Yours may differ.</p>
{C1}{C2}{C3}{C4}{C5}
<h3>How the five connect</h3>
<figure class="fig">{d_school()}</figure>
<p>Look at who is in the picture. A teacher with thirty-four students and no break. A psychologist with four buildings. Each is inside a machine of their own, and each machine's output is the next one's input. The exhausted teacher is the one who writes the name on the board, and the one who makes the referral. The overloaded psychologist is the one with ninety minutes for Marcus.</p>
<p>And look at the two children at the ends. One is over-invested in and bonded to pain. The other is written off on paper. Both leave school carrying a sentence about themselves that someone else wrote: <em>he made me who I am</em>, and <em>I'm one of the bad kids.</em></p>
<p><strong>This is why I say there are no villains here, and why it still has to change.</strong> It is also why the adults who work with children matter so much to this map. They are the people in the building who can see all five at once.</p></div>''')
    a(stop("Which of the five did you recognize first: from being the child, or from being the adult?"))
    a("</div>".join(S["s10"].rsplit("</div>", 1)[:1]) + NEWCONN + "</div>")

    a(part(5, "What this could do", "If people could see it, what would actually change?"))
    a(S["s11"]); a(S["s12"]); a(S["s14"]); a(S["s15"])
    a(f'''<div class="sec" id="n17"><div class="kick">17 · The best case</div><h2>The world that saw it</h2>
<p class="lede">Here is what I'm working toward. Not a revolution. An ordinary Tuesday, some years from now, in a world where this is common knowledge.</p>
<div class="scene">
<p>A fifteen-year-old gets a message from someone new that says everything she's been waiting to hear. She feels the rush. She also recognizes the speed. She shows it to a friend, and the friend says, “That's fast.” They both know what that means, because they learned the word at ten, the way they learned to look both ways.</p>
<p>A father hears his own father's sentence starting in his mouth. He stops halfway through it. He kneels down and says, “Tell me more.” His son will not remember this moment. He will just grow up without that sentence in him.</p>
<p>A teacher writes no names on the board. When a boy who's been struggling hands something in, she says so, out loud, in front of everyone.</p>
<p>A school psychologist opens a file. The first paragraph says what happened to the child. The second says what the child is good at. At the meeting, the mother is sitting next to her, and she has already been told what she can ask.</p>
<p>A nurse says “four patients too many” in a staff meeting, and nobody says “welcome to nursing.” Someone writes the number down.</p>
<p>A director is about to launch a new program. Before she does, someone at the table runs eight questions over it. Two of the answers are “no.” They fix those first.</p>
<p>A man reads an offer that has to be signed today. He says, “I'll answer on Friday.” The offer is still there on Friday. The next one isn't, and he's glad.</p>
<p>A woman lies down in the afternoon because she is tired. She doesn't finish the list first.</p></div>
<figure class="fig">{d_ripple()}</figure>
<p>Nothing was torn down to get there. No one was blamed. People could simply see what they were inside of: in their own lives, in the institutions around them, in the architecture of the world they live in. And once it could be seen, it could be chosen or refused.</p>
<p>The systems that ran on unmet need didn't collapse. They lost their supply. People stopped paying for conditional versions of things that were theirs to begin with, and started building the places that should have been there.</p>
<div class="pull">A pattern that runs everywhere can only survive while it stays unnamed. That is the whole of it. I'm writing the names.</div></div>''')

    a(part(6, "I need help", "What am I asking of you?"))
    a('''<div class="sec" id="n18"><div class="kick">18 · The ask</div><h2>I've mapped it. I can't carry it alone.</h2>
<p class="lede">I've written this through twenty-six sectors and I'm still writing. What I can't do by myself is test it, sharpen it, and put it in front of the people it's for.</p>
<div class="asks4">
<div><i>10 min</i><b>Read one sector that touches your life</b><p>Tell me one thing that rang true and one thing that didn't.</p></div>
<div><i>If you work with people</i><b>Try the worksheet on one real situation</b><p>Teacher, counsellor, clinician, coach, pastor, manager. Tell me where it helped and where it got in the way.</p></div>
<div><i>If you have training I don't</i><b>Review a chapter</b><p>Tell me what is over-stated. I would rather be corrected than admired.</p></div>
<div><i>If you know one person</i><b>Send it to them</b><p>That is the whole distribution plan.</p></div></div>
<p>Everything is free and will stay free. It's all at <strong>noblefathercreations.com</strong>: The Fractal, Fractal², the Pattern Decoder, The Sacred Divide, and Playground Protectors.</p>
<p class="sig">The pattern that was installed in me, I now see. The pattern I carried, I now name. The pattern I passed on, I now interrupt. Not because I am guilty. Because I am awake.</p></div>''')

    a('<div class="part ref"><i>Reference</i><h2>Tools, lenses and limits</h2><p>For use, for checking, and for disagreeing.</p></div>')
    a(S["s13"]); a(S["s3"]); a(S["s16"])
    a('''<div class="sec" id="n22"><div class="kick">22 · From the series</div><h2>The thirty inversions, as they appear on screen</h2>
<p class="lede">These four frames are from the short-form version of The Fractal. Each technique is shown as something good, reversed.</p>
<div class="slides"><img src="slide-002.jpg" alt="The eight steps"><img src="slide-003.jpg" alt="Thirty inversions, 1 of 2"><img src="slide-004.jpg" alt="Thirty inversions, 2 of 2"><img src="slide-005.jpg" alt="Three levels"></div>
<p class="small">Read the gold words on their own, top to bottom: unconditional love, generosity, promise, welcome, worth, knowing, choice. That column is the curriculum.</p></div>''')
    a('''<div class="sec" id="n23"><div class="kick">23 · In the open</div><h2>How this document was built to persuade you</h2>
<p class="lede">A document about manipulation should show its own hand. I used persuasion here on purpose. These are the levers, so you can judge whether I used them fairly.</p>
<table><tr><th>What I did</th><th>Where</th><th>Why I think it's fair</th></tr>
<tr><td><b>Opened with a question and left it open</b></td><td>The page after the cover</td><td>It is answered in full, in Sections 9 to 11.</td></tr>
<tr><td><b>Showed you a scene before I explained it</b></td><td>Every combination</td><td>You can check it against your own life before you hear my reading of it.</td></tr>
<tr><td><b>Wrote in the second person</b></td><td>The scenes</td><td>It puts you inside the experience. It can also put words in your mouth, which is why each one is marked as a composite.</td></tr>
<tr><td><b>Used large numbers</b></td><td>Sections 6 and 9</td><td>They are counted, and the unfinished parts are stated.</td></tr>
<tr><td><b>Put the original beside the copy</b></td><td>Throughout</td><td>Both sides are shown, so you can compare for yourself.</td></tr>
<tr><td><b>Asked you questions and gave you space to answer</b></td><td>“Stop and notice”</td><td>Your answer is yours. I never see it.</td></tr>
<tr><td><b>Ended with a hopeful picture and a small ask</b></td><td>Sections 17 and 18</td><td>The ask is easy to refuse, and nothing depends on your saying yes today.</td></tr></table>
<p><strong>What I chose not to use:</strong> urgency, flattery, fear, or the claim that doubting me is a symptom of the pattern. Those are on the map as techniques. If you disagree with any of this after reading it, you're still doing the work, and I'd like to hear why.</p></div>''')
    if foil:
        m = re.search(r'<section class="letter pb" id="asks">.*$', foil_html, re.S).group(0)
        m = re.sub(r'</section>\s*$', '', m)
        a("</section>" + renum(m).replace("read Section 15 and", "read Combinations 4 and 5 and Section 15, and"))
    a("</section>")
    return "\n".join(P)

EXTRA = '''
.part{break-before:page;background:#07080B;color:#EEE9DE;padding:2.2em 2em 1.8em;margin:0 0 1.6em;border-radius:4px}
.part i{font-family:var(--sans);font-style:normal;font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:#E9B949;font-weight:650}
.part h2{font-size:3rem;color:#F6F1E6;margin:.15em 0 .2em;font-weight:480}
.part p{font-size:1.25rem;color:#C9C3B6;margin:0;font-style:italic}
.part.ref{background:var(--paper-2);color:var(--ink)} .part.ref h2{color:var(--ink)} .part.ref p{color:var(--ink-2)} .part.ref i{color:var(--gold)}
.part+.sec{margin-top:0;border-top:0;padding-top:0}
.hook{padding-top:18mm}
.hook p{max-width:30em;margin:0 0 .9em}
.hook .h1{font-size:1.5rem;line-height:1.3;color:var(--ink-2)}
.hook .h2{font-size:1.9rem;font-weight:560;margin:1em 0 .5em}
.hook .h3{font-size:1.16rem;line-height:1.5}
.hook .h4{font-size:2.9rem;line-height:1.1;font-weight:560;color:var(--gold);margin:1em 0 .6em;letter-spacing:-.015em}
.hook .h5{font-family:var(--sans);font-size:.9rem;color:var(--ink-3);border-top:1.5px solid var(--ink);padding-top:1em;margin-top:2em}
td.mv{font-family:var(--sans);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--gold);padding-top:.9em !important;border-bottom:1.5px solid var(--ink) !important}
.stop{border:1.5px dashed var(--gold-2);border-radius:4px;padding:.8em 1em .6em;margin:1.6em 0;background:#fff}
.stop b{font-family:var(--sans);font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.stop p{font-size:1.1rem;font-style:italic;margin:.3em 0 .4em;max-width:34em}
.imps{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.5em;margin:1em 0 1.3em}
.imp{border-top:2px solid var(--fact);background:var(--paper-2);padding:.55em .7em .5em;break-inside:avoid;position:relative}
.imp i{font-family:var(--sans);font-style:normal;font-size:.62rem;font-weight:700;color:var(--ink-3);position:absolute;right:.7em;top:.6em}
.imp b{display:block;font-size:.98rem;line-height:1.15;margin-bottom:.25em;padding-right:1.4em;color:#1F4560}
.imp p{font-size:.8rem;line-height:1.36;margin:0 0 .35em}
.imp span{font-family:var(--sans);font-size:.6rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.combo{border-top:3px solid var(--ink);margin:2.6em 0 0;padding-top:.9em}
.ckick,h3.cname,.ctag{break-after:avoid}
#n22{break-inside:avoid}
.part.first{break-before:auto;margin-top:1.4em}
.ckick{font-family:var(--sans);font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:var(--gold)}
h3.cname{font-size:2.3rem;margin:.1em 0 .1em;font-weight:540}
.ctag{font-size:1.2rem;font-style:italic;color:var(--ink-2);margin:0 0 .9em}
.scene{border-left:3px solid var(--gold);padding:.2em 0 .1em 1.2em;margin:.6em 0 1em}
.scene p{font-size:1.02rem;line-height:1.52;max-width:35em;margin:0 0 .62em}
.scene p:last-child{font-size:1.14rem;margin-top:.8em}
.cut{font-family:var(--sans);font-size:.86rem;font-weight:600;color:var(--ink);margin:0 0 .4em}
.combo .cols{gap:0 1.6em;break-inside:avoid;margin-top:.5em}
.combo h4{margin-top:.6em}
.combo .box{margin:.5em 0 .6em;padding:.8em 1em .4em}
.combo ul.small,.combo ol.small{padding-left:1.2em;margin:0 0 .4em}
.combo li{margin-bottom:.3em}
.cq{font-size:1.2rem;font-style:italic;border-top:1px solid var(--line);padding-top:.7em;margin-top:.6em;max-width:33em;break-inside:avoid}
.asks4{display:grid;grid-template-columns:1fr 1fr;gap:.7em;margin:1em 0 1.4em}
.asks4 div{border-top:3px solid var(--gold);background:var(--paper-2);padding:.8em 1em .5em;break-inside:avoid}
.asks4 i{font-family:var(--sans);font-style:normal;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700;display:block}
.asks4 b{font-size:1.12rem;display:block;margin:.2em 0 .25em}
.asks4 p{font-size:.92rem;margin:0 0 .4em}
.slides{display:grid;grid-template-columns:repeat(4,1fr);gap:.6em;margin:1em 0}
.slides img{width:100%;border-radius:6px;display:block}
'''
CSS = (HERE / "base.css").read_text() + (HERE / "extra.css").read_text() + EXTRA
foot = "Why I Wrote This · The Fractal and Fractal² · Shae Stovell"
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Why I Wrote This</title><style>{CSS}\n@page{{@bottom-left{{content:"{foot}"}}}}</style></head><body>{build()}</body></html>'
(HERE / f"final-{ED}.html").write_text(doc)
print(ED, "fields:", ns["_f"][0], "bytes:", len(doc))
