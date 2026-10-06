# memfit agent guide

`memfit` answers one question for an AI accelerator: **does this LLM fit in device memory, and how many
concurrent requests can it serve?**

## Files

| Path | Status | What to do |
|---|---|---|
| `src/memfit/capacity.py` | TODO | Implement the 3 functions marked `# TODO: implement` |
| `tests/test_capacity.py` | TODO | Implement test scenarios S1-S6 listed in the module docstring |
| `src/memfit/catalog.py` | Done | Do not edit, no need to read |
| `src/memfit/cli.py` | Done | Do not edit, no need to read |

## Workflow

When the user asks you to implement or complete `memfit`, do these four steps in order.
Do not stop or ask for confirmation between steps.

1. **Plan.** Read `src/memfit/capacity.py` and `tests/test_capacity.py`, and nothing else.
   Then tell the user your plan in at most 5 short bullets.
2. **Implement.** Replace the three `raise NotImplementedError` bodies in `src/memfit/capacity.py`.
   The exact formula for each function is in its docstring. Follow it literally.
   Write code that already satisfies the lint rules below.
3. **Test.** In `tests/test_capacity.py`, write one test function per scenario (S1-S6) with the exact
   values from the table. Then run lint and tests together with this single command:

   ```bash
   uv run --no-sync ruff format . && uv run --no-sync ruff check . && uv run --no-sync pytest
   ```

   Ruff must report `All checks passed!` and all 6 tests must pass.
   If Ruff reports an error, fix the code it points at. If a test fails, fix the implementation.
   Never change the expected values.
4. **Demo.** Run the real program:

   ```bash
   uv run --no-sync memfit --device accel-48g
   ```

   Then summarize the table in 2-3 sentences: which models fit, and how quantization changes the
   maximum number of concurrent requests.

## Lint rules (enforced by Ruff)

Keep these in mind while writing code, so the check passes on the first run:

- Lines are at most 119 characters. Indent with 4 spaces. Use double quotes.
- Names: `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants.
- No `print()`, no unused imports, no unused variables.
- Keep every existing docstring exactly as it is. Put your code below the docstring.
- Add type hints to test functions: `def test_s1_weight_bytes_fp16() -> None:`.
- Do not add `# noqa` comments or edit `pyproject.toml` to silence an error. Fix the code instead.

## Rules

- Run everything through `uv run --no-sync ...`. Never use `pip`, bare `python`, bare `pytest`,
  `uv sync`, or `uv add`.
- Standard library only. Do not add dependencies or create new files.
- Do not change function signatures, constants, dataclasses, or docstrings.
- Integer math only: use `//`, never `/`, `round()`, or floats.
- Keep it minimal: no extra features, no refactoring, no tests beyond S1-S6.
- Do not run `git` or `pre-commit`.
- Write code and comments in English. Talk to the user in Korean.
