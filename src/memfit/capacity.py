"""Memory capacity math for serving an LLM on an accelerator.

Device memory holds the model weights once, plus one KV cache per concurrent request.
All functions return exact integers. Use integer math only (``//``, never ``/``).
"""

from dataclasses import dataclass

GIB = 1024**3

# Bits per weight parameter, by quantization scheme.
WEIGHT_BITS = {"fp16": 16, "int8": 8, "int4": 4}

# The KV cache is stored as fp16: 2 bytes per element.
KV_BYTES_PER_ELEMENT = 2


@dataclass
class ModelSpec:
    """Architecture numbers needed to estimate a model's memory use."""

    name: str
    num_params: int
    num_layers: int
    num_kv_heads: int
    head_dim: int


@dataclass
class DeviceSpec:
    """An accelerator and its memory size in GiB."""

    name: str
    memory_gib: int


def weight_bytes(model: ModelSpec, quant: str) -> int:
    """Return the memory used by the model weights, in bytes.

    Raises ``ValueError`` when ``quant`` is not a key of ``WEIGHT_BITS``.
    """
    # TODO: implement
    raise NotImplementedError


def kv_cache_bytes_per_request(model: ModelSpec, context_len: int) -> int:
    """Return the KV cache memory one request needs, in bytes.

    Each layer stores a key tensor and a value tensor for every token of the context.
    """
    # TODO: implement
    raise NotImplementedError


def max_concurrent_requests(model: ModelSpec, device: DeviceSpec, quant: str, context_len: int) -> int:
    """Return how many requests the device can serve at the same time.

    Returns 0 when the weights alone do not fit in device memory.
    """
    # TODO: implement
    raise NotImplementedError


def max_context_len(model: ModelSpec, device: DeviceSpec, quant: str, num_requests: int) -> int:
    """Return the largest context length per request that still allows ``num_requests`` at the same time.

    Returns 0 when the weights alone do not fit in device memory.
    """
    # TODO: implement
    raise NotImplementedError
