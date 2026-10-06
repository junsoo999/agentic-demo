"""Built-in model and device catalog used by the CLI.

Model numbers are the publicly documented architecture values. Devices are illustrative
memory sizes, not real product specifications.
"""

from memfit.capacity import DeviceSpec, ModelSpec

MODELS: dict[str, ModelSpec] = {
    spec.name: spec
    for spec in (
        ModelSpec("phi-3-mini", num_params=3_821_079_552, num_layers=32, num_kv_heads=32, head_dim=96),
        ModelSpec("mistral-7b", num_params=7_248_023_552, num_layers=32, num_kv_heads=8, head_dim=128),
        ModelSpec("llama-3.1-8b", num_params=8_030_261_248, num_layers=32, num_kv_heads=8, head_dim=128),
        ModelSpec("llama-3.3-70b", num_params=70_553_706_496, num_layers=80, num_kv_heads=8, head_dim=128),
    )
}

DEVICES: dict[str, DeviceSpec] = {
    spec.name: spec
    for spec in (
        DeviceSpec("accel-24g", memory_gib=24),
        DeviceSpec("accel-48g", memory_gib=48),
        DeviceSpec("accel-80g", memory_gib=80),
    )
}
