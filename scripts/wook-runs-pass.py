#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seventh 2026-09-10 pass: RUNS IN EVERY DIRECTION, all 81 remaining cards.

Applies the rule from content/wook-audits/wook-book-wide-additions.md, Part B,
to every RUNS card in chapters 9-24 that the audit flagged (chapters 1-8 were
already fine). Rule: name at least three specific people who run this play,
drawn from roles the book has already established, with at most one
universality sentence, placed last as the conclusion rather than the whole
card.

Structural edit, not string-match: for each chapter this locates every
'<div class="subcard runs">' block in document order, and replaces only the
inner <p> text after the sub-tag, so it can't collide with identical phrasing
reused elsewhere in the book (many of these cards previously shared near-
identical formula sentences). Chapters are processed in descending order so
earlier byte offsets stay valid while later ones are being edited.

Run: python3 scripts/wook-runs-pass.py   (idempotent -- re-run is a no-op
once applied, detected by the new copy already being present)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# chapter -> new RUNS card text, in track order (must match current track count)
NEW_RUNS = {
 9: [
  "The Free Cap Funnel is run by the shirtless guy with the cooler who's suddenly your best friend, the camp mom two rows over, the touring DJ's merch girl, and the sober-looking stranger who bought you water first. Forty-five minutes of warmth, then the bag. Warmth is not gendered. Neither is the absence of a test kit.",
  "The Lag slows down whether the message starts at the medic tent, the Bunk Police table, a camp group chat, or one sober friend who heard something at 2 a.m. It's a physics problem, not a character problem: the faster the message moves through any of those relays, the smaller the Lag becomes for the next person.",
  "The shame that produces the Spiral can hit the first-timer worried her parents will find out, the touring musician worried about his reputation, the undocumented festie worried about anything involving a badge, and the sober crew captain who feels like she should have caught it sooner. The stakes attached to legal consequences are not equally distributed. Both are true. The Override still applies — with awareness of whose stakes are highest.",
  "The Buddy Who Bailed is the best friend who went to find the afters, the hookup who left for a different stage, the camp mate who assumed someone else had it covered, and the person who genuinely thought you'd be fine. Any gender, any configuration, any level of scene experience. The four-hour rule and the extraction code word don't care which one left.",
  "The Medical Tent Math runs through the camp lead doing the count at 3 a.m., the sober anchor watching gray lips and deciding, the total stranger who steps in because nobody else moved, and the medic who's seen this exact hesitation a hundred times. It is universal and human, and the fix isn't eliminating the math — it's pre-loading the non-negotiable list so the decision is already made.",
 ],
 10: [
  "The Borrowed Mule is asked of the girlfriend at the gas station, the tour bus new hire, the camp's youngest member, and the friend who's never said no to anything yet. Romantic partners, close friends, tour-bus relationships, camp hierarchies, touring crews — any gender. The person asked is the one with the least leverage to refuse, not the least competence to do it.",
  "The Rehearsed Sentence gets prepared by the boyfriend nodding along at the gas station, the camp lead who's done this before, the tour manager smoothing over a border stop, and the friend who's said “it's chill” so many times it doesn't register as a lie anymore. The person who prepares it usually holds more power in the relationship. The person it's prepared for usually holds more trust.",
  "The Unchill No runs on the girlfriend who doesn't want to be the buzzkill, the new guy who doesn't want to seem uptight, the camp member with less social capital than the person asking, and anyone whose no has historically cost them more than the yes would. The calculation happens in everyone's nervous system. The outcome depends on what was practiced before the moment.",
  "The dog does not discriminate — not by who's driving, who's riding shotgun, who agreed to what at the gas station, or who was told “they don't search girls' stuff.” Neither does constructive possession. Both apply to the boyfriend, the homie, the girlfriend, and everyone else in the car regardless of who packed the bag.",
  "The Ride-Or-Die One-Way runs through the girlfriend who's proven her loyalty for a year, the best friend who's covered for him twice already, the queer partner whose devotion gets treated as infinite, and the camp family member who's never once said no. Not just heterosexual dyads — same-sex partnerships, close friendships, camp families, and touring crews all produce it when one person's loyalty is treated as a resource by someone who doesn't match it.",
 ],
 11: [
  "The Consensual Encounter Approach is worked by the state trooper with the kind eyes, the K-9 handler who asks about your weekend first, the plainclothes task force officer parked past the exit ramp, and the friendly local deputy who knows the festival by name. The friendly register does not change by who is wearing the badge.",
  "The Soft Ask comes from the trooper who “just wants to ask a couple quick things,” the K-9 handler who mentions the dog almost as an afterthought, the second officer who arrives to “make it faster,” and the supervisor who steps in sounding more reasonable than the first two. It lands on every demographic. The register is calibrated to feel low-stakes no matter who's receiving it.",
  "Probable cause gets manufactured from the air freshener hanging from the mirror, the two cars traveling together, the nervous passenger who won't make eye contact, and the smell the officer swears he detected before he opened the window. It can be built from behaviors that vary across demographic groups. The dog's threshold doesn't discriminate. The officer's discretion does. Know both.",
  "The leak comes from the front-seat passenger answering a question nobody asked, the back-seat friend who overshares to seem cooperative, the driver's girlfriend trying to smooth things over, and Carter, who just wants this to be over and says one sentence too many. It runs in every vehicle configuration. The driver-only policy works regardless of who's talking.",
  "The nervous yes comes from the twenty-year-old in the back seat, the camp lead who's driven this stretch a hundred times and still freezes, the passenger who's never been pulled over before, and the driver whose hands won't stop shaking on the wheel. It's a human nervous system response. It does not care about the vehicle's occupants' identities. The eighty-three percent does not discriminate. The pre-committed no works regardless.",
 ],
 12: [
  "The Not-Really-A-Dealer shows up as the guy who “just knows a guy,” the femme distributor with the spreadsheet and the Venmo, the touring crew member who's been doing this since he was nineteen, and the camp lead who fronts for the whole group. The narrative is gender-neutral. The batch doesn't care who's holding it.",
  "The chain-of-trust error runs through the tour crew's usual connect, the camp's two-year relationship with a specific source, the femme distributor whose reputation has never once been questioned, and the friend of a friend everyone vouches for without having met him. It doesn't care about the quality of the human relationship. It cares about the quality of the batch, which only the test can establish.",
  "The Skipped Test gets skipped by the touring vet who's done this a hundred times, the first-timer who doesn't own a kit, the camp lead in a hurry before doors, and the distributor who's never once had a bad batch. The reasons are identical regardless of who's skipping it: inconvenience, momentum, trust in the source, belief that this time is probably fine. None of those reasons change the test's function.",
  "The Screenshot Drop runs equally against the guy who bought from a stranger, the woman who bought from her regular, the nonbinary festie who bought from a friend of a friend, and everyone across the distribution spectrum who assumed they'd remember exactly what it looked like. The no-recall problem is a physics problem. It has no social bias.",
  "The Forty-A-Cap Reframe runs across the guy fronting eight hundred dollars for eighty caps, the femme distributor who prices hers the same way, the touring vet who's done the math a dozen times, and anyone who's decided a fair price is the same thing as due diligence. It runs across all genders and all distribution scales. The moral licensing through fair pricing is available to anyone who charges a fair price. It is equally unavailable as accountability.",
 ],
 13: [
  "The First Free One is deployed by the femme camp lead who's been feeding your row for three years, the touring sound guy whose generosity built his whole reputation, the ceremony holder passing the mason jar like a sacrament, and the beautiful stranger whose beauty was the first free thing. The invoice does not have a gender. Everyone eventually gets handed one.",
  "The Mason Jar gets passed by the ceremony holder who says the medicine knows what you need, the camp elder who's done this every year since the beginning, the touring artist who trusts his own judgment more than yours, and the stranger who decides for you before you've decided for yourself. The person who decides what goes into someone else's body without their knowledge is deploying a specific form of control that runs across every identity configuration. The seal protocol applies regardless of who's holding the jar.",
  "The Reciprocity Ratchet gets wound by the camp lead who remembers every favor she's ever done you, the touring crew member who's been quietly counting, the ceremony holder who frames every gift as building a relationship, and the friend who brings up the U-Haul from two summers ago. The ledger runs in every relationship where care gets converted to leverage. The check applies regardless.",
  "The Slow Door Close is worked by the camp mom who takes it personally when you try to leave early, the touring artist who needs one more minute of your night, the ceremony holder who makes the exit feel like a small betrayal, and the friend who's mastered the art of one more thing before you go. It runs across every configuration of gender, identity, and scene tenure. The cost is inflated by warmth, not by gender. The two-text rule works regardless.",
  "The morning debt gets collected by whoever's holding the coffee the next day — the camp lead managing the story, the touring partner smoothing the narrative, the ceremony holder who needs last night to have meant what he said it meant, and the friend who needs you to agree with her version before you've had water. The gender of the person holding the coffee is not the variable. The variable is whether the other person's experience of the night is allowed to exist on its own terms.",
 ],
 14: [
  "The Three-Asks Pattern is run by the friendly male officer, the plainclothes woman working the merch line, the nonbinary task force member posted at the rail, and any civilian Wook who's learned empirically that the third ask is the one that closes. It doesn't have a gender. It has a count.",
  "The Mutual Friend Lie gets told by the undercover who name-drops a camp lead you've actually met, the plainclothes officer who claims to know your vendor row neighbor, the informant who's memorized three names deep, and anyone running the same script across a different demographic context. The names change. The function is identical. The verify protocol applies universally.",
  "The “at cost” gap gets set by the undercover offering a price too good to question, the plainclothes buyer who frames it as a favor between festies, the task force member playing broke and generous at once, and anyone wearing the community's own language back at you. It runs across every demographic. The legal system does not evaluate the sincerity of the community context. The body wire records the phrase.",
  "The tells get performed by the undercover with the glitter applied one YouTube tutorial too evenly, the plainclothes officer whose merch-tent shirt still has the fold lines, the task force member who leads with music before logistics, and anyone trained to run camp-without-network. Scuffs. Music-before-logistics. Warmth-without-friction. Camp-without-network. The pattern holds across the demographic variety of the people trained to run it.",
 ],
 15: [
  "The Geometry Trap gets set by the tour bus regular who suggests moving somewhere quieter, the camp acquaintance with the drawn curtains, the friend-of-a-friend who's “just right over there,” and anyone who's learned that a private space changes what's possible. The gender of the person running it is irrelevant. The geometry is the play. It runs equally regardless of who constructed it.",
  "The chain dilutes the same way whether it passes through the tour crew's usual guy, the camp's newest addition vouched for by someone half-remembered, the festival hookup's roommate, or the friend of a friend everyone agrees is “basically family.” The vibe-memory problem is universal. The verification protocol is also universal.",
  "The witness deters the touring vet with a reputation to protect, the camp lead who's careful in front of others, the stranger who's only opportunistic when nobody's watching, and anyone across every predatory gender and identity configuration. The witness is not protection against ideological violence. It is protection against opportunistic material crime, which is what this chapter addresses.",
  "Whoever hits the unguarded camp isn't a specific archetype — the opportunistic vendor row neighbor, the festie passing through at 4 a.m., the person who's been casing tents since Thursday, the stranger who just noticed nobody locked the trailer. They come in every gender, identity, and presentation. The target-hardening works regardless.",
  "The no-recourse structure gets built by anyone who's identified a category of victim who can't easily report — the undocumented festie, the person on probation, the minor who snuck in, the person whose ID doesn't match who they told the officer they were. It is created by and benefits people of any gender or identity. It is not gendered. It is opportunistic. The protection is the prevention.",
 ],
 16: [
  "The plan gets chosen by the first-timer crew who thinks phones will be enough, the veteran group that's gotten lucky every year so far, the couple who assumes they'll just feel it, and Sister Lou's briefing skippers of every configuration. It's chosen equally by groups of every gender, identity, and experience level. The coding of preparation as uncool runs equally across demographics. The plan is gender-neutral. So is the solution.",
  "The vacuum affects the festie who only goes by her scene name, the touring artist known only by his stage handle, the first-timer whose government name nobody in the crew has bothered to learn, and the sober anchor who's the only one who wrote anything down. The specific complications vary by identity. The solution — legal name and emergency contact held by one trusted crew member — applies universally.",
  "The Cascade doesn't care whether it's the camp lead's phone, the sober anchor's phone, the newest crew member's phone, or the one person who forgot their battery pack. Love does not charge phones. The portable battery charges phones.",
  "The four-hour mark applies the same way whether the missing person is the camp veteran, the first-timer, the sober anchor's own partner, or the friend everyone assumed was with someone else. It applies equally regardless of the identity of the missing person or the group conducting the search. The escalation protocol works the same way across all demographics. The information needs at the safety desk are the same.",
  "The Briefing gets skipped by the tight-knit veteran crew who's sure they don't need it, the first-timer group that doesn't know it exists, the couple who figure they'll stay together anyway, and the camp that ran it once three years ago and never again. It is skipped by groups of every composition, identity, experience level, and scene tenure. It is skipped because it feels like overkill. It has never once been overkill.",
 ],
 17: [
  "The free first bump gets offered by Wedge, by the femme operator two camps over, by the nonbinary distributor everyone trusts, by the camp lead who fronts for newcomers, and by the booking agent who's figured out that giving first produces a return. The funnel is not gendered. The architecture is.",
  "The dependency gets built by the plug who remembers your order, the camp connect who always has extra, the touring supplier who checks in between runs, and anyone whose genuine care produces structural dependency whether they meant it to or not. It runs across every supply relationship dynamic regardless of the supplier's gender or the customer's.",
  "The Dose-And-Decide gets run by the plug who waits until you're already in it, the camp connect who frames the ask as casual, the touring supplier whose timing is never accidental, and anyone whose capacity to negotiate depends on someone else's capacity to wait. It runs across every supply relationship and every context where one person's capacity is affected and the other person's timing is strategic. It is not gendered. It has a very good close rate.",
  "The threat gets made by the plug who goes cold the moment you push back, the camp connect whose warmth turns conditional, the touring supplier who reminds you what you'd be losing, and anyone with leverage and a dependency. Its sophistication is not gendered. Its effectiveness is universal.",
  "The Plug Romance runs through the male dealer who starts calling it something else, the femme distributor whose customers become something else, the nonbinary supplier whose access and affection blur, and anyone whose supply relationship and romantic interest have been allowed to become entangled. The gender distribution of who runs it and who receives it varies. The structural architecture is gender-neutral.",
  "The Captivity runs through the supply arrangement that's costly to walk away from, the touring crew position that's hard to quit mid-run, the camp housing that's tied to staying loyal, and any relationship where the cost of leaving has outgrown the value of staying. It runs in every context where the mid-leg exit is economically or logistically costly.",
 ],
 18: [
  "El is fifty-four. El could be forty-four. El could be the femme founder of a healing collective three states over, the nonbinary elder who built a residential network in the Pacific Northwest, or the touring bandleader running the same structure out of a converted bus. The Family Frame is not gendered. The bus could be any vehicle. The mason jar could be any prop.",
  "The Bus Hierarchy isn't unique to El's crew — it runs in the healing collective two states over, the spiritual community with the charismatic teacher, the residential program with the rotating volunteer staff, and any traveling crew with a center and a circle of people orbiting it. The center can be any gender.",
  "El runs the conscription on the women in his bus. The femme community leader runs it on her network. The queer collective lead runs it on chosen family. The camp lead runs it on first-timers who don't yet know they can say no. The duty-activation is the Track, not the gender of the person running it.",
  "The Sister Word gets deployed by El on the women in his bus, by the femme elder who's built enough community to own its vocabulary, by the nonbinary organizer whose language everyone has adopted, and by anyone who controls the words a group uses to talk about itself. It runs equally when the language controller is a femme, a nonbinary person, a queer community elder, or a man like El.",
  "The disappearance gets managed by El about the women who leave his bus, by the collective that never talks about who used to be here, by the residential program whose alumni simply stop being mentioned, and by any group that controls the narrative of its own exits. It runs equally in groups led by any gender or identity.",
  "The Napkin Network gets passed by the woman who's been on the bus three years and knows what not to say out loud, by the newest member of the healing collective who overhears something and writes it down, by the friend who slips a folded note at the gas station, and by anyone in harm's way passing warning to anyone about to be. It is the most democratic tool in this book. It requires only something to write with and someone to receive it.",
  "The Long Exit gets planned by the woman quietly rebuilding a bank account outside El's system, by the collective member reconnecting with a sister she stopped calling, by the residential program alum reaching out to an old coworker, and by anyone in a group led by any gender or identity configuration. The planning is the same. The external resources vary. The first week is the same: identify one external connection and strengthen it.",
 ],
 19: [
  "The Identity Erosion Drift claims the accountant who started going to one festival a year and now measures his life in laps, the mother who used to cook and now can't remember the last home-cooked meal, the twenty-two-year-old who dropped out because the semester conflicted with a run, and the sound engineer who hasn't had a Tuesday conversation with his sister in three years. It's not gendered. It's just what loving a thing that never says stop does to a calendar.",
  "The Lock catches the vendor who can't picture a life off the lot, the camp lead who's been the camp lead so long she doesn't remember who she was before, the touring crew member who's never had a Tuesday job, and anyone who's invested heavily enough that leaving feels like erasure. The catastrophization grammar is universal. The smaller season experiment works regardless.",
  "The Move runs through the community that's warm when you're posting and cooler when you're not, the crew that checks in more during a build season than an off one, the collective that notices you more when you're useful to it, and any group where belonging correlates, quietly, with participation. It runs across all community types, all demographics, all festival scenes. It is not malicious. It is structural.",
  "The Indoctrination runs through the veteran who can't talk to his old coworkers anymore, the first-timer who's already embarrassed by her old friend group, the touring artist who's stopped explaining himself to anyone outside the circuit, and any subculture with enough immersion and enough contrast with the mainstream. It is not gendered, not specific to any festival type, not specific to any demographic. It is structural.",
  "The Hollowing Spiral runs in the vendor who's given the lot ten years and can't picture an eleventh without it, the sound tech whose whole calendar is load-ins, the sober mentor whose entire identity became the scene she was supposed to be recovering into, and anyone who has invested total identity in a single context. It is not gendered. It is not scene-specific. The festival version is this chapter. The chapter's counter-drop works regardless of which context produced the spiral.",
 ],
 20: [
  "The Comedown Text is sent by the ex who waits for the drive home, the recruiter who calls the Monday after, the family member with news timed for the exit, and the friend who needs an answer before you've slept. The window doesn't care who's knocking.",
  "The urgency gets inserted by the plug who needs an answer before you've decompressed, the ex who picks Sunday afternoon on purpose, the recruiter with a forty-eight-hour deadline, and the family member whose news always seems to land the moment you walk in the door. It runs in every domain and across every demographic. The window's amplification of present bias is universal. The Tuesday Lockbox works universally.",
  "The Loan gets taken out by the ex who catches you mid-afterglow, the new connection who asks for your number while the high is still running, the recruiter who calls right after your best set of the year, and anyone who's been watching for the window and knows exactly when it opens. It runs in every direction and across every identity configuration. The feeling is universal. The borrowing is universal. The source check is universal.",
  "The Wristband Commitment isn't gendered — not for the first-timer still wearing hers three showers later, not for the veteran who's cut his off a hundred times and still feels the pull, not for the sober mentor who knows exactly how long the window stays open. The window is universal. The wristband is a timer that runs in every festie's nervous system regardless of identity.",
 ],
 22: [
  "The Encore is installed by the ex who reframed every good thing you did as suspicious, the manager whose voice still narrates your Monday mornings two years after you quit, the parent whose disappointment runs on autoplay, and the friend group that decided who you were before you did. It doesn't have a gender. It has a function: make 3 a.m. worse.",
  "The Spiral runs in the aftermath of whatever happened to the first-timer who can't remember the sequence, the veteran who's had this exact fog before, the sober anchor doing her own after-action report, and anyone who experienced a high-intensity harm-producing event regardless of their identity. The Encore's use of fragmentation is equally available regardless of what happened.",
  "The Triage sorts the camp mate who still texts every day, the acquaintance who quietly stops making eye contact, the touring friend who goes conspicuously silent, and the handful of people who show up and keep showing up. The specific shape of the split varies. The mechanism is constant: social cost gradient, provisional alignment, the active base. The active base is what the chapter is for.",
  "The Phantom Limb aches for the vendor who left a toxic row and still misses the smell of the coffee cart, the sound tech who quit a bad crew and still misses the specific joke that only worked backstage, the camp member who left the family bus and still misses Sunday breakfast, and anyone who left a community that was also their social world, identity context, and supply chain of belonging. It is not gendered. It is the cost of leaving any place that was genuinely home.",
  "The Wobble hits the first-timer a week after her first big weekend, the veteran two decades into the scene, the sober mentor who thought he'd built immunity to it, and anyone who experienced harm in a high-intensity context. It is universal. It is not gendered. It is the nervous system doing what the nervous system does after something significant. The trajectory is known. The landing is on the other side.",
  "The Decom Spiral runs through the production crew coming off a six-day build, the touring artist coming off a run, the first-timer coming off her first festival ever, and anyone returning from a high-intensity environment to a lower-stimulation one. It is universal, universal, universal. It does not indicate something wrong with you. The protocol is food and sleep and time and the floor.",
  "The Spillover runs in the survivor who flinches at a specific bassline in a grocery store, the veteran who can't be in a crowded room the same way anymore, the first-timer startled by a stranger's cologne, and survivors of every kind of harm in every context. It is universal. The specific triggers are scene-specific. The mechanism is human.",
 ],
 23: [
  "The honest inventory belongs to the camp lead auditing his own six years, the twenty-three-year-old checking whether one bad night was a mistake or the start of a pattern, and the veteran of the scene who has more names on the list than she expected. The format applies to everyone. Nobody's exempt because their intentions were good.",
  "The distinction applies the same way to the camp lead running his third audit, the first-season vendor checking a single bad night, the touring artist counting how many times a version of the same excuse has come up, and anyone running the audit regardless of their identity. The analysis is the same. The inventory is the same.",
  "The architecture applies whether it's the camp lead apologizing to someone he outranks, the veteran apologizing to a first-timer, the vendor apologizing to a customer, or anyone adjusting for a power differential, a platform, and whether contact is even appropriate. The specific delivery changes. The architecture is the same.",
  "The Restitution Question asks the same thing of the camp lead who took credit for someone's idea, the vendor who underpaid a helper, the veteran who let a bad pattern slide for years, and anyone facing a different kind of harm. What action, not what words. The question applies universally.",
  "The Test is available to the camp lead who's learned the vocabulary of accountability, the veteran who's stopped saying the specific things he got called out for, the vendor who's cleaned up his language but not his behavior, and anyone of any identity, tenure, or position. The vocabulary is equally available to everyone. The closed-door audit is the only test that matters.",
 ],
 24: [
  "The whisper network gets carried by the camp mom who's been doing this for a decade, the vendor row regular who hears everything, the sound tech who's seen every crew come through, and anyone of any gender, identity, or tenure level. Its quality is determined by the protocol, not by the person carrying it.",
  "The Burden falls on the camp lead who's fifty-four and has run this row for a decade, on the twenty-six-year-old who inherited the role because nobody else would, on the nonbinary organizer everyone calls “mom” whether she asked for it or not, and on the sober mentor who took the job because someone had to. It falls equally on camp leads of every gender, identity, and tenure. The role carries the weight regardless of who's standing under it.",
  "The missing stair exists in the collective with the most explicit values statement, the crew that talks about accountability constantly, the touring circuit with a formal code of conduct, and the camp that's never had to write one down. The communities with the most explicit accountability commitments may have the most deeply normalized stairs, because the accountability vocabulary gets used to explain why the routing is actually a values-consistent response.",
  "Every role on the roster is available to every person — the camp lead who routes around him, the vendor who vouches for him, the sound tech who's known for a decade and says nothing, and the newcomer who has no idea any of this is happening. The specific configuration of who holds which role in any given Wook's operation reflects the social structure of the specific community.",
  "The community compact works the same way for the small camp writing its first agreement, the mid-size crew formalizing what's always been unspoken, the touring circuit building something bigger, and any community regardless of composition. The mechanism adapts. The need is universal.",
  "The Reporting Pathway Audit applies the same way to the festival's official channel, the camp organization's internal process, the practitioner collective's ethics board, and the booker network's informal grapevine. Different institutional contexts. Same audit mechanics.",
  "The Rebrand Tour is available to any Wook regardless of identity — the guy run out of one circuit who resurfaces three states over, the vendor blacklisted from one row who sets up on another, the camp lead pushed out of one crew who founds a new one. The circuits that are most geographically or culturally isolated are the most attractive targets. Build the cross-circuit connections before you need them.",
  "The Cold Shoulder gets run by the festival committee that's “still reviewing” six months later, the collective's ethics board that never quite convenes, the camp organization whose process exists on paper and nowhere else, and institutions of every size, every stated value, and every explicit accountability commitment. The mechanism doesn't care about the mission statement. The Parallel-Track Protocol applies universally.",
 ],
}

MARKER_TAG = "<!--nf-runs-v2-->"  # written into each replaced card so re-runs are no-ops


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def find_runs_cards(chunk):
    """Return list of (block_start, block_end, inner_p_start, inner_p_end)
    for every '<div class="subcard runs">...</div>' in document order."""
    out = []
    OPEN = '<div class="subcard runs">'
    for m in re.finditer(re.escape(OPEN), chunk):
        block_start = m.start()
        i = m.end()
        d = 1
        for t in re.finditer(r'</?div\b[^>]*>', chunk[i:]):
            d += -1 if t.group(0).startswith('</') else 1
            if d == 0:
                block_end = i + t.end()
                break
        # inner content is everything between the sub-tag </p> and the closing </div>
        sub_tag_close = chunk.index('</p>', m.end()) + 4
        out.append((block_start, block_end, sub_tag_close, block_end - len('</div>')))
    return out


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    if MARKER_TAG in html:
        print("already applied (marker present) -- nothing to do")
        return 0

    applied = 0
    for n in sorted(NEW_RUNS, reverse=True):
        texts = NEW_RUNS[n]
        s, e = bounds(html, n)
        chunk = html[s:e]
        cards = find_runs_cards(chunk)
        assert len(cards) == len(texts), (
            "ch%d: found %d RUNS cards, have %d replacement texts" % (n, len(cards), len(texts))
        )
        # rebuild chunk back-to-front so offsets stay valid
        for (block_start, block_end, p_start, p_end), new_text in zip(reversed(cards), reversed(texts)):
            new_inner = "<p>%s</p>%s" % (new_text, MARKER_TAG)
            chunk = chunk[:p_start] + new_inner + chunk[p_end:]
            applied += 1
        html = html[:s] + chunk + html[e:]

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes" % (format(before, ","), format(len(html), ",")))
    print("applied %d RUNS card rewrites across %d chapters" % (applied, len(NEW_RUNS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
