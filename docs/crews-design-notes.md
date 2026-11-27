# CREWS: design notes and sources

How the CREWS framework was put together, which ideas came from where, and what it is for. The [README](../README.md) covers installation and usage; the full dimension definitions are in [`crews-analysis/SKILL.md`](../crews-analysis/SKILL.md).

---

## Approach

CREWS began as a personal method for a second, slow reading of a work: read once quickly, then go scene by scene and record *what changes* between each scene's first moment and its last. The starting list was a writer's list (who enters and exits; archetypes; circumstances; objectives; stakes; status; perspective; subtext). It was then checked against a shelf of craft books on playwriting, screenwriting and fiction, and expanded with the ideas that each book handles best.

The framework came out of repeated trimming, not accumulation. The working rule was that a dimension stays only if it catches something the others miss and changes what a writer would do. Every version was tested on real texts before it was kept, and the results of those tests drove most of the later changes (see [Testing history](#testing-history)).

Three commitments held throughout:

- **Change over description.** Each dimension asks what shifts in the scene, not what is there.
- **No privileged tradition.** Western conflict-climax structure is one story shape among several (kishotenketsu, episodic, spiralling); the framework asks which shape the material has rather than measuring it against one.
- **Mechanisms, not paraphrase.** The analysis names the craft choice that produces an effect; it avoids restating the work's own imagery in the analyst's voice.

## Where each element comes from

| Element | Main sources | Notes |
|---|---|---|
| 1. Characters present and complexity revealed | Thomas; Ball; Rabiger | Replaced the original "archetypes (revealed and hidden)" with Thomas's type / intermediate / complex scale, which tracks how much inner life a scene reveals |
| 2. Status and power dynamics | Thomas; Edgar; Rabiger | Edgar's distinction between office, rank and character |
| 3. Subtext | Rabiger; Thomas; Salesses | Salesses's inside/outside story |
| 4. Format and ritual | Edgar; Thomas | Trials, ceremonies, meetings and checkpoints as borrowed dramatic structures |
| 5. Circumstances, stasis, and intrusion | Ball; Thomas; Lowe | Ball's stasis/intrusion folded into Thomas's given circumstances; Lowe's story-world vs. primary narrative added later |
| 6. Objectives and the A→B→C pattern | Thomas; Rabiger; Cowgill; Ball; Squire | Reveal vs. reversal from Ball (as Squire credits it); the "go for A, get B" phrasing, the C step (the character adapts within the scene) and the reveal/reversal alternation diagnostic as set out by Squire |
| 7. Stakes | Cowgill; Gulino; Kress; Lowe | Gulino's hope vs. fear; Lowe's forms of narrative power |
| 8. Choreography of knowledge and dramatic irony | Edgar (via Michael Eaton); Gulino; Ball; Salesses | Gulino's revelation and recognition; Salesses's "what is left out, and for whom" |
| 9. Dangling causes and payoffs | Gulino; Kress; Cowgill | Gulino's dangling causes; Kress's promises to the reader; Cowgill's plant and payoff |
| 10. Perspective and narration | Salesses; Rabiger | "Whose scene is it?" |
| 11. Information management | Ball; Thomas; Rabiger; Salesses; Lowe | Merges exposition technique, tempo and information density; Lowe's postponement, screening and misdirection as modes of withholding |
| 12. Mood and atmosphere | Thomas; Rabiger | Thomas's split between interior mood and external atmosphere |
| S: "Why is this scene compelling?" | Vaughan (*Story and Plot*), via Squire | An evaluative check on connective scenes that do a job but don't earn attention |
| Meta-question: "Who hired the CREWS?" | Salesses; Lowe | Implied reader, implied author, what is left out, story shape (Salesses); transparency and control level (Lowe) |
| Scene vs. chapter; screenplay-sense scene definition | Thomas; Rabiger; French scenes | Hardened after a test on contemplative prose (see below) |
| Temporal orbits | Original to CREWS | Unit of analysis for prose that resists scene breaks; came out of the Krasznahorkai test |
| Non-reversal | Original to CREWS | A place where a reversal is expected and deliberately withheld; identified during the Pelevin test |
| Scene cards for a wall | Frank Daniel, via David Lynch | The 3×5 scene-card method; implemented in the companion `crews-cards` skill |

Full citations:

- David Ball, *Backwards and Forwards*
- James Thomas, *Script Analysis for Actors, Directors, and Designers*
- Damon Kiely, *How to Read a Play*
- David Edgar, *How Plays Work*
- Paul Gulino, *Screenwriting: The Sequence Approach*
- Matthew Salesses, *Craft in the Real World*
- Linda Cowgill, *Writing Short Films*
- Nancy Kress, *Beginnings, Middles and Ends*
- Michael Rabiger, *Directing*
- N. J. Lowe, *The Classical Plot and the Invention of Western Narrative*

Kiely's active reading and dramatic action informed the reading method generally rather than a single dimension. Squire, Vaughan and the Frank Daniel scene-card method are cited in full under [Attribution corrections](#attribution-corrections).

### Attribution corrections

- **A→B→C and reveal/reversal.** These came into CREWS through Aurin Squire, "[Writing Tip: Go for A and Get B](https://sixperfections.blogspot.com/2026/04/writing-tip-go-for-and-get-b.html)," *Six Perfections*, April 6, 2026. The post sets out the whole pattern. A scene goes for A and gets B, which is either a reveal or a reversal. Good scenes stop at B; great ones add a C, in which the character adapts or transforms. A story should alternate reveals and reversals, because a run of reversals feels melodramatic and a run of reveals feels flat. Squire credits the reveal/reversal framework to David Ball's *Backwards and Forwards*. CREWS credits Ball for the distinction and Squire for the A→B→C formulation and the alternation rule.
- **"Why is this scene compelling?"** This came into CREWS through Aurin Squire, "[5 Questions for Scene Analysis](https://sixperfections.blogspot.com/2026/04/5-questions-for-scene-analysis.html)," *Six Perfections*, April 5, 2026. Squire says the questions are based on a *Story and Plot* article. That article is Tom Vaughan, "[Five Questions For Every Scene](https://storyandplot.substack.com/p/five-questions-for-every-scene)," *Story and Plot* (Substack), March 27, 2025 ([mirror](https://theweeklyemail.storyandplot.com/five-questions-for-every-scene/)). Vaughan's fifth question asks what makes a scene worth watching in its own right; the wording CREWS uses is Squire's.
- **Scene cards for a wall.** The method is usually credited to David Lynch, but Lynch credits it to Frank Daniel, who taught him film analysis at the AFI's Center for Advanced Film Studies (from 1970). Daniel's version: collect ideas for about 70 scenes, one per 3×5 card, and you have a feature. Lynch still worked this way in 1990, though by then he dictated the cards to an assistant. Source: Richard B. Woodward, "[A Dark Lens on America](https://www.nytimes.com/1990/01/14/magazine/a-dark-lens-on-america.html)," *The New York Times Magazine*, January 14, 1990, section 6, p. 18. The skill's calibration range of 60–90 scenes for a feature or novel is consistent with Daniel's number.

### General references and inspiration

These didn't supply specific dimensions, but they shaped the thinking behind CREWS and are good reading alongside it:

- **Lincoln Michel**, [*Counter Craft*](https://countercraft.substack.com/): a newsletter on the craft of fiction writing, how publishing works, and offbeat books.
- **Scott Myers**, "[How I Write A Script (Parts 1–10)](https://gointothestory.blcklst.com/how-i-write-a-script-parts-1-10-2d40d46c89dd/)," *Go Into The Story*, July 6, 2012: a screenwriter's whole process in ten parts, from story concept, brainstorming, research and character development through plotting, outlining, a script diary, the first draft, rewriting and editing.
- **Andrew Bashford**, [*Writing with Andrew*](https://www.youtube.com/@WritingwithAndrew): a YouTube channel on writing principles and techniques, by a writing instructor and teacher trainer.

## Key design decisions

- **Twelve dimensions, five headings.** The candidate list ran to about fifteen. Exposition, tempo and density became one dimension (information management); stasis and intrusion were folded into circumstances.
- **Kept separate on purpose.** Subtext and choreography of knowledge look alike but run on different axes: subtext is vertical (the gap inside a character between surface and interior), knowledge is horizontal (who knows what, across characters and audience). Format and ritual stays distinct from status, because a format's rules can cut against the status of the people inside it.
- **Salesses as a lens, not a thirteenth dimension.** The implied-reader question applies to the whole work, so it became the meta-question ("Who hired the CREWS?") asked after the scene pass. Later tests split it into separate fields (implied reader, implied author, tone, intended effect, craft choices, transparency, story shape), with the craft-choices field written to a three-move template: name the choice, say what it does structurally, connect it to the stance.
- **Selective borrowing from Lowe.** Lowe's "conservation of narrative power" was narrowed to a question about the forms power takes and when it converts from one form to another, so that it also applies to non-Aristotelian shapes. His categories of economy and amplitude were dropped as already covered by existing dimensions. Transparency, control level and the three suspense modes were added.
- **Silent dimensions are signals.** Each scene reports only the dimensions that are live in it. An empty dimension tells you something about the scene; it isn't a gap in the analysis.
- **Human checkpoint before analysis.** The skill proposes a scene list and a cast list (canonical names and aliases), then waits for confirmation. Scene segmentation is where analyses go wrong most often, and it is cheap to fix at that stage.
- **Two skills, one contract.** The original single skill was split into `crews-analysis` (full-form Markdown) and `crews-cards` (compression into printable cards), so that each skill triggers only on its own kind of request. The cards skill depends on the analysis file's heading structure, which is fixed for that reason. A third skill (a shot-list generator) would also fit this split.
- **Cards favour the structural spine.** When a card overflows, description and payoffs are cut first; A→B→C, function and mood are never cut to make the layout fit.

## Testing history

Each test changed the framework:

- **le Carré**, *The Spy Who Came in from the Cold* (ch. 1): the first calibration on tight third-person genre prose.
- **Grin**, *The Golden Chain* (Russian, analysed in English): showed that a story can work as kishotenketsu rather than as a conflict arc; later used for the full card workflow when preparing an adaptation.
- **An unpublished draft chapter by the author of CREWS**: the first cross-scene pattern analysis; it found a gap between the outside story (a successful night) and the inside story (moral compromise).
- **Krasznahorkai**, *Herscht 07769* (ch. 1): led to temporal orbits.
- **Pelevin**, "Crystal World": led to the non-reversal category, the implied-author field and Markdown formatting rules.
- **An original short script by the author of CREWS** (across several drafts): confirmed the framework is useful for revision. The analysis surfaced a passive stretch in the protagonist's arc, which was fixed by reordering scenes.
- **Kehlmann**, *The Director*, and **Turgenev**, "The Singers": the Turgenev run produced too many scene breaks in contemplative prose. This led to the stricter scene definition, the rule that extended description does not break a scene, scene-count calibration ranges, and the checkpoint.
- **O. Henry**, "The Gift of the Magi": the public worked example in [`examples/`](../examples/gift-of-the-magi/).

## Likely use cases

- **Revising your own draft.** Run CREWS on a script or story to find scenes that function without being compelling, plants that are never paid off, long runs of reveals with no reversal, and passive stretches in a protagonist's arc. Then decide what to restructure.
- **Preparing an adaptation.** Break a novel or novella into scenes, print the micro cards, and lay the whole work out on a wall to see what to keep, compress, reorder or relocate.
- **Studying published work.** Analyse a novel, play or film you admire to see how it does what it does: how knowledge is distributed, how suspense is built, what is withheld, and what shape the story takes.
- **Teaching craft.** The meta-section names the mechanism behind each effect, which makes it usable as a basis for workshop discussion, close-reading exercises or lecture examples. Pairing a conventional text with an unconventional one (le Carré with Krasznahorkai, say) shows students the framework adapting to the form.
- **Giving structured feedback.** Use the dimensions as a shared vocabulary for workshop critique, so that feedback is about a specific scene and dimension rather than general impressions.
- **Cross-cultural and cross-language reading.** The implied-reader and story-shape fields bring out the assumptions a work makes about its audience. This helps when reading in translation or across traditions.
