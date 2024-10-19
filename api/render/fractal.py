from models.fractal import Vector3F, JuliaConfig, MandelbrotConfig

import cupy as cp
import numpy as np
from PIL import Image





def render_julia(config: JuliaConfig) -> np.ndarray:
    bound_x_min = -1.5
    bound_x_max = 1.5
    if config.dimensions.width < config.dimensions.height:
        bound_x_min *= (config.dimensions.width / config.dimensions.height)
        bound_x_max *= (config.dimensions.width / config.dimensions.height)
    bound_y_min = -1.5
    bound_y_max = 1.5
    if config.dimensions.width >= config.dimensions.height:
        bound_y_min *= (config.dimensions.height / config.dimensions.width)
        bound_y_max *= (config.dimensions.height / config.dimensions.width)

    x_min = bound_x_min + config.center.x * config.scale
    x_max = bound_x_max + config.center.x * config.scale
    y_min = bound_y_min + config.center.y * config.scale
    y_max = bound_y_max + config.center.y * config.scale
    x_range = x_max - x_min
    y_range = y_max - y_min

    full_width = config.dimensions.width
    full_height = config.dimensions.height
    width = config.dimensions.view_max_x - config.dimensions.view_min_x
    height = config.dimensions.view_max_y - config.dimensions.view_min_y
    x_min += x_range * (config.dimensions.view_min_x / full_width)
    x_max -= x_range * (1 - ((config.dimensions.view_max_x + 1) / full_width))
    y_min += y_range * (config.dimensions.view_min_y / full_height)
    y_max -= y_range * (1 - ((config.dimensions.view_max_y + 1) / full_height))
    x_min /= config.scale
    x_max /= config.scale
    y_min /= config.scale
    y_max /= config.scale

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
        jitter_real = real + (cp.random.rand(height, width) - 0.5) * (x_max - x_min) / full_width
        jitter_imag = imag + (cp.random.rand(height, width) - 0.5) * (y_max - y_min) / full_height
        z = jitter_real + 1j * jitter_imag
        iterations = cp.zeros(z.shape, dtype=int)

        for i in range(config.iterations):
            mask = cp.abs(z) < 2
            z[mask] = z[mask] ** 2 + complex(config.constant.x, config.constant.y)
            iterations[mask] = i

        mod = cp.sqrt(cp.abs(z) ** 2)
        smooth_iterations = iterations - cp.log2(cp.maximum(1, cp.log2(mod)))
        normalized_iterations = np.clip(cp.asnumpy(smooth_iterations / config.iterations), 0, 1)

        final_r_channel += cp.asarray(np.interp(normalized_iterations, step_values, r_colors).astype(np.float32))
        final_g_channel += cp.asarray(np.interp(normalized_iterations, step_values, g_colors).astype(np.float32))
        final_b_channel += cp.asarray(np.interp(normalized_iterations, step_values, b_colors).astype(np.float32))

    final_r_channel /= config.samples
    final_g_channel /= config.samples
    final_b_channel /= config.samples
    return cp.asnumpy(cp.stack([final_r_channel, final_g_channel, final_b_channel], axis=-1).astype(cp.uint8))


def render_mandelbrot(config: MandelbrotConfig) -> np.ndarray:
    x_min = -2.0 + config.center.x
    x_max = 1.0 + config.center.x
    y_min = -1.5 + config.center.y
    y_max = 1.5 + config.center.y
    x_range = x_max - x_min
    y_range = y_max - y_min

    full_width = config.dimensions.width
    full_height = config.dimensions.height
    width = config.dimensions.view_max_x - config.dimensions.view_min_x
    height = config.dimensions.view_max_y - config.dimensions.view_min_y
    x_min += x_range * (config.dimensions.view_min_x / full_width)
    x_max -= x_range * (1 - ((config.dimensions.view_max_x + 1) / full_width))
    y_min += y_range * (config.dimensions.view_min_y / full_height)
    y_max -= y_range * (1 - ((config.dimensions.view_max_y + 1) / full_height))
    x_min /= config.scale
    x_max /= config.scale
    y_min /= config.scale
    y_max /= config.scale

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
        jitter_real = real + (cp.random.rand(height, width) - 0.5) * (x_max - x_min) / full_width
        jitter_imag = imag + (cp.random.rand(height, width) - 0.5) * (y_max - y_min) / full_height
        c = jitter_real + 1j * jitter_imag
        z = cp.zeros_like(c, dtype=np.complex128)
        iterations = cp.zeros(c.shape, dtype=np.float32)

        for i in range(config.iterations):
            mask = cp.abs(z) <= 2
            z[mask] = z[mask] ** 2 + c[mask]
            diverged = mask & (cp.abs(z) > 2)
            iterations[diverged] = i

        mod = cp.sqrt(cp.abs(z) ** 2)
        smooth_iterations = iterations - cp.log2(cp.maximum(1, cp.log2(mod)))
        normalized_iterations = np.clip(cp.asnumpy(smooth_iterations / config.iterations), 0, 1)

        final_r_channel += cp.asarray(np.interp(normalized_iterations, step_values, r_colors).astype(np.float32))
        final_g_channel += cp.asarray(np.interp(normalized_iterations, step_values, g_colors).astype(np.float32))
        final_b_channel += cp.asarray(np.interp(normalized_iterations, step_values, b_colors).astype(np.float32))

    final_r_channel /= config.samples
    final_g_channel /= config.samples
    final_b_channel /= config.samples
    return cp.asnumpy(cp.stack([final_r_channel, final_g_channel, final_b_channel], axis=-1).astype(cp.uint8))


def fractal_image(data: np.ndarray) -> Image:
    return Image.fromarray(data)