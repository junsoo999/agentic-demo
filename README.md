<!---
Copyright 2026 The HyperAccel. All rights reserved.
-->

<p align="center">
    <br>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logos/hyperaccel_logo_dark.png" width="400">
        <source media="(prefers-color-scheme: light)" srcset="docs/assets/logos/hyperaccel_logo_light.png" width="400">
        <img src="docs/assets/logos/hyperaccel_logo_light.png" width="400" alt="HyperAccel Logo">
    </picture>
    <br>
</p>

<h1 align="center">memfit: LLM Memory Capacity Calculator for HyperAccel Bertha</h1>

<h3 align="center">An Agentic Coding Demo with opencode</h3>

<p align="center">
<b>Does this LLM fit in device memory, and how many concurrent requests can it serve?</b><br>
A coding agent answers that question live by finishing this small CLI in about a minute.
</p>

---

`memfit` is a small CLI that sizes an LLM against an accelerator's memory: weights once, plus one KV cache per concurrent request.

This repository is a demo template. The capacity math and its tests are intentionally left unimplemented so a coding agent ([opencode](https://opencode.ai)) can finish them live, guided by [`AGENTS.md`](AGENTS.md).

## Demo runbook

One-time setup:

```bash
uv sync
```

Before the demo, show the starting state (the program fails with `NotImplementedError`):

```bash
uv run --no-sync memfit
```

Start `opencode` in the repository root and enter:

```text
memfit을 완성해줘.
```

The agent implements the four functions in `src/memfit/capacity.py` from the formulas in `AGENTS.md`, writes tests S2-S7 in `tests/test_capacity.py` following the given S1 example, runs `pytest`, and runs `memfit --device bertha-500-mp` to report the result.

Reset to the starting state for the next run:

```bash
git restore src tests
```

## Memory model

| Quantity | Formula |
|---|---|
| Weights | `num_params * bits // 8` (fp16 = 16, int8 = 8, int4 = 4) |
| KV cache per request | `2 * num_layers * num_kv_heads * head_dim * context_len * 2 bytes` |
| Max concurrent requests | `(device_memory - weights) // kv_cache_per_request`, or 0 when the weights do not fit |
| Max context length for N requests | `(device_memory - weights) // (N * kv_cache_per_token)`, or 0 when the weights do not fit |

Devices in `src/memfit/catalog.py`: `bertha-500-es` (128 GiB) and `bertha-500-mp` (192 GiB).
