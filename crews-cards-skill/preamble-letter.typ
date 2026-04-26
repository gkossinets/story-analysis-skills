// Preamble for CREWS letter cards (8.5x11 inches).
// Verdana 11pt body, no headers or footers.
// Each Markdown thematic break (---) becomes a weak page break;
// card title lines are plain bold text, not headings.

#set page(paper: "us-letter", margin: 1in)
#set text(font: "Verdana", size: 11pt)
#set par(leading: 0.65em, spacing: 1.2em)

// pandoc emits #horizontalrule for "---" in markdown; make it a pagebreak
#let horizontalrule = pagebreak(weak: true)
