#!/usr/local/bin/python3

from argparse import ArgumentParser
import glob
import numpy as np
from imageio import imread, imwrite
import os

def pfm_to_image(pfm_path, image_path, scale=1.0, offset=0.0, normalize=True, flip_y=False):
    """
    Converts a PFM file to an image format (e.g., PNG, JPEG).

    Parameters
    ----------
    pfm_path : str
        Path to input PFM file.
    image_path : str
        Path to output image file.
    scale : float
        Scale factor applied before saving.
    offset : float
        Offset applied before saving.
    normalize : bool
        Normalize data to [0, 1] range before saving.
    flip_y : bool
        Flip the image vertically before saving.
    """
    data = imread(pfm_path)
    
    if flip_y:
        data = np.flip(data, axis=0)

    # Apply scale and offset
    data = data * scale + offset

    # Normalize to [0, 1] for proper display/saving
    if normalize:
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max != data_min:
            data = (data - data_min) / (data_max - data_min)
        else:
            data = np.zeros_like(data)

    # Convert to 8-bit unsigned int for standard image formats
    data_uint8 = (data * 255).astype(np.uint8)

    imwrite(image_path, data_uint8)


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert PFM files to common image formats (PNG, JPG, etc.)')
    parser.add_argument('pfms', type=str, nargs='+', help='List of input PFM files to convert')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale pixel values before saving')
    parser.add_argument('--offset', type=float, default=0.0, help='Offset pixel values before saving')
    parser.add_argument('--normalize', action='store_true', help='Normalize data to [0,1] before saving')
    parser.add_argument('--flip_y', action='store_true', help='Flip image vertically before saving')
    parser.add_argument('--ext', type=str, default='.png', choices=['.png', '.jpg', '.jpeg', '.tiff'], 
                        help='Output image extension')

    args = parser.parse_args()

    pfms = []
    for pattern in args.pfms:
        pfms.extend(glob.glob(pattern))

    for pfm in pfms:
        base_name = os.path.splitext(pfm)[0]
        output = base_name + args.ext
        os.makedirs(os.path.dirname(output), exist_ok=True)
        pfm_to_image(pfm, output, args.scale, args.offset, args.normalize, args.flip_y)
        print(f'Saved: {output}')