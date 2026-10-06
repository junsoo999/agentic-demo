"""Tests for memfit.capacity.

Write exactly one test function per scenario below, using the exact values listed.
All scenarios use the ``TINY`` model defined in this file.

| ID | Function under test          | Input                                    | Expected          |
|----|------------------------------|------------------------------------------|-------------------|
| S1 | weight_bytes                 | TINY, "fp16"                             | 2_000_000_000     |
| S2 | weight_bytes                 | TINY, "int4"                             | 500_000_000       |
| S3 | weight_bytes                 | TINY, "fp32"                             | raises ValueError |
| S4 | kv_cache_bytes_per_request   | TINY, context_len=1024                   | 2_097_152         |
| S5 | max_concurrent_requests      | TINY, DeviceSpec("d4", 4), "fp16", 1024  | 1094              |
| S6 | max_concurrent_requests      | TINY, DeviceSpec("d1", 1), "fp16", 1024  | 0 (does not fit)  |

Suggested names: test_s1_weight_bytes_fp16, test_s2_weight_bytes_int4, ...
"""

import pytest

from memfit.capacity import (
    DeviceSpec,
    ModelSpec,
    kv_cache_bytes_per_request,
    max_concurrent_requests,
    weight_bytes,
)

TINY = ModelSpec("tiny", num_params=1_000_000_000, num_layers=2, num_kv_heads=4, head_dim=64)

# TODO: implement scenarios S1-S6
