# Triage MGMT Issues

Finds all visible unassigned bugs in the `MGMT` Jira project in `To Do` or `New`
status. Dispatches one subagent per selected issue using `jira-triage-complexity`
and returns a summary table and JSON report of grades and failures.

Requires Jira read access, the `assisted-installer-skills` plugin, and a harness
with subagent support. Optional inputs include repository context, an assessment
limit, concurrency, worker timeout, and a local report path. Limited runs still
enumerate all matches before selecting issues.

Jira and source access remain read-only; only a requested local report is written.
See [SKILL.md](SKILL.md) for the execution instructions and report contract.
