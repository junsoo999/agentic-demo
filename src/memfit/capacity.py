"""Memory capacity math for serving an LLM on an accelerator.

Device memory is split into two parts:

- Model weights, loaded once and shared by every request.
- KV cache, allocated separately for each concurrent request.

All functions return exact integers (bytes or request counts). Use integer math only.
"""

from dataclasses import dataclass

GIB = 1024**3

# Bits used to store one weight parameter, per quantization scheme.
WEIGHT_BITS = {"fp16": 16, "int8": 8, "int4": 4}

# The KV cache is always stored as fp16: 2 bytes per element.
KV_BYTES_PER_ELEMENT = 2


@dataclass(frozen=True)
class ModelSpec:
    """Architecture numbers needed to estimate a model's memory use."""

    name: str
    num_params: int
    num_layers: int
    num_kv_heads: int
    head_dim: int


@dataclass(frozen=True)
class DeviceSpec:
    """An accelerator and its memory size in GiB."""

    name: str
    memory_gib: int


def weight_bytes(model: ModelSpec, quant: str) -> int:
    """Return the memory used by the model weights, in bytes.

    Formula:
        model.num_params * WEIGHT_BITS[quant] // 8

    Args:
        model: The model to size.
        quant: Quantization scheme, one of the keys of ``WEIGHT_BITS``.

    Returns:
        Weight memory in bytes.

    Raises:
        ValueError: When ``quant`` is not a key of ``WEIGHT_BITS``.
    """
    # TODO: implement
    raise NotImplementedError


def kv_cache_bytes_per_request(model: ModelSpec, context_len: int) -> int:
    """Return the KV cache memory one request needs, in bytes.

    Each layer stores a key tensor and a value tensor (hence the factor 2).

    Formula:
        2 * model.num_layers * model.num_kv_heads * model.head_dim * context_len * KV_BYTES_PER_ELEMENT

    Args:
        model: The model to size.
        context_len: Context length in tokens reserved for each request.

    Returns:
        KV cache memory for a single request, in bytes.
    """
    # TODO: implement
    raise NotImplementedError


def max_concurrent_requests(model: ModelSpec, device: DeviceSpec, quant: str, context_len: int) -> int:
    """Return how many requests the device can serve at the same time.

    Formula:
        free = device.memory_gib * GIB - weight_bytes(model, quant)
        if free < 0: the weights do not fit, return 0
        otherwise:   return free // kv_cache_bytes_per_request(model, context_len)

    Args:
        model: The model to serve.
        device: The accelerator to serve it on.
        quant: Quantization scheme for the weights.
        context_len: Context length in tokens reserved for each request.

    Returns:
        Maximum number of concurrent requests, or 0 when the weights do not fit.
    """
    # TODO: implement
    raise NotImplementedError
