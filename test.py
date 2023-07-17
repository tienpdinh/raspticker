import imageio.v2 as imageio
import numpy as np

image = imageio.imread('assets/DKNG.pbm')

print((np.invert(image) * 255).tolist())