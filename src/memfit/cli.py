"""Command-line entry point: print a capacity table for one device."""

import argparse
from collections.abc import Sequence

from memfit.capacity import (
    GIB,
    WEIGHT_BITS,
    kv_cache_bytes_per_request,
    max_concurrent_requests,
    max_context_len,
    weight_bytes,
)
from memfit.catalog import DEVICES, MODELS


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the ``memfit`` command."""
    parser = argparse.ArgumentParser(
        prog="memfit",
        description="Show which models fit on a device and how many concurrent requests each can serve.",
    )
    parser.add_argument("-d", "--device", choices=sorted(DEVICES), default="bertha-500-es", help="target device")
    parser.add_argument("-c", "--context", type=int, default=8192, help="context length per request, in tokens")
    parser.add_argument("-n", "--requests", type=int, default=16, help="concurrent requests for the max-context column")
    parser.add_argument("-m", "--model", choices=sorted(MODELS), help="show a single model (default: all)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ``memfit`` command.

    Args:
        argv: Command-line arguments; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code.
    """
    args = build_parser().parse_args(argv)
    device = DEVICES[args.device]
    models = [MODELS[args.model]] if args.model else list(MODELS.values())

    print(f"Device: {device.name} ({device.memory_gib} GiB) | context: {args.context} tokens per request")
    print()
    print(f"{'model':<15}{'quant':<7}{'weights':>12}{'KV/request':>13}   {'max requests':<14}max context @{args.requests}")
    print("-" * 78)
    for model in models:
        for quant in WEIGHT_BITS:
            weights_gib = weight_bytes(model, quant) / GIB
            kv_gib = kv_cache_bytes_per_request(model, args.context) / GIB
            count = max_concurrent_requests(model, device, quant, args.context)
            context = max_context_len(model, device, quant, args.requests)
            verdict = str(count) if count > 0 else "does not fit"
            print(f"{model.name:<15}{quant:<7}{weights_gib:>8.2f} GiB{kv_gib:>9.2f} GiB   {verdict:<14}{context}")
    return 0
