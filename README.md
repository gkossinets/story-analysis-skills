# story-analysis-skills

Claude skills for story structure and scene analysis using the CREWS framework.

---

## crews-analysis

A close-reading framework for stories, screenplays, stage plays, novels, and films. CREWS tracks twelve dimensions across five headings (Characters, Relationships, Engine, Writing, Scene function), applied scene by scene, with a meta-question ("Who hired the CREWS?") asked of the work as a whole. The output is a Markdown analysis file suitable for editorial use, craft instruction, or feeding into the companion `crews-cards` skill for physical wall layout.

### What it does

Given a screenplay, stage play, story, novel chapter, or film, the skill:

1. Splits the work into scenes (or temporal orbits, for genuinely non-linear prose).
2. Applies twelve dimensions to each scene, surfacing only what is live; silent dimensions are signals about the scene, not gaps in the analysis.
3. Compiles cross-scene patterns: reveal/reversal rhythm; dangling causes; status and power arcs; mood arc; structural devices; tempo and density.
4. Steps back to a meta-section answering who the work is for; who its implied author is; what it argues; how its craft choices construct those positions; whether the storytelling apparatus is hidden or exposed (transparency).

Output is a single Markdown file per work, scannable as short labelled bullets rather than prose.

### The framework

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

(+ at the level of the work: who hired the CREWS?)
```

### Principles

- **Synthesis without hierarchy.** Twelve dimensions drawn from playwriting, screenwriting, fiction craft, and narrative theory; none privileged. The implied audience is not assumed to be Western or realist by default.
- **Pluralism on story shape.** Western conflict-climax, kishotenketsu, episodic, and spiralling structures are all in scope; the framework asks which shape fits the material, not which to impose.
- **Silent dimensions are signals.** A dimension that goes dormant in a scene is information about the scene, not a gap in the analysis. Bullets surface only what is live.
- **Pedagogical framing in the meta-section.** For each observation, identify the craft choice that produces the effect, not just the effect itself; avoid metaphorical restatement of the work in the analyst's own voice.
- **Conventional scene breaks where possible.** Temporal orbits are a fallback for genuinely non-linear prose (Krasznahorkai, late Bernhard, some Sebald), not a default.

### How to invoke

The skill triggers on phrases like "CREWS analysis," "scene analysis," "analyze this scene/screenplay/story," "break this into scenes," "apply the CREWS framework," and similar. It is explicitly not triggered by requests for scene cards or wall layouts; that work is handled by the companion `crews-cards` skill, which reads the file this skill produces.

**Output:** a `[source-stem]-crews-analysis.md` file in the same directory as the source.

### Sources and lineage

The framework is a synthesis; no single source covers all twelve dimensions. Each contributes some part of the apparatus:

- **David Ball**, *Backwards and Forwards*: stasis, intrusion, dominoes; the A→B→C movement; the reveal/reversal distinction.
- **James Thomas**, *Script Analysis for Actors, Directors, and Designers*: given circumstances; beats and units; tempo, rhythm, mood; character complexity; social status.
- **Damon Kiely**, *How to Read a Play*: active reading; dramatic action.
- **David Edgar**, *How Plays Work*: format and ritual; choreography of knowledge (via Michael Eaton).
- **Paul Gulino**, *Screenwriting: The Sequence Approach*: dangling causes and payoffs; dramatic irony; revelation and recognition; telegraphing; preparation by contrast.
- **Matthew Salesses**, *Craft in the Real World*: implied reader; audience expectations; kishotenketsu as alternative story shape; what is left out.
- **Linda Cowgill**, *Writing Short Films*: setup; inciting incident; plant and payoff; escalation.
- **Nancy Kress**, *Beginnings, Middles and Ends*: promises to the reader; dangling causes.
- **Michael Rabiger**, *Directing*: dramatic unit analysis; through-lines; character scene analysis; exposition checking.
- **N. J. Lowe**, *The Classical Plot and the Invention of Western Narrative*: story-world vs. primary-narrative; control level; forms of narrative power; transparency as a craft axis; postponement, screening, and misdirection as suspense modes.

---

## crews-cards

Converts a CREWS analysis Markdown file into printable scene cards for physical wall layout. This is a presentation layer over a file produced by `crews-analysis` — it does not perform original analysis.

### What it does

Two card formats:

- **Micro cards** (3×5 inches) — one compact card per scene, dense, for large wall layouts
- **Letter cards** (8.5×11 inches) — one expanded card per scene, one dimension per line, for close-up review

Each deck includes a cover card (from the Overview and "Who hired the CREWS?" sections) and a rhythm map card (from Cross-scene patterns) at the tail.

Optional PDF compilation via pandoc and typst using the bundled `compile.sh` script and typst preamble files in `crews-cards-skill/`.

### How to invoke

Trigger phrases: "card mode," "letter mode," "micro cards," "index cards," "3×5 cards," "one card per scene," "print the analysis as cards."

**Input:** an absolute path to a `*-crews-analysis.md` file produced by `crews-analysis`.

**Output:** `[stem]-cards.md`, and optionally `[stem]-cards-3x5.pdf` or `[stem]-cards-letter.pdf`.

---

## Workflow

Run `crews-analysis` first to produce the Markdown analysis file, then run `crews-cards` to compress it into printable cards.
