# memfit agent guide

`memfit` answers one question: **does this LLM fit in device memory, and how many concurrent requests
can it serve?**

Two files are unfinished. Everything else is done; do not read or edit it.

| Path | What to do |
|---|---|
| `src/memfit/capacity.py` | Fill in the 4 function bodies marked `# TODO: implement`, using the formulas below |
| `tests/test_capacity.py` | Write tests S2-S7 in the same style as the given `test_s1_weight_bytes_fp16` |

## Formulas

Use these names exactly as they appear in `src/memfit/capacity.py`. Integer math only: `//`, never `/`.

```text
weight_bytes(model, quant):
    if quant is not a key of WEIGHT_BITS: raise ValueError(quant)
    return model.num_params * WEIGHT_BITS[quant] // 8

kv_cache_bytes_per_request(model, context_len):
    return 2 * model.num_layers * model.num_kv_heads * model.head_dim * context_len * KV_BYTES_PER_ELEMENT

max_concurrent_requests(model, device, quant, context_len):
    free = device.memory_gib * GIB - weight_bytes(model, quant)
    if free < 0: return 0
    return free // kv_cache_bytes_per_request(model, context_len)

max_context_len(model, device, quant, num_requests):
    free = device.memory_gib * GIB - weight_bytes(model, quant)
    if free < 0: return 0
    kv_per_token = kv_cache_bytes_per_request(model, 1)
    return free // (num_requests * kv_per_token)
```

## Steps

When the user asks you to complete `memfit`, do these steps in order without stopping to ask.

1. Read `src/memfit/capacity.py` and `tests/test_capacity.py`. Nothing else.
2. In `src/memfit/capacity.py`, replace each `raise NotImplementedError` with the matching formula above,
   written as Python. Keep the docstrings.
3. In `tests/test_capacity.py`, write one test function per row S2-S7, named `test_s<N>_...`, each with a
   single `assert` on the exact `Expected` value. For S3 use `with pytest.raises(ValueError):`.
4. Run the tests. They must report `7 passed`. If one fails, fix the function body, never the expected value.

   ```bash
   uv run --no-sync pytest
   ```

5. Run the program and summarize the table in 2-3 sentences (which models fit, how quantization changes
   the request count and the context length):

   ```bash
   uv run --no-sync memfit --device bertha-500-mp
   ```

## Rules

- Always use `uv run --no-sync ...`. Never use `pip`, bare `python`, bare `pytest`, `uv sync`, or `uv add`.
- Do not change signatures, constants, dataclasses, or docstrings. Do not create files or add dependencies.
- Code in English. Talk to the user in Korean.
