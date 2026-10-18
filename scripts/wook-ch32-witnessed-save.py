#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace Chapter 32's Save with the witnessed audit.

The chapter's one real logical hole: the PLURth Angel audits himself,
alone, and asks the reader to take the completeness of the confession on
trust -- from the narrator who has just finished explaining how he
engineered that trust. The book spends 164 Tracks teaching that a
self-report is the least reliable account and that you need a witness
before the yes. Chapter 32 violated its own thesis in its architecture,
and the old Save opted out of the house form entirely ("There is no
Field Report here", 256 words of exposition where every other chapter
runs the scenario clean).

The rewrite stages it. Three things make it work:

1. The witness was always there. The cold open describes two people
   sixty yards north and omits the one four feet away -- so the scene's
   first move is the reveal that the confession chapter was still
   editing while it confessed.
2. Bear Tevaru is the only possible witness. Canon has him as the
   scene's long-tenured witness, and as the person who has "sat with the
   person-after-the-batch more times than any other recurring cast
   member" -- which gives him standing to name the one thing the list
   cannot: that the book manufactures the feeling of readiness, and that
   he is the one who sees what happens to people who walk in feeling it.
3. The Watermelon Moment is a hand reaching for a pen. The author's
   reflex, on being handed the only objection that lands, is to turn it
   into Confession Seventeen. The witness watches the hand. The hand
   stops. The objection stays six words on painter's tape and never
   becomes a numbered item -- which is also why the count stays at
   sixteen everywhere else in the book.

The Save's actual save is the one counter-drop the book cannot run for
the reader: find a real person to read your list back. The author had to
invent one. The reader does not.

Idempotent: asserts the old Save is present exactly once, and is a no-op
once the new one is in.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

OLD_START = "<p>Author Direct Address. The conversation that is itself the Save.</p>"
OLD_END = "<p>That is the Save.</p>"

NEW = """<p>Author Direct Address. Same campfire. One witness. Watermelon Moment present.</p>
<p>Bear has been sitting on the other side of this fire since before the light changed.</p>
<p>I told you about the two people sixty yards north working the shade structure. I told you about the ratchet straps, and how everything carries in the empty air now. I did not tell you about the man four feet away with his boots off, because a man alone at a fire confessing is a better image than a man being watched while he does it.</p>
<p>That is the machine still running, in the same breath where I told you it had stopped.</p>
<p>He is forty-four. He has been striking stages for thirty-two years and he strikes them in the same order every time, and he is not striking anything this morning, which is how I know he has been waiting for me to finish.</p>
<p>&ldquo;Read it to me,&rdquo; he says.</p>
<p>So I read him the list. All sixteen, in order, exactly as they appear above. It takes considerably longer out loud than it does on the page. He does not interrupt once. Somewhere around the middle he pulls the roll of painter&rsquo;s tape off his belt, tears a strip, and writes something on it against his knee, and I cannot see what it says.</p>
<p>When I stop, he says: &ldquo;That&rsquo;s a real list.&rdquo;</p>
<p>I wait.</p>
<p>&ldquo;Most guys don&rsquo;t write that one,&rdquo; he says. &ldquo;Most guys write the book, and then they write a second book about how brave the first book was.&rdquo;</p>
<p>Then he says: &ldquo;You left one off.&rdquo;</p>
<p>I tell him the list is complete to the best of my knowledge.</p>
<p>&ldquo;Yeah,&rdquo; he says. &ldquo;That&rsquo;s the part that&rsquo;s true and the part that&rsquo;s the problem.&rdquo;</p>
<p>He turns the tape around.</p>
<p>What is written on it is not a technique. It is six words.</p>
<p class="board-q">THEY FEEL SAFER THAN THEY ARE.</p>
<p>&ldquo;You told them how you worked them,&rdquo; he says. &ldquo;You didn&rsquo;t tell them what it does. They&rsquo;ve got the vocabulary now. They&rsquo;ve got the counter-drops and the sixteen and the vow. So they walk into the next lot a half step looser than they walked into the last one, because they read a book about it.&rdquo;</p>
<p>I say that is true of every safety book ever written.</p>
<p>&ldquo;Sure,&rdquo; he says. &ldquo;I&rsquo;m the one who sits with them after. Thirty-two years of sitting with them after. I&rsquo;m telling you what it looks like when somebody walks in feeling ready.&rdquo;</p>
<p>And here is the part I have to give you, because the whole chapter is worth nothing if I skip it.</p>
<p>I reached for my pen.</p>
<p>Not after considering it. Before. My hand was moving toward the pen before he finished the sentence, because the objection was good, and a good objection is material, and material is the thing I do. I was going to write it down. I was going to make it Confession Seventeen. I was going to take the one sentence anybody has said to me this morning that actually landed, and turn it into more book.</p>
<p>He watched my hand.</p>
<p>He did not say anything about it. He just watched my hand, and my hand stopped, and that stopping is the only clean thing I have done since the sun came up.</p>
<p>That is the watermelon moment. Not a feeling. A hand, halfway to a pen, in front of somebody who was looking.</p>
<p>So it does not go on the list. It stays six words on a strip of painter&rsquo;s tape, and it never becomes a numbered item, because the moment it becomes a numbered item it is the machine again, wearing the last honest thing in the chapter as a costume.</p>
<p>Then I tell him the thing I have been sitting on since the light changed. I tell him he is not real. I tell him I built him &mdash; the forty-four, the thirty-two years, the board, the tape &mdash; and that I confessed exactly that in Confession Eight while he was sitting four feet away listening to me do it.</p>
<p>&ldquo;I know what I am,&rdquo; he says.</p>
<p>He puts his boots back on.</p>
<p>&ldquo;I&rsquo;m what you made when you needed somebody to be harder on you than you&rsquo;re willing to be by yourself. That&rsquo;s a real thing to need.&rdquo; He stands, and knees crack, and he does not comment on it. &ldquo;It&rsquo;s also not the same as getting caught. Somebody who actually caught you wouldn&rsquo;t be sitting here being useful about it.&rdquo;</p>
<p>That is the Save, and it is not mine. It is yours.</p>
<p>I had to invent a man to tell me what I left off, because at four in the morning with a flashlight under my chin there was nobody on the other side of the fire. You do not have to invent one. That is the entire difference between your situation and mine, and it is the last useful thing this book has to hand you.</p>
<p><strong class="lead">Find the person who will read your list back to you.</strong> Not the one who agrees with it. The one who turns the tape around.</p>
<p>One name. Somebody with standing to say the thing you would otherwise build an imaginary soundman to avoid hearing. Then tell them, out loud, that they have the job &mdash; because a witness who does not know they are allowed to speak is just an audience.</p>
<p>That is the counter-drop for this chapter, and it is the only one in this book I cannot run for you.</p>
<p>Bear is sixty yards north now, doing the thing he was always going to be doing, which is coiling somebody else&rsquo;s cable better than they coiled it.</p>
<p>&ldquo;You still don&rsquo;t go over-under,&rdquo; he calls back. &ldquo;Thirty-two years I&rsquo;ve been telling people.&rdquo;</p>
<p>He is right. He has been right for thirty-one chapters.</p>"""


def main():
    raw = WOOK.read_text(errors="surrogateescape")

    if "THEY FEEL SAFER THAN THEY ARE" in raw:
        print("witnessed Save already in place -- no-op")
        return 0

    i = raw.find(OLD_START)
    if i == -1:
        raise SystemExit("old Save opening not found")
    j = raw.find(OLD_END, i)
    if j == -1:
        raise SystemExit("old Save closing not found")
    j += len(OLD_END)

    old = raw[i:j]
    if raw.count(OLD_START) != 1:
        raise SystemExit(f"Save opening appears {raw.count(OLD_START)}x, expected 1")

    raw = raw[:i] + NEW + raw[j:]
    WOOK.write_text(raw, errors="surrogateescape")
    print(f"replaced {len(old.split())} words with {len(NEW.split())} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
