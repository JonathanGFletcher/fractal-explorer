# Import necessary libraries
import numpy as np
import cupy as cp
from PIL import Image
import matplotlib.pyplot as plt

# Julia set parameters
width, height = 800, 800   # Image dimensions
x_min, x_max = -1.5, 1.5   # Real axis range
y_min, y_max = -1.5, 1.5   # Imaginary axis range
c = complex(-0.8, 0.156)   # Constant in the Julia set formula
max_iterations = 256       # Maximum iterations to determine escape

# Step 1: Create coordinate grids for the complex plane
x_coords = cp.linspace(x_min, x_max, width)
y_coords = cp.linspace(y_min, y_max, height)
real, imag = cp.meshgrid(x_coords, y_coords)

# Step 2: Initialize the complex grid z = x + yi
z = real + 1j * imag

# Step 3: Initialize an array to store the number of iterations for each pixel
iterations = cp.zeros(z.shape, dtype=int)

# Step 4: Iterate the Julia set equation
for i in range(max_iterations):
    mask = cp.abs(z) < 2  # Check which points have not yet escaped
    z[mask] = z[mask] ** 2 + c  # Apply the Julia set formula to points that haven't escaped
    iterations[mask] = i  # Record the iteration at which the point escapes

# Step 5: Normalize the iteration count to 0-255 for coloring
normalized_iterations = cp.uint8(255 * iterations / max_iterations)

# Step 6: Create a grayscale image from the iteration counts
julia_image_np = cp.asnumpy(normalized_iterations)

# Step 7: Convert the array to an image and display it
julia_image = Image.fromarray(julia_image_np)
julia_image.show()