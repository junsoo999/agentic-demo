---
description: Reference when you need the repo's overall purpose and structure. Read this first before adding features or refactoring.
alwaysApply: false
---

# Project context

## Overview

`agentic-demo` is a **live-demo template** for showing a coding agent (opencode) finish a small, meaningful
program in about one minute. The program is `memfit`, a CLI that answers one question for an AI accelerator:
**does this LLM fit in device memory, and how many concurrent requests can it serve?**

## The template is intentionally unfinished

Two files ship incomplete on purpose. The demo agent completes them live.

| Path | Starting state | Completed by |
|---|---|---|
| `src/memfit/capacity.py` | Three functions raise `NotImplementedError`; formulas are in the docstrings | The demo agent |
| `tests/test_capacity.py` | Scenario table S1-S6 in the module docstring, no test functions | The demo agent |

**Do not implement these two files when maintaining the template.** A change that fills them in destroys the
demo. Only complete them when the user explicitly asks to run or rehearse the demo itself, and restore the
starting state afterwards with `git restore src tests`.

## Repository layout

```text
agentic-demo/
├── AGENTS.md                 # instructions opencode follows during the demo
├── src/memfit/
│   ├── __init__.py
│   ├── capacity.py           # dataclasses, constants, and the 3 TODO functions
│   ├── catalog.py            # MODELS and DEVICES used by the CLI
│   └── cli.py                # argparse entry point, prints the capacity table
├── tests/
│   └── test_capacity.py      # scenario table + TINY model fixture
├── docs/assets/logos/        # logo assets referenced from README
├── .claude/rules/            # this directory (agent-facing rules for Claude Code)
├── pyproject.toml            # dependencies, Ruff rule sets, pytest config
├── .pre-commit-config.yaml   # commit-time gate: Ruff, ty, markdownlint, file hygiene
├── uv.lock
├── CONTRIBUTING.md           # contribution guide for human readers
└── README.md                 # demo runbook and memory model
```

## Memory model

| Quantity | Formula |
|---|---|
| Weights | `num_params * WEIGHT_BITS[quant] // 8` (fp16 = 16, int8 = 8, int4 = 4) |
| KV cache per request | `2 * num_layers * num_kv_heads * head_dim * context_len * KV_BYTES_PER_ELEMENT` |
| Max concurrent requests | `(device.memory_gib * GIB - weights) // kv_cache_per_request`, or 0 when the weights do not fit |

The docstrings in `capacity.py` are the source of truth for these formulas. The scenario table in
`tests/test_capacity.py` and the table in `README.md` must stay consistent with them.

## CLI entry point

`pyproject.toml` registers `memfit = "memfit.cli:main"`.

```bash
uv run --no-sync memfit                       # all models on accel-24g, context 8192
uv run --no-sync memfit --device accel-48g    # pick a device
uv run --no-sync memfit -m llama-3.1-8b -c 4096
```

## Two agent instruction files, two audiences

- `AGENTS.md` is read by **opencode during the demo**. It is tuned for a weak model and a one-minute budget:
  keep it short, literal, and step-by-step.
- `.claude/rules/` is read by **Claude Code when maintaining the template**.

## Typical tasks

1. **Tune the demo** — adjust `AGENTS.md`, docstrings in `capacity.py`, or the scenario table so the demo agent
   finishes faster or more reliably.
2. **Change the catalog** — edit `MODELS` / `DEVICES` in `src/memfit/catalog.py`. Devices are illustrative
   memory sizes, not real product specifications.
3. **Change the memory model** — update the docstring formulas, recompute the expected values in the scenario
   table, and update `README.md` together.
