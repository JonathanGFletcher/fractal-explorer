from models.fractal import Vector3F, FractalConfig

import cupy as cp
import numpy as np
from PIL import Image





def render_julia(config: FractalConfig) -> np.ndarray:
    # Julia set parameters
    # width, height = 800, 800   # Image dimensions
    x_min, x_max = -0.0005, 0.0005   # Real axis range
    y_min, y_max = -0.0005, 0.0005   # Imaginary axis range
    # c = complex(-0.8, 0.156)   # Constant in the Julia set formula
    # max_iterations = 256       # Maximum iterations to determine escape

    # Step 1: Create coordinate grids for the complex plane
    x_coords = cp.linspace(x_min, x_max, config.dimensions.width)
    y_coords = cp.linspace(y_min, y_max, config.dimensions.height)
    real, imag = cp.meshgrid(x_coords, y_coords)

    # Step 2: Initialize the complex grid z = x + yi
    z = real + 1j * imag

    # Step 3: Initialize an array to store the number of iterations for each pixel
    iterations = cp.zeros(z.shape, dtype=int)

    # Step 4: Iterate the Julia set equation
    for i in range(config.iterations):
        mask = cp.abs(z) < 2  # Check which points have not yet escaped
        z[mask] = z[mask] ** 2 + complex(config.constant.x, config.constant.y)  # Apply the Julia set formula to points that haven't escaped
        iterations[mask] = i  # Record the iteration at which the point escapes

    # Step 5: Normalize the iteration count to 0-255 for coloring
    # normalized_iterations = cp.uint8(255 * iterations / config.iterations)
    normalized_iterations = cp.clip(255 * (iterations / config.iterations), 0, 255).astype(cp.uint8)

    # Step 6: Create a grayscale image from the iteration counts
    return cp.asnumpy(normalized_iterations)


def fractal_image(data: np.ndarray) -> Image:
    return Image.fromarray(data)