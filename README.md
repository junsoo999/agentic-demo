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

<h3 align="center">
Agentic Demo
</h3>

---

`memfit` answers one question for an AI accelerator: **does this LLM fit in device memory, and how many concurrent requests can it serve?**

This repository is a demo template. The capacity math and its tests are intentionally left unimplemented so a coding agent ([opencode](https://opencode.ai)) can finish them live, guided by [`AGENTS.md`](AGENTS.md).

## Demo runbook

One-time setup:

```bash
uv sync
uv run --no-sync pre-commit install
```

Before the demo, show the starting state (the program fails with `NotImplementedError`):

```bash
uv run --no-sync memfit
```

Start `opencode` in the repository root and enter:

```text
memfit을 완성해줘.
```

The agent then follows the four steps in `AGENTS.md`: plan, implement `src/memfit/capacity.py`, write the six test scenarios in `tests/test_capacity.py` and pass Ruff and pytest, and run `memfit --device accel-48g` to report the result.

Reset to the starting state for the next run (requires the template to be committed):

```bash
git restore src tests
```

## Memory model

| Quantity | Formula |
|---|---|
| Weights | `num_params * bits / 8` (fp16 = 16, int8 = 8, int4 = 4) |
| KV cache per request | `2 * num_layers * num_kv_heads * head_dim * context_len * 2 bytes` |
| Max concurrent requests | `(device_memory - weights) // kv_cache_per_request` |

Devices in `src/memfit/catalog.py` are illustrative memory sizes, not real product specifications.
