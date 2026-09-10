#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tenth 2026-09-10 pass: pull the two mega-cards out of SOBER TUESDAY.

Chapter 5's last SOBER TUESDAY card ran to 6,381 characters -- five times
the format -- because the Capacity Spectrum, the Bystander Interruption
Kit, and the Morning-After Reckoning were all crammed inside it. Chapter
23's did the same at 8,993 characters, holding the entire sixteen-move
Author's Wook Confession. Both are reference material, not a one-line
Tuesday joke, and both make the chapter's most important content the
hardest to find.

This does not touch a word of the content -- it moves it. Chapter 5's three
sub-sections become their own standalone panels, styled like the book's
other direct-address sections (before-we-roll). Chapter 23's Confession
becomes one standalone panel the same way, with its own #wook-confession
anchor so it can be linked to directly.

Run: python3 scripts/wook-component-split-pass.py   (idempotent)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

CH5_OLD = (
'<div class="subcard tuesday"><p class="sub-tag">☕ SOBER TUESDAY</p><p>“The company culture here is about radical honesty.” Said by a manager who then uses the radical honesty frame to override your HR complaint. Sacred container, same mechanism, different costume.</p>'
'<p class="plain-tag">\U0001f4d0 THE CAPACITY SPECTRUM</p><p>What each state can and cannot consent to.</p><p>Build this in your head. Refer to it during. Refer to it when someone is trying to tell you that a specific state can consent to a specific thing.</p><p><strong class="lead">Clear baseline:</strong> Can consent to anything. Can revoke consent to anything. The standard.</p><p>One to two standard drinks / mild cannabis / low-dose edible: Can consent to most things. Judgment is slightly altered. Significant decisions — money, housing, career, new sexual relationships — are better made at baseline. Not emergencies but watch the clock.</p><p>Moderate dose — three to four drinks / moderate cannabis / one tested cap of MDMA: Can consent to physical intimacy with a known partner with established consent framework. Cannot reliably consent to new partners, financial agreements, major commitments, or situations involving significant power asymmetry. The executive function is attending a different meeting.</p><p>Peak dose — at or above heavy alcohol / psychedelic plateau / K-hole adjacent / significant dissociation: Cannot consent to new physical sexual contact. Cannot consent to financial transactions. Cannot consent to anything that requires executive function assessment. Can consent to: water, rest, presence, care, music, an anchor staying close. That is approximately the full list.</p><p><strong class="lead">Blackout / unconscious / medical distress:</strong> Cannot consent to anything. Anyone who proceeds on the basis that this state is consent is not confused about consent. They are running the play.</p><p>This is not a rule imposed by someone who wants to limit your fun. This is a description of how human cognitive function actually works under these conditions. The Wook who tells you that you can consent perfectly well at peak is telling you something that is not true, and they know it is not true, and they are telling you anyway because the alternative requires them to wait until you are capable of a genuine yes.</p>'
'<p class="plain-tag">\U0001f9f0 THE BYSTANDER INTERRUPTION KIT</p><p>For hoopers, glovers, vendors, painters, photographers, crew, and anyone within eyeshot of a bad scene.</p><p>You don’t have to be certain. You don’t have to know. You don’t have to have evidence that passes any standard of legal scrutiny. You just have to see something that looks wrong and walk over.</p><p>The interruption is the magic. The Wook’s momentum requires an unobserved container. Walk over and the container no longer exists.</p><p>Three interruption moves. In escalating order.</p><p>The Casual Break-In:</p><p>Walk up to the person who looks off. “Hey — oh my god, is this you? I’ve been looking everywhere.” Friendly, warm, no drama, physical presence inserted into the situation. You don’t know the person. That is fine. You know what “I’ve been looking everywhere” communicates to the person being targeted: someone came for me. The Wook knows what it communicates too.</p><p>The Direct Check-In:</p><p>“Hey — sorry to interrupt. Can I check in with her directly for a second?” Not aggressive. Just: insert yourself, create a third presence, and ask the person directly if they are okay. Watch their face. Watch their body. If they are fine and this is a regular conversation, they will tell you and you will leave and nothing will have been lost. If they are not fine, the interruption just became load-bearing.</p><p>The Named Escalation:</p><p>“I’m with harm reduction. Protocol is I check in with this person directly and I’m going to take it from here.” You do not have to actually be with harm reduction. You do have to say it with the calm confidence of someone who has said it before. Then you stay, you get the person’s location, you get their anchor, you walk them toward staff, medical, or their crew. You hand them off to a safe resource and you document what you saw.</p><p>The Bystander’s one rule:</p><p>You do not need to be certain. You do not need to be right. You need to see something that looks wrong and walk over. The cost of a false positive is a slightly awkward interaction. The cost of a false negative is what this chapter is about.</p>'
'<p class="plain-tag">\U0001f305 THE MORNING-AFTER RECKONING</p><p>For readers who may have crossed a line themselves.</p><p>This section is here because this chapter is the chapter where some of you are going to recognize yourself on the other side.</p><p>Maybe you brought an eight-ball and called it generosity. Maybe you waited for peak to have the conversation. Maybe you told someone a version of the night that was helpful to you before they could form their own version. Maybe you ran the Dose Creep because you wanted company and told yourself it was care.</p><p>Maybe you have been doing this for a long time and have never called it what it is.</p><p>Here is what is true:</p><p>You cannot undo the past instances. You cannot unring the bell. The harm occurred regardless of whether you intended it as harm.</p><p>Here is what is also true:</p><p>Stopping is possible. Right now, today, next event. The next time you pack the bag, ask yourself whose capacity you are planning to work with tonight. If the answer involves someone being lowered, you have the information you need.</p><p>The Morning-After Reckoning does not require a public confession, a letter, a ceremony, or a group process. It requires a private reckoning with your own behavior and a changed behavior at the next event.</p><p>If the person you harmed is available and wants contact, that is a separate process that requires their consent and their terms, not your timeline.</p><p>If you are carrying this and want to do something with it: DanceSafe, MAPS, and several harm-reduction organizations have resources for people who have caused harm in substance-adjacent situations and want to do accountability work. The resources exist. They are not gentle. They are necessary.</p><p>The scene does not get safer by only teaching potential targets. It gets safer when the people on the other side of this chapter also read it and reckon with it.</p></div>'
)

CH5_NEW = (
'<div class="subcard tuesday"><p class="sub-tag">☕ SOBER TUESDAY</p><p>“The company culture here is about radical honesty.” Said by a manager who then uses the radical honesty frame to override your HR complaint. Sacred container, same mechanism, different costume.</p></div>'
# note: the original chapter's own </section> (closing this track panel) already
# follows CH5_OLD untouched in the document -- do not add another one here.
'<section class="panel pp-cream prose" id="capacity-spectrum"><svg class="doodle st-tr" aria-hidden="true"><use href="#bolt"/></svg><h2 class="zine-h">\U0001f4d0 THE CAPACITY SPECTRUM</h2><p class="script-note">— What each state can and cannot consent to.</p>'
'<p>Build this in your head. Refer to it during. Refer to it when someone is trying to tell you that a specific state can consent to a specific thing.</p><p><strong class="lead">Clear baseline:</strong> Can consent to anything. Can revoke consent to anything. The standard.</p><p>One to two standard drinks / mild cannabis / low-dose edible: Can consent to most things. Judgment is slightly altered. Significant decisions — money, housing, career, new sexual relationships — are better made at baseline. Not emergencies but watch the clock.</p><p>Moderate dose — three to four drinks / moderate cannabis / one tested cap of MDMA: Can consent to physical intimacy with a known partner with established consent framework. Cannot reliably consent to new partners, financial agreements, major commitments, or situations involving significant power asymmetry. The executive function is attending a different meeting.</p><p>Peak dose — at or above heavy alcohol / psychedelic plateau / K-hole adjacent / significant dissociation: Cannot consent to new physical sexual contact. Cannot consent to financial transactions. Cannot consent to anything that requires executive function assessment. Can consent to: water, rest, presence, care, music, an anchor staying close. That is approximately the full list.</p><p><strong class="lead">Blackout / unconscious / medical distress:</strong> Cannot consent to anything. Anyone who proceeds on the basis that this state is consent is not confused about consent. They are running the play.</p><p>This is not a rule imposed by someone who wants to limit your fun. This is a description of how human cognitive function actually works under these conditions. The Wook who tells you that you can consent perfectly well at peak is telling you something that is not true, and they know it is not true, and they are telling you anyway because the alternative requires them to wait until you are capable of a genuine yes.</p></section>'
'<section class="panel pp-cream prose" id="bystander-kit"><svg class="doodle st-tr" aria-hidden="true"><use href="#bolt"/></svg><h2 class="zine-h">\U0001f9f0 THE BYSTANDER INTERRUPTION KIT</h2><p class="script-note">— For hoopers, glovers, vendors, painters, photographers, crew, and anyone within eyeshot of a bad scene.</p>'
'<p>You don’t have to be certain. You don’t have to know. You don’t have to have evidence that passes any standard of legal scrutiny. You just have to see something that looks wrong and walk over.</p><p>The interruption is the magic. The Wook’s momentum requires an unobserved container. Walk over and the container no longer exists.</p><p>Three interruption moves. In escalating order.</p><p>The Casual Break-In:</p><p>Walk up to the person who looks off. “Hey — oh my god, is this you? I’ve been looking everywhere.” Friendly, warm, no drama, physical presence inserted into the situation. You don’t know the person. That is fine. You know what “I’ve been looking everywhere” communicates to the person being targeted: someone came for me. The Wook knows what it communicates too.</p><p>The Direct Check-In:</p><p>“Hey — sorry to interrupt. Can I check in with her directly for a second?” Not aggressive. Just: insert yourself, create a third presence, and ask the person directly if they are okay. Watch their face. Watch their body. If they are fine and this is a regular conversation, they will tell you and you will leave and nothing will have been lost. If they are not fine, the interruption just became load-bearing.</p><p>The Named Escalation:</p><p>“I’m with harm reduction. Protocol is I check in with this person directly and I’m going to take it from here.” You do not have to actually be with harm reduction. You do have to say it with the calm confidence of someone who has said it before. Then you stay, you get the person’s location, you get their anchor, you walk them toward staff, medical, or their crew. You hand them off to a safe resource and you document what you saw.</p><p>The Bystander’s one rule:</p><p>You do not need to be certain. You do not need to be right. You need to see something that looks wrong and walk over. The cost of a false positive is a slightly awkward interaction. The cost of a false negative is what this chapter is about.</p></section>'
'<section class="panel pp-cream prose" id="morning-after-reckoning"><svg class="doodle st-tr" aria-hidden="true"><use href="#bolt"/></svg><h2 class="zine-h">\U0001f305 THE MORNING-AFTER RECKONING</h2><p class="script-note">— For readers who may have crossed a line themselves.</p>'
'<p>This section is here because this chapter is the chapter where some of you are going to recognize yourself on the other side.</p><p>Maybe you brought an eight-ball and called it generosity. Maybe you waited for peak to have the conversation. Maybe you told someone a version of the night that was helpful to you before they could form their own version. Maybe you ran the Dose Creep because you wanted company and told yourself it was care.</p><p>Maybe you have been doing this for a long time and have never called it what it is.</p><p>Here is what is true:</p><p>You cannot undo the past instances. You cannot unring the bell. The harm occurred regardless of whether you intended it as harm.</p><p>Here is what is also true:</p><p>Stopping is possible. Right now, today, next event. The next time you pack the bag, ask yourself whose capacity you are planning to work with tonight. If the answer involves someone being lowered, you have the information you need.</p><p>The Morning-After Reckoning does not require a public confession, a letter, a ceremony, or a group process. It requires a private reckoning with your own behavior and a changed behavior at the next event.</p><p>If the person you harmed is available and wants contact, that is a separate process that requires their consent and their terms, not your timeline.</p><p>If you are carrying this and want to do something with it: DanceSafe, MAPS, and several harm-reduction organizations have resources for people who have caused harm in substance-adjacent situations and want to do accountability work. The resources exist. They are not gentle. They are necessary.</p><p>The scene does not get safer by only teaching potential targets. It gets safer when the people on the other side of this chapter also read it and reckon with it.</p></section>'
)

CH23_MARKER = 'THE AUTHOR’S WOOK CONFESSION'


def split_ch23(html):
    start_marker = '<div class="subcard tuesday"><p class="sub-tag">☕ SOBER TUESDAY</p>'
    idx = html.find(CH23_MARKER)
    assert idx != -1, "ch23: confession marker not found"
    card_start = html.rfind(start_marker, 0, idx)
    j = card_start + len('<div class="subcard tuesday">')
    d = 1
    import re as _re
    for t in _re.finditer(r'</?div\b[^>]*>', html[j:]):
        d += -1 if t.group(0).startswith('</') else 1
        if d == 0:
            card_end = j + t.end()
            break
    card = html[card_start:card_end]
    # split the card into: sober-tuesday intro <p> and the confession body
    header = '<p class="plain-tag">\U0001f58a️ ' + CH23_MARKER + '</p>'
    hi = card.index(header)
    intro = card[:hi]  # '<div class="subcard tuesday">...<p>...</p>'
    body = card[hi + len(header):-len('</div>')]  # everything up to the closing </div>, header stripped
    new_intro = intro + '</div>'
    new_confession_section = (
        # note: the chapter's own </section> already follows the original card
        # untouched -- do not add another one before opening this new section.
        '<section class="panel pp-purple prose" id="wook-confession">'
        '<svg class="doodle st-tr" aria-hidden="true"><use href="#bolt"/></svg>'
        '<h2 class="zine-h light">\U0001f58a️ THE AUTHOR’S WOOK CONFESSION</h2>'
        '<p class="script-note">— First person. From the PLURth Angel. The sixteen moves this book ran on you.</p>'
        + body + '</section>'
    )
    new_block = new_intro + new_confession_section
    return html[:card_start] + new_block + html[card_end:], (card_start, card_end)


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    if 'id="capacity-spectrum"' in html and 'id="wook-confession"' in html:
        print("already applied -- nothing to do")
        return 0

    n5 = html.count(CH5_OLD)
    assert n5 == 1, "ch5 mega-card: %d matches, expected 1" % n5
    html = html.replace(CH5_OLD, CH5_NEW, 1)

    html, _ = split_ch23(html)

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes" % (format(before, ","), format(len(html), ",")))
    print("ch5: Capacity Spectrum / Bystander Kit / Morning-After Reckoning now standalone panels")
    print("ch23: The Author's Wook Confession now its own panel, id=wook-confession")
    return 0


if __name__ == "__main__":
    sys.exit(main())
