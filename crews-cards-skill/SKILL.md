---
name: crews-cards
description: Use this skill when the user wants to convert a CREWS analysis Markdown file into printable scene cards for physical wall layout. Trigger on phrases like "card mode," "letter mode," "micro cards," "letter cards," "Lynch cards," "index cards," "3x5 cards," "one card per scene," "one page per scene," "print the analysis as cards," "make cards from the analysis," or any request to turn a CREWS analysis into a physical card format. This skill reads a `*-crews-analysis.md` file produced by the crews-analysis skill and produces a compressed cards Markdown file, with optional compilation to PDF via pandoc and typst. Do NOT trigger for original scene analysis — that is the crews-analysis skill, which must be run first.
---

# CREWS cards: compress analysis into printable scene cards

## Overview

This skill takes a full-form CREWS analysis Markdown file and compresses it into scene cards suitable for physical wall layout. It does not perform analysis; it is a presentation layer over a file produced by the `crews-analysis` skill. If the user has not yet run the analysis, run that first.

Two card formats are supported:

- **Micro cards** (3×5 inches) — one compact card per scene, dense, for large wall layouts
- **Letter cards** (8.5×11 inches) — one expanded card per scene, one dimension per line, for close-up review

Both formats generate a cover card at the head of the deck and a rhythm map card at the tail.

---

## Inputs and outputs

**Input:** an absolute path to a CREWS analysis Markdown file with the structure produced by the `crews-analysis` skill. Key sections expected:

- `## Overview` (premise, characters with super-objectives, implied reader, story shape, motifs, formats, control level)
- `## Scene-by-scene` with `### Scene NN — ...` headings for each scene
- `## Cross-scene patterns` (rhythm, suspense, dangling causes, status and power arcs, mood arc)
- `## Who hired the CREWS?` (meta-question answer)

If the input file lacks these sections, stop and tell the user the file does not match the expected structure; ask whether they want to run `crews-analysis` first.

**Outputs** (all in the same directory as the input):

- `[stem]-cards.md` — the compressed Markdown cards (always produced)
- `[stem]-cards-body.typ` — pandoc output (produced if pandoc is available)
- `[stem]-cards-final.typ` — preamble + body concatenated (produced if pandoc is available)
- `[stem]-cards-3x5.pdf` or `[stem]-cards-letter.pdf` — the compiled PDF (produced if pandoc and typst are both available)

Where `[stem]` is the input filename with `-crews-analysis` stripped. E.g., `a-to-z-crews-analysis.md` → `a-to-z-cards.md`.

---

## How to run

### Step 1: confirm inputs

Confirm with the user:

- **Input analysis file:** absolute path
- **Card format:** micro (3×5) or letter (8.5×11). If they say just "cards," ask.
- **Compile to PDF?** Yes by default if pandoc and typst are available; skip if either is missing

### Step 2: read and validate the analysis file

Read the input file. Verify it has the four expected H2 sections listed above. If not, stop and explain.

### Step 3: write the cards Markdown

Produce a Markdown file where each card starts with a bold title line, followed by a blank line, followed by the card body. Each card ends with a Markdown thematic break (`---`) on its own line. The preamble turns every thematic break into a page break, so card boundaries are explicit and the layout is bulletproof regardless of content length — though each card should still be tight enough to fit its page.

The file has three parts in order:

1. **Cover card** — one, generated from `## Overview` and `## Who hired the CREWS?`
2. **Scene cards** — one per scene, in reading order
3. **Rhythm map card** — one, generated from `## Cross-scene patterns`

Between major structural units (acts, sequences), insert a thin divider card:

```markdown
**── Act II ──**

---
```

Use these only when the analysis file includes explicit structural dividers.

#### Cover card template

```markdown
**COVER — [Title] by [Author]**

**Premise:** [one sentence]

**Characters:**

- [Name] — [role]; wants [super-objective]; gets [outcome] (→ [transforms])
- ...

**Implied reader:** [who this is for]

**Implied author:** [moral, ideological, or emotional stance]

**Tone:** [register]

**Story shape:** [three-act | kishotenketsu | episodic | other]

**Key motifs:** [recurring images, objects, phrases]

**Formats used:** [trials, rituals, ceremonies, etc.]

**Control level:** [agencies that direct events without being directly affected — gods, fate, the state, surveillance, the algorithm, market forces, ideology; omit if absent]

**Intended effect:** [what the reader is meant to know, feel, or recognise by the end]

---
```

On 3×5 micro cards, the cover is the only card allowed to overflow to a second page. Typst's weak pagebreak rule still forces each subsequent scene card onto its own page, but the cover itself may spill when the character list is long. Letter-size cards have ample room and do not overflow.

The character list is the structural spine of the work scaled up from scene to story — the A→B→C pattern (wants → gets → transforms) at the level of the whole piece. Include only characters who carry structural weight; minor characters belong in scene cards, not here. A typical feature-length work has three to six entries; an ensemble piece may have more, a two-hander fewer.

Where a want/gets frame would distort the material — type-driven characters, static figures, chorus-like ensembles, or works where a character's dominant structural characteristic is something other than pursuit of an objective — substitute the live dimension. Options: character type (type / intermediate / complex); social status and its movement; function as a force (protagonist, antagonist, foil, gatekeeper, catalyst); or a single defining circumstance. One line per character, period. If a character needs more, the cover is the wrong place.

#### Micro card template (3×5)

```markdown
**[NN] — [Location, time]**

[Characters present]

[One-sentence action: what happens and what changes]

**A→B→C:** [wants] → [gets] ([reveal | reversal]) → [transforms, if applicable]

**Function:** [setup | inciting | rising | twist | climax | release | bridge]

**↓** [plants introduced]

**↑** [payoffs of earlier plants]

**Mood:** [one phrase]

**Hook:** [why compelling in its own right]

---
```

**Line budget for micro cards.** Micro cards must fit on a single 3×5 page. Assuming typst rendering at roughly 65 characters per rendered line with Verdana 8pt, allocate the budget per field as follows:

- Header: 1 line
- Characters: 1 line; for ensembles of six or more, use collective phrasing ("the full ensemble; enter Molly, Ben Drake") rather than enumerating
- Description: 1–2 lines. The A→B→C carries the beats, so the description just orients
- A→B→C: up to 3 lines. This is the structural spine; do not amputate for layout
- Function: 1 line
- ↓ plants: 1–2 lines; cap at roughly three items
- ↑ payoffs: 1–2 lines; cap at roughly three items, chosen for structural weight
- Mood: 1 line
- Hook: 1–2 lines; prefer a single image to a quote-plus-gloss

Target total: up to 15 rendered lines (counted including blank-line paragraph separations). Blank lines between paragraphs add only a small fraction of a rendered line each — six blank-line separations cost roughly two rendered lines in typst's compiled output. This means a card with 11 content items plus 10 paragraph separations still fits on one 3×5 page. If the card exceeds the budget, tighten in this order: description, ↑ payoffs, character list, hook. A→B→C, Function, and Mood stay protected; those are what makes the card a card rather than a summary.

After drafting each scene, estimate the rendered line count by dividing each field's character count by 65 and rounding up. If the total exceeds 15, or if a non-structural field exceeds its budget, tighten in this order: description, ↑ payoffs, character list, hook. A→B→C, Function, and Mood stay protected; those are what makes the card a card rather than a summary.

#### Letter card template (8.5×11)

```markdown
**Scene [NN] — [Location, time, weather if relevant]**

**Present:** [Characters]

**Format/ritual:** [if notable]

**Action:** [One sentence]

**A:** [objective]

**B:** [outcome] ([reveal | reversal])

**C:** [transformation, if applicable]

**Stakes:** [what's at risk]

**Subtext:** [gap, if live]

**Knowledge:** [dramatic irony, if live]

**Plants ↓:** [dangling causes introduced]

**Payoffs ↑:** [dangling causes closed]

**Function:** [role in larger structure]

**Mood:** [atmosphere — short phrase]

**Compelling because:** [why the scene earns its place]

---
```

Letter cards can afford one expanded dimension per line. Silent dimensions are still omitted.

#### Rhythm map card template

```markdown
**RHYTHM MAP — [Title]**

**Reveal/reversal rhythm** (r = reveal, R = reversal, N = non-reversal):

r r R r r r R R r r r R N r ...

**Notes:** [flag any notable runs — long stretches of r without R, R clusters that risk melodrama, or deliberate N's where a reversal was expected]

**Suspense:** [dominant mode(s) — postponement, screening, misdirection; any shifts across the work]

**Dangling cause map:**

- ↓ [cause] (NN) → ↑ [payoff] (NN)
- ↓ [cause] (NN) → ↑ [payoff] (NN)

**Unresolved:**

- [list of dangling causes never paid off]

**Status and power arcs:**

- [Character]: [start status; form of power held] → [end status; form of power held] via scenes [NN, NN, NN]; note significant conversions

**Mood arc:**

- [summary of atmospheric movement across the work]

---
```

To derive the compact rhythm string from the analysis file's per-scene rhythm list, map each bullet's classification to a symbol:

- `setup` → `r` (the opening is a small reveal of world and situation)
- `reveal` → `r`
- `reversal` → `R`
- `non-reversal` → `N`

Preserve scene order; the position of each symbol corresponds to its scene number.

#### Card conventions (both formats)

- **Characters present** — list only characters physically present in the scene. Named but absent characters belong in the plants or action line if they matter; passing mentions can be omitted.
- **Scene vs. orbit** — if the analysis file marks a unit with `[orbit]`, preserve that tag on the card.
- **Scene number references** — within parentheses on rhythm map or plant/payoff lines, refer to scene numbers by bare number, not "scene N" or "scenes N, M". E.g., "Molly's music (23); Duroc's helm-hand (3, 18)".
- **Silent dimensions** — omit any line not live in the scene. A sparse card is a signal about the scene, not a failure of analysis.

### Step 4: compile to PDF (optional)

If the user requested PDF output, invoke the bundled compile script from the skill directory. The script checks for pandoc and typst on PATH, resolves its own location to find the preamble, and writes the output files alongside the input Markdown.

For micro cards (3×5):

```bash
bash <skill-dir>/compile.sh <stem>-cards.md 3x5
```

For letter cards (8.5×11):

```bash
bash <skill-dir>/compile.sh <stem>-cards.md letter
```

`<skill-dir>` is the absolute path to the `crews-cards-skill/` directory (wherever it lives on the user's machine); the skill reads this from its own invocation context. `<stem>-cards.md` is the Markdown file written in Step 3.

If the script exits non-zero, report the error to the user. Common failures:

- `pandoc` or `typst` not found — the script will print install instructions
- Preamble file missing — indicates a damaged skill installation
- Input file not found — the stem was computed wrongly; check Step 3's output path

### Step 5: report

Report the output files by absolute path. If PDF compilation succeeded, confirm the compile worked; note Verdana as the default font (falls back if not installed).

---

## Typography notes

Both preambles use Verdana 8pt (micro) or 11pt (letter) as the default body font. On macOS, Verdana ships with Microsoft Office; if not installed, typst will fall back to its default sans-serif and warn. The user can edit the preamble files to change fonts without touching this skill.

Card titles are plain bold lines, not Markdown headings. Page breaks are driven by Markdown thematic breaks (`---`) at the end of each card; the preamble intercepts typst's rendering of thematic breaks and converts them to weak page breaks. This guarantees one card per page regardless of body length, and keeps the title line visually separated from the first body line by a normal paragraph break.

**Blank lines between paragraphs and list items.** Generated card Markdown must include blank lines between every paragraph, every list, and every bold-label line. This is standard Markdown paragraph separation — required for lists to render correctly and for the file to be readable in Markdown editors and Google Docs. The typst paragraph-spacing setting in the preamble keeps the rendered separation modest so the 3×5 budget is preserved.

---

## Skill directory contents

The skill directory contains:

- `SKILL.md` — this file
- `preamble-3x5.typ` — typst preamble for 3×5 micro cards
- `preamble-letter.typ` — typst preamble for 8.5×11 letter cards
- `compile.sh` — bash script that runs pandoc and typst against a cards Markdown file; resolves its own location to find the preambles, so the skill is portable

The compile script is the only supported way to compile cards to PDF. It must remain executable (`chmod +x compile.sh`); if sharing the skill via a zip or a git repository where execute bits are not preserved, instruct recipients to re-apply executable permissions on unpack.
