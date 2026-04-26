// Preamble for CREWS micro cards (3x5 inches).
// Verdana 8pt, tight margins, no headers or footers.
// Each Markdown thematic break (---) becomes a weak page break;
// card title lines are plain bold text, not headings.

#set page(width: 5in, height: 3in, margin: 0.2in)
#set text(font: "Verdana", size: 8pt)
#set par(leading: 0.5em, spacing: 1.0em)

// pandoc emits #horizontalrule for "---" in markdown; make it a pagebreak
#let horizontalrule = pagebreak(weak: true)
