from nunif.utils import pil_io
from nunif.transforms import image_magick as IM
from nunif.utils.image_loader import list_images
from torchvision.transforms import (
    functional as TF,
    InterpolationMode
)
import argparse
from os import path
import os


def modcrop(im):
    w, h = im.size
    w_pad = -(w % 4)
    h_pad = -(h % 4)
    if w_pad != 0 or h_pad != 0:
        im = TF.pad(im, (0, 0, w_pad, h_pad))
    return im


def wand_scale(im, filename, output_dir, filter_type, scale, blur):
    c, h, w = im.shape
    im = IM.resize(im, size=(h // scale, w // scale),
                   filter_type=filter_type, blur=blur)
    basename = path.splitext(path.basename(filename))[0]
    im = pil_io.to_image(im)
    im.save(path.join(output_dir, f"{basename}_{filter_type}_blur{blur}.png"))


def downscaling_test(filename, output_dir, scale):
    im, _ = pil_io.load_image_simple(filename)
    im = modcrop(im)
    im = pil_io.to_tensor(im)
    for filter_type in ("box", "sinc", "lanczos", "catrom", "triangle"):
        for blur in (1, 0.95, 1.05):
            wand_scale(im, filename, output_dir, filter_type, scale, blur)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="input directory or file")
    parser.add_argument("--scale", "-s", type=int, required=True, choices=[2, 4],
                        help="downscaling factor")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="output directory")
    args = parser.parse_args()
    if path.isdir(args.input):
        files = list_images(args.input)
    else:
        files = [args.input]

    os.makedirs(args.output, exist_ok=True)
    for filename in files:
        downscaling_test(filename, args.output, args.scale)


if __name__ == "__main__":
    main()
