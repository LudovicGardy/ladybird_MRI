from skimage.transform import resize
import numpy as np


def resize_volume(volume: np.ndarray, downscale_factor: float) -> np.ndarray:
    new_shape = (
        int(volume.shape[0] * downscale_factor),
        int(volume.shape[1] * downscale_factor),
        int(volume.shape[2] * downscale_factor),
    )
    return resize(volume, new_shape, anti_aliasing=True)
