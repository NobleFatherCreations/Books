---
doc_type: combo
doc_id: CORP-C185
sector: Corporate & Consulting
sector_id: CORP
category_id: CAT05
category_name: Accountability Evasion Composites
combo_id: C185
combo_name: The Wall
legacy_id: P13 (proposed 4-5 Nov 2026, approved 5 Nov)
tactics:
  - Stonewalling
  - Feigned Ignorance
  - Reverse Psychology
  - Limited Hangout
  - Lying
  - Competitive Victimhood
tags: [vendor-breach, incident-report, account-team, disclosure, support-tickets]
fit_tier: A
version: 1
status: draft
---

# C185: The Wall — Corporate & Consulting

## Before the Story

This chain can install a belief that asking again will only wear you out, and a reflex to accept a small confession or a bigger sorrow as the end of a question that was never answered.

If you never see how it got in, it can follow you long after, as:

- A habit of explaining the same thing three times, slowly and patiently, before anyone has even said they don't understand.
- An automatic thought when an answer feels thin, "at least they admitted something," that lets the larger thing go.
- A pull to comfort the other person whenever you raise your own hurt, until your question disappears.

**A point in a life.** Two decades into a security career.

**Where it happens.** A company and its outside vendor.

*You won't be told what this chain is called, or what is inside it, until the story ends.*

## Cold Open

You're a chief information security officer at a company that depends on an outside vendor for a system holding customer records. You're forty-six, you've spent two decades learning that the first account of an incident is never the whole account, and you have a habit of asking the same question three different ways. Your vendor's account team is friendly. You've been on their calls for four years.

**The first week, your office**

On a Tuesday, a threat feed shows a pattern that looks like it touches the vendor's environment. You open a ticket and send a short, specific question: has anything unusual been observed in the environment that hosts your data between the first and the ninth of the month, and if so, what was affected? You attach the dates. You keep the wording neutral on purpose.

Nothing comes back. Not a refusal, not an acknowledgment. The ticket sits at "Awaiting vendor." On Thursday you phone the account director. He's warm and says he'll look into it. On Friday you call again, and he says the team is busy and he'll have an update on Monday. On Monday there's no update. In the ticket thread a support agent writes that the matter has been "forwarded to the relevant team." You refresh the page until your eyes ache.

You ask again, with a more specific question. This time a reply arrives quickly, and says the team isn't aware of anything that fits the description. You ask whether that means nothing happened or that nobody has looked. The reply suggests you may be reading too much into a routine feed.

You mention that your board's audit committee meets in three weeks. The account director calls, and his voice has softened. He says he hopes you don't feel he's hiding something, because that would really hurt, given how long the two of you have worked together. "If you don't trust us," he says, "take it straight to your committee. Pull the contract. I'd understand." You find yourself saying that of course you don't think so, that nobody needs to go that far. Your face is warm.

**Two weeks later, your office**

On the Wednesday, the vendor sends "Incident Report, Version 1." It's a page and a half. It says that on a single day a misconfiguration briefly exposed a storage location, that the exposure was "limited in duration," that "no evidence of misuse has been identified," and that the issue has been fixed. It doesn't give a start date. It doesn't say which records, how many, or who reviewed the logs. You write back with five numbered questions. The reply comes the same afternoon, polite and brief. It confirms the single day and says that, in the interests of openness, the vendor wishes to share that a second configuration issue was also found, on a different date, and has also been fixed. You note that this is a new fact. The account director says it should give you comfort, because the vendor has been very open.

When you press for the log review and the number of records, the reply says the vendor can confirm that "no customer data left the environment." You ask how that is known. The reply says the security team confirmed it. You ask for the report. The reply says the report is internal. You read it twice, and your jaw sets. That evening an internal note appears in the ticket thread, visible by mistake, timestamped the morning before that reply: "Outbound transfer from affected storage confirmed. Do not share with customer yet." By the next morning it's gone.

On the next call the account director says his team has been working nights, that two of them are exhausted, and that he's had a very hard month himself, with an illness in the family. He asks, kindly, whether you could let the team recover before another round of questions. The call ends with you apologizing for the pressure.

**Two months later, the audit committee**

Two months later you're in the boardroom on the sixth floor, and the audit committee chair asks how confident you are that customer records were untouched. You hear yourself say, "We are reviewing," in the vendor's soft voice. The chair waits. You add that the vendor was quick to disclose a second issue, which you've been counting as a point in their favor, and you move on to the renewal. Nobody asks you to go back.

Afterward, in the corridor, your deputy asks about the transfer note you mentioned once. You tell her you're sure it was nothing, then spend ten minutes asking how she's coping with the workload. You used to press until the gaps closed. Now you ask once, begin with an apology, and open the ticket at three in the morning to see whether anyone has answered. No one has.

You close the laptop. In front of you are the first version of the incident report, the ticket thread and a page of your own notes. The page lists everything you were told, in order. Whether the records left is still not on it.

## The Name

That's **The Wall**.

## Definition

The Wall is the sequence where questions are absorbed rather than answered, using Stonewalling, Feigned Ignorance, Reverse Psychology, Limited Hangout, Lying and Competitive Victimhood to convert a person's patience and willingness to explain again into the loss of answers and the energy to keep asking. It benefits whoever would otherwise have to disclose or change something, and it exploits the practical reality that a customer needs the vendor to continue working. It is hard to detect because silence, slow response and partial disclosure also arise from caution, legal review and genuine uncertainty. In this sector the person may lose time in which to protect customers, the ability to report accurately to a board or regulator, and trust in their own judgment. Intent would require additional evidence, and a vendor in an active investigation may be limited in what it can say.

## Verbal Breakdown

The component tactics, in order:

1. **Stonewalling** — A ticket left at "Awaiting vendor," an account director who says on Thursday he will look into it and promises an update on Monday that never comes, and an agent noting the matter has been "forwarded to the relevant team." This functions by making the cost of asking, in time and goodwill, higher than the cost of staying uninformed. Concern rises when silence follows only the questions that matter most.

2. **Feigned Ignorance** — A quick reply that the team "is not aware of anything that fits the description," and a suggestion that you may be reading too much into a routine feed when you ask whether anyone has looked. This functions by answering a narrower question than the one asked, so that the absence of a finding sounds like an absence of an event. Concern rises when you ask whether nobody looked and do not get a direct answer.

3. **Reverse Psychology** — An invitation to do the opposite: hurt that you might think him hiding something, then "If you don't trust us, take it straight to your committee. Pull the contract," and you say nobody needs to go that far. This functions by making the asker responsible for the relationship, so that continued questioning looks like an accusation. Concern rises when you find yourself reassuring the party you are questioning.

4. **Limited Hangout** — A page-and-a-half report with no start date, no records and no reviewer, then, "in the interests of transparency," a second configuration issue on another date, offered as a reason for comfort that closes the thread. This functions by giving enough to look candid while keeping back the scope, the dates and the records. Concern rises when the disclosure is offered only after a deadline or a board date is mentioned, and the larger questions are called settled.

5. **Lying** — A sentence the vendor's own note contradicts: "No customer data left the environment," confirmed by a security team whose report is internal, while a ticket note timestamped earlier reads "Outbound transfer from affected storage confirmed. Do not share with customer yet." This functions by filling the gap with certainty at the moment the target is least able to test it. Concern rises when a flat assurance is given, and the supporting report is withheld, and a later version contradicts it. Falsehood would need to be established by the later record, and not assumed.

6. **Competitive Victimhood** — The account director says his team has been working nights, two people are exhausted, he has had a very hard month with a family illness, and asks you to let them recover before another round of questions. This functions by answering one person's concern with another person's greater distress, so that continuing to ask appears insensitive. Concern rises when personal hardship is raised only after a specific request.

## Why This Order

**Stonewalling** has to come first because it establishes tempo. Silence is not a refusal, and it cannot be challenged as one. It teaches that asking is slow and costly, and it buys the time in which the first account hardens. It has to come before the narrower reply that nothing fits, because a ticket left to sit for days shows you that asking is slow and costly, and the first account settles in the meantime.

> You email your landlord about a leak. Nothing. A text on Thursday says, "Will look into it." By the following week you have stopped counting the days. Flip it: if the landlord had replied "what leak?" before you had even waited a day, you would send photos and ask for a date in writing.

**Feigned Ignorance** narrows the question without denying anything. It sets up a second phase: when you ask the narrower question again, you are told nothing was found, and you cannot easily show that the narrower question was not the one you asked. It has to come before the account director's hurt, because a reply that says nothing was found leaves you asking whether anyone looked, and that question is what he then treats as distrust.

> You ask the shop whether your parcel left the depot. "We have no record of anything matching that," says the assistant, and you cannot tell whether it never left or nobody checked. Flip it: if the assistant had sounded hurt that you doubted the shop before saying anything about records, you would kindly ask again where the parcel is.

**Reverse Psychology** is the pivot. Up to now you were the customer making a reasonable inquiry; after it, you are the one whose suspicion might damage a relationship. It turns your diligence into an emotional burden. It has to come before the second configuration issue, because only a client who has been made to reassure him will take a small volunteered fact as proof that the vendor is open.

> You ask a friend why a refund is taking so long. "I'd hate to think you don't trust me," she says. Now you are the one doing the reassuring. Flip it: if your friend cheerfully owned up to one small slip about the refund before any talk of trust, you would thank her and still ask where the rest stands.

The **Limited Hangout** is the key conversion point. A small admission arrives at the moment of greatest pressure, and it does two jobs: it makes the vendor look open, and it supplies a story that the matter has been addressed. The unanswered scope, dates and records are then framed as detail. It has to come before the flat statement about customer data, because the dates, the records and the log review are still unanswered, and a firm sentence then becomes the best information you have.

> Your teenager cheerfully admits to being ten minutes late. You are so pleased by the honesty that you never ask about the other two hours. Flip it: if your teenager had said flatly "I was home by ten" before admitting to anything, you would calmly ask a few gentle questions about the evening.

**Lying** fills what remains. It works because the previous steps have already established that you will not get the report, and a flat statement now appears to be the best information available. It also gives plausible deniability if a later version corrects it. It has to come before the account director's hard month, because once you have been told the data never left and the report is internal, your next question is the one his team's exhaustion can be set against.

> After weeks of being told you cannot see the invoice, someone says flatly, "It was paid in March." Without the paper, that sentence is the best you have. Flip it: if the person had told you how hard their own weeks had been before saying anything about the invoice, you would still ask kindly to see the paper.

**Competitive Victimhood** closes the loop and shifts the moral weight. It meets your remaining questions with a story about someone else's suffering, which is hard to answer without seeming heartless. It has to come last, because by now you hold a thin report and a flat denial, and his worn-out team and family illness are what stand between you and one more round of questions.

> You ask your contractor why the job is late. He tells you about his sick mother and his own awful month. You end up apologizing. Flip it: if the contractor's tale of a hard month came first and a flat "it's all done" came afterwards, you would ask to see the finished job before apologizing for anything.

What weakens the sequence: written questions with numbered points and a response date; a request to see the log review method; a second channel to someone senior at the vendor; and a record that is shared with your own counsel and audit committee.

## Why the System Produces This Order

Nobody has to design this sequence. It falls out of what a vendor relationship around a sensitive system is built to produce. A support queue has no duty to answer quickly, and its tickets pass through legal and security review before anything goes out. An account team is rewarded for keeping the client, and the renewal depends on the relationship staying warm. And the customer can see only what the vendor chooses to send, while its own board expects answers.

Stonewalling comes first because the queue is slow by default and the first account of an incident has to be checked inside the vendor before anyone commits to it. Silence is the cheapest response that cannot be called a refusal, and it buys the days in which the first account is written.

Feigned Ignorance comes second because the first reply is drafted from what the front line has been told, not from what the logs show. A narrow question gets a narrow answer: "not aware of anything that fits" is true of the person writing it, and it leaves you to prove the question was the one you asked.

Reverse Psychology comes third because an account team is judged on warmth, and a client who mentions the board threatens the thing the team is measured on. The easiest reply is to treat the question as a loss of trust, which has the client reassure the vendor.

The Limited Hangout comes fourth because by the time a written report is expected, something has to be given. A second, smaller issue is the natural thing to hand over: it is real, it can be shared, and it makes the report look complete.

Lying comes fifth because a report must say something, and a flat statement is shorter than "we do not yet know". By now the client has learned that the underlying report will not be shown, so the statement stands as the best information available.

Competitive Victimhood comes last because the account director is a person, and the exhaustion of a team that has worked nights is real. It is the last thing left to say to a client who keeps asking, and it is very hard to answer without sounding heartless.

Put it together and the order is the order this setting needs: delay, a narrow answer, a test of loyalty, a partial disclosure, a flat denial and a plea for sympathy. What it turns the person into is a security officer who has been taught, call by call, to stop asking.

## On Purpose

Nobody orchestrated what you just read. A ticket queue, a renewal and a team that answers to its own managers are what this setting produces, and the people inside were doing their jobs. This is what it looks like when one person does it knowingly, to a client's finance lead. The tactics are the same and so is their order. Only the chooser has changed.

Ignatius Dunmore, a finance controller, wrote to her company's outsourced payroll provider asking whether a batch of payments had been sent twice. Nothing came back for six days, apart from a note that the matter had been "passed to the relevant team." When she wrote again with a narrower question, the reply said no one was aware of anything matching it. She asked whether that meant it hadn't happened or hadn't been checked. Her relationship manager, Desmond Aquino, phoned and said it would hurt him if she doubted them after five years, and that she was welcome to take it to her auditors. She told him she didn't doubt them. A week later a short report arrived. It listed one duplicate of a small amount and added, helpfully, that a second small one had also been found and fixed. When she asked for the totals, Desmond said flatly that all other payments had been reconciled. She asked for the reconciliation. He said it was internal. On the next call he said his team had been up late, that his father was unwell, and could she give them a few weeks before the next round of questions. She apologized for the pressure and closed the file.

Desmond was never confused about what he was doing. He told a colleague he could always tell when a client had stopped pushing.

From the inside, the person in the middle can't tell the difference, and doesn't need to. The pattern is what to watch for, whether or not anyone intends it. The way out is the same either way: slow it down, and bring someone in.

## Individual Level

The person may begin to doubt whether their question is reasonable. Over time, they may soften their language, cut questions, and apologize for asking. They may find themselves reassuring the party they are questioning and then resenting it. They may lose energy for follow-up and carry a quiet worry that they are the one being unfair.

## Institutional Echo

Vendor relationships can operationalize this pattern through structure. Support ticket systems can route a question among queues so that no single person owns the answer. A first incident report that is issued quickly and updated later may be a legitimate holding statement, but it can also become the settled account. Account teams are typically measured on retention, which can create an incentive to reassure. Legal review and investigation confidentiality may genuinely restrict disclosure, and customers may not be able to tell the difference between restriction and avoidance. Contract notification terms may set specific timelines, and what they require needs qualified review. The pattern is more credible when partial disclosures arrive after pressure, later versions contradict earlier ones, and requests for method or evidence are refused without a reason.

## Civilizational Echo

The myth is that a good partner is one you do not need to check, and that asking for proof is an insult. Around it sits the idea that professionals handle things quietly and that transparency is a gift rather than a duty. The social value exploited is courtesy: our reluctance to press someone who seems tired, sincere or hurt. The language that makes it sound normal is "we take this very seriously," "we are working on it," and "I really hope you trust us." The public story is a responsible vendor and an understanding customer. The private loss is the customer's ability to know what happened to the people whose records they hold.

## Observable Indicators

1. Tickets about a possible incident remain unacknowledged or are redirected between queues.
2. A narrow answer is given to a broader question, and is described as a full answer.
3. Questions about scope or method are met with comments on the relationship or on the asker's tone.
4. A partial disclosure is offered after a deadline, a board date or a regulator is mentioned.
5. The partial disclosure is described as evidence of openness and is used to end further questions.
6. A flat assurance, such as "no data left the environment," is given with no supporting report.
7. A later version of a report or message contradicts or revises an earlier assurance.
8. A report is described as internal when its findings are being relied on in the reply.
9. The date range or the records affected in the vendor's report differ from the dates in your question.
10. The vendor's own hardship, workload or distress is raised in response to a specific request.

## Evidence To Preserve — Additions

- Version 1 of the incident report and every later version, with dates received.
- The complete support ticket thread, including timestamps, status changes and who responded.
- Your original written questions, numbered, and the date each was sent.
- A dated log of calls with the account team, written the same day, with one-line summaries.
- The contract and its security, notification and audit provisions, as signed.
- Your own system logs and alerts relevant to the same dates, from systems you are authorized to access.
- Internal escalation emails to your management, audit committee and counsel, with dates.

Plus the Universal Evidence list in the Sector Standards.

## False-Positive Check — Specific

Real incidents are confusing, early reports are often incomplete, and legal review commonly slows what a vendor can say. A vendor may also decline to share an internal report for genuine reasons. The discriminator is **whether the answers become more complete under written questions, or move on without ever answering them**. A good-faith vendor revises, acknowledges what is unknown and gives a date for the next update. This pattern leaves the same gaps in version two as in version one.

Other benign lookalikes:

- **An active investigation.** A vendor may truly not know yet.
- **Counsel-limited statements.** Cautious wording may reflect advice, not avoidance.
- **A fatigued team.** Exhaustion in an incident can be real and not a tactic.
- **A genuine second finding.** A newly discovered issue may be disclosed honestly.
- **A holding statement.** A first report may be accurate for what was known when it was written.

Concern strengthens when: partial disclosures come only after pressure from a board date or deadline; later versions contradict earlier assurances; requests for the method or the report are refused without a reason; and your own questions begin to be treated as a relationship problem.

Apply the Universal Benign Explanations and concern tests in the Sector Standards.

## Recognition Cue Cards

**SPOT IT — The Silence Test:**
Ask: "Which of my questions got an answer, and which were left unanswered?"
Concern rises if: the unanswered ones are consistently those about scope, dates and records.

**SPOT IT — The Narrow Answer Test:**
Ask: "Did they answer the question I asked, or an easier one?"
Concern rises if: "not aware of anything" is offered when I asked whether anyone had looked.

**SPOT IT — The Reassurance Test:**
Ask: "Am I the one comforting them?"
Concern rises if: I am apologizing for asking, or have started to reassure the party I am questioning.

**SPOT IT — The Small Admission Test:**
Ask: "Did a new fact arrive only when I mentioned a deadline, and was it then treated as the end of the matter?"
Concern rises if: yes, and the larger questions are said to have been answered.

## Chain Breakers

- **Put every question in writing,** numbered, with a response date, and keep it short and neutral.
- **Ask what has and has not been checked.** "Which logs have been reviewed, over which dates, by whom?"
- **Do not accept "no evidence" as "no event."** Ask what would be needed to find evidence.
- **Reread the contract's notification terms** with your counsel, and calendar any dates it sets.
- **Use a second channel** to a senior contact at the vendor, such as the security lead or an executive sponsor, in writing.
- **Send a same-day summary after every call,** and invite corrections.
- **Brief your own management and audit committee early,** with the facts and the gaps, and avoid softening them.
- **Preserve your own logs lawfully;** do not try to access the vendor's systems or anything you are not authorized to reach.

## Escalation Triggers — Specific

**LOW → MODERATE:** A ticket stays unanswered for longer than the contract's response terms; a narrow answer is given to a broad question; or a partial disclosure arrives and is described as complete.

**MODERATE → HIGH:** Version two contradicts a flat assurance; customer or employee data may be affected and you cannot confirm scope; the vendor refuses to share the method or the report; or you have a notification duty of your own and the answers are not enough to meet it. Consider your counsel, your audit committee or board, an independent forensic specialist, a data protection or financial services regulator where one has jurisdiction, and the contract's dispute process.

**HIGH → URGENT:** Signs of fraud in progress, extortion or a ransom demand, threats to you or colleagues, a risk to physical safety, or abuse of vulnerable people's data. Contact local emergency services or law enforcement and your counsel, and do not negotiate under threat. Do not confront anyone and do not delete evidence.

Tier definitions and sector bodies are in the Sector Standards.

## Safer Response Language

- "Thank you. To be sure I have it right, could you confirm in writing which dates and records the review covered?"
- "I understand the team is under strain. I still need a named owner and a date for the next update."
- "I am not asking whether you are being open. I am asking for the scope."
- "Does 'no evidence of misuse' mean it was checked and none was found, or that it has not yet been checked?"
- "Please send the method used to review the logs, or tell me in writing why it cannot be shared."
- "I will brief my audit committee on Thursday and I want to report accurately. What can you confirm by Wednesday?"

## Where Each Tactic Happened

| | Tactic | Scene | The moment |
|---|---|---|---|
| 1 | Stonewalling | The first week, your office | Your ticket sits unanswered, then is "forwarded to the relevant team" |
| 2 | Feigned Ignorance | The first week, your office | Told the team isn't aware of anything, with no sign anyone looked |
| 3 | Reverse Psychology | The first week, your office | You end up reassuring him that you do not distrust him |
| 4 | Limited Hangout | Two weeks later, your office | A second, smaller issue is volunteered while the scope stays unanswered |
| 5 | Lying | Two weeks later, your office | Told no customer data left, with the report kept internal |
| 6 | Competitive Victimhood | Two weeks later, your office | His tired team and hard month end your questions with an apology |

## Reflection

How many times have you asked the same question, and what is it costing you to keep apologizing for asking?
