# Single-issue report contract

Return one JSON object with all fields below, including for blocked requests.
Use JSON null for unavailable scalar values and empty arrays for unavailable
collections. No run counts or batch records are needed.

| Field | Value |
| --- | --- |
| `issue_key` | Issue key, or null if no single issue was identified. |
| `issue_url` | Known Jira URL, or null; do not invent a URL. |
| `summary` | Issue summary, or null if unavailable. |
| `status` | `complete` or `blocked`. |
| `score` | Integer 1–10 when complete; null when blocked. |
| `confidence` | `high`, `medium`, or `low` when complete; null when blocked. |
| `rationale` | Short explanation of the rating's dominant factors, or why grading is blocked. |
| `evidence` | Array of objects with `source` and `observation` strings. Cite issue/comment URLs or repository paths with lines; identify caller-supplied records when no link is available. |
| `unknowns` | Array of missing facts or explicit assumptions that affect the rating. |
| `validation` | Array of likely tests or checks, inferred from available evidence; do not execute them. |
| `next_action` | Smallest useful next step or clarification. |
| `report_file` | Object with `path`, `status`, and `error`, as defined below. |

Optional report-file delivery is independent of assessment:

- No output path requested: `path: null`, `status: "not_requested"`, `error: null`.
- Written: requested `path`, `status: "written"`, `error: null`.
- Write failed: requested `path`, `status: "failed"`, and the actual error string.

When writing is requested, save the same JSON result and return it to the caller.
On write failure, return the result with updated `report_file` fields, retaining the
score and assessment status. Supplied evidence must not be represented as a fresh
Jira fetch or an atomic snapshot.
