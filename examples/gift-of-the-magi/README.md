# Worked example: "The Gift of the Magi"

O. Henry's 1905 story (about 2,000 words, public domain) run through both skills. It's short enough to read in ten minutes and check every claim in the analysis against the text.

| Step | File | What it shows |
|---|---|---|
| Source | [`gift-of-the-magi.md`](gift-of-the-magi.md) | The text, from *The Four Million* (1906) via Wikisource |
| Checkpoint | [`01-scene-list.md`](01-scene-list.md) | The scene list and cast list `crews-analysis` presents for confirmation before analysing, with the boundary calls flagged |
| Analysis | [`gift-of-the-magi-crews-analysis.md`](gift-of-the-magi-crews-analysis.md) | The full CREWS analysis: overview, seven scenes, cross-scene patterns, "Who hired the CREWS?" |
| Micro cards | [`gift-of-the-magi-cards-3x5.md`](gift-of-the-magi-cards-3x5.md) → [PDF](gift-of-the-magi-cards-3x5.pdf), [large-print PDF](gift-of-the-magi-cards-3x5-large.pdf) | 3×5 cards, one per 5×3 in page, for printing straight onto index cards (8pt; large print 10pt) |
| Letter cards | [`gift-of-the-magi-cards-letter.md`](gift-of-the-magi-cards-letter.md) → [PDF](gift-of-the-magi-cards-letter.pdf) | One page per scene for close review |

Each deck has a key card after the cover; [Reading the cards](../../docs/reading-the-cards.md) explains the fields and symbols in full.

## What to look for

- **A non-reversal.** Scene 05 builds to the climax the reader expects (Jim's verdict on Della's cut hair) and then doesn't deliver it. The rhythm string `r r r r N R R` shows how that defused climax sets up the double reversal in 06.
- **Two reversals on different axes.** 06 reverses the couple's fortune; the narrator's coda (07) reverses the story's judgment of them, from "foolish" to "wisest".
- **Choreography of knowledge.** The narration stays with Della, so her secret looks like the only one (misdirection); in 05 the narrator looks away (screening) and openly promises a payoff.
- **A transparency seam.** Jim's combs appear only at the moment of payoff. The analysis notes that focalisation explains why Jim's purchase is hidden, but not why Della's own long desire for the combs was never shown.
- **A claim-scope check.** The plot is compatible with both "foolish" and "wisest"; the analysis points out that the story settles the question by declaration in the coda, not by anything the plot demonstrates.

## Regenerating the PDFs

From the repository root:

```bash
cd examples/gift-of-the-magi
python3 ../../crews-cards/scripts/make_cards.py gift-of-the-magi-cards-3x5.md --format 3x5
python3 ../../crews-cards/scripts/make_cards.py gift-of-the-magi-cards-3x5.md --format 3x5 --large
python3 ../../crews-cards/scripts/make_cards.py gift-of-the-magi-cards-letter.md --format letter
```
