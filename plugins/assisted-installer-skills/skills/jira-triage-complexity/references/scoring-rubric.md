# Complexity rubric

Rate implementation scope, design and integration work, risk, coordination, and
validation burden. This is an ordinal planning aid, not duration, story points,
or priority.

| Score | Anchor |
| --- | --- |
| 1 | Trivial, isolated change with an obvious check. |
| 2 | Small change with a known approach and straightforward validation. |
| 3 | Bounded fix or enhancement requiring modest investigation and focused tests. |
| 4 | Contained component change with limited design choices and several affected paths. |
| 5 | Moderate feature or fix involving interfaces or substantial test changes. |
| 6 | Significant integration or design work with demanding validation. |
| 7 | Major compatibility or design tradeoffs and substantial coordination or regression testing. |
| 8 | Broad change with high operational, security, or data risk and extensive validation. |
| 9 | Architectural change or migration with complex dependencies and rollout planning. |
| 10 | Exceptionally complex change combining deep design, difficult integration, and extensive validation or rollout demands. |

Choose the best-fitting anchor and explain the dominant factors; do not average
dimensions or default to the highest plausible score. Repository and file counts
alone do not determine complexity. A mechanical change across repositories can
be simple, and a single-repository redesign can be a 10.

## Confidence and uncertainty

- `high`: requirements and the relevant implementation and validation paths are
  supported by evidence; no material assumptions affect the score.
- `medium`: the approach is supported but some bounded assumptions remain.
- `low`: a provisional rating is defensible; state assumptions that could change it.

Missing access or vague descriptions are evidence gaps, not proof of difficult
work. Actual research or design decisions required by the task can add
complexity. If unresolved alternatives prevent a defensible rating, return
`blocked` with a null score and confidence and the smallest needed clarification.
