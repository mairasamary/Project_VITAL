# Project VITAL — Authenticated Accessibility Manual Audit

Use this after the Stage 2 automated scans.

## Target 1 — Authenticated landing page

### Keyboard-only navigation

Without using the mouse:

- [ ] Can you reach the major navigation controls?
- [ ] Is focus visible at every step?
- [ ] Does focus move in a logical order?
- [ ] Can you activate controls with keyboard conventions?
- [ ] Can you escape menus/dialogs without becoming trapped?

Record at least one example where the automated `keyboard-focus-sequence.json` did or did not match your human experience.

### Zoom and reflow

At browser zoom levels such as 200%:

- [ ] Is important content still available?
- [ ] Is horizontal scrolling required for ordinary reading?
- [ ] Do controls overlap?
- [ ] Are menus/dialogs still usable?

### Labels and instructions

- [ ] Do controls have visible labels?
- [ ] Are icon-only controls understandable?
- [ ] Does visible text agree with the accessible name?
- [ ] Are status/error messages understandable?

---

## Target 2 — Patient finder

### Keyboard-only search flow

Attempt a simple patient-finder task using keyboard only.

- [ ] Reach the search controls.
- [ ] Understand what each field does.
- [ ] Enter a search value.
- [ ] Execute the search.
- [ ] Navigate the results.
- [ ] Identify whether focus moves unexpectedly.

### Structure

- [ ] Is there a meaningful page title?
- [ ] Are headings/regions understandable?
- [ ] Are result controls/links distinguishable?
- [ ] Are tables/lists understandable without relying only on visual layout?

---

## Automated versus manual evidence

### Automated finding requiring interpretation

Rule:

Observed element:

What axe reported:

What you observed manually:

Your conclusion:

### Manual finding not adequately established by automation

Property:

Steps:

Observed behavior:

Relevant WCAG principle/success criterion (if known):

Why automation alone was insufficient:

---

## Do not conclude

Do not write:

> "The page is accessible because axe passed."

Instead state the limited evidence that your automated and manual tests actually establish.
