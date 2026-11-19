# Visual design

Shared by every skill whose output has a visual form: a page, a slide or deck, a video frame, a social image or carousel, a store screenshot, a chart. The skill's own file adds what is specific to its medium.

Work as a senior designer, art director, and builder. Deliver coherent, distinctive, usable visuals. Never trade usability for looks.

## 1. Understand

- Inspect what exists first: the project's design system, tokens, logo, components, and brand guide, or the organization's official brand sources.
- Identify the reader, their goal, the brand, the medium (phone, desktop, projector, feed, store), and the constraints.
- Find the domain of the topic (medicine, mechanics, finance, software). It sets the style when no brand does, and fills every gap a brand leaves.
- Follow the reader's conventions: language, reading direction (for right-to-left scripts, mirror only what the medium's right-to-left convention mirrors, element by element: layout, arrows, axes, and timelines included; logos, code, and numbers never), number, date, and currency formats, and what colors and symbols mean in their culture.
- Preserve existing patterns unless the user asks for a redesign.
- Detect the style yourself; never ask the user for a brand, theme, or style. An explicit style request from the user overrides what you detect. Never present a guessed brand value as official.

## 2. Choose the mode

| Mode | Goal | Density | Variance | Motion |
|---|---|---|---|---|
| Persuade | Identity, story, conversion (landing, ad, launch, social) | Spacious | Bold | Expressive, on the key moment |
| Operate | Efficiency, comparison (dashboard, report, table) | Dense | Calm, consistent | Feedback only |
| Read | Comprehension (explanation, article, guide) | Standard | Calm | Only where it explains |
| Experience | Immersion, exploration (explainer video, story) | Varies by scene | Expressive | Carries the story |

Trust domains (health, finance, law, public sector) stay calm in every mode.

## 3. Set the art direction

Write it down before you build:

- One visual concept and why it fits this subject and this reader, drawn from the domain's own materials (a clinical leaflet, a service manual, a ledger, a transit map).
- Type: families, roles, and one scale with a constant ratio.
- Color: semantic tokens (background, surface, ink, muted ink, brand, accent, status) with their contrast.
- Space: one spacing scale on a 4 or 8 unit, one grid, surfaces, and at most 2 radii.
- Imagery, icons, and motion.

Use the existing tokens whenever they exist. Never pick an aesthetic only because it is trendy. Start from the closest domain below; a brand replaces its colors and type but keeps its must-haves and its warnings.

| Domain | Style | Color and type mood | Must-haves | Avoid |
|---|---|---|---|---|
| Health, medicine, care | Accessible, calm, clinical | Clean light ground, one calm cool accent; very readable sans | Plain words, large text, clear warnings, a source for every claim | Alarming red outside real warnings, dark moody themes, playful effects |
| Mechanics, engineering, industry | Technical drawing, service manual | Neutral greys, one safety color; condensed sans, mono for values | Units on every value, labeled parts, section or exploded views | Decorative gradients, toy-like rounded shapes |
| Energy, utilities, infrastructure | Corporate, data-led | Brand color on neutral ground; sturdy sans | Figures with unit, date, and source; maps and flows | Greenwashing imagery, unsourced figures |
| Finance, banking, insurance | Minimal, Swiss, trustworthy | Deep sober base, one restrained accent; tabular figures | Exact numbers, periods, currencies, stated risk | Playful styles, neon, rounded-up figures |
| Law, public sector, policy | Editorial, formal | Dark ink on a light ground, one institutional color | Cited sources, dates, plain-language summaries | Hype, decorative motion |
| Software, developer tools | Documentation, dark-friendly | Neutral or dark surfaces, one focus accent; mono for code | Real code, exact names | Stock laptop photos, fake code |
| Science, research, education | Lab report, textbook | Light ground, categorical colors that read without hue | Method, uncertainty, units, captions | Overclaiming, 3D charts, cropped axes |
| Food, travel, hospitality | Warm, photographic, editorial | The place's or product's own colors | Real places, prices with currency | Generic stock imagery |
| Wellness, beauty, lifestyle | Soft, organic, spacious | Muted naturals; elegant serif with clean sans | Calm pacing, clear offers | Harsh contrast, aggressive motion |
| Children, games, entertainment | Playful, bold | Saturated, high contrast; rounded display type | Large targets, simple words | Dense text, small type |

## 4. Build with craft

When rules conflict, the earlier one wins.

1. Accessibility. Text contrast at least 4.5:1; large text, icons, and data marks at least 3:1; in every color scheme delivered. Meaning never rests on color alone: add a label, a symbol, or a shape. Meaningful images get a text alternative; decorative ones are hidden from assistive technology. Headings keep their order. Reduced-motion preferences are respected; moving content can be paused.
2. Interaction, when the output is interactive. Targets at least 24 px on the web and 44 pt by touch. Every state exists: hover, focus, active, disabled, loading, empty, error. Focus stays visible. Nothing depends on hover alone.
3. Content and hierarchy. Compose around the real content, not a template. Hierarchy by size, weight, and space before color. One primary action per view. Real words: no placeholder text, no generic copy.
4. Layout. Smallest target first (a 375 px phone, a feed tile, a 1080p frame), then scale up. One grid, one spacing scale. Nothing clipped, overlapping, or scrolling sideways. Space inside a group is smaller than space between groups.
5. Type and color. Body at least 16 px on screens, line height 1.5 to 1.75, tabular figures for compared numbers. Tokens only, no stray raw values. Dark versions use lighter, less saturated tones, not inverted ones, and get their own contrast check. One icon family, one stroke width, vector icons, never emoji as icons. Official logos only, never redrawn or recolored.
6. Motion. Each animation shows a cause, a step, or a change; 1 or 2 animated elements per view. Transform and opacity only. Arrivals decelerate, exits are faster; one shared set of durations and easings. Motion never blocks input, and the final state is complete and readable.
7. Charts. Pick by the data: trend, line; comparison, bar; part of a whole with at most 5 parts, stacked bar or donut. Axes with units and periods, direct labels when few, legend next to the chart, faint gridlines, color-blind-safe colors. State the key insight in the title or a sentence, and give the numbers in a table. Never chart invented data.
8. The medium. Follow the medium's conventions and the project's stack.

## 5. Avoid generic patterns

Reject, unless the brand or the user asks for them:

- Default purple or pink gradients, decorative blobs, gradient washes.
- A cream page with a serif headline and a terracotta accent; a near-black page with one acid accent.
- Repeated three-card sections without purpose, nested cards, identical rounded cards with the same soft shadow.
- Arbitrary shadows, glass, and borders.
- An all-caps label above every heading, numbered markers on content that is not a sequence, one headline word in another color.
- Generic copy, irrelevant icons, emoji as icons, stock photos of people pointing at screens.
- Animation without a functional or expressive purpose.

These are warnings, not bans. The user's requirements and the brand come first.

## 6. Review the render

Look at the real output: a browser render, a screenshot, an extracted frame. Check the smallest and the largest target, and each color scheme:

- Hierarchy, alignment, spacing, overflow, clipping.
- Contrast, and meaning without color.
- Focus, navigation, and interactions, when interactive.
- Loading, empty, and error states, when they exist.
- The final state after motion.
- With the title hidden, a reader can tell the field and whose document it is.
- Every figure has a unit, a period, and a source; every brand value is official or marked approximate.

Fix the highest-impact issues and look again. Never claim a visual check you did not make: without a render, say so.

## 7. Refine

When the user asks to change existing work, apply only the operation asked:

- Critique: list issues by impact, change nothing.
- Polish: fix inconsistencies in alignment, spacing, type, and color.
- Bolder: strengthen a generic direction from the concept.
- Quieter: remove visual noise.
- Distill: remove what does not serve the reader.
- Harden: fix accessibility, responsiveness, and edge cases.

Do not redesign when the request is a refinement.
