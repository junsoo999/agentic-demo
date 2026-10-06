"""Tests for memfit.capacity.

``test_s1_weight_bytes_fp16`` is written for you. Write S2-S6 in the same style, using the exact values below.
All rows use the ``TINY`` model.

| ID | Function                   | Input                                   | Expected          |
|----|----------------------------|-----------------------------------------|-------------------|
| S1 | weight_bytes               | TINY, "fp16"                            | 2_000_000_000     |
| S2 | weight_bytes               | TINY, "int4"                            | 500_000_000       |
| S3 | weight_bytes               | TINY, "fp32"                            | raises ValueError |
| S4 | kv_cache_bytes_per_request | TINY, 1024                              | 2_097_152         |
| S5 | max_concurrent_requests    | TINY, DeviceSpec("d4", 4), "fp16", 1024 | 1094              |
| S6 | max_concurrent_requests    | TINY, DeviceSpec("d1", 1), "fp16", 1024 | 0                 |
| S7 | max_context_len            | TINY, DeviceSpec("d4", 4), "fp16", 8    | 140_073           |

For S3 use ``with pytest.raises(ValueError):``.
"""

import pytest

from memfit.capacity import (
    DeviceSpec,
    ModelSpec,
    kv_cache_bytes_per_request,
    max_concurrent_requests,
    max_context_len,
    weight_bytes,
)

TINY = ModelSpec("tiny", num_params=1_000_000_000, num_layers=2, num_kv_heads=4, head_dim=64)


def test_s1_weight_bytes_fp16() -> None:
    assert weight_bytes(TINY, "fp16") == 2_000_000_000


# TODO: write test_s2 ... test_s7 here
