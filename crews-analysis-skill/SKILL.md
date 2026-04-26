---
name: crews-analysis
description: Use this skill when the user asks to analyze a scene, chapter, passage, or whole work from a story, screenplay, stage play, novel, or film using the CREWS framework and wants the output as a full-form Markdown analysis file. Trigger on phrases like "CREWS analysis," "scene analysis," "analyze this scene," "break this into scenes," "apply the CREWS framework," "analyze this screenplay/story," or any request to systematically examine narrative structure, character dynamics, dramatic engine, craft choices, or scene function. Also trigger when the user asks to identify scene breaks, track changes across scenes, or do a cross-scene pattern analysis. Do NOT trigger for requests to produce scene cards, index cards, letter cards, "card mode," or physical-wall layouts — that is the crews-cards skill, which reads the Markdown file this skill produces.
---

# CREWS analysis: scene-by-scene framework

## Overview

CREWS is a scene-by-scene analysis framework for stories, screenplays, stage plays, and films. It tracks twelve dimensions grouped under five headings, plus a meta-question. The mnemonic is **CREWS** (Characters, Relationships, Engine, Writing, Scene function); the meta-question is **"Who hired the CREWS?"**

This skill produces a **full-form Markdown analysis file** intended to be both useful as a standalone close reading and as input to the companion `crews-cards` skill, which compresses the analysis into printable scene cards. Keep the two tasks separate: do not attempt to produce cards from this skill.

The framework synthesises principles from:

- **David Ball**, *Backwards and Forwards* — stasis, intrusion, dominoes
- **James Thomas**, *Script Analysis for Actors, Directors, and Designers* — given circumstances, beats/units/scenes, tempo/rhythm/mood, character complexity, social status
- **Damon Kiely**, *How to Read a Play* — active reading, dramatic action
- **David Edgar**, *How Plays Work* — format and ritual, choreography of knowledge (via Michael Eaton)
- **Paul Gulino**, *Screenwriting: The Sequence Approach* — dangling causes and payoffs, dramatic irony, revelation and recognition, telegraphing, preparation by contrast
- **Matthew Salesses**, *Craft in the Real World* — implied reader, audience expectations, cultural assumptions, kishotenketsu as alternative story shape, what is left out
- **Linda Cowgill**, *Writing Short Films* — setup, inciting incident, rising action, plant and payoff
- **Nancy Kress**, *Beginnings, Middles and Ends* — promises to the reader, dangling causes
- **Michael Rabiger**, *Directing* — dramatic unit analysis, through-lines, character scene analysis, exposition checking
- **N. J. Lowe**, *The Classical Plot and the Invention of Western Narrative* — story-world vs. primary-narrative; control level; forms of narrative power; transparency as a craft axis; postponement, screening, and misdirection as suspense modes

---

## How to run the analysis

### Step 1: confirm scope and output path

Before beginning, confirm with the user:

- **Source:** which file or text is being analysed
- **Scope:** full work (default); a named act, sequence, or chapter; or a single scene
- **Output path:** where to save the Markdown file. Default is the same directory as the source, with filename `[source-stem]-crews-analysis.md`. If the source is not a local file (e.g., a pasted text or a film being viewed), ask for a project directory

### Step 2: split into scenes

Break the text into scenes based on changes in:

- Location (interior/exterior, specific place)
- Time (continuous action vs. jump; flashback; flash-forward)
- Character configuration (French scenes: who enters or exits)

**Prefer conventional scene breakdown.** Flashbacks, flash-forwards, intercut sequences, and dream sequences are all conventional scene structures; a jump in time or place is a scene break, not an orbit. Number scenes sequentially in the order they appear in the text (reading order, not chronological story order), regardless of internal time movement. If the work uses explicit act or sequence breaks, record them between scenes; do not renumber across breaks.

**Temporal orbits** are a fallback only for genuinely non-linear prose — stream of consciousness, spiralling narration, associative digression that cannot be cleanly segmented (e.g., Krasznahorkai, late Bernhard, some Sebald). If the text admits a scene structure at all, use scenes. Mark an orbit with `[orbit]` after its number only when scene segmentation would distort the material.

### Step 3: apply CREWS to each scene

For each scene, work through the five headings and twelve dimensions. Omit any dimension that is not live in a given scene — a silent dimension is a signal about the scene, not a gap in analysis.

**Scannability rules.** The output must read quickly on the page:

- Prefer bullet lists to multi-sentence paragraphs
- One idea per bullet; one clause or short sentence per idea
- Use inline labels (`Status:`, `Subtext:`) to anchor bullets where a heading covers more than one dimension
- No more than two or three bullets per dimension unless the scene genuinely demands it
- Target 20 to 30 rendered lines per scene; scenes consistently longer than 40 lines should be tightened
- **Separate adjacent bold-label lines with a blank line.** Standard Markdown collapses single newlines, so `**Present:** ...` followed by `**Action:** ...` on the next line renders as one run-on paragraph in most editors and in Google Docs. Always insert a blank line between two consecutive bold-label lines (e.g., between `**Premise:**` and `**Implied reader:**`, or between `**Present:**` and `**Action:**`). Bulleted lists do not need this treatment — bullets already separate visually

### Step 4: cross-scene patterns

After the scene pass, compile the patterns that only become visible across the whole work:

- **Reveal/reversal rhythm:** classify each scene's primary movement as a reveal (the audience or a character learns something unexpected) or a reversal (the terms of the situation are fundamentally changed); map the sequence. Long runs of reveals without a reversal may feel flat; clustered reversals may feel melodramatic. A particularly potent structural move is the deliberate **non-reversal**: a place where the audience expects a reversal (final confrontation, climactic revelation, defeat) but encounters its absence. Mark these explicitly when present; they often sit where a conventional climax would be expected.
- **Dangling cause map:** plants and payoffs, matched by scene number; list anything unresolved separately.
- **Status and power arcs:** for each major character, the trajectory of status and form of narrative power across the work; note any significant conversions of power.
- **Mood arc:** how atmosphere shifts across the whole piece.
- **Structural devices:** recurring objects, repeated formats, motifs.
- **Tempo and density:** which scenes are dense, which are sparse, where the pace breaks.

### Step 5: who hired the CREWS?

Step back from the scene-level work and answer the meta-questions below. Two rules govern this section:

1. **Pedagogical framing.** The reader of this analysis wants to understand how the story is built and what it is designed to do. For each observation, identify the craft choices that produce the effect, not just the effect itself.
2. **No florid restatement.** Avoid metaphor-making in the analysis's own voice. Flowery formulations — the source's metaphors paraphrased into your prose, cute compound phrases, imagistic plot summary — are restatement, not analysis. State positions plainly; cite mechanisms by name.

The fields:

- **Implied reader:** who is the work for? What cultural, historical, or literary knowledge does it assume? What expectations does it engage, fulfil, violate, or invert? What is left out, and what does that omission tell you about whom the work addresses?
- **Implied author:** what moral, ideological, or emotional position does the story construct through its craft choices? Following Salesses: the implied author is distinct from both the narrator and the real author; it is the persona the text's choices imply, and may differ from the stance the narrator appears to hold. Is the implied author affectionate, ironic, satirical, elegiac, righteous, pessimistic, hopeful, contemptuous, ambivalent, reverent? What is its stance toward the characters, toward the world depicted, toward the implied reader?
- **Tone:** how is the story oriented toward its material? Ironic, pessimistic, inspiring, tragic, comic, mystical, satirical, clinical, campy, elegiac, deadpan, etc. Name the tone plainly; note any significant tonal shifts across the work.
- **Message or intended effect:** what (if anything) is the story arguing, asserting, or asking? What is the implied reader meant to know, feel, see, or recognise by the end that they did not at the start? If the story's moral position is genuinely ambiguous or suspended, say so — deliberate ambiguity is a craft position, not an absence.
- **Craft choices that construct these positions:** two or three specific devices that do the work. For each, follow a three-move template: (1) name the choice, (2) state what it does structurally, (3) connect it to the larger stance. Devices worth considering: distribution of knowledge between narrator, characters, and reader; what is withheld and for how long; the shape of the arc (conventional climax vs. deliberate non-reversal); perspective and focalisation; selection of what is told vs. dramatised; formats and rituals the story inhabits or subverts; tempo and density choices. This is where the analysis becomes most pedagogical.
- **Transparency:** is the storytelling apparatus hidden, or exposed as part of the work's argument? When transparency is in force, two technical tests apply: do outcomes follow from existing setup (no deus ex machina); are game elements planted before use, not produced when needed? When the apparatus is deliberately exposed (visible authorial hand, direct address, archival juxtaposition that breaks the fictive frame, formal patterning that proclaims itself), is the exposure purposeful?
- **Story shape:** Western conflict-climax arc, kishotenketsu (introduction, development, twist, reconciliation), episodic, spiralling, or some other shape. Note any tension between the shape the material suggests and the shape the implied reader might expect. The framework does not privilege one tradition over another.

Keep each answer tight — roughly two to four sentences per field, and craft-choice bullets to a line or two each. Brevity and pedagogical clarity over completeness.

---

## Output file structure

Write a single Markdown file using exactly the heading structure below. The `crews-cards` skill depends on these H2 and H3 headings to parse the file reliably, so do not deviate. Dimensions inside a scene use bold inline dividers, not H4 headings.

```markdown
# CREWS analysis: [Title] by [Author]

## Overview

**Premise:** [one sentence]

**Characters:**
- [Name] — [role or function]; wants [super-objective]; gets [outcome] (→ [transforms, if applicable])
- [Name] — [role or function]; wants [super-objective]; gets [outcome]
- ...

**Implied reader:** [who this is for; assumed cultural conventions — one phrase]

**Implied author:** [moral, ideological, or emotional stance — one phrase]

**Tone:** [register — one phrase; e.g., ironic-elegiac, satirical, deadpan, tragic]

**Story shape:** [Western three-act | kishotenketsu | episodic | other]

**Key motifs:** [recurring images, objects, phrases]

**Formats used:** [trials, rituals, ceremonies, checkpoints, etc.]

**Control level:** [agencies that direct events without being themselves directly affected (gods, fate, the state, bureaucracy, surveillance, the algorithm, market forces, ideology); articulate or implicit; omit if absent]

**Intended effect:** [what the reader is meant to know, feel, or recognise by the end — one sentence]

## Scene-by-scene

### Scene 01 — [Location, time, weather if relevant]

**Present:** [Characters physically present]

**Action:** [One-sentence summary of what happens and what changes]

**Characters**
- [Bullet per character about complexity revealed, entrances, exits]

**Relationships**
- Status: [power dynamics; shifts if any]
- Subtext: [gap between surface and interior, if live]
- Format/ritual: [social structure of the scene, if notable]

**Engine**
- Circumstances: [given circumstances; stasis and intrusion]
- A→B→C: [wants] → [gets] ([reveal | reversal]) → [transforms, if applicable]
- Stakes: [what is at risk; whether they rise or lower]
- Knowledge: [who knows what; dramatic irony, if live]
- Plants ↓: [dangling causes introduced]
- Payoffs ↑: [earlier plants closed]

**Writing**
- Perspective: [POV, psychic distance]
- Information: [what is delivered, withheld, how; exposition technique]
- Mood: [emotional weather; atmosphere]

**Scene function**
- Function: [setup | inciting | rising | twist | climax | release | bridge | reconciliation]
- What changes: [first-moment vs. last-moment state]
- Compelling because: [why the scene earns its place in its own right]

### Scene 02 — ...

[And so on, with `── Act II ──` or `── Sequence 3 ──` style dividers between major structural units as needed.]

## Cross-scene patterns

**Reveal/reversal rhythm:**
- 01 — [scene reference]: **setup**
- 02 — [scene reference]: **reveal** ([what is revealed])
- 03 — [scene reference]: **reveal** ([what is revealed])
- 08 — [scene reference]: **reversal** ([what is reversed])
- 11 — [scene reference]: **non-reversal** ([the expected reversal that is absent])
- ...

[Short paragraph or bullet list of rhythm observations: flag long runs of reveals without a reversal; clustered R's that risk melodrama; deliberate non-reversals where a reversal was expected.]

**Dangling cause map:**
- ↓ [cause] (03) → ↑ [payoff] (17)
- ↓ [cause] (05) → ↑ [payoff] (11)

**Unresolved:**
- [dangling causes never paid off]

**Status and power arcs:**
- [Character]: [start status; form of power held] → [end status; form of power held] via scenes [NN, NN, NN]; note significant conversions

**Mood arc:**
- [bullets tracking atmospheric movement across the work]

**Structural devices:**
- [recurring objects, motifs, formats]

## Who hired the CREWS?

**Implied reader:** [fuller discussion of who the work is for; cultural and literary knowledge assumed; expectations engaged, met, or violated; what is left out and what that omission signals — two to four sentences]

**Implied author:** [the persona the craft choices construct — moral, ideological, or emotional stance; relation to the narrator; stance toward characters and reader — two to four sentences]

**Tone:** [one or two phrases naming the register; note any significant shifts]

**Message or intended effect:** [what the story argues, asserts, or asks; what the implied reader is meant to know, feel, or recognise by the end — two to four sentences. If the position is deliberately ambiguous, say so]

**Craft choices that construct these positions:**
- [Choice]: [what it does structurally]; [connection to the larger stance]
- [Choice]: [what it does structurally]; [connection to the larger stance]
- [Choice]: [what it does structurally]; [connection to the larger stance]

**Transparency:** [hidden | exposed | mixed]. [Brief note on whether the apparatus is foregrounded as part of the argument, and any explicit violations of "outcomes from setup" or "elements planted before use."]

**Story shape:** [Western conflict-climax arc | kishotenketsu | episodic | spiralling | other]. [Brief note on any tension between the shape the material suggests and the shape the implied reader might expect.]
```

Omit any section or bullet that is not live. A sparse analysis file is a signal about the work, not a failure of analysis.

---

## The twelve dimensions (reference)

### C — Characters

**1. Characters present and complexity revealed.** Who enters, exits, is present? What do we learn about them in this scene? Are they a type (single dominant trait), intermediate (limited self-awareness), or complex (intensely conscious of their circumstances)? What new facets are shown through action, speech, or reaction? How does an entrance or exit change the scene's dynamics?

Sources: Thomas (character types); Ball (characters as forces); Rabiger (character scene analysis questions).

### R — Relationships and social texture

**2. Status and power dynamics.** Who holds power, who defers, who resists? Do status positions shift during the scene? Is structural power (rank, money, role) aligned with or opposed to interpersonal power (wit, information, will)? What are the rewards for conformity and penalties for violation?

Sources: Thomas (social status, willpower, values); Edgar (office vs. rank vs. character); Rabiger (authority, volition, competence).

**3. Subtext.** What do characters think or feel but not say? Where is the gap between surface behaviour and interior state? Where is the gap widest? How does subtext create tension or irony?

Sources: Rabiger (subtext extraction, dramatic beats); Thomas (internal action in dialogue); Salesses (inside/outside story).

**4. Format and ritual.** What is the social structure of the scene (a trial, a ceremony, a negotiation, a dinner, a checkpoint procedure, a sales pitch, a lesson)? What are its built-in rules, roles, and expected behaviours? Where do characters conform to or violate the format? If a control level is operating in the work, is the scene's format one of its instruments?

Sources: Edgar (formats borrowed from life); Thomas (given circumstances as social context).

### E — Engine (what drives the scene forward)

**5. Circumstances, stasis, and intrusion.** What are the given circumstances (time, place, weather, objects, social conditions)? What is the equilibrium at the scene's start? Is it disturbed? By what? What was stable before the change, and how does that clarify the dramatic weight of the change? What is in the story-world but outside the primary narrative (backstory, offstage events, simultaneous action elsewhere)?

Sources: Ball (stasis, intrusion, battle for new stasis); Thomas (given circumstances — geography, society, economics, politics, culture, spirituality); Lowe (story-world vs. primary-narrative distinction).

**6. Objectives and the A→B→C pattern.** What does each character want, in this scene and longer-term? Do objectives shift during the scene? Is there a gap between stated and actual objectives? Is there a clear "go for A, get B" movement — a character pursues A and encounters something unexpected (B), as either a reveal (the situation is not what it appeared) or a reversal (the terms have fundamentally changed)? In the strongest scenes, B provokes a further transformation (C): the character adapts, decides, or changes in response, within the same scene. A→B scenes move the story forward; A→B→C scenes are where characters grow.

Sources: Thomas (super-objectives, through-action); Rabiger (moment-by-moment objectives); Cowgill (protagonist goal, inciting incident); Ball (dominoes; A→B→C; reveals and reversals).

**7. Stakes.** What is at risk? Do the stakes rise or lower? Are they material, emotional, moral, or existential? Are the stakes the same for all characters, or do different characters experience different stakes in the same situation? What forms of power are in play (information, moral position, instrumental, social, positional), and does any of it shift form?

Sources: Cowgill (escalation of tension); Gulino (hope vs. fear); Kress (promises and consequences); Lowe (forms of narrative power).

**8. Choreography of knowledge and dramatic irony.** Who knows what? Does the audience know more than the characters (dramatic irony), or less? Are there scenes of revelation (audience learns something a character doesn't) or recognition (character catches up to what the audience already knew)? How does the distribution of knowledge create tension, comedy, or suspense?

Sources: Edgar ("choreography of knowledge" via Michael Eaton); Gulino (ironic tension, revelation and recognition, hierarchies of knowledge); Ball (exposition technique); Salesses (what is left out and for whom).

**9. Dangling causes and payoffs.** What promises, threats, predictions, expressions of intent or fear are planted? What earlier plants are paid off? A dangling cause is any expression of intent, warning, threat, hope, fear, or prediction for which no immediate answer is provided; it thrusts audience attention into the future.

Sources: Gulino (dangling causes, dialogue hooks, telegraphing, preparation by contrast, motifs); Kress (promises to the reader); Cowgill (plant and payoff).

### W — Writing (craft and narration)

**10. Perspective and narration.** Whose scene is it? What is the POV and does it shift? How tight is the psychic distance? Is there a gap between a narrating self and an experiencing self (as in retrospective first person)? How does the perspective choice shape what the audience can and cannot know?

Sources: Salesses (implied author, POV as cultural choice); Rabiger (whose scene is it? how tight is perspective?).

**11. Information management.** What new information is delivered, and how (through action, dialogue, objects, dramatic irony, voiceover, flashback)? What is withheld, and by what mechanism (postponement, where the audience waits for a known outcome; screening, where the viewpoint blocks information the audience knows must exist; misdirection, where information is on the board but mis-flagged)? How dense is the scene informationally, and how fast does it move? Is exposition organic or awkward? Does the scene assume its reader already knows certain things?

Combines exposition technique, tempo, and information density.

Sources: Ball (exposition relevant to action); Thomas (tempo); Rabiger (checking exposition); Salesses (context for the implied audience); Lowe (modes of withholding information).

**12. Mood and atmosphere.** What is the emotional weather of the scene? Character mood is interior (a state of mind or feeling). Scene atmosphere is generated externally (by setting, light, sound, objects, time of day, weather). Do mood and atmosphere reinforce or counterpoint each other?

Sources: Thomas (mood vs. atmosphere); Rabiger (rhythmic design, emotional ebbs and flows).

### S — Scene function and key changes

For each scene, a brief summary answering:

- What is the scene's role in the larger structure (setup, inciting incident, escalation, reversal, climax, resolution — or, in kishotenketsu terms: introduction, development, twist, reconciliation)?
- What has changed between the scene's first moment and its last — in situation, in relationships, in what the audience knows, in how the audience feels?
- **Why is this scene compelling to watch (or read) in its own right?** Beyond its structural role, what makes it interesting as a self-contained experience? What generates the humour, tension, dread, or delight? This is an evaluative check, not just an analytical one; it catches scenes that serve a plot function but fail to earn the audience's attention on their own terms. Especially important for small connective scenes that writers tend to underserve.

---

## Adapting CREWS to different forms

**Screenplays and stage plays.** Scene breaks are usually explicit (sluglines, act/scene divisions, French scenes). The framework applies directly.

**Conventional prose fiction.** Break chapters into scenes at changes of location, time, or character configuration. Interior monologue maps to subtext; narrative summary maps to information management.

**Unconventional or non-linear prose.** Use temporal orbits rather than scenes only when the text genuinely resists segmentation. Track which timeframes or locations the narration circles back to, and treat each orbit as a unit of analysis. Note that the narration's movement between orbits is itself a craft choice worth examining under Writing.

**Film (viewing).** Scene breaks follow cuts or transitions. Add attention to visual and sonic dimensions under Mood/atmosphere (lighting, colour, sound design, music) and under Format (how the camera's position creates or disrupts the social structure of the scene).

**Short forms (poems, flash fiction).** The framework may be too granular. Consider applying only the five headings (C, R, E, W, S) without breaking into twelve subdimensions.

---

## Quick reference

```
C  Characters
   1. Characters present and complexity revealed

R  Relationships and social texture
   2. Status and power dynamics
   3. Subtext
   4. Format and ritual

E  Engine
   5. Circumstances, stasis, and intrusion
   6. Objectives and the A→B→C pattern
   7. Stakes
   8. Choreography of knowledge and dramatic irony
   9. Dangling causes and payoffs

W  Writing
  10. Perspective and narration
  11. Information management
  12. Mood and atmosphere

S  Scene function and key changes
   — Why is this scene compelling to watch?
   (+ periodically: who hired the CREWS?)
```

---

## Handoff to crews-cards

When the analysis is complete, tell the user the output file path and note that the `crews-cards` skill can convert the file into 3×5 index cards or letter-size cards for wall layout, with optional PDF compilation via pandoc and typst.
