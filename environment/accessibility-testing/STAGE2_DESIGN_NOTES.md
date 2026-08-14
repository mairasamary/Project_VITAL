# Stage 2 Design Notes

## Why authenticated baseline tests do not fail on axe violations

OpenEMR is an existing production-scale open-source application. The course objective is to teach students to discover, interpret, and reason about accessibility issues.

If CI simply required the entire existing interface to have zero axe violations, existing baseline issues could make every student branch red before students change anything.

Therefore Stage 2 first establishes the actual baseline.

Later CI should distinguish:

```text
known baseline issue
new regression introduced by student/change
```

or test a scoped component/interface where an explicit threshold is meaningful.

## Keyboard automation limitation

The focus-sequence test records what receives focus and selected CSS properties. It does not prove:

- logical focus order;
- usability of the focused control;
- meaningful visible focus;
- absence of every keyboard trap;
- screen-reader usability.

Human evaluation remains required.

## Authenticated credentials

Only the local synthetic/course OpenEMR credentials are used.

Do not commit passwords or hard-code them into tests.
