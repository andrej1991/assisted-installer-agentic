---
name: triage-mgmt-issues
description: Grade unassigned bugs in the MGMT Jira project in To Do or New status, using one jira-triage-complexity subagent per issue.
---

# Triage MGMT Issues

## Inputs and prerequisites

Require Jira read access, subagent dispatch, and worker access to
`jira-triage-complexity` from `assisted-installer-skills`. Discover that skill
through the harness and load its public contract and the
[workflow report contract](references/report-contract.md). Block if unavailable.

The invoker supplies authenticated Jira read access and handles the choice of
client, provider-specific query syntax, and pagination mechanics. This workflow
defines the canonical JQL, required evidence, ordering, and completeness checks;
it must not prescribe a Jira client or embed provider-specific commands. Use
the supplied capability and return `blocked` if it cannot satisfy those checks.

Optional inputs: repository context, local report path, parallel workers
(default 4, capped by harness capacity), worker timeout (default 10 minutes), and
maximum issues (default all). Limits must be positive; worker/issue counts must
be integers. "Stop after N issues" limits assessments, not concurrency.

## Retrieve the issue set

1. Verify access to the `MGMT` project and search with this exact JQL:

   ```jql
   project = MGMT AND issuetype = Bug AND assignee IS EMPTY AND status IN ("To Do", "New") ORDER BY key ASC
   ```

2. Complete pagination even for limited assessments, deduplicating by key while
   preserving query order. Retain issue payloads, sources, and report metadata.
   On retrieval failure or uncertain completeness, return `blocked` with discovered
   keys and the error; dispatch nothing.
3. Freeze the first N keys when limited, otherwise all keys. Never replace failed
   assessments or poll for new work. Successful retrieval with no matches returns
   `empty`. Selection covers caller-visible issues during retrieval, not a snapshot.

## Dispatch and collect

Queue one dedicated subagent per selected issue within the concurrency limit.
Give each worker its issue payload and sources, repository context, discovered
skill identity, worker response contract, and these instructions:

> Load and use `jira-triage-complexity` from `assisted-installer-skills` for this
> issue only. Follow its rubric and contract, fetching additional context only
> when needed. Do not select issues, delegate, write files, mutate Jira/source,
> or run tests. Return `{skill_used, result, error}` with the skill's unchanged
> JSON result; report loading failure instead of improvising a grade.

Start each timeout at worker launch, excluding queue time. Collect results and
release finished workers when required by the harness. Stop timed-out workers
before reusing their slots. If a slot cannot be released, do not exceed capacity;
mark remaining jobs ungraded if none can proceed.

Validate issue identity, required-skill use, and the shared result contract.
Check loading/invocation traces when available; absent traces mean unverified,
not missing skill use. Without traces, accept an explicit worker declaration
and disclose this verification limit in the summary. Known non-use, missing
declarations, malformed responses, worker failures, and timeouts are ungraded.
Preserve valid results; never retry automatically, substitute skills, or grade
in the parent.

## Output and stopping conditions

Return the aggregate report and optionally save its JSON to the requested local
path. This is the only permitted write; Jira/source remain read-only and no tests
are run.

- `complete`: enumeration finished and every selected issue has a valid grade.
- `partial`: at least one issue was graded and at least one remains ungraded.
- `blocked`: a prerequisite or enumeration failed, or no selected issue could be graded.
- `empty`: enumeration finished with zero matches; no workers were started.

Stop on prerequisite failure; otherwise finish the frozen queue within worker
deadlines and report all outcomes.
