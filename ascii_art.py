#!/usr/bin/env python3
"""
Image → ASCII Art Converter
- Loads an image or generates a demo gradient (--demo)
- Resizes by target width with character-aspect compensation
- Maps grayscale intensities to characters
- Writes ASCII .txt
- Renders ASCII back into a .png using a monospace font (Consolas if available)

Usage examples:
  python ascii_art.py --demo -w 100
  python ascii_art.py -i examples\your_photo.jpg -w 120 --out-text out\photo_120.txt --out-image out\photo_120.png
"""

import argparse
import os
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont


DEFAULT_CHARSET = "@%#*+=-:. "
CHARSETS = {
    "dense": "@%#*+=-:. ",
    "blocks": "█▓▒░ ",
    "simple": "#*+=-:. ",
    "dots": "•:·. ",
}

WINDOWS_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\consola.ttf",  # Consolas
    r"C:\Windows\Fonts\cour.ttf",     # Courier New
    r"C:\Windows\Fonts\lucon.ttf",    # Lucida Console
]


def find_monospace_font(font_path: Optional[str]) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try requested path, then common Windows monospace fonts, else default bitmap."""
    if font_path:
        fp = Path(font_path)
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size=12)
            except Exception:
                pass
    for candidate in WINDOWS_FONT_CANDIDATES:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size=12)
            except Exception:
                continue
    # Fallback. Not guaranteed monospace, but usually okay.
    return ImageFont.load_default()


def char_cell_size(font: ImageFont.ImageFont) -> Tuple[int, int]:
    """Measure single-character width/height with current font."""
    # Using getbbox for consistent metrics
    bbox = font.getbbox("A")
    cw = bbox[2] - bbox[0]
    ch = bbox[3] - bbox[1]
    return max(1, cw), max(1, ch)


def generate_demo_image(path: Path, size: int = 256) -> Path:
    """Create a simple gradient demo image."""
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            val = int(255 * (x / (size - 1) * 0.6 + y / (size - 1) * 0.4))
            arr[y, x] = (val, val, val)
    Image.fromarray(arr).save(path)
    return path


def image_to_ascii_lines(
    img: Image.Image,
    width: int,
    charset: str,
    invert: bool,
    scale_y: float,
) -> List[str]:
    """
    Convert an Image to lines of ASCII.
    scale_y compensates for characters being taller than they are wide.
      Typical good values: 0.45 to 0.6. Default 0.5.
    """
    if width < 10:
        raise ValueError("Width is too small. Try >= 40, ideally 80–200.")

    # Convert to grayscale
    gray = img.convert("L")

    # Compute target size with aspect correction
    w0, h0 = gray.size
    ratio = width / float(w0)
    new_h = max(1, int(h0 * ratio * scale_y))
    gray = gray.resize((width, new_h), Image.BICUBIC)

    # Map intensities to character indices
    arr = np.array(gray, dtype=np.uint8)
    if invert:
        arr = 255 - arr

    # 0 (black) → charset[-1]? We want darker → "heavier" char.
    # Using 1 - (val/255) to flip: 0 → 1, 255 → 0
    vals = 1.0 - (arr.astype(np.float32) / 255.0)
    idx = (vals * (len(charset) - 1)).round().astype(np.int32)
    idx = np.clip(idx, 0, len(charset) - 1)

    # Build lines
    lines = ["".join(charset[i] for i in row) for row in idx]
    return lines


def render_ascii_to_image(
    lines: List[str],
    out_path: Path,
    font_path: Optional[str] = None,
    font_size: int = 12,
    fg: str = "black",
    bg: str = "white",
) -> Path:
    """Render ASCII lines to a PNG image with a monospace font."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load font
    font = find_monospace_font(font_path)
    if isinstance(font, ImageFont.FreeTypeFont) and font_size != 12:
        # Re-open with requested size
        font = ImageFont.truetype(font.path, size=font_size)

    # Measure cell size
    cw, ch = char_cell_size(font)

    num_rows = len(lines)
    num_cols = max((len(line) for line in lines), default=0)

    if num_cols == 0 or num_rows == 0:
        # Avoid zero-size images
        num_cols = 1
        num_rows = 1
        lines = [""]

    # Compute image size
    img_w = max(1, num_cols * cw)
    img_h = max(1, num_rows * ch)

    # Draw
    im = Image.new("RGB", (img_w, img_h), color=bg)
    draw = ImageDraw.Draw(im)

    y = 0
    for line in lines:
        draw.text((0, y), line, fill=fg, font=font)
        y += ch

    im.save(out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art (.txt and rendered .png).")
    parser.add_argument("-i", "--input", type=str, help="Path to input image (png/jpg/webp). Omit with --demo.")
    parser.add_argument("-w", "--width", type=int, default=120, help="Target character width (80–200 looks good).")
    parser.add_argument("--invert", action="store_true", help="Invert brightness mapping.")
    parser.add_argument("--charset", type=str, default="dense", choices=list(CHARSETS.keys()),
                        help="Character set to use.")
    parser.add_argument("--scale-y", type=float, default=0.5,
                        help="Height scaling factor for character aspect compensation (0.45–0.6).")
    parser.add_argument("--out-text", type=str, help="Output .txt path (default: out/<name>_<w>.txt)")
    parser.add_argument("--out-image", type=str, help="Output .png path (default: out/<name>_<w>.png)")
    parser.add_argument("--font-path", type=str, default=None, help="Path to a .ttf monospace font.")
    parser.add_argument("--font-size", type=int, default=14, help="Font size for rendered image.")
    parser.add_argument("--demo", action="store_true", help="Generate and use a demo gradient image.")
    args = parser.parse_args()

    # Resolve input
    input_path: Optional[Path] = None
    if args.demo:
        input_path = Path("examples/demo.png")
        if not input_path.exists():
            print("Creating demo gradient:", input_path)
            generate_demo_image(input_path)
    else:
        if not args.input:
            raise SystemExit("Error: provide --input <path> or use --demo.")
        input_path = Path(args.input)
        if not input_path.exists():
            raise SystemExit(f"Error: input image not found: {input_path}")

    # Load image
    img = Image.open(input_path).convert("RGB")

    # Pick charset
    charset = CHARSETS[args.charset]

    # Convert to ASCII
    lines = image_to_ascii_lines(
        img=img,
        width=args.width,
        charset=charset,
        invert=args.invert,
        scale_y=args.scale_y,
    )

    # Prepare outputs
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True, parents=True)
    stem = input_path.stem
    out_txt = Path(args.out_text) if args.out_text else out_dir / f"{stem}_{args.width}.txt"
    out_png = Path(args.out_image) if args.out_image else out_dir / f"{stem}_{args.width}.png"

    # Write text
    out_txt.write_text("\n".join(lines), encoding="utf-8")

    # Render to image
    render_ascii_to_image(
        lines=lines,
        out_path=out_png,
        font_path=args.font_path,
        font_size=args.font_size,
        fg="black",
        bg="white",
    )

    print(f"ASCII text saved to: {out_txt}")
    print(f"Rendered PNG saved to: {out_png}")
    print("Done.")


if __name__ == "__main__":
    main()
