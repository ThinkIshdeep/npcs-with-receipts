# Synopsis — NPCs With Receipts

**Ishdeep Singh · 12 November 2026**

## V2 interface release

An illustrated social town.

- Selectable residents in a spatial town and portrait strip
- Private memory dossiers distinguish direct observations and rumours
- Borrowing, repayment and helping update the coin and trust ledgers
- Day progression, sourced gossip and lexical memory search

Dialogue is authored and rule-based. No LLM is hidden behind the characters. The underlying domain scope and research-extension boundaries below remain explicit.

## Implemented release

Runnable source: `lab/npcs.py`. Interface and backend are included. Tests and benchmark outputs accompany this distribution.

## Limits of the implemented release

Structured rule-based social agents and TF-IDF memory retrieval. No language-model dialogue or human believability study.

## Measured evaluation

```json
{
  "checks": {
    "private_observation": true,
    "one_hop_rumour": true,
    "distant_character_unaware": true,
    "coin_conservation": true,
    "debt_repaid": true
  },
  "note": "Deterministic world invariants; believability requires a human study."
}
```

## Original specification and proposed extensions

The material below preserves the design ambitions. Future-tense features and anticipated challenges are not completed-development claims.

NPCs With Receipts

**Tagline:** The shopkeeper remembers. Unfortunately, so does his entire friend group.

### Concept, problem, and users

This is a small playable town whose characters maintain goals, relationships, memories, and beliefs. Ordinary scripted characters often reset social context or know events they never witnessed. Here, every important action should have a traceable source and a consequence consistent with the game world.

The target audience is game developers, agent researchers, and players interested in emergent stories. The central comparison is structured social memory versus a long conversation history with no explicit knowledge model.

### Proposed product and workflow

The player borrows, trades, helps, lies, and returns to the same characters later. NPCs keep schedules, manage limited resources, and share rumours. A developer inspector exposes remembered events, current beliefs, relationship changes, and selected actions. Replay branches show how a different choice changes the town.

Start with three characters and one shop, then expand toward eight to twelve characters. Screens: playable town, dialogue panel, social graph, character inspector, event timeline, and replay comparison. The personality layer changes wording; the world engine decides which actions are legal.

### Data and system design

Separate objective world events from each character's beliefs. Suggested records are `WorldEvent`, `Observation`, `Memory`, `Belief`, `Relationship`, `Goal`, and `ActionProposal`. A memory carries an observer, source, timestamp, confidence, and links to supporting events. A rumour can be believed without becoming objective truth.

Synthetic interaction scripts provide reproducible tests. Human ratings of consistency and believability are a later consented study. Hold out event sequences and character combinations; do not evaluate only on the exact scripted demonstrations used during development.

### Algorithms and experiments

Baseline: scripted dialogue and a short recent-event buffer. Advanced version: relevance-and-recency memory retrieval, structured belief updates, and hierarchical planning over explicit actions. A language model may propose dialogue or intentions, while validators enforce inventory, money, location, and observation permissions.

Proposed decision cycle: update observations; retrieve relevant memories; propose a legal goal-directed action; validate preconditions; execute; write the resulting event. If a proposal fails validation, record the reason and choose a fallback action. Never allow generated text alone to create money or teleport a character.

Evaluate event-recall accuracy, unsupported-knowledge rate, illegal-action rate, goal completion, and blinded consistency ratings. Ask questions whose answer depends on who observed an event. Ablate provenance, decay, and trust-weighted rumours separately. A seeded replay should reproduce world transitions even if optional dialogue wording varies.

### Anticipated problems, in my voice

| What could go wrong | My likely reaction | Engineering response |
|---|---|---|
| Every NPC immediately knows a private event | “The whole town has premium CCTV inside its brain.” | Enforce observation boundaries and rumour paths |
| A character pays with money it does not own | “Financial planning by pure confidence.” | Authoritative resource ledger and action validation |
| Old rumours overpower corrected facts | “The correction got two views. The gossip got a sequel.” | Track source reliability and explicit belief revision |

### Demo, milestones, and limits

Demo: borrow from one NPC, let a second hear a rumour, and inspect why a third changes its behaviour. Then repay the debt and compare propagation of the correction. Milestones: legal world actions; persistent memory; belief boundaries; social propagation; replay study. The deliverable is a bounded social simulation, not evidence of human-like consciousness or unrestricted autonomous agents.




## Problems actually encountered during the makeover

| The problem | In my voice | What changed |
|---|---|---|
| Sample B overwrote the file used by sample A | “Bro, this is an A/B test, why did B steal A’s identity?” | Recordings now get unique file names; a regression test checks both files remain distinct and unchanged. |
| A duplicate highlight followed row positions instead of duplicate evidence | “Apparently every third row had been arrested on vibes.” | Duplicate highlights now use exact record content and jump to a real duplicate. |
| The table displayed a rounded number that search did not match | “I copied the number from your own screen, my guy.” | Search checks both raw values and the formatted values visible in the table. |
| Graph labels became tiny on a phone | “Causal inference, now available to ants.” | Graph workspaces keep readable node widths and scroll within their own viewport. |
| Robot movement and the play button disagreed about whether it was running | “Gordon left the parking spot while the button was still contemplating life.” | The live flag is synchronized after accepted commands and remains off after rejected commands. |
| Fast screenshots caught an interface between renders | “The UI took a smoke break precisely when the camera arrived.” | Captures were inspected, incomplete frames replaced, and videos labelled as edited screenshots. |

These are observed build issues. Proposed research challenges in the original specifications remain proposed; this log does not invent months of model training or real deployments.
