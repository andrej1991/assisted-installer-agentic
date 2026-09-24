# Jira Triage Complexity

Grades one Jira issue's implementation complexity from 1–10, with confidence,
reasoning, and sources. Accepts an issue key, URL, or supplied record; repository
context is optional. It does not assess suitability for AI handling.

Returns a JSON assessment or an explanation of why grading is blocked. Jira and
source access are read-only; a local report is written only when requested.
Batch selection and delegation belong to workflows.

See [SKILL.md](SKILL.md) for the execution instructions and report contract.
