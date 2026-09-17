# -*- coding: utf-8 -*-
"""R.A.V.E. gap scenarios — the practical first-timer failures.

The existing 14 cards are almost entirely about people. Missing: the three
things that actually go wrong at a first festival -- a fake ticket at the
gate, a dead phone and a lost group, and everything you own being in an
unlockable nylon bag.
"""

ADD = [
("rave", {
 "section": "CAPTURE",
 "hook": "I'VE GOT A SPARE",
 "archetype": "The Ticket That Does Not Scan",
 "clinical": "Resale Fraud / Point-of-Entry Exploitation",
 "who": "A stranger outside the gate, or a friendly account in a resale group who has been messaging you for a fortnight. Plausible, apologetic, in a hurry, and about to be unreachable.",
 "scene": "It sold out and this was the only way. The PDF looked real. The bank transfer went to a name slightly different from the account you were talking to, which he explained. You are now at the gate, four hundred miles from home, with your camping gear on your back, watching a scanner go red, and the number you have been messaging is no longer receiving messages.",
 "tells": [
  "Bank transfer, crypto, or a friends-and-family payment — all irreversible",
  "The account name does not match the person you have been talking to",
  "Urgency about deciding, and a reason resale platforms cannot be used",
  "A screenshot or PDF rather than a transfer through the official system",
  "Price is below face value, or a surprisingly simple explanation for why",
  "They want to meet outside the gate rather than transfer in advance",
 ],
 "happening": "Ticket fraud spikes for sold-out events and targets first-timers because they do not know that the only safe routes are the official resale platform or a transfer inside the ticketing system — both of which make the fraud impossible rather than merely detectable. A PDF proves nothing: the same barcode can be sold to nine people and the first through the gate is the only one who gets in. Irreversible payment is the tell that matters most, because it is chosen for exactly that property, and because a card payment would have given you a chargeback.",
 "check": "R.A.V.E. — “V” CHECK: “Is this going through the official resale system, and can I reverse the payment?” Two noes means it is not a ticket, it is a donation.",
 "darkTitle": "Stranded Is The Second Problem",
 "dark": "The money is not the worst of it. A first-timer at a rural gate with no ticket, no phone signal, no accommodation, a tent, and no way home until the coach on Monday is a genuinely vulnerable person, and there are people at every gate who understand that perfectly. Offers of somewhere to sleep, a way in, or a lift arrive quickly and some of them are exactly what they look like and some are not. So decide the fallback before you travel: what you do, who you call, and how you get home if you do not get in. Nobody expects to need that plan, and the people who needed it always wished they had made it.",
 "move": "Buy from the official seller or the event's own resale platform. If you already have a private ticket, pay by card or a service with buyer protection, never by bank transfer, and verify the ticket through the ticketing company before you travel. Have a get-home plan and the money for it, kept separate.",
 "say": "Happy to buy it if you transfer it through the official system — I don't do PDFs or bank transfers, I've been burned. — I'll pay by card with protection or not at all.",
 "truth": "A screenshot is not a ticket. If the payment cannot be reversed, that is the reason they chose it.",
}),
("rave", {
 "section": "CONDITION",
 "hook": "MY PHONE'S DEAD AND I DON'T KNOW WHERE ANYONE IS",
 "archetype": "The Predictable Crisis Nobody Plans For",
 "clinical": "Communication Failure / Situational Vulnerability",
 "who": "Not a person — the standard second evening of a first festival. Eighty thousand people, no signal, four percent battery, a camp that all looks the same, and the growing realization that you do not actually know where you are.",
 "scene": "You got separated at the changeover. Your phone died twenty minutes ago. You cannot remember whether the camp is left or right of the big flag, all the flags look the same in the dark, and you have just discovered that you do not know a single person's phone number by heart because you have never needed to.",
 "tells": [
  "No meeting point was ever agreed, because everyone assumed phones",
  "You do not know anyone's number without your phone",
  "Your camp has no distinguishing landmark you could describe",
  "No power bank, and the charging tent has a two-hour queue",
  "You have started walking to look for them, which makes it worse",
  "You have been drinking, it is dark, and you are now alone",
 ],
 "happening": "This is the single most common bad night at a first festival, and it is entirely preventable with about four minutes of Thursday planning. It matters beyond inconvenience because it produces exactly the state every predatory pattern in this guide needs: a visibly lost, overwhelmed, slightly drunk newcomer with no way to contact anyone, wandering a dark site. The help that arrives is usually genuine. The point is not to need to rely on whoever it happens to be.",
 "check": "R.A.V.E. — “V” CHECK: “If my phone died right now, could I get back to my camp and reach my people?” That is a Thursday question with a Thursday answer.",
 "darkTitle": "Lost And New Is The Target Profile",
 "dark": "If you read only one line of this guide, read this one: the state described above is the exact profile that the approaches in the first nine pages of this guide are written for. Overwhelmed, isolated, uncontactable, unable to verify anything anybody tells you, and grateful to the first person who is kind. That is not an argument for being frightened of strangers, most of whom will genuinely help you. It is an argument for making sure that you are never in the position of having to take whatever help appears, because you have a meeting point, a written number, and a charged phone.",
 "move": "On Thursday: agree a physical meeting point and a fallback time with your group, photograph your tent and a landmark near it, write two phone numbers and your camp location on paper in your pocket, and carry two charged power banks. If it happens anyway: go to the meeting point and stay there, or to welfare, and do not wander.",
 "say": "Before we split up — if anyone loses everyone, the big oak by the water point, on the hour. Everyone got that? Write it on your arm.",
 "truth": "Phones die at festivals. Plan for the version of the weekend where yours already has.",
}),
("rave", {
 "section": "CONDITION",
 "hook": "IT'S FINE, NOBODY STEALS HERE",
 "archetype": "Everything You Own In An Unlockable Bag",
 "clinical": "Opportunistic Theft / Misplaced Trust Heuristic",
 "who": "Mostly opportunists working the campsites during headline sets, when the fields empty out and thousands of tents stand unattended for two hours. Occasionally someone who has been watching your camp specifically since Thursday.",
 "scene": "Everyone said the campsite was safe and mostly it is and you believed it, so your passport, your bank card, your keys and your spare phone are in your tent, which is closed with a zip that a child could open, while you are a mile away watching the headliner along with everybody else in the field.",
 "tells": [
  "Valuables kept in a tent, which is a bag, not a room",
  "Nobody in your camp stays behind during the big sets",
  "Your camp is on a main thoroughfare or at the edge",
  "Someone unfamiliar has been friendly about which sets you are going to",
  "No photographs of your gear, no serial numbers, no contents insurance",
  "You are carrying every card you own rather than one",
 ],
 "happening": "Campsite theft is almost entirely opportunistic and almost entirely timed — it happens during the headline sets, when the campsite is empty and nobody will be back for hours. The advice that the campsite is safe is broadly true and slightly dangerous, because it is true about people and not about opportunity. The practical loss is rarely the phone; it is the passport, the car keys, the bank cards and the house keys, which turn a stolen bag into a genuinely hard week rather than an annoying one.",
 "check": "R.A.V.E. — “A” CHECK: “What is in my tent right now that I could not get home without?” Whatever that is should not be in there.",
 "darkTitle": "The Keys Are Worse Than The Phone",
 "dark": "Think past the value of the objects. Car keys taken from a tent mean somebody knows there is a vehicle in that car park and now has the means to open it. House keys plus a driving licence or an addressed letter in the same bag mean somebody has your address and your keys, and you are four hours from home and will not be back for two days. That is the version worth preventing, and it is prevented by separation rather than by security: cards, keys and documents split across your body, the car, and a locker, so that no single loss is catastrophic.",
 "move": "Rent the locker — it is the best value item at any festival. Keep one bank card and a photo of your ID on you, leave the passport at home unless the event requires it, and never keep house keys and your address in the same place. Photograph your gear before you travel.",
 "say": "I'm doing a locker for the cards and keys — anyone want to split one? — Someone's always at camp during the headliner, let's rota it.",
 "truth": "A tent is a bag with a zip. Anything you cannot get home without does not live in a bag with a zip.",
}),
]
