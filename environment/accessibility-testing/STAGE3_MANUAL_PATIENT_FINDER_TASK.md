# Stage 3 — Manual Patient Finder Accessibility Task

Use the real local OpenEMR patient finder.

## Task

Using the keyboard only:

1. navigate to or open the Patient Finder;
2. reach a patient-search input;
3. enter a search value;
4. execute the search;
5. navigate into or through the results;
6. return to the search controls.

## Record

### Operability

- Was every required control reachable?
- Was there any keyboard trap?
- Did standard Enter/Space behavior work where expected?

### Focus

- Was focus visible at every step?
- Did focus order match the visual/logical workflow?
- Did focus unexpectedly move after the search?

### Names and instructions

- Could you determine the purpose of each search control?
- Were buttons/links understandable without relying on icon appearance?
- Did the result controls communicate their purpose?

### Automated comparison

The patient-finder axe baseline included findings such as:

```text
aria-hidden-focus
color-contrast
html-has-lang
```

Pick at least one automated result and manually investigate whether/how it affects the task.

### Manual-only observation

Identify at least one accessibility property that the axe output did not establish.

Do not conclude that the workflow is accessible solely because the task was technically possible.
