# Instructions for Claude Code: update crews-cards skill

These instructions update the `crews-cards` skill at `/Users/gkossinets/My Drive/Claude/crews-cards-skill/` to (1) restore bold-line headers with thematic-break page separators, (2) require blank lines between paragraphs and list items in generated card Markdown, and (3) replace hardcoded absolute paths with a portable compile script.

Work through the changes in order. After each change, verify by reading back the affected file.

---

## Change 1: switch card headers from H1 to bold first line; page breaks via `---`

**Problem.** Currently every card starts with an H1 heading (`# 01 — ...`). The preamble's show rule turns H1 into bold text plus a weak pagebreak, but in practice this places the header too close to the first line of the body. We want a plain bold line followed by a blank line before the body, with page breaks carried by Markdown thematic breaks (`---`).

**Change in the three card templates inside `SKILL.md`.**

Replace in the Cover card template:

```markdown
# COVER — [Title] by [Author]
```

with:

```markdown
**COVER — [Title] by [Author]**
```

At the very end of the cover card template (after the `**Intended effect:** ...` line), before the fenced code block closes, add a line containing only `---`.

Replace in the Micro card template:

```markdown
# [NN] — [Location, time]
```

with:

```markdown
**[NN] — [Location, time]**
```

At the very end of the micro card template, after the `**Hook:** ...` line and before the closing fence, add a line containing only `---`.

Replace in the Letter card template:

```markdown
# Scene [NN] — [Location, time, weather if relevant]
```

with:

```markdown
**Scene [NN] — [Location, time, weather if relevant]**
```

At the very end of the letter card template, after the `**Compelling because:** ...` line and before the closing fence, add a line containing only `---`.

Replace in the Rhythm map card template:

```markdown
# RHYTHM MAP — [Title]
```

with:

```markdown
**RHYTHM MAP — [Title]**
```

At the very end of the rhythm map template, after the `**Mood arc:** ...` block and before the closing fence, add a line containing only `---`.

Also update the divider-card example (the act/sequence break) from:

```markdown
# ── Act II ──
```

to:

```markdown
**── Act II ──**

---
```

**Change in Step 3's opening prose.** The current text reads:

> Produce a Markdown file where each card starts with a level-1 heading. The preamble turns every H1 into a page break, so the card layout is bulletproof regardless of content length — though each card should still be tight enough to fit its page.

Replace with:

> Produce a Markdown file where each card starts with a bold title line, followed by a blank line, followed by the card body. Each card ends with a Markdown thematic break (`---`) on its own line. The preamble turns every thematic break into a page break, so card boundaries are explicit and the layout is bulletproof regardless of content length — though each card should still be tight enough to fit its page.

**Change in both preamble files.**

Replace the entire contents of `preamble-3x5.typ` with:

```typst
// Preamble for CREWS micro cards (3x5 inches).
// Verdana 8pt, tight margins, no headers or footers.
// Each Markdown thematic break (---) becomes a weak page break;
// card title lines are plain bold text, not headings.

#set page(width: 5in, height: 3in, margin: 0.2in)
#set text(font: "Verdana", size: 8pt)
#set par(leading: 0.5em, spacing: 1.0em)

// pandoc emits #horizontalrule for "---" in markdown; make it a pagebreak
#let horizontalrule = pagebreak(weak: true)
```

Replace the entire contents of `preamble-letter.typ` with:

```typst
// Preamble for CREWS letter cards (8.5x11 inches).
// Verdana 11pt body, no headers or footers.
// Each Markdown thematic break (---) becomes a weak page break;
// card title lines are plain bold text, not headings.

#set page(paper: "us-letter", margin: 1in)
#set text(font: "Verdana", size: 11pt)
#set par(leading: 0.65em, spacing: 1.2em)

// pandoc emits #horizontalrule for "---" in markdown; make it a pagebreak
#let horizontalrule = pagebreak(weak: true)
```

Note the `par(spacing: ...)` values are unchanged from before (`1.0em` micro / `1.2em` letter). The assumption that these values consume a full rendered line per paragraph break was wrong; empirical testing shows blank lines in source add only a small fraction of a rendered line per break — six blank lines cost about two rendered lines on a 3×5 card. The existing values produce the right visible-but-modest separation.

**Update the Typography notes section.** Replace the current paragraph:

> The preambles restyle H1 headings to bolded body-size text (not large titles) because the card layout treats the header as a first line, not a display element. Each H1 forces a page break via `pagebreak(weak: true)`, guaranteeing one card per page regardless of body length.

with:

> Card titles are plain bold lines, not Markdown headings. Page breaks are driven by Markdown thematic breaks (`---`) at the end of each card; the preamble intercepts typst's rendering of thematic breaks and converts them to weak page breaks. This guarantees one card per page regardless of body length, and keeps the title line visually separated from the first body line by a normal paragraph break.

---

## Change 2: require blank lines between paragraphs and list items in generated card Markdown

**Problem.** The current skill explicitly tells Claude *not* to put blank lines between adjacent bold-label lines, relying on `--from markdown+hard_line_breaks` to preserve line-by-line layout. In practice this produces Markdown that renders correctly in typst but renders as run-on paragraphs in every other Markdown editor and in Google Docs — and it also breaks list rendering when list items are adjacent to paragraphs.

**Change in the three card templates.** For each card template, insert a blank line between every adjacent pair of non-empty lines. The templates should look like this after the change:

**Cover card** (showing the full template; note blank line before and after the character list, and between each bold-label block):

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

**Intended effect:** [what the reader is meant to know, feel, or recognise by the end]

---
```

**Micro card:**

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

**Letter card:**

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

**Rhythm map card** (note also the promotion of the rhythm notes from a parenthetical to its own `**Notes:**` paragraph):

```markdown
**RHYTHM MAP — [Title]**

**Reveal/reversal rhythm** (r = reveal, R = reversal, n = non-reversal):

r r R r r r R R r r r R n r ...

**Notes:** [flag any notable runs — long stretches of r without R, R clusters that risk melodrama, or deliberate n's where a reversal was expected]

**Dangling cause map:**

- ↓ [cause] (NN) → ↑ [payoff] (NN)
- ↓ [cause] (NN) → ↑ [payoff] (NN)

**Unresolved:**

- [list of dangling causes never paid off]

**Status arcs:**

- [Character]: [start status] → [end status] via scenes [NN, NN, NN]

**Mood arc:**

- [summary of atmospheric movement across the work]

---
```

**Update the line budget for micro cards.** In the "Line budget for micro cards" section, replace:

> Target total: up to 15 rendered lines; aim lower to leave slack for variable typography.

with:

> Target total: up to 15 rendered lines (counted including blank-line paragraph separations). Blank lines between paragraphs add only a small fraction of a rendered line each — six blank-line separations cost roughly two rendered lines in typst's compiled output. This means a card with 11 content items plus 10 paragraph separations still fits on one 3×5 page. If the card exceeds the budget, tighten in this order: description, ↑ payoffs, character list, hook. A→B→C, Function, and Mood stay protected; those are what makes the card a card rather than a summary.

Keep the subsequent paragraph about estimating rendered line count by dividing character counts by 65; it still applies to content line length (how long each paragraph runs before wrapping).

**Delete the entire "Line breaks between adjacent bold labels" subsection** at the end of the Typography notes section. That advice is now reversed. Replace it with:

> **Blank lines between paragraphs and list items.** Generated card Markdown must include blank lines between every paragraph, every list, and every bold-label line. This is standard Markdown paragraph separation — required for lists to render correctly and for the file to be readable in Markdown editors and Google Docs. The typst paragraph-spacing setting in the preamble keeps the rendered separation modest so the 3×5 budget is preserved.

---

## Change 3: replace hardcoded absolute paths with a compile script

**Problem.** Step 4 of the skill currently invokes `cat` with absolute paths to `/Users/gkossinets/My Drive/Claude/crews-cards-skill/preamble-*.typ`. These paths hardcode both the user's username and the skill's location on Google Drive, which prevents the skill from being shared.

**Solution.** Create a small bash script inside the skill directory that handles the compile pipeline, resolves its own location to find the preambles, and exposes a clean invocation. Update SKILL.md to call the script with relative-to-skill paths.

**Create a new file** at `/Users/gkossinets/My Drive/Claude/crews-cards-skill/compile.sh` with this content:

```bash
#!/usr/bin/env bash
# Compile a CREWS cards Markdown file to PDF via pandoc + typst.
#
# Usage:
#   bash compile.sh <input.md> <format>
#
# Arguments:
#   input.md — path to a crews-cards Markdown file (ending in -cards.md)
#   format   — either "3x5" or "letter"
#
# Outputs three files alongside the input:
#   <stem>-body.typ       (pandoc output)
#   <stem>-final.typ      (preamble + body concatenated)
#   <stem>-<format>.pdf   (typst output)
#
# Requires: pandoc, typst on PATH. Verdana font if available; typst will
# fall back to its default sans-serif and warn if not.

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: bash compile.sh <input.md> <format>" >&2
  echo "  <format> is '3x5' or 'letter'" >&2
  exit 1
fi

INPUT="$1"
FORMAT="$2"

if [ ! -f "$INPUT" ]; then
  echo "Error: input file not found: $INPUT" >&2
  exit 1
fi

case "$FORMAT" in
  3x5|letter) ;;
  *)
    echo "Error: format must be '3x5' or 'letter' (got '$FORMAT')" >&2
    exit 1
    ;;
esac

# Check for required tools.
for tool in pandoc typst; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: $tool not found on PATH. Install with 'brew install $tool' on macOS." >&2
    exit 1
  fi
done

# Resolve the skill directory (where this script and the preambles live).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREAMBLE="$SCRIPT_DIR/preamble-$FORMAT.typ"

if [ ! -f "$PREAMBLE" ]; then
  echo "Error: preamble not found: $PREAMBLE" >&2
  exit 1
fi

# Derive stem and output paths.
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
INPUT_BASE="$(basename "$INPUT" .md)"
STEM="$INPUT_DIR/$INPUT_BASE"

BODY="$STEM-body.typ"
FINAL="$STEM-final.typ"
PDF="$STEM-$FORMAT.pdf"

# Compile.
pandoc "$INPUT" -o "$BODY" --to typst --from markdown+hard_line_breaks
cat "$PREAMBLE" "$BODY" > "$FINAL"
typst compile "$FINAL" "$PDF"

echo "Compiled: $PDF"
```

Make the script executable:

```bash
chmod +x /Users/gkossinets/My\ Drive/Claude/crews-cards-skill/compile.sh
```

**Update Step 4 in SKILL.md.** Replace the entire Step 4 ("compile to PDF (optional)") section with:

```markdown
### Step 4: compile to PDF (optional)

If the user requested PDF output, invoke the bundled compile script from the skill directory. The script checks for pandoc and typst on PATH, resolves its own location to find the preamble, and writes the output files alongside the input Markdown.

For micro cards (3×5):

​```bash
bash <skill-dir>/compile.sh <stem>-cards.md 3x5
​```

For letter cards (8.5×11):

​```bash
bash <skill-dir>/compile.sh <stem>-cards.md letter
​```

`<skill-dir>` is the absolute path to the `crews-cards-skill/` directory (wherever it lives on the user's machine); the skill reads this from its own invocation context. `<stem>-cards.md` is the Markdown file written in Step 3.

If the script exits non-zero, report the error to the user. Common failures:

- `pandoc` or `typst` not found — the script will print install instructions
- Preamble file missing — indicates a damaged skill installation
- Input file not found — the stem was computed wrongly; check Step 3's output path
```

**Update the "Preamble locations" section at the end of SKILL.md.** Replace the entire section:

```markdown
## Preamble locations

Absolute paths to the preamble files:

- `/Users/gkossinets/My Drive/Claude/crews-cards-skill/preamble-3x5.typ`
- `/Users/gkossinets/My Drive/Claude/crews-cards-skill/preamble-letter.typ`

The card skill reads these in place; they do not need to be copied to the working directory (the `cat` command in Step 4 concatenates directly from the skill directory).
```

with:

```markdown
## Skill directory contents

The skill directory contains:

- `SKILL.md` — this file
- `preamble-3x5.typ` — typst preamble for 3×5 micro cards
- `preamble-letter.typ` — typst preamble for 8.5×11 letter cards
- `compile.sh` — bash script that runs pandoc and typst against a cards Markdown file; resolves its own location to find the preambles, so the skill is portable

The compile script is the only supported way to compile cards to PDF. It must remain executable (`chmod +x compile.sh`); if sharing the skill via a zip or a git repository where execute bits are not preserved, instruct recipients to re-apply executable permissions on unpack.
```

---

## Verification steps

After all three changes are applied:

1. Read back `SKILL.md` and check that every fenced-code template starts with a `**Bold title**` line and ends with a `---` line.
2. Read back both preamble files and confirm the `#show line: it => pagebreak(weak: true)` rule is present and the heading show-rule is gone.
3. Read back `compile.sh` and confirm it is executable (`ls -l`).
4. Run a test compile against an existing `*-cards.md` file if available, in both formats, and confirm the output PDFs render one card per page with the title line visually separated from the first body line.

If the test compile produces cards that feel too cramped or too spacious, adjust the `par(spacing: ...)` value in the relevant preamble (lower → tighter, higher → more breathing room). Report any such adjustment back to the user for confirmation.

## Note on the old rhythm map parenthetical

While making Change 2, the rhythm map's "(flag any notable runs...)" parenthetical has been promoted to a `**Notes:**` paragraph. This is a small structural improvement that follows from the blank-line convention — the parenthetical style only made sense when paragraphs were packed together. Confirmed separately in the templates above.
