---
description: Reference when creating PRs, writing commits, or naming branches.
globs:
  - "CONTRIBUTING.md"
alwaysApply: false
---

# Contribution guide

This file is the agent-facing quick reference; `CONTRIBUTING.md` at the repo root is the authoritative document for human readers.

## PR title rules

PR titles must match the format `[<TAG>] <body>`, where `<TAG>` is one of:

| Tag | Meaning |
|---|---|
| `FEAT` | A new feature |
| `FIX` | A bug fix |
| `DOCS` | Documentation only changes |
| `STYLE` | Code style changes (formatting, semicolons, etc.) |
| `REFACTOR` | Code refactoring without behavior change |
| `PERF` | Performance improvement |
| `TEST` | Add or correct tests |
| `BUILD` | Build system or external dependency changes |
| `CI` | CI configuration or script changes |
| `CHORE` | Other changes that don't modify src or test files |
| `REVERT` | Revert a previous commit |
| `HOTFIX` | Urgent bug fix |
| `BOT` | Automation (dependabot, uv-lock-update, …) |

- Body must be **English**, 1–150 characters, alphanumeric plus `` _-.,&*[]:/`<>=#+ ``.
- Exactly one space between tag and body.

No workflow validates this in this repository, so check it by hand.

### Examples

- `[FEAT] Add memfit demo template`
- `[FIX] Correct KV cache formula in capacity docstring`
- `[DOCS] Update demo runbook`
- `[CHORE] Tune AGENTS.md for faster demo runs`
- `[BOT] Automated uv.lock update`

## Branch naming

- Format: `<TAG>-<description>` — `<TAG>` is UPPER_CASE and taken from the PR title tag list above; the `<description>` after the first hyphen is lowercase kebab-case.
- Examples:
  - `FEAT-add-memfit-template`
  - `FIX-kv-cache-formula`
  - `DOCS-update-demo-runbook`
  - `BOT-uv-lock-update`

## Commit messages

### Subject

`[tag] <summary>` — English, 50 characters max, imperative mood.

### Body

- Blank line between subject and body.
- Focus on **what** and **why**, not how.
- Imperative ("Add capacity stubs", not "Added capacity stubs").
- For automation or pair work, use `Co-Authored-By:` trailers.

## PR body

There is no PR template in this repository. Cover these in the description:

1. **PR Type** — feat / fix / docs / style / refactor / perf / test / build / ci / chore / revert
2. **Summary of changes** — 1–3 sentences
3. **Related issues** — `Closes SOFT-XXXX` (omit if no Jira ticket)
4. **Detailed description** — what / why / scope of impact
5. **Test plan** — exact commands and outcomes
6. **For reviewers** — anything that needs special attention plus the checklist

## PR checklist

- [ ] `src/memfit/capacity.py` and `tests/test_capacity.py` are still in the unfinished starting state
- [ ] Formulas in docstrings, the scenario table, `AGENTS.md`, and `README.md` agree with each other
- [ ] Expected values in the scenario table were verified against a throwaway implementation (see `build-and-test.md`)
- [ ] Type hints and Google-style docstrings added
- [ ] `uv run --no-sync pre-commit run --all-files` passes
- [ ] Changes to `AGENTS.md` or docstrings were rehearsed with the real demo agent

## Code review criteria

Reviewers focus on:

- **Demo reliability**: can a weak model follow `AGENTS.md` and the docstrings literally and finish in about one minute?
- **Demo integrity**: the template does not ship with the solution, and nothing leaks it (no solved copies, no hints beyond the docstring formulas).
- **Consistency**: formulas, scenario values, and documentation match.
- **Simplicity**: standard library only, few files, no features the demo does not show.
- **Type safety**: every public API has type hints.
