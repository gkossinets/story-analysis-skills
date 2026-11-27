#!/usr/bin/env python3
"""Render a CREWS cards Markdown file to a printable PDF (or HTML).

The only dependency is
reportlab (preinstalled in Claude's code sandbox; otherwise
`pip install reportlab`). If reportlab is missing, the script falls back
to a self-contained HTML file that you can print to PDF from a browser.

Usage:
    python3 make_cards.py <stem>-cards.md --format 3x5
    python3 make_cards.py <stem>-cards.md --format 3x5-sheet [--paper a4]
    python3 make_cards.py <stem>-cards.md --format letter
    python3 make_cards.py <stem>-cards.md --format letter --html
    python3 make_cards.py <stem>-cards.md --format 3x5 --large

Formats:
    3x5        one 5x3 in card per page (for printing straight onto index cards)
    3x5-sheet  four 5x3 in cards per landscape letter/A4 sheet, with cut marks
    letter     one card per US-letter page (use --paper a4 for A4)

Every card is set at one type size: 8pt for 3x5 and 11pt for letter by
default; 10pt and 12pt with --large; or any size with --size. A card too long for one card continues onto further cards,
each headed with the card's title and "(cont.)". The script reports which
cards ran to more than one; scene cards should fit on one.

Input conventions (written by the crews-cards skill):
    - cards are separated by a line containing only `---`
    - blocks inside a card are separated by blank lines
    - a block is a paragraph or a bullet list (`- ` items)
    - inline **bold** and *italic* are supported
    - a card whose only content is a bold line (e.g. **── Act II ──**)
      is rendered as a centred divider card

A key card explaining the symbols is inserted after the cover, unless the
Markdown already has a card titled KEY or --no-key is given.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FONT_DIR = SCRIPT_DIR.parent / "fonts"

INCH = 72.0

# Page geometry and type sizes per format (all in points).
FORMATS = {
    # One type size per format (as in the original typst version). Cards
    # never shrink: a long card continues onto further cards.
    "3x5": dict(card_w=5 * INCH, card_h=3 * INCH, margin=0.2 * INCH,
                size=8.0, leading=1.25, gap=0.55),
    "letter": dict(card_w=8.5 * INCH, card_h=11 * INCH, margin=1.0 * INCH,
                   size=11.0, leading=1.3, gap=0.7),
}
PAPER = {"letter": (8.5 * INCH, 11 * INCH), "a4": (595.28, 841.89)}


# --------------------------------------------------------------------------
# Markdown subset parsing
# --------------------------------------------------------------------------

RULE_RE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")


def split_cards(text: str) -> list[list[dict]]:
    """Return a list of cards; each card is a list of blocks."""
    text = text.replace("\r\n", "\n")
    # Drop a YAML front-matter block if present.
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1 and ":" in text[4:end]:
            text = text[end + 5:]
    cards, current = [], []
    for line in text.split("\n"):
        if RULE_RE.match(line):
            cards.append(current)
            current = []
        else:
            current.append(line)
    cards.append(current)
    parsed = [parse_blocks(lines) for lines in cards]
    return [c for c in parsed if c]


def parse_blocks(lines: list[str]) -> list[dict]:
    blocks, buf = [], []

    def flush():
        if not buf:
            return
        if all(BULLET_RE.match(l) or (l.startswith("  ") and i > 0)
               for i, l in enumerate(buf)):
            items = []
            for l in buf:
                m = BULLET_RE.match(l)
                if m:
                    items.append(m.group(1).strip())
                else:  # continuation of previous item
                    items[-1] += " " + l.strip()
            blocks.append({"type": "list", "items": items})
        else:
            # Mixed: a paragraph line followed directly by bullets.
            para, items = [], []
            for l in buf:
                m = BULLET_RE.match(l)
                if m:
                    items.append(m.group(1).strip())
                elif items:
                    items[-1] += " " + l.strip()
                else:
                    para.append(l.strip())
            if para:
                blocks.append({"type": "para", "lines": para})
            if items:
                blocks.append({"type": "list", "items": items})
        buf.clear()

    for line in lines:
        if line.strip() == "":
            flush()
        elif line.lstrip().startswith("#"):
            flush()  # headings: treat as bold paragraph
            blocks.append({"type": "para",
                           "lines": ["**" + line.lstrip("# ").strip() + "**"]})
        else:
            buf.append(line.rstrip())
    flush()
    return blocks


INLINE_RE = re.compile(r"(\*\*(.+?)\*\*|\*(?!\s)(.+?)(?<!\s)\*|`(.+?)`)")


def inline_markup(s: str, kind: str) -> str:
    """Convert **bold** / *italic* / `code` to reportlab or HTML markup."""
    out, pos = [], 0
    for m in INLINE_RE.finditer(s):
        out.append(html.escape(s[pos:m.start()], quote=False))
        if m.group(2) is not None:
            out.append(f"<b>{html.escape(m.group(2), quote=False)}</b>")
        elif m.group(3) is not None:
            out.append(f"<i>{html.escape(m.group(3), quote=False)}</i>")
        else:
            tag = "code" if kind == "html" else "font"
            inner = html.escape(m.group(4), quote=False)
            out.append(f"<code>{inner}</code>" if kind == "html"
                       else f"<{tag} face='CardMono'>{inner}</{tag}>")
        pos = m.end()
    out.append(html.escape(s[pos:], quote=False))
    return "".join(out)


def is_divider(card: list[dict]) -> bool:
    if len(card) != 1 or card[0]["type"] != "para":
        return False
    lines = card[0]["lines"]
    return len(lines) == 1 and re.fullmatch(r"\*\*[^*]+\*\*", lines[0]) is not None \
        and "──" in lines[0]


def is_scene(card: list[dict]) -> bool:
    """Scene cards are titled '01 — ...' or 'Scene 01 — ...'."""
    return re.match(r"^(scene\s+)?\d+", card_title(card), re.I) is not None


def card_title(card: list[dict]) -> str:
    first = card[0]
    raw = first["lines"][0] if first["type"] == "para" else first["items"][0]
    return re.sub(r"\*+", "", raw).strip()[:70]


# --------------------------------------------------------------------------
# Key card (inserted after the cover unless --no-key)
# --------------------------------------------------------------------------

KEY_MICRO = """**KEY — How to read these cards**

**NN — Place, time:** scene number and setting

**A→B→C:** goes for → gets instead → changes (if at all)

**r**\u00a0reveal: not what it seemed · **R**\u00a0reversal: the terms change · **N**\u00a0non-reversal: an expected reversal doesn't come

**Function:** the scene's job (setup, inciting, rising, twist, climax, release, bridge, reconciliation)

**↓**\u00a0plant: a promise or question left open · **↑**\u00a0payoff: one closed · **(NN)** scene

**Mood:** emotional weather · **Hook:** why it grips on its own

**(cont.)** continued card · **Rhythm map:** one letter per scene
"""

KEY_LETTER = """**KEY — How to read these cards**

**Scene NN — Place, time:** scene number in reading order, and the setting

**Present:** characters physically present · **Format/ritual:** the social structure the scene borrows (a sale, a trial, a dinner)

**A / B / C:** what a character goes for (A); what they get instead (B), as a reveal or a reversal; how they change in response (C), if they do

**Reveal (r):** it turns out the situation isn't what it seemed · **Reversal (R):** the terms of the situation change · **Non-reversal (N):** a reversal the story has prepared doesn't come

**Stakes:** what is at risk · **Subtext:** what goes unsaid · **Knowledge:** who knows what, and what the reader knows that characters don't

**Plants ↓:** promises, threats, fears or questions left open · **Payoffs ↑:** earlier plants closed · **(NN)** scene numbers

**Function:** the scene's job in the whole (setup, inciting, rising, twist, climax, release, bridge, reconciliation)

**Mood:** the scene's emotional weather · **Compelling because:** why it holds attention on its own

**(cont.)** continues the previous card · **Rhythm map:** one letter per scene, in order (r, R, N)

Only live dimensions appear; a missing line is a signal about the scene.
"""


def add_key_card(cards, fmt):
    """Insert the key card after the cover (or first, if there's no cover)."""
    if any(card_title(c).upper().startswith("KEY") for c in cards):
        return cards  # the Markdown already has one
    key = parse_blocks((KEY_MICRO if fmt.startswith("3x5")
                        else KEY_LETTER).split("\n"))
    at = 1 if card_title(cards[0]).upper().startswith("COVER") else 0
    return cards[:at] + [key] + cards[at:]


# --------------------------------------------------------------------------
# PDF rendering (reportlab)
# --------------------------------------------------------------------------

def register_fonts(user_font: str | None):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping

    if user_font:
        reg = Path(user_font)
        bold = reg.with_name(reg.stem + "-Bold" + reg.suffix)
        faces = {"regular": reg, "bold": bold if bold.exists() else reg,
                 "italic": reg, "bolditalic": bold if bold.exists() else reg}
    else:
        faces = {"regular": FONT_DIR / "DejaVuSans.ttf",
                 "bold": FONT_DIR / "DejaVuSans-Bold.ttf",
                 "italic": FONT_DIR / "DejaVuSans-Oblique.ttf",
                 "bolditalic": FONT_DIR / "DejaVuSans-BoldOblique.ttf"}
    missing = [str(p) for p in faces.values() if not p.exists()]
    if missing:
        sys.exit("Error: font file(s) not found: " + ", ".join(missing))
    names = {"regular": "Card", "bold": "Card-Bold",
             "italic": "Card-Italic", "bolditalic": "Card-BoldItalic"}
    for key, path in faces.items():
        pdfmetrics.registerFont(TTFont(names[key], str(path)))
    addMapping("Card", 0, 0, "Card")
    addMapping("Card", 1, 0, "Card-Bold")
    addMapping("Card", 0, 1, "Card-Italic")
    addMapping("Card", 1, 1, "Card-BoldItalic")
    # Monospace: fall back to the regular face (code is rare on cards).
    pdfmetrics.registerFont(TTFont("CardMono", str(faces["regular"])))


def build_flowables(card, size, geom, divider=False):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.platypus.flowables import HRFlowable

    lead = size * geom["leading"]
    gap = size * geom["gap"]
    body = ParagraphStyle("body", fontName="Card", fontSize=size, leading=lead,
                          spaceAfter=gap)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=size * 1.1,
                            bulletIndent=size * 0.15, spaceAfter=size * 0.2)
    if divider:
        title = ParagraphStyle("div", parent=body, fontSize=size * 1.8,
                               leading=size * 2.2, alignment=TA_CENTER)
        text = inline_markup(card[0]["lines"][0], "rl")
        inner_h = geom["card_h"] - 2 * geom["margin"]
        return [Spacer(1, inner_h / 2 - size * 1.5), Paragraph(text, title)]

    flow = []
    for i, block in enumerate(card):
        if block["type"] == "para":
            text = "<br/>".join(inline_markup(l, "rl") for l in block["lines"])
            if i == 0:
                t_style = ParagraphStyle("title", parent=body,
                                         fontSize=size * 1.12,
                                         leading=size * 1.12 * geom["leading"],
                                         spaceAfter=size * 0.3)
                flow.append(Paragraph(text, t_style))
                flow.append(HRFlowable(width="100%", thickness=0.5,
                                       color="#999999", spaceBefore=0,
                                       spaceAfter=gap))
            else:
                para = Paragraph(text, body)
                plain = re.sub(r"<[^>]+>", "", text).strip()
                para._crews_label = plain.endswith(":")
                flow.append(para)
        else:
            for j, item in enumerate(block["items"]):
                st = bullet
                if j == len(block["items"]) - 1:
                    st = ParagraphStyle("bl", parent=bullet, spaceAfter=gap)
                flow.append(Paragraph(inline_markup(item, "rl"), st,
                                      bulletText="•"))
    return flow


def cont_header(title, size, geom):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    st = ParagraphStyle("cont", fontName="Card-Bold", fontSize=size,
                        leading=size * geom["leading"], spaceAfter=size * 0.6,
                        textColor="#777777")
    return Paragraph(html.escape(title, quote=False) + " (cont.)", st)


def flow_height(flow, width, height):
    total = 0.0
    for i, f in enumerate(flow):
        _, h = f.wrap(width, height)
        total += h
        if i:
            total += f.getSpaceBefore()
        if i < len(flow) - 1:
            total += f.getSpaceAfter()
    return total


def card_flowables(card, geom, divider):
    """Build a card's flowables at the format's fixed type size."""
    return build_flowables(card, geom["size"], geom, divider)


def render_pdf(cards, fmt, paper, out_path, user_font):
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Frame

    register_fonts(user_font)
    geom = dict(FORMATS["3x5" if fmt.startswith("3x5") else "letter"])
    if fmt == "letter" and paper == "a4":
        geom["card_w"], geom["card_h"] = PAPER["a4"]
        geom["margin"] = 0.9 * INCH

    sheet = fmt == "3x5-sheet"
    if sheet:
        pw, ph = PAPER[paper][1], PAPER[paper][0]  # landscape
        slots_x = [(pw - 2 * geom["card_w"]) / 2 + k * geom["card_w"]
                   for k in range(2)]
        slots_y = [(ph - 2 * geom["card_h"]) / 2 + k * geom["card_h"]
                   for k in (1, 0)]
        slots = [(x, y) for y in slots_y for x in slots_x]
        page_size = (pw, ph)
    else:
        page_size = (geom["card_w"], geom["card_h"])

    c = canvas.Canvas(str(out_path), pagesize=page_size)
    c.setTitle(out_path.stem)
    c.setCreator("crews-cards make_cards.py")
    report = []

    face_no = 0  # running count of card faces drawn

    def new_frame():
        nonlocal face_no
        if sheet:
            slot = face_no % 4
            if slot == 0 and face_no:
                c.showPage()
            if slot == 0:
                draw_cut_marks(c, slots, geom)
            ox, oy = slots[slot]
        else:
            if face_no:
                c.showPage()
            ox, oy = 0, 0
        face_no += 1
        return Frame(ox, oy, geom["card_w"], geom["card_h"],
                     leftPadding=geom["margin"], rightPadding=geom["margin"],
                     topPadding=geom["margin"], bottomPadding=geom["margin"],
                     showBoundary=0)

    inner_w = geom["card_w"] - 2 * geom["margin"]
    inner_h = geom["card_h"] - 2 * geom["margin"] - 1  # rounding margin

    def take_face(queue):
        """Pop the flowables that fit on one card face, splitting a
        paragraph across faces when it won't fit whole."""
        face, used = [], 0.0
        while queue:
            f = queue[0]
            _, h = f.wrap(inner_w, inner_h)
            before = f.getSpaceBefore() if face else 0
            if used + before + h <= inner_h:
                face.append(queue.pop(0))
                used += before + h + f.getSpaceAfter()
                continue
            room = inner_h - used - before
            parts = f.split(inner_w, room) if room > 0 else []
            if len(parts) >= 2:
                queue.pop(0)
                face.append(parts[0])
                queue[0:0] = parts[1:]
            elif not face:  # unsplittable and taller than a card: draw anyway
                face.append(queue.pop(0))
            break
        # Don't strand a label ("Dangling cause map:") at the foot of a card.
        if queue and len(face) > 1 and getattr(face[-1], "_crews_label", False):
            queue.insert(0, face.pop())
        return face

    for idx, card in enumerate(cards, 1):
        divider = is_divider(card)
        queue = card_flowables(card, geom, divider)
        size = geom["size"]
        faces = 0
        while queue:
            if faces:  # continuation: repeat the title, marked (cont.)
                queue.insert(0, cont_header(card_title(card), size, geom))
            face = take_face(queue)
            frame = new_frame()
            for f in face:
                frame.add(f, c)
            faces += 1
            if faces > 50:
                sys.exit(f"Error: card {idx} would need more than 50 cards.")
        report.append({"card": idx, "title": card_title(card),
                       "faces": faces, "scene": is_scene(card)})

    c.save()
    return report


def draw_cut_marks(c, slots, geom):
    c.saveState()
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.setLineWidth(0.3)
    c.setDash(2, 3)
    for x, y in slots:
        c.rect(x, y, geom["card_w"], geom["card_h"], stroke=1, fill=0)
    c.restoreState()


# --------------------------------------------------------------------------
# HTML fallback (no dependencies; print to PDF from a browser)
# --------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>
@page {{ size: {pw} {ph}; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #ddd; }}
body {{ font-family: "DejaVu Sans", Verdana, "Segoe UI", Helvetica, Arial, sans-serif; }}
.card {{ width: {cw}; min-height: {ch}; padding: {m}; background: #fff;
        margin: 0.25in auto; page-break-after: always;
        break-after: page; font-size: {size}pt; line-height: {lead}; }}
.card li, .card p {{ break-inside: avoid; }}
.card p {{ margin: 0 0 {gap}em 0; }}
.card ul {{ margin: 0 0 {gap}em 0; padding-left: 1.1em; }}
.card li {{ margin: 0 0 0.2em 0; }}
.card .title {{ font-size: 1.12em; border-bottom: 0.5pt solid #999;
               padding-bottom: 0.3em; }}
.card.divider {{ display: flex; align-items: center; justify-content: center;
                font-size: {div}pt; font-weight: bold; }}
.note {{ font: 13px/1.4 sans-serif; max-width: 40em; margin: 1em auto; }}
@media print {{ html, body {{ background: #fff; }} .card {{ margin: 0; }}
               .note {{ display: none; }} }}
</style></head><body>
<p class="note">Print this page and choose <b>Save as PDF</b>. Set margins to
<b>None</b> and paper size to <b>{paper_label}</b>. Every card uses the same
type size; a card too long for one page continues onto the next.</p>
{cards}
</body></html>
"""


def render_html(cards, fmt, paper, out_path):
    key = "3x5" if fmt.startswith("3x5") else "letter"
    geom = FORMATS[key]
    if key == "letter" and paper == "a4":
        cw, ch, label = "210mm", "297mm", "A4"
    elif key == "letter":
        cw, ch, label = "8.5in", "11in", "Letter"
    else:
        cw, ch, label = "5in", "3in", "5 x 3 in (custom)"
    parts = []
    for card in cards:
        if is_divider(card):
            text = inline_markup(card[0]["lines"][0], "html")
            parts.append(f'<section class="card divider">{text}</section>')
            continue
        inner = []
        for i, block in enumerate(card):
            if block["type"] == "para":
                text = "<br>".join(inline_markup(l, "html") for l in block["lines"])
                cls = ' class="title"' if i == 0 else ""
                inner.append(f"<p{cls}>{text}</p>")
            else:
                items = "".join(f"<li>{inline_markup(it, 'html')}</li>"
                                for it in block["items"])
                inner.append(f"<ul>{items}</ul>")
        parts.append('<section class="card">' + "".join(inner) + "</section>")
    m = f"{geom['margin'] / INCH:.2f}in"
    out_path.write_text(HTML_TEMPLATE.format(
        title=html.escape(out_path.stem), pw=cw, ph=ch, cw=cw, ch=ch, m=m,
        size=geom["size"], lead=geom["leading"],
        gap=geom["gap"], div=geom["size"] * 1.8, paper_label=label,
        cards="\n".join(parts)), encoding="utf-8")


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="path to a *-cards.md file")
    ap.add_argument("--format", "-f", required=True,
                    choices=["3x5", "3x5-sheet", "letter"])
    ap.add_argument("--paper", choices=["letter", "a4"], default="letter",
                    help="sheet paper for 3x5-sheet, or page size for letter "
                         "cards (default: letter)")
    ap.add_argument("--out", "-o", help="output path (default: alongside input)")
    ap.add_argument("--html", action="store_true",
                    help="write printable HTML instead of PDF")
    ap.add_argument("--font", help="path to a .ttf to use instead of the "
                                   "bundled DejaVu Sans (a sibling "
                                   "<name>-Bold.ttf is used for bold if present)")
    ap.add_argument("--no-key", action="store_true",
                    help="leave out the key card (inserted after the cover "
                         "by default)")
    ap.add_argument("--large", action="store_true",
                    help="large print: 10pt for 3x5, 12pt for letter")
    ap.add_argument("--size", type=float,
                    help="type size in points for every card (default: 8 for "
                         "3x5, 11 for letter)")
    ap.add_argument("--json", action="store_true",
                    help="print the fit report as JSON")
    args = ap.parse_args()

    src = Path(args.input).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"Error: input file not found: {src}")
    cards = split_cards(src.read_text(encoding="utf-8"))
    if not cards:
        sys.exit("Error: no cards found (cards are separated by '---' lines).")
    if not args.no_key:
        cards = add_key_card(cards, args.format)

    # Output name: <input stem> plus any format tokens it doesn't already
    # carry, e.g. x-cards-3x5.md -> x-cards-3x5.pdf, x-cards-3x5-sheet.pdf.
    tokens = {"3x5": ["3x5"], "3x5-sheet": ["3x5", "sheet"],
              "letter": ["letter"]}[args.format]
    if args.paper == "a4":
        tokens.append("a4")
    if args.size:
        tokens.append(f"{args.size:g}pt")
    elif args.large:
        tokens.append("large")
    name = src.stem
    for t in tokens:
        if not re.search(rf"(^|-){re.escape(t)}(-|$)", name):
            name += "-" + t
    use_html = args.html
    if not use_html:
        try:
            import reportlab  # noqa: F401
        except ImportError:
            print("reportlab is not installed; writing printable HTML instead.\n"
                  "For a direct PDF: pip install reportlab", file=sys.stderr)
            use_html = True

    if args.large:
        FORMATS["3x5"]["size"], FORMATS["letter"]["size"] = 10.0, 12.0
    if args.size:
        for g in FORMATS.values():
            g["size"] = args.size
    if FORMATS["3x5"]["size"] > 8.0:
        # Larger type on a small card: tighten spacing to keep scene cards
        # on one card.
        FORMATS["3x5"].update(leading=1.2, gap=0.4)
    ext = ".html" if use_html else ".pdf"
    out = Path(args.out).expanduser().resolve() if args.out else \
        src.with_name(name + ext)

    if use_html:
        render_html(cards, args.format, args.paper, out)
        print(f"Wrote {out}  ({len(cards)} cards; open in a browser and "
              f"print to PDF)")
        return

    report = render_pdf(cards, args.format, args.paper, out, args.font)
    if args.json:
        print(json.dumps({"output": str(out), "cards": report}, indent=2))
        return
    size = FORMATS["3x5" if args.format.startswith("3x5") else "letter"]["size"]
    total = sum(r["faces"] for r in report)
    print(f"Wrote {out}  ({len(report)} cards, {total} printed, "
          f"all at {size:g}pt)")
    multi = [r for r in report if r["faces"] > 1]
    for r in multi:
        note = ("  <- scene card: tighten to fit one card" if r["scene"]
                else "")
        print(f"  card {r['card']:>3} runs to {r['faces']} cards: "
              f"{r['title']}{note}")

if __name__ == "__main__":
    main()
