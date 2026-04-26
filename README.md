# story-analysis-skills

Claude skills for story structure and scene analysis using the CREWS framework.

## Skills

### crews-analysis

Analyzes a scene, chapter, passage, or whole work from a story, screenplay, stage play, novel, or film using the CREWS framework and produces a full-form Markdown analysis file.

**CREWS** tracks twelve dimensions grouped under five headings:

- **C** — Characters present and complexity revealed
- **R** — Relationships and social texture (status, subtext, format/ritual)
- **E** — Engine: circumstances, objectives (A→B→C), stakes, choreography of knowledge, dangling causes
- **W** — Writing: perspective, information management, mood
- **S** — Scene function and key changes

After the scene pass the skill compiles cross-scene patterns (reveal/reversal rhythm, dangling cause map, status arcs, mood arc) and answers the meta-question "Who hired the CREWS?" — implied reader, implied author, tone, message, and story shape.

**Trigger phrases:** "CREWS analysis," "analyze this scene," "break this into scenes," "apply the CREWS framework," or any request to examine narrative structure, character dynamics, dramatic engine, craft choices, or scene function.

**Output:** a `[source-stem]-crews-analysis.md` file in the same directory as the source.

---

### crews-cards

Converts a CREWS analysis Markdown file into printable scene cards for physical wall layout. This is a presentation layer over a file produced by `crews-analysis` — it does not perform original analysis.

Two formats:

- **Micro cards** (3×5 inches) — one compact card per scene, dense, for large wall layouts
- **Letter cards** (8.5×11 inches) — one expanded card per scene, one dimension per line, for close-up review

Each deck includes a cover card (from the Overview and "Who hired the CREWS?" sections) and a rhythm map card (from Cross-scene patterns) at the tail.

Optional PDF compilation via pandoc and typst using the bundled `compile.sh` script and typst preamble files.

**Trigger phrases:** "card mode," "letter mode," "micro cards," "index cards," "3×5 cards," "one card per scene," "print the analysis as cards."

**Input:** an absolute path to a `*-crews-analysis.md` file produced by `crews-analysis`.

**Output:** `[stem]-cards.md`, and optionally `[stem]-cards-3x5.pdf` or `[stem]-cards-letter.pdf`.

---

## Workflow

Run `crews-analysis` first to produce the Markdown analysis file, then run `crews-cards` to compress it into printable cards.
