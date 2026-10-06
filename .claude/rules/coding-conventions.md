---
description: Reference when writing or editing Python code. Covers style, naming, docstrings, type hints, and CLI conventions.
globs:
  - "**/*.py"
alwaysApply: false
---

# Coding conventions

Python coding rules for `src/memfit/` and `tests/`.

## Python style

### General

- **PEP 8** with project overrides
- **Google-style docstrings** on every public module, class, and function
- **Ruff** for formatting and linting; rule sets are selected in `[tool.ruff.lint]` in `pyproject.toml`
- **ty** (Astral) for type checking, run as a pre-commit hook
- Python **3.10+** target
- All public functions and classes carry **type hints**
- **Standard library only** — `memfit` has no runtime dependencies; do not add any
- **uv only** — do not use `pip install`, `python` directly, or `source .venv/bin/activate`

### Line length and indentation

- **Max line length**: 119
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: double quotes for strings

### Naming

- **Functions and variables**: `snake_case` (e.g. `weight_bytes()`, `context_len`)
- **Classes**: `CapWords` (e.g. `ModelSpec`, `DeviceSpec`)
- **Modules**: `snake_case` (e.g. `capacity`, `catalog`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g. `GIB`, `WEIGHT_BITS`)
- **Private**: single leading underscore

### Docstrings

- Triple double quotes
- First line: short imperative summary, terminated with a period
- For non-trivial functions: Args / Returns / Raises sections
- Google style; types live in type hints, not in the docstring

```python
def weight_bytes(model: ModelSpec, quant: str) -> int:
    """Return the memory used by the model weights, in bytes.

    Args:
        model: The model to size.
        quant: Quantization scheme, one of the keys of ``WEIGHT_BITS``.

    Returns:
        Weight memory in bytes.

    Raises:
        ValueError: When ``quant`` is not a key of ``WEIGHT_BITS``.
    """
```

### Imports

- stdlib → third-party → local, separated by blank lines
- Use absolute imports (`from memfit.capacity import ...`)

## Capacity math (`src/memfit/capacity.py`)

- Functions are **pure**: no I/O, no globals mutated.
- **Integer math only**: sizes are exact byte counts. Use `//`, never `/`, `round()`, or floats.
  Conversion to GiB for display happens in `cli.py` only.
- Specs are frozen dataclasses (`ModelSpec`, `DeviceSpec`).
- Invalid input raises `ValueError`; "does not fit" is a normal result (`0`), not an error.

### Docstrings here are the demo agent's specification

The demo agent implements each function from its docstring alone, so:

- Keep the `Formula:` block literal and complete — it should translate to code line by line.
- Use the exact field and constant names from the code.
- The demo agent's code must pass Ruff as written, so keep the stubs lint-clean and the formulas
  short enough to fit in 119 columns.
- Do not change signatures, constants, or dataclass fields without updating `AGENTS.md`,
  the scenario table in `tests/test_capacity.py`, and `README.md` together.

## CLI conventions (`src/memfit/cli.py`)

- Use **argparse** (standard library).
- Keep the CLI thin: parsing and formatting only. All math lives in `capacity.py`.
- `print()` is allowed in `cli.py` only (Ruff `T20` is ignored for that file and enforced everywhere else).
- Provide a short option for every long option (`-d/--device`, `-c/--context`, `-m/--model`).
- `main()` returns the process exit code.
- Help text and table output are in English.

## Tests (`tests/`)

- One test function per scenario, named `test_s<N>_<what>`.
- Expected values are exact integers taken from the scenario table; never recompute them with the
  formula under test.
- Test functions carry type hints (`-> None`); docstrings are optional (Ruff `D` is ignored under `tests/`).
