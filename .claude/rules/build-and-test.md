---
description: Reference when changing build, lint, or test setup, or when running validation commands. Covers uv, Ruff, pre-commit, and pytest usage.
globs:
  - "pyproject.toml"
  - ".pre-commit-config.yaml"
  - "src/**"
  - "tests/**"
alwaysApply: false
---

# Build and test guide

`memfit` is a pure-Python project with no runtime dependencies. There is no CI in this repository:
pre-commit is the gate.

## Stack

- **Python**: 3.10+
- **Package manager**: [uv](https://github.com/astral-sh/uv) (build backend: `uv_build`, `src/` layout)
- **Linter / formatter**: Ruff
- **Type checker**: ty (Astral), as a pre-commit hook
- **Commit gate**: pre-commit
- **Tests**: pytest (`tests/`)

## uv environment rules (required)

### Do not

- Do not use `pip install` — use `uv pip install`.
- Do not run `source .venv/bin/activate` — uv manages the environment.
- Do not invoke `python` directly — use `uv run --no-sync python`.
- Do not invoke `pytest` directly — use `uv run --no-sync pytest`.

### Do

- `uv sync` — sync dependencies from `pyproject.toml` (one-time setup, and after changing dependencies).
- `uv run --no-sync pre-commit install` — install the git hook (one-time setup).
- `uv run --no-sync python <script>` — run a Python script.
- `uv lock --upgrade` — refresh the lockfile.

## Validation commands

```bash
# All hooks (authoritative gate; only sees files git knows about)
uv run --no-sync pre-commit run --all-files

# Ruff alone (fast; this is what the demo agent runs)
uv run --no-sync ruff format .
uv run --no-sync ruff check .

# Tests
uv run --no-sync pytest
```

## Lint setup

Ruff rule sets are selected in `[tool.ruff.lint]` in `pyproject.toml`:

| Rule set | Purpose |
|---|---|
| `E`, `W` | pycodestyle |
| `F` | pyflakes (unused imports and variables, undefined names) |
| `I` | import sorting |
| `N` | PEP 8 naming |
| `D` | Google-style docstrings |
| `B` | flake8-bugbear |
| `UP` | pyupgrade |
| `T20` | no `print()` |

Per-file ignores:

- `tests/**` ignores `F401` and `D`. The skeleton ships with imports the demo agent will use, and
  `ruff --fix` must not strip them.
- `src/memfit/cli.py` ignores `T20`; it is the only place allowed to print.

Pre-commit hooks (`.pre-commit-config.yaml`):

| Hook | Target | Purpose |
|---|---|---|
| `ruff-format` | `*.py` | Python format |
| `ruff` (`--fix`) | `*.py` | Python lint with auto-fix |
| `ty-check` | `*.py` | Type check |
| `trailing-whitespace` | all | Strip trailing whitespace |
| `end-of-file-fixer` | all | Ensure final newline |
| `check-yaml` | `*.yml` / `*.yaml` | YAML syntax |
| `check-added-large-files` | all | Block oversized files |
| `markdownlint` | `*.md` | Markdown quality (rules tuned in `.markdownlint.yaml`) |

Keep the `ruff-pre-commit` `rev` in step with the Ruff version in `uv.lock`, so the hook and the
demo agent's `uv run ruff` agree.

### Lint and the demo

The demo agent runs Ruff directly, not pre-commit: Ruff takes milliseconds, while pre-commit needs staged
files and a warm hook cache. `AGENTS.md` lists the rules the agent must keep in mind and gives it one
combined command (`ruff format` + `ruff check` + `pytest`).

When you add or tighten a Ruff rule, check that a straightforward solution still passes it, and add a
matching line to the "Lint rules" section of `AGENTS.md`. A rule the demo agent trips over costs a fix
round-trip inside a one-minute budget.

## Expected results depend on the template state

The template ships unfinished on purpose (see `project-context.md`), so the starting state looks broken:

| Command | Starting state (template) | After the demo agent finishes |
|---|---|---|
| `uv run --no-sync pytest` | `no tests ran` (exit code 5) | `6 passed` |
| `uv run --no-sync memfit` | `NotImplementedError` traceback | Capacity table |
| `uv run --no-sync ruff check .` | Passes | Passes |
| `uv run --no-sync pre-commit run --all-files` | Passes | Passes |

Neither starting-state failure is a bug to fix.

## Verifying a template change without spoiling the demo

When you change formulas, scenarios, the catalog, the CLI, or lint rules, check the result against a
throwaway copy instead of implementing the functions in the repo:

1. Copy `src/` and `tests/` to a temporary directory outside the repo.
2. Fill in the three functions and the six tests in the copy.
3. Run the copy with `PYTHONPATH=<copy>/src uv run --no-sync pytest <copy>/tests`.
4. Lint the solved files with `uv run --no-sync ruff check --config pyproject.toml <copy>/src/memfit/capacity.py`.
5. Confirm `git status` shows no unintended changes under `src/` or `tests/`.

## Tests

- Layout: `tests/` (`testpaths` in `pyproject.toml`)
- File pattern: `test_*.py`; function pattern: `test_*`

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `uv run --no-sync ...` fails with `Failed to spawn` | The environment is not synced. Run `uv sync` once. |
| `uv sync` fails to parse `uv.lock` | The lockfile is empty or corrupt. Delete it and rerun `uv sync`. |
| `pre-commit run` reports `Skipped` or misses files | Hooks only see files git tracks. `git add` new files first, or pass `--files <path>`. |
| First `pre-commit run` is slow | It builds hook environments once (needs network). Run it before the demo, never during. |
| `memfit` output did not change after an edit | The package is installed editable from `src/`; check you edited `src/memfit/`, not a copy. |
