---
name: crews-cards
description: Use this skill when the user wants to turn a CREWS analysis Markdown file into printable scene cards for a physical wall layout, as Markdown plus a ready-to-print PDF. Trigger on phrases like "card mode," "letter mode," "micro cards," "letter cards," "Lynch cards," "index cards," "3x5 cards," "one card per scene," "one page per scene," "large-print cards," "print the analysis as cards," "make cards from the analysis," or any request to turn a CREWS analysis into a physical card format. Reads a `*-crews-analysis.md` file produced by the crews-analysis skill; renders the PDF with a bundled Python script. Do NOT trigger for original scene analysis; that is the crews-analysis skill, which must be run first.
---

# CREWS cards: compress an analysis into printable scene cards

## Overview

This skill takes a full-form CREWS analysis Markdown file and compresses it into scene cards for a physical wall layout. It does not perform analysis; it is a presentation layer over a file produced by the `crews-analysis` skill. If the user has no analysis file yet, run that skill first.

Two card formats:

- **Micro cards** (3×5 inches): one compact card per scene, for large wall layouts. Printable straight onto index cards, or four to a sheet of letter or A4 paper with cut lines.
- **Letter cards** (8.5×11 inches, or A4): one expanded card per scene, one dimension per line, for close-up review.

Both formats open with a cover card, followed by a key card explaining the symbols, and close with a rhythm map card.

The PDF is produced by `scripts/make_cards.py`, which needs only Python 3 and reportlab. It bundles its own font and sets every card at the same type size (8pt for micro cards, 11pt for letter). A card too long for one card continues onto the next, and the script reports which cards ran over, so card length is checked by measurement, not estimation.

---

## Inputs and outputs

**Input:** a CREWS analysis Markdown file with the structure produced by `crews-analysis`. Expected H2 sections:

- `## Overview` (premise, characters with super-objectives, implied reader, story shape, motifs, formats, control level)
- `## Scene-by-scene`, with a `### Scene NN — ...` heading per scene
- `## Cross-scene patterns` (rhythm, suspense, dangling causes, status and power arcs, mood arc)
- `## Who hired the CREWS?`

If the file lacks these sections, stop and say so; ask whether the user wants to run `crews-analysis` first.

**Outputs**, written next to the input (or to the session's output folder if the input's folder isn't writable):

| Format | Markdown | PDF |
|---|---|---|
| micro | `[stem]-cards-3x5.md` | `[stem]-cards-3x5.pdf` (one card per 5×3 in page) and, on request, `[stem]-cards-3x5-sheet.pdf` (four per sheet) |
| letter | `[stem]-cards-letter.md` | `[stem]-cards-letter.pdf` (or `-letter-a4.pdf`) |

`[stem]` is the input filename with `-crews-analysis` removed: `a-to-z-crews-analysis.md` → `a-to-z-cards-3x5.md`.

---

## How to run

### Step 1: confirm the format

- If the user says "micro," "index," "3×5," or similar, use micro. If they say "letter," "one page per scene," or similar, use letter. If they just say "cards," ask which (or offer both).
- For micro cards, the default PDF is one card per 5×3 page (for printers that take index cards). Offer the four-per-sheet version if they'll print on ordinary paper. Use A4 if the user is outside North America or asks for it.
- **Type size:** standard print is 8pt (micro) or 11pt (letter). Offer **large print** (10pt micro, 12pt letter) if the user wants cards readable from further away, or mentions legibility; any other size also works ("9pt cards"). Don't ask unless it matters to the user; standard is the default.
- PDF output is on by default; skip it only if the user wants Markdown alone.

### Step 2: read and validate the analysis file

Read the input file and check for the four H2 sections above.

### Step 3: write the cards Markdown

Each card starts with a bold title line, then a blank line, then the card body. Each card ends with a line containing only `---`. The renderer starts a new card at every `---`, so card boundaries are explicit.

The file has three parts, in order:

1. **Cover card**, from `## Overview` and `## Who hired the CREWS?`
2. **Scene cards**, one per scene, in reading order
3. **Rhythm map card**, from `## Cross-scene patterns`

Don't write a key card: the renderer inserts a standard one after the cover (a version for micro cards and one for letter cards), so it's identical in every deck. If the user wants a custom key, write a card titled `**KEY — ...**` and the renderer will use it instead; if they want none, pass `--no-key`.

Where the analysis marks acts or sequences, insert a divider card between them; the renderer centres it:

```markdown
**── Act II ──**

---
```

**Blank lines.** Put a blank line between every paragraph, every list, and every bold-label line. Without them, Markdown editors (and Google Docs) run consecutive label lines together, and the renderer treats them as a single paragraph.

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

**Control level:** [agencies that direct events without being directly affected (gods, fate, the state, surveillance, the algorithm, market forces, ideology); omit if absent]

**Intended effect:** [what the reader is meant to know, feel, or recognise by the end]

---
```

The character list is the work's structural spine, scaled up from scene to story: the A→B→C pattern (wants → gets → transforms) for the whole piece. Include only characters who carry structural weight; a typical feature-length work has three to six, an ensemble more, a two-hander fewer.

Where a want/gets frame would distort the material (type-driven characters, static figures, chorus-like ensembles, or characters whose dominant trait is something other than pursuing an objective), substitute the live dimension: character type (type / intermediate / complex); social status and its movement; function as a force (protagonist, antagonist, foil, gatekeeper, catalyst); or a single defining circumstance. One line per character. If a character needs more, the cover is the wrong place.

The cover and the rhythm map may take as many cards as they need; the renderer continues them onto further cards, each headed with the title and "(cont.)", at the same type size as every other card. Scene cards must fit on one card.

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

**Content budget.** A micro card holds about 14–16 short lines (roughly 75 characters each) at 8pt, or about 12 lines of roughly 60 characters in large print (10pt). In large print, keep each field to its minimum below. Aim for:

- Characters: one line; for ensembles of six or more, use collective phrasing ("the full ensemble; enter Molly, Ben Drake")
- Description: one or two lines; the A→B→C carries the beats, so the description just orients
- A→B→C: up to three lines; this is the structural spine, so don't amputate it for layout
- ↓ plants and ↑ payoffs: one or two lines each; about three items, chosen for structural weight
- Hook: one or two lines; a single image beats a quote-plus-gloss

You don't need to count characters; the renderer measures each card. A scene card must fit on one card: when the renderer reports one as overflowing, tighten it in this order: description, ↑ payoffs, character list, hook. A→B→C, Function and Mood stay protected; they make the card a card rather than a summary.

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

**Mood:** [atmosphere; short phrase]

**Compelling because:** [why the scene earns its place]

---
```

Letter cards can afford one expanded dimension per line. Silent dimensions are still omitted.

#### Rhythm map card template

```markdown
**RHYTHM MAP — [Title]**

**Reveal/reversal rhythm** (r = reveal, R = reversal, N = non-reversal):

r r R r r r R R r r r R N r ...

**Notes:** [notable runs: long stretches of r without R; R clusters that risk melodrama; deliberate N's where a reversal was expected]

**Suspense:** [dominant mode(s): postponement, screening, misdirection; shifts across the work]

**Dangling cause map:**

- ↓ [cause] (NN) → ↑ [payoff] (NN)
- ↓ [cause] (NN) → ↑ [payoff] (NN)

**Unresolved:**

- [dangling causes never paid off]

**Status and power arcs:**

- [Character]: [start status; form of power held] → [end status; form of power held] via scenes [NN, NN, NN]; note significant conversions

**Mood arc:**

- [summary of atmospheric movement across the work]

---
```

On micro cards, short lists (Unresolved, Mood arc) can be written as a single labelled line to save space.

To build the rhythm string from the analysis file's per-scene rhythm list, map each classification to a symbol, in scene order:

- `setup` → `r` (the opening is a small reveal of world and situation)
- `reveal` → `r`
- `reversal` → `R`
- `non-reversal` → `N`

#### Card conventions (both formats)

- **Characters present:** only characters physically present in the scene. Named but absent characters belong in the plants or action line if they matter.
- **Scene vs. orbit:** if the analysis marks a unit `[orbit]`, keep that tag on the card.
- **Scene number references:** in parentheses, use bare numbers, not "scene N": "Molly's music (23); Duroc's helm-hand (3, 18)".
- **Silent dimensions:** omit any line that isn't live. A sparse card is a signal about the scene, not a failure of analysis.
- **Inline styling:** `**bold**` and `*italic*` are rendered; other Markdown (headings, links, tables) is not expected on cards.

### Step 4: render the PDF

Run the bundled script. `<skill-dir>` is this skill's own directory.

```bash
# micro cards, one per 5×3 page
python3 <skill-dir>/scripts/make_cards.py <stem>-cards-3x5.md --format 3x5

# micro cards, four per landscape sheet with cut lines (add --paper a4 for A4)
python3 <skill-dir>/scripts/make_cards.py <stem>-cards-3x5.md --format 3x5-sheet

# letter cards (add --paper a4 for A4)
python3 <skill-dir>/scripts/make_cards.py <stem>-cards-letter.md --format letter

# large print (10pt micro, 12pt letter), or any size with --size
python3 <skill-dir>/scripts/make_cards.py <stem>-cards-3x5.md --format 3x5 --large
python3 <skill-dir>/scripts/make_cards.py <stem>-cards-3x5.md --format 3x5 --size 9
```

Large-print and custom-size PDFs get their own suffix (`-large`, `-9pt`), so they don't overwrite the standard deck.

**If reportlab is missing**, the script says so and writes a printable HTML file instead. First try to install it (`pip install reportlab`; add `--break-system-packages` if pip refuses on a system-managed Python) and re-run. If installation isn't possible, deliver the HTML and tell the user to open it in a browser and print with **Save as PDF**, margins **None**. The HTML uses the same fixed type sizes; a long card flows onto the next printed page.

**Read the report.** The script lists any card that ran onto more than one printed card:

- *Cover or rhythm map runs to several cards:* fine.
- *Scene card runs to several cards* (marked "tighten to fit one card"): tighten it in the Markdown (Step 3 priority order) and re-run. Two rounds of tightening are usually enough.
- The renderer never breaks a card directly after a label line such as "Dangling cause map:"; the label moves to the next card with its list.

If you can view images, rasterise one or two pages (e.g. `pdftoppm -r 80 -png -f 1 -l 2 <pdf> preview`) and look at them before reporting.

Other options: `--font path/to/Font.ttf` uses a different typeface (a sibling `Font-Bold.ttf` is picked up for bold); `--out` sets the output path; `--no-key` leaves out the key card; `--large` and `--size` set the type size for every card (larger type on 3×5 cards also tightens line spacing slightly); `--json` prints the fit report as JSON.

### Step 5: report

Give the user the output files: by path when working in their file system; as downloadable files when working in a chat session. Mention any cards that were shrunk noticeably or continued, and which format to print on which paper.

---

## Typography

The bundled font is DejaVu Sans (in `fonts/`, with its licence), a humanist sans close to Verdana in proportions. It's bundled so that every user gets identical output and the arrows and rules the cards rely on (→ ↓ ↑ ─) always render. Every card in a deck uses the same size: by default 8pt for micro cards and 11pt for letter cards (the sizes of the original typst version); with `--large`, 10pt and 12pt; or any size with `--size`. Cards never shrink to fit. Card titles carry a thin rule beneath them.

---

## Skill directory contents

- `SKILL.md`: this file
- `scripts/make_cards.py`: Markdown-to-PDF card renderer (reportlab), with an HTML fallback; also holds the text of the standard key cards
- `fonts/`: DejaVu Sans regular, bold, oblique and bold oblique, plus `LICENSE-DejaVu.txt`
