# Coverage map and claim contract

Load before Workflow step 4. Use it to build the Coverage map and Facts sections.

## Coverage map

One row per question. Fields: question, source, answer shape, gap, section.

- **Question:** the wording as supplied or observed, verbatim.
- **Source:** `search results` (related questions shown on a results page), `AI answer` (asked of an assistant), `autocomplete`, `search-performance export`, `supplied notes` (name the file that asks the question), or `inferred`. `inferred` means the topic needs the question but no supplied source shows anyone asking it. Never present an inferred question as observed.
- **Answer shape:** direct, definition, list, table, steps, or comparison. The shape sets the block the page carries.
- **Gap:** write a gap only when an observed answer shows one. Gap types: `brand absent` (the business is missing from the observed answers), `answer incomplete` (the observed answers do not answer the question), or `weak source` (the answer leans on a thin source that a solid page could replace). Write the observed reason beside the type. If nothing was observed, write `not measured`. A page nobody read is not a gap.
- **Section:** the outline heading that answers the question. Every question appears under one heading.

When there are several rows, group them by the job each does for the reader (defines the term, compares options, answers a doubt, or helps with a step in progress) and list gap rows first. If no gap appears, say so in the brief's first lines.

## Claim contract

The Facts section holds three lists. Omit an empty list.

- **May say:** facts with a supplied source, in their approved wording.
- **Must not say:** claims nobody can back, such as invented counts, guarantees, speed claims, or compliance claims.
- **Needs checking first:** comparisons, numbers, outcomes, testimonials, certifications, and prices whose only source is the business's own marketing copy. A claim in this list stays out of the draft until someone confirms it.

## Depth

- Measure depth on the surface the page targets: the sources that AI answers cite, or the top organic results for a search. Count their standalone answers and concrete facts. Word count does not set depth.
- Length follows that count. Heuristic default: when intent calls for one, open with a direct answer of 40 to 60 words. This default is a rule of thumb, not a measured fact.
- Use the question's own wording as the H2 when the question is the reader's.
- When depth is not measured, write `not measured` and set length from the job of the page.

## Failure modes

- **Keyword outline:** headings that repeat the keyword, with no observed questions.
- **Invented question:** a question nobody observed, not labelled `inferred`.
- **Laundered claim:** a homepage claim moved to may say.
- **False ready:** a Ready verdict while claims sit under needs checking first or inputs stay open.
