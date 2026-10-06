# Maintaining the demo template

## What this repo is

A live-demo template: a coding agent (opencode) finishes `memfit`, a CLI that tells whether an LLM fits in
accelerator memory and how many concurrent requests it can serve. The demo agent reads `AGENTS.md`, then only
`src/memfit/capacity.py` and `tests/test_capacity.py`. Keep those three files short and literal; they are the
entire context of a weak model on a one-minute budget.

## Intentionally unfinished

| Path | Starting state | After the demo |
|---|---|---|
| `src/memfit/capacity.py` | Four functions `raise NotImplementedError`; the formulas live in `AGENTS.md` | Implemented |
| `tests/test_capacity.py` | Scenario table S1-S7 and the finished S1 test as a pattern; S2-S7 missing | 7 tests pass |

Never implement these two files while maintaining the template. Only complete them to run or rehearse the demo,
and restore with `git restore src tests` afterwards. So in the starting state, `uv run --no-sync pytest` reports
`1 failed` and `uv run --no-sync memfit` raises `NotImplementedError`. Neither is a bug.

## Memory model

| Quantity | Formula |
|---|---|
| Weights | `num_params * WEIGHT_BITS[quant] // 8` (fp16 = 16, int8 = 8, int4 = 4) |
| KV cache per request | `2 * num_layers * num_kv_heads * head_dim * context_len * KV_BYTES_PER_ELEMENT` |
| Max concurrent requests | `(memory_gib * GIB - weights) // kv_cache_per_request`, or 0 when the weights do not fit |
| Max context length for N requests | `(memory_gib * GIB - weights) // (N * kv_cache_bytes_per_request(model, 1))`, or 0 when the weights do not fit |

The formula table in `AGENTS.md` is the source of truth. The scenario table in `tests/test_capacity.py` and the
table in `README.md` must agree with it. The docstrings in `capacity.py` describe behavior only and must not
contain the formulas or the solution. Change these together.

## Conventions

- Python 3.10+, standard library only, no runtime dependencies. Dev dependency: pytest only. There is no linter.
- Run everything through `uv run --no-sync ...`. Never `pip`, bare `python`, or bare `pytest`.
- Capacity functions are pure and use integer math only (`//`). GiB conversion for display lives in `cli.py`.
- Tests: one function per scenario, `test_s<N>_<what>`, expected values copied from the table. S1 ships finished
  as the pattern the demo agent copies; `import pytest` is there for the `ValueError` scenario.
- Devices in `src/memfit/catalog.py`: `bertha-500-es` (128 GiB) and `bertha-500-mp` (192 GiB). Keep names and
  sizes in step with the real products.

## Verifying a change without spoiling the demo

1. Copy `src/` and `tests/` to a temporary directory outside the repo.
2. Fill in the four function bodies and write tests S2-S7 in the copy.
3. `PYTHONPATH=<copy>/src uv run --no-sync pytest <copy>/tests` must report `7 passed`.
4. `git status` must show no changes under `src/` or `tests/` beyond what you intended.
5. If you changed `AGENTS.md`, rehearse with the real demo agent.

## Git conventions

- Branch: `<TAG>-<kebab-description>`, e.g. `FEAT-add-memfit-template`.
- Commit subject: `[tag] <summary>`, imperative, 50 characters max. Body says what and why.
- PR title: `[<TAG>] <body>` with TAG one of FEAT, FIX, DOCS, STYLE, REFACTOR, PERF, TEST, BUILD, CI, CHORE,
  REVERT, HOTFIX, BOT. Body in English, 1-150 characters.
- PR body: type, summary, related issue (`Closes SOFT-XXXX` if any), what/why, test plan, notes for reviewers.
- Review focus: can a weak model finish in about a minute, does nothing leak the solution, do formulas, scenario
  values, and docs agree, and is it still standard-library-only.
