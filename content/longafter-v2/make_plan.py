#!/usr/bin/env python3
"""Source of truth for the structure of The Long After, 2nd edition: parts, chapter order, web addresses,
target searches and required links. Writes plan.json. Chapter text lives in NN-*.md beside it.
Columns: slug, title, primary search phrase, secondary phrases, Decoder pages, Feminine passages, heavy"""
import json
from pathlib import Path
F = {  # The Sovereign Divine Feminine: where it covers the same ground (from inside the relationship / leaving)
 "psc": "post-separation-control#core-concept", "psc-q": "post-separation-control#quick-start",
 "psc-o": "post-separation-control#o-orient-return-to-facts-and-pattern", "psc-r": "post-separation-control#r-respond-dont-react",
 "psc-rc": "post-separation-control#reality-check-manipulation-vs-friction", "psc-it": "post-separation-control#if-then-plans",
 "log": "liberation-logistics#top", "leash": "the-digital-leash#core-concept", "leash-r": "the-digital-leash#r-respond-scripts-soft-firm-final",
 "smear": "digital-smear-campaigns#core-concept", "siege": "the-social-siege#core-concept", "play": "the-sovereign-playbook#core-concept",
 "rescue": "the-30-minute-rescue#top", "admin": "the-administrative-cage#core-concept", "synth": "synthetic-evidence#core-concept",
 "mother": "the-motherhood-matrix#core-concept", "cycle": "the-manipulation-cycle#core-concept",
}
P = [
 ("start", "Start here", [
  ("where-are-you-right-now", "Where are you right now?", "what to do after leaving an abusive relationship", [], [], [], False),
  ("if-youre-not-safe-right-now", "If you're not safe right now", "domestic abuse help", ["domestic violence hotline", "crisis line"], [], ["rescue"], True),
  ("how-to-use-this-book", "How to use this book, and what it is not", "post separation abuse book", ["free book", "what this book is not"], [], [], False),
 ]),
 ("i", "What is happening", [
  ("leaving-was-the-middle", "Leaving was the middle", "after leaving an abusive relationship", ["aftermath of leaving an abusive relationship", "why is it still hard after I left"], [], ["psc"], False),
  ("what-is-post-separation-abuse", "What post-separation abuse is", "post separation abuse", ["what is post separation abuse", "post separation abuse examples", "is post separation abuse a crime", "post separation abuse and coercive control"], ["legal-abuse", "smear-campaigns", "children-as-leverage", "financial-control"], ["psc"], False),
  ("why-it-often-gets-worse-first", "Why it often gets worse first", "is leaving an abusive relationship the most dangerous time", ["ex getting worse after breakup", "separation risk"], ["intimidation"], ["psc-o"], True),
  ("the-shape-it-takes-when-they-cant-reach-you-directly", "The shape it takes when they can't reach you directly", "post separation control", ["why is my ex still controlling me", "ex still controlling after breakup"], ["punishment-by-proxy", "monitoring-surveillance"], ["psc"], False),
  ("is-my-ex-a-narcissist", "Is my ex a narcissist?", "narcissist after breakup", ["what does a narcissist do after a breakup", "will a narcissist come back", "why did the narcissist block me", "can a narcissist change"], ["darvo", "smear-campaigns", "hoovering-relief-bait"], ["cycle"], False),
  ("abuse-or-a-hard-breakup", "Abuse, or a hard breakup?", "normal breakup vs narcissist breakup", ["is it abuse or conflict", "am I the abuser"], ["false-equivalence", "self-gaslighting-induction"], ["psc-rc"], False),
  ("if-your-story-doesnt-look-like-the-usual-one", "If your story doesn't look like the usual one", "post separation abuse against men", ["abuse in same sex relationships", "leaving a controlling family", "forced marriage"], ["identity-based-isolation", "status-threats"], [], False),
  ("the-first-30-days", "The first 30 days", "after leaving an abusive relationship checklist", ["what to do after leaving an abusive relationship", "first steps after leaving"], ["account-control"], ["log"], False),
  ("if-they-left-you", "If they left you", "after a narcissist breaks up with you", ["hoovering after discard", "when a narcissist leaves you", "why did my ex move on so fast"], ["blame-discard", "triangulation"], ["cycle"], False),
  ("still-under-the-same-roof", "Still under the same roof", "separated but living together", ["how to leave when you live together", "co parenting but living together"], ["time-control", "mobility-control"], ["log"], True),
 ]),
 ("ii", "Staying safe after you leave", [
  ("a-safety-plan-for-after-youve-left", "A safety plan for after you've left", "safety plan after leaving an abusive relationship", ["how to stay safe after leaving", "post separation safety plan"], [], ["log", "psc-o"], True),
  ("warning-signs-to-take-seriously", "Warning signs to take seriously", "domestic violence risk factors", ["strangulation warning sign", "danger assessment"], ["intimidation", "emotional-blackmail-via-self-harm-threats"], ["log"], True),
  ("surveillance-and-technology", "Surveillance and technology", "is my ex tracking me", ["tracker on my car", "stalkerware signs", "location sharing after breakup"], ["monitoring-surveillance", "location-tracking", "account-control"], ["leash"], False),
  ("stalking-and-harassment", "Stalking and harassment after a breakup", "stalking after a breakup", ["ex harassing me", "what counts as stalking"], ["monitoring-surveillance", "intimidation"], ["psc"], True),
  ("intimate-images-and-online-threats", "Intimate images and online threats", "ex threatening to post pictures", ["revenge porn", "intimate image abuse", "sextortion by ex"], ["doxxing", "reputation-hijacking"], ["synth"], True),
  ("your-address-your-records-your-mail", "Your address, your records, your mail", "address confidentiality program", ["hide my address from my ex", "remove my address from people search sites"], ["location-tracking"], ["log"], False),
 ]),
 ("iii", "How it continues", [
  ("children-as-the-channel", "Children as the channel", "post separation abuse child custody", ["using children as leverage", "signs you are co parenting with a narcissist"], ["children-as-leverage", "triangulation", "parentification"], ["mother", "psc-o"], True),
  ("money-as-the-channel", "Money as the channel", "post separation financial abuse", ["ex won't pay child support", "coerced debt", "economic abuse after separation"], ["financial-control", "financial-enmeshment", "financial-dependence-by-design"], ["admin"], False),
  ("the-narrative-campaign", "The narrative campaign", "smear campaign after breakup", ["ex telling lies about me", "how to respond to a smear campaign"], ["smear-campaigns", "narrative-monopoly", "reputation-hijacking"], ["smear", "siege"], False),
  ("your-family-and-mutual-friends", "Your family and mutual friends", "flying monkeys", ["my family sided with my ex", "mutual friends after breakup"], ["flying-monkeys-proxy-recruitment", "silent-coalitions"], ["siege"], False),
  ("the-new-partner", "The new partner", "ex contacting my new partner", ["my ex's new partner contacted me", "warning the new partner"], ["triangulation", "smear-campaigns"], [], False),
  ("hoovering", "Hoovering", "hoovering", ["hoovering after breakup", "why is my ex contacting me again", "will a narcissist come back", "how long does hoovering last"], ["hoovering-relief-bait", "intermittent-reinforcement-push-pull", "future-faking", "love-bombing"], ["psc", "cycle"], False),
  ("when-they-say-youre-the-abuser", "When they say you're the abuser", "reactive abuse", ["false allegations in custody", "ex called CPS on me", "DARVO"], ["darvo", "false-reports", "preemptive-accusation-complaint-weaponization"], ["psc"], False),
  ("when-it-stops", "When it stops", "does post separation abuse ever end", ["how long does post separation abuse last", "when does post separation abuse stop"], ["intermittent-reinforcement-push-pull"], [], False),
 ]),
 ("iv", "Contact", [
  ("no-contact-low-contact", "No contact, low contact, or contact you can't avoid", "no contact with ex", ["how to go no contact with kids", "low contact"], ["controlled-communication"], ["psc-q", "play"], False),
  ("grey-rock-and-written-only-contact", "Grey rock and written-only contact", "grey rock method", ["how to grey rock someone", "does grey rock work", "grey rock a narcissist"], ["stonewalling"], ["play", "psc-r"], False),
  ("words-you-can-use", "Words you can use", "phrases to use when co parenting with a narcissist", ["how to respond to an ex", "BIFF response"], ["guilt-tripping", "emotional-blackmail"], ["leash-r"], False),
  ("messages-you-dont-have-to-answer", "Messages you don't have to answer", "should I respond to my ex", ["do I have to reply to my ex", "ex texting me"], ["time-control", "false-dilemma"], ["psc-it"], False),
 ]),
 ("v", "Courts and the systems", [
  ("what-to-document-and-how", "What to document and how", "how to document post separation abuse", ["how to document abuse for court", "evidence log"], ["false-reports"], ["log", "synth"], False),
  ("systems-abuse", "Systems abuse and litigation abuse", "litigation abuse", ["litigation abuse in family court", "how to prove litigation abuse", "legal abuse", "vexatious litigant"], ["legal-abuse", "administrative-escalation", "legal-administrative-threats"], ["admin", "psc"], False),
  ("solicitors-legal-aid-and-no-money", "Legal help with little or no money", "free legal help domestic violence", ["legal aid domestic abuse", "pro bono family lawyer"], [], ["log"], False),
  ("family-court-honestly", "Family court, honestly", "family court coercive control", ["post separation abuse custody", "how often do narcissists win in court", "parental alienation accusation"], ["children-as-leverage", "legal-abuse"], ["admin"], False),
  ("your-day-in-court", "Your day in court", "what to expect at a family court hearing", ["custody hearing tips", "court with an abusive ex"], ["intimidation"], [], False),
  ("divorce-and-separation-proceedings", "Divorce and separation proceedings", "divorcing a narcissist", ["divorce with an abusive spouse", "financial disclosure hiding assets", "mediation and domestic abuse"], ["financial-control", "time-control"], ["admin"], False),
  ("police-and-protective-orders", "Protective orders", "how does a protective order work", ["restraining order after breakup", "how long does a protective order last", "do protective orders work"], ["intimidation"], ["log"], True),
  ("police-and-reporting", "Police and reporting", "can I report post separation abuse to the police", ["coercive control offence", "Clare's Law"], ["false-reports"], ["log"], False),
  ("housing-and-benefits", "Housing and benefits", "housing help after domestic abuse", ["break lease domestic violence", "benefits after separation"], ["financial-dependence-by-design"], [], False),
  ("where-to-find-the-right-body", "Where to find the right body", "where to get help after domestic abuse", ["who to contact about my ex"], ["administrative-escalation"], [], False),
  ("untangling-the-paperwork", "Untangling: the house, the car, the accounts and the paperwork", "what to change after leaving an abusive relationship", ["change beneficiary after divorce", "joint mortgage abusive ex"], ["financial-enmeshment", "account-control"], ["log"], False),
 ]),
 ("vi", "Children", [
  ("co-parenting-or-parallel-parenting", "Co-parenting or parallel parenting?", "co parenting with a narcissist", ["parallel parenting", "can you co parent with a narcissist", "can parallel parenting be court ordered"], ["children-as-leverage", "controlled-communication"], ["mother"], False),
  ("handovers", "Handovers", "safe custody exchange", ["custody exchange with abusive ex", "supervised exchange"], ["intimidation", "children-as-leverage"], [], False),
  ("your-children-and-what-to-say", "Your children, and what to say", "how to explain divorce to a child", ["what to tell kids about an abusive parent"], ["parentification"], ["mother"], False),
  ("how-children-react", "How children react, and what helps them", "effects of domestic abuse on children", ["signs a child is affected by domestic violence", "child therapy after domestic abuse"], ["parentification", "golden-child-elevation"], [], True),
  ("when-your-child-is-pulled-in", "When your child is pulled into it", "child repeating what the other parent says", ["child refusing visits", "ex using child to spy"], ["children-as-leverage", "triangulation"], [], True),
  ("apps-calendars-and-the-parenting-plan", "Apps, calendars and the parenting plan", "co parenting app court approved", ["parenting plan high conflict", "co parenting communication app"], ["controlled-communication"], [], False),
  ("moving-passports-and-travel-with-children", "Moving, passports and travel with children", "moving away from abusive ex with child", ["passport alert child abduction", "relocation custody"], ["mobility-control"], [], True),
  ("pregnant-or-with-a-new-baby", "Pregnant, or with a new baby", "leaving an abusive relationship while pregnant", ["newborn custody abusive ex"], ["vulnerability-weaponization"], ["mother"], True),
 ]),
 ("vii", "Feelings", [
  ("the-trauma-bond", "The trauma bond: why you miss someone who hurt you", "trauma bond", ["what is a trauma bond", "how to break a trauma bond", "how long does a trauma bond last", "trauma bond withdrawal", "trauma bond vs love"], ["trauma-bonding", "intermittent-reinforcement-push-pull"], ["cycle"], False),
  ("what-youre-allowed-to-feel-about-someone-you-left", "What you're allowed to feel about someone you left", "why do I miss my abuser", ["missing someone who hurt you", "feelings after leaving an abusive relationship"], [], [], False),
  ("the-grief-nobody-will-let-you-have", "The grief nobody will let you have", "grief after leaving an abusive relationship", ["grieving a toxic relationship"], [], [], False),
  ("guilt-and-shame", "Guilt and shame", "guilt after leaving an abusive relationship", ["feeling guilty about leaving", "was it my fault"], ["shame-installation", "guilt-tripping"], [], False),
  ("anger-arriving-late", "Anger, arriving late", "anger after narcissistic abuse", ["angry years after breakup"], [], [], False),
  ("checking-their-profile", "Checking their profile", "checking ex's social media", ["why can't I stop thinking about my ex", "obsessive thoughts about ex"], ["intermittent-reinforcement-push-pull"], [], False),
  ("closure-and-forgiveness", "Closure you give yourself, and whether you have to forgive", "closure after narcissistic abuse", ["do I have to forgive my abuser", "closure letter to ex"], ["forced-forgiveness-weaponized-forgiveness", "apologies-without-repair"], [], False),
  ("the-anniversary-effect", "The anniversary effect", "anniversary reaction trauma", ["trauma anniversary", "hard dates after abuse"], [], [], False),
  ("memory", "Memory, and doubting yourself", "am I making it up", ["gaslighting after breakup", "memory loss after abuse"], ["gaslighting", "self-gaslighting-induction"], [], False),
 ]),
 ("viii", "Body, health and help", [
  ("what-your-nervous-system-is-doing", "What your nervous system is doing", "hypervigilance after abuse", ["anxiety after narcissistic abuse", "complex PTSD after abuse"], [], [], False),
  ("sleep", "Sleep", "can't sleep after breakup", ["insomnia after trauma"], ["sleep-deprivation"], [], False),
  ("getting-sick-after-leaving", "Getting sick after leaving", "getting sick after leaving an abusive relationship", ["stress illness after breakup"], [], [], False),
  ("if-there-was-sexual-abuse", "If there was sexual abuse or reproductive coercion", "sexual abuse in a relationship", ["reproductive coercion", "marital rape"], [], ["rescue"], True),
  ("drinking-drugs-and-getting-through", "Drinking, drugs and other ways of getting through", "drinking after breakup", ["self medicating after trauma"], [], [], True),
  ("finding-a-therapist-who-understands-this", "Finding a therapist who understands this", "therapist for trauma bond", ["therapy for trauma bond", "counseling after leaving an abusive relationship", "trauma informed therapist"], ["weaponized-therapy-speak"], [], False),
  ("when-its-more-than-aftermath", "When it's more than aftermath", "suicidal after leaving abusive relationship", ["crisis help"], [], [], True),
 ]),
 ("ix", "The people around you", [
  ("the-friends-who-didnt-believe-you", "The friends who didn't believe you", "friends don't believe me abuse", [], ["silent-coalitions"], ["siege"], False),
  ("the-friends-who-did-and-are-tired", "The friends who did, and are tired", "supporting a friend after abuse", ["compassion fatigue friend"], ["support-system-exhaustion"], [], False),
  ("your-parents", "Your parents", "parents don't support me after divorce", [], ["golden-child-elevation"], [], False),
  ("telling-someone-new", "Telling someone new", "when to tell a new partner about abuse", [], [], [], False),
  ("making-new-people-from-scratch", "Making new people from scratch", "making friends after an abusive relationship", ["lonely after breakup"], ["isolation"], [], False),
  ("sharing-a-town-a-workplace-or-a-community", "When you share a town, a workplace or a community", "ex in the same friend group", ["working with an ex", "church after divorce abuse"], ["silent-coalitions"], [], False),
 ]),
 ("x", "Rebuilding", [
  ("money-from-zero", "Money from zero", "rebuilding finances after an abusive relationship", ["coerced debt credit report"], ["financial-control"], ["log"], False),
  ("work-again", "Work again", "domestic violence leave", ["explaining a gap after abuse"], [], [], False),
  ("a-home-that-feels-like-yours", "A home that feels like yours", "feeling safe at home after abuse", [], [], [], False),
  ("pets-and-the-things-left-behind", "Pets and the things left behind", "ex took my dog", ["pet foster domestic violence", "getting belongings from ex"], ["children-as-leverage"], ["log"], False),
  ("holidays-and-the-first-year", "Holidays and the first year's calendar", "first holidays after divorce", ["holiday custody abusive ex"], [], [], False),
  ("your-own-tastes-rediscovered", "Your own tastes, rediscovered", "finding yourself after an abusive relationship", ["who am I after abuse"], ["identity-erosion"], [], False),
  ("trust-as-a-practice", "Trust as a practice", "trust issues after abuse", ["learning to trust again"], [], [], False),
  ("dating-when-youre-ready-and-when-youre-not", "Dating, when you're ready and when you're not", "dating after an abusive relationship", ["red flags dating"], ["love-bombing", "future-faking"], [], False),
  ("the-version-of-you-from-before", "The version of you from before", "will I ever be the same after abuse", [], ["identity-erosion"], [], False),
  ("what-recovered-actually-means", "What “recovered” actually means", "recovery from narcissistic abuse", ["healing after abuse signs"], [], [], False),
 ]),
 ("xi", "The ledger", [
  ("if-you-go-back", "If you go back", "how many times does it take to leave an abusive relationship", ["going back to an abuser"], ["hoovering-relief-bait"], [], False),
  ("helping-someone-in-year-one", "Helping someone in year one", "how to help a friend who left an abusive relationship", [], [], [], False),
  ("what-this-book-might-have-wrong", "What this book might have wrong", "post separation abuse research", [], [], [], False),
  ("the-long-after", "The long after", "life after narcissistic abuse", ["healing years later"], [], [], False),
 ]),
 ("tools", "Toolbox", [
  ("the-record", "The record", "abuse documentation template", ["incident log template"], [], ["log"], False),
  ("safety-plan-worksheet", "Safety plan worksheet", "safety plan worksheet domestic violence", [], [], ["log"], True),
  ("device-and-account-audit", "Device and account audit", "how to check phone for stalkerware", [], ["monitoring-surveillance"], ["leash"], False),
  ("court-day-checklist", "Court day checklist", "family court checklist", [], [], [], False),
  ("pocket-card-words-you-can-use", "Words you can use: the pocket card", "how to reply to an abusive ex", [], [], [], False),
  ("the-card", "The card", "post separation abuse summary", [], [], [], False),
  ("find-help", "Find help", "domestic abuse help near me", [], [], [], True),
  ("a-to-z", "A to Z: the words, plainly", "post separation abuse terms", ["hoovering meaning", "trauma bond meaning", "grey rock meaning"], [], [], False),
  ("questions-people-ask", "Questions people ask", "post separation abuse questions", [], [], [], False),
  ("for-professionals", "For professionals", "post separation abuse resource for advocates", [], [], [], False),
  ("all-sources", "Every source in this book", "domestic abuse research sources", ["post separation abuse sources"], [], [], False),
 ]),
]
OLD_GONE = {"what-this-book-is-not": "how-to-use-this-book"}   # first-edition addresses that now live elsewhere
out = {"parts": [], "chapters": [], "feminine": F, "old_redirects": OLD_GONE}
for pid, ptitle, chs in P:
    out["parts"].append({"id": pid, "title": ptitle, "chapters": [c[0] for c in chs]})
    for i, (slug, title, kw, kw2, dec, fem, heavy) in enumerate(chs, 1):
        out["chapters"].append({"slug": slug, "part": pid, "n": i, "title": title, "keyword": kw, "keywords2": kw2,
                                "decoder": dec, "feminine": [F[x] for x in fem], "heavy": heavy})
Path(__file__).with_name("plan.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
nch = sum(1 for c in out["chapters"] if c["part"] not in ("start", "tools"))
print(f"{len(out['parts'])} sections, {nch} chapters, {len(out['chapters'])} pages")
