from models.fractal import Vector3F, FractalConfig

import cupy as cp
import numpy as np
from PIL import Image





def render_julia(config: FractalConfig) -> np.ndarray:
    x_min = (-1.5 + config.center.x) / config.scale
    x_max = (1.5 + config.center.x) / config.scale
    y_min = (-1.5 + config.center.y) / config.scale
    y_max = (1.5 + config.center.y) / config.scale

    width = config.dimensions.width
    height = config.dimensions.height
    x_coords = cp.linspace(x_min, x_max, width)
    y_coords = cp.linspace(y_min, y_max, height)
    real, imag = cp.meshgrid(x_coords, y_coords)

    step_values = [step.value for step in config.colors]
    r_colors = [step.color.x for step in config.colors]
    g_colors = [step.color.y for step in config.colors]
    b_colors = [step.color.z for step in config.colors]

    final_r_channel = cp.zeros((height, width), dtype=cp.float32)
    final_g_channel = cp.zeros((height, width), dtype=cp.float32)
    final_b_channel = cp.zeros((height, width), dtype=cp.float32)

    for _ in range(config.samples):
        jitter_real = real + (cp.random.rand(height, width) - 0.5) * (x_max - x_min) / width
        jitter_imag = imag + (cp.random.rand(height, width) - 0.5) * (y_max - y_min) / height
        z = jitter_real + 1j * jitter_imag
        iterations = cp.zeros(z.shape, dtype=int)

        for i in range(config.iterations):
            mask = cp.abs(z) < 2
            z[mask] = z[mask] ** 2 + complex(config.constant.x, config.constant.y)
            iterations[mask] = i

        normalized_iterations = np.clip(cp.asnumpy(iterations / config.iterations), 0, 1)

        final_r_channel += cp.asarray(np.interp(normalized_iterations, step_values, r_colors).astype(np.float32))
        final_g_channel += cp.asarray(np.interp(normalized_iterations, step_values, g_colors).astype(np.float32))
        final_b_channel += cp.asarray(np.interp(normalized_iterations, step_values, b_colors).astype(np.float32))

    final_r_channel /= config.samples
    final_g_channel /= config.samples
    final_b_channel /= config.samples
    return cp.asnumpy(cp.stack([final_r_channel, final_g_channel, final_b_channel], axis=-1).astype(cp.uint8))


def fractal_image(data: np.ndarray) -> Image:
    return Image.fromarray(data)