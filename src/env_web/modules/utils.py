from skimage.transform import resize

def resize_volume(volume, downscale_factor):
    # Downscale the volume to speed up rendering
    new_shape = (int(volume.shape[0] * downscale_factor),
                 int(volume.shape[1] * downscale_factor),
                 int(volume.shape[2] * downscale_factor))
    return resize(volume, new_shape, anti_aliasing=True)