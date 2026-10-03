#!/usr/bin/env python3
"""Generates a tangent-space normal map (OpenGL convention: green = image up)
from a color texture, using its luminance as a height field.

Usage: generate-normal-map.py <color_texture> <output.png> [mean_tilt_deg]

The bump strength is chosen so that the mean angle between the normals and the
flat surface normal is mean_tilt_deg (default: 25). A negative value inverts
the height (for textures where the darker parts are higher, e.g. light mortar
between dark bricks). The texture is assumed to be tileable: gradients wrap
around the borders.
"""
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter


def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    target_tilt = float(sys.argv[3]) if len(sys.argv) > 3 else 25.0
    sign = -1.0 if target_tilt < 0 else 1.0
    target_tilt = abs(target_tilt)

    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float64) / 255.0
    height = rgb @ np.array([0.299, 0.587, 0.114])

    # Remove low-frequency shading baked into the color, and pixel noise:
    size = max(height.shape)
    height = height - gaussian_filter(height, sigma=size / 16, mode="wrap")
    height = gaussian_filter(height, sigma=size / 1024, mode="wrap")

    # Gradients with wrap-around (central differences), in units of the
    # texture width:
    dh_dcol = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5
    dh_drow = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5

    def normals(k):
        nx = -k * dh_dcol
        ny = k * dh_drow  # image up = -row
        nz = np.ones_like(height)
        norm = np.sqrt(nx * nx + ny * ny + nz * nz)
        return np.stack([nx, ny, nz], axis=-1) / norm[..., None]

    def mean_tilt(k):
        return np.degrees(np.arccos(np.clip(normals(k)[..., 2], -1, 1))).mean()

    # Bisection on the (monotonic) bump strength:
    lo, hi = 0.0, 1.0
    while mean_tilt(hi) < target_tilt and hi < 1e6:
        hi *= 2
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if mean_tilt(mid) < target_tilt:
            lo = mid
        else:
            hi = mid
    n = normals(sign * 0.5 * (lo + hi))

    out = np.clip((n * 0.5 + 0.5) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGB").save(dst, optimize=True)


if __name__ == "__main__":
    main()
