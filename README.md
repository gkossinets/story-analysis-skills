# story-analysis-skills

Two Claude skills for close reading of stories, screenplays, plays, novels and films with the **CREWS** framework, and for turning the analysis into printable scene cards for a wall.

- **`crews-analysis`** breaks a work into scenes and analyses each one across twelve dimensions, then steps back to ask what the whole work is built to do. Output: one Markdown file.
- **`crews-cards`** compresses that file into scene cards (3×5 index cards or letter pages) and renders a print-ready PDF. Output: Markdown plus PDF.

Neither skill needs pandoc, typst or LaTeX. The card PDFs are made by a small bundled Python script whose only dependency is reportlab (already present in Claude's code sandbox on claude.ai; `pip install reportlab` elsewhere). Without reportlab, the script writes a printable HTML file instead.

**See it working:** [`examples/gift-of-the-magi/`](examples/gift-of-the-magi/) runs both skills on O. Henry's "The Gift of the Magi" (public domain), with the source text, the scene-list checkpoint, the full analysis, and both card decks as Markdown and PDF.

---

## Install

### Claude (web, desktop, mobile)

Skills work on all Claude plans, including Free.

1. Make sure code execution is enabled (**Settings → Capabilities**; it may be labelled "Code execution and file creation" or "Create and edit files"). On Team and Enterprise plans an owner controls this, and whether members may upload skills, under **Organization settings → Plugins & skills**.
2. Download `crews-analysis.zip` and `crews-cards.zip` from the [latest release](https://github.com/gkossinets/story-analysis-skills/releases/latest), or build them from a clone with `make` (they land in `dist/`). Each zip has the skill folder itself as its top level, which the uploader requires.
3. Go to **Customize → Skills**, choose **+ → Create skill → Upload a skill**, and upload each zip.
4. Toggle each skill on; uploaded skills are not enabled automatically.

Skills enabled in your Claude account also load in Claude Code when you sign in with the same account.

### Claude Code (local)

Copy or symlink the two folders into your personal skills directory:

```bash
git clone https://github.com/gkossinets/story-analysis-skills.git
mkdir -p ~/.claude/skills
ln -s "$PWD/story-analysis-skills/crews-analysis" ~/.claude/skills/crews-analysis
ln -s "$PWD/story-analysis-skills/crews-cards"    ~/.claude/skills/crews-cards
pip install reportlab   # for card PDFs; optional (HTML fallback otherwise)
```

Keep the folder names as they are: each must match the `name` in its `SKILL.md`.

---

## Use

1. **Analyse.** Give Claude a story, screenplay or chapter (attach it, paste it, or point to a file) and ask for a *CREWS analysis*. Claude first proposes a scene list and a cast list and waits for you to confirm or adjust the breakdown; say "proceed," or ask it to split, merge or rename. It then writes `[title]-crews-analysis.md`.
2. **Make cards.** Ask for *micro cards* (3×5) or *letter cards*. Claude writes the cards Markdown, renders the PDF at one consistent type size, and tightens any scene card that runs past one card (the cover and rhythm map may take several). For 3×5 cards you can have one card per page (for printers that take index cards) or four per sheet of letter or A4 paper with cut lines. Cards print at 8pt (3×5) or 11pt (letter) by default; ask for *large print* to get 10pt and 12pt.

You can also run the renderer yourself:

```bash
python3 crews-cards/scripts/make_cards.py my-story-cards-3x5.md --format 3x5
python3 crews-cards/scripts/make_cards.py my-story-cards-3x5.md --format 3x5-sheet --paper a4
python3 crews-cards/scripts/make_cards.py my-story-cards-letter.md --format letter
python3 crews-cards/scripts/make_cards.py my-story-cards-letter.md --format letter --html
python3 crews-cards/scripts/make_cards.py my-story-cards-3x5.md --format 3x5 --large      # 10pt; or --size 9
```

---

## The framework

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

Given a work, `crews-analysis`:

1. Splits it into scenes (or, for genuinely non-linear prose, temporal orbits), with a cast list of canonical names and aliases, and stops for your review.
2. Applies the twelve dimensions to each scene, reporting only those that are live; a silent dimension is a signal about the scene, not a gap in the analysis.
3. Compiles cross-scene patterns: reveal/reversal rhythm (including deliberate non-reversals); suspense modes; the dangling-cause map; status and power arcs; mood arc; structural devices; tempo.
4. Answers the meta-question, *who hired the CREWS?*: implied reader, implied author, tone, intended effect, the craft choices that produce them, transparency of the storytelling apparatus, and story shape.

The output is scannable labelled bullets, not essay prose.

### Principles

- **Synthesis without hierarchy.** The dimensions are drawn from playwriting, screenwriting, fiction craft and narrative theory, and none is privileged. The implied audience is not assumed to be Western or realist by default.
- **Pluralism on story shape.** Conflict-climax, kishotenketsu, episodic and spiralling structures are all in scope; the framework asks which shape fits the material rather than imposing one.
- **Silent dimensions are signals.** Bullets surface only what is live in a scene.
- **Mechanisms, not restatement.** In the meta-section every observation names the craft choice that produces an effect, and the analysis avoids paraphrasing the work's own metaphors back at it.
- **Conventional scene breaks where possible.** Temporal orbits are a fallback for prose that resists segmentation (Krasznahorkai, late Bernhard, some Sebald), not a default.

### Card formats

- **Micro cards (3×5 in):** heading, characters present, one-line action, A→B→C, function, plants ↓ and payoffs ↑, mood, and a hook (why the scene is compelling in its own right). Dense, for laying out a whole work on a wall.
- **Letter cards (8.5×11 in or A4):** one dimension per line, for close review of individual scenes.
- Every deck opens with a **cover card** (premise, structural characters, implied reader and author, shape, motifs, control level, intended effect) and a **key card** explaining the symbols, and closes with a **rhythm map** (the reveal/reversal string, suspense, dangling-cause map, power and mood arcs).

**[Reading the cards](docs/reading-the-cards.md)** explains every field and symbol (A→B→C, reveal/reversal/non-reversal, ↓ plants and ↑ payoffs, function, mood, hook, the rhythm map) with examples from the demo, plus some notes on working with a deck on a wall.

---

## Sources and lineage

The framework is a synthesis; no single source covers all twelve dimensions. [Design notes](docs/crews-design-notes.md) map each dimension to its sources and record how testing on real texts shaped the framework.

- **David Ball**, *Backwards and Forwards*: stasis, intrusion, dominoes; the reveal/reversal distinction.
- **James Thomas**, *Script Analysis for Actors, Directors, and Designers*: given circumstances; beats and units; tempo, rhythm, mood; character complexity; social status.
- **Damon Kiely**, *How to Read a Play*: active reading; dramatic action.
- **David Edgar**, *How Plays Work*: format and ritual; choreography of knowledge (via Michael Eaton).
- **Paul Gulino**, *Screenwriting: The Sequence Approach*: dangling causes and payoffs; dramatic irony; revelation and recognition; telegraphing; preparation by contrast.
- **Matthew Salesses**, *Craft in the Real World*: implied reader; audience expectations; kishotenketsu as an alternative story shape; what is left out.
- **Linda Cowgill**, *Writing Short Films*: setup; inciting incident; plant and payoff; escalation.
- **Nancy Kress**, *Beginnings, Middles and Ends*: promises to the reader; dangling causes.
- **Michael Rabiger**, *Directing*: dramatic unit analysis; through-lines; character scene analysis; exposition checking.
- **N. J. Lowe**, *The Classical Plot and the Invention of Western Narrative*: story-world vs. primary narrative; control level; forms of narrative power; transparency as a craft axis; postponement, screening and misdirection as suspense modes.
- **Aurin Squire**, *Six Perfections* blog: the "go for A, get B" movement and its C step (A→B→C), with reveals and reversals alternating across a work ("[Writing Tip: Go for A and Get B](https://sixperfections.blogspot.com/2026/04/writing-tip-go-for-and-get-b.html)," 2026); the question "why is this scene compelling to watch?" ("[5 Questions for Scene Analysis](https://sixperfections.blogspot.com/2026/04/5-questions-for-scene-analysis.html)," 2026, adapted from Tom Vaughan, "[Five Questions For Every Scene](https://storyandplot.substack.com/p/five-questions-for-every-scene)," *Story and Plot*, 2025).

---

## Repository layout

```
crews-analysis/
  SKILL.md                    analysis workflow, output structure, dimension reference
crews-cards/
  SKILL.md                    card templates and rendering workflow
  scripts/make_cards.py       Markdown → PDF (reportlab) or printable HTML
  fonts/                      DejaVu Sans (bundled for consistent output; see LICENSE-DejaVu.txt)
Makefile                      builds dist/crews-analysis.zip and dist/crews-cards.zip for upload
LICENSE, LICENSE-CC-BY-4.0.txt
docs/
  reading-the-cards.md        guide to the card fields and symbols (for readers; not loaded by the skills)
  crews-design-notes.md       how the framework was built: sources per dimension, testing history
examples/
  gift-of-the-magi/           worked example: source, checkpoint, analysis, cards, PDFs
```

---

## License

- **Code** (`crews-cards/scripts/`, `Makefile`): [MIT](LICENSE).
- **Skill text, docs and examples** (the `SKILL.md` files, `docs/`, this README, the analyses and cards in `examples/`): [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Reuse and adapt freely, with attribution.
- **Exceptions:** O. Henry's story text in `examples/` is public domain. The bundled DejaVu fonts are distributed under the Bitstream Vera licence with public-domain DejaVu changes; see `crews-cards/fonts/LICENSE-DejaVu.txt`.
