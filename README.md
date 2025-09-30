# Image to ASCII Art Converter

Turn images into ASCII text and also a rendered PNG of that ASCII using a monospace font.

## Features
- Resize by target **character width** with aspect compensation
- Multiple charsets: `dense`, `blocks`, `simple`, `dots`
- Optional invert
- Outputs:
  - `out/<name>_<width>.txt` (ASCII)
  - `out/<name>_<width>.png` (rendered ASCII image)

## Quickstart

```bash
# create and activate venv (Windows PowerShell)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt

# demo run (generates a gradient)
python ascii_art.py --demo -w 100

Then open out/ to see:
demo_100.txt
demo_100.png

Convert your own image
Put an image in examples/, then:
python ascii_art.py -i examples\your_photo.jpg -w 120 --font-size 16

Options:
--width target characters per line (80–200 looks good)
--invert flips bright/dark mapping
--charset one of dense | blocks | simple | dots
--scale-y aspect compensation (default 0.5)
--font-path set a specific font (e.g. C:\Windows\Fonts\consola.ttf)
--font-size size for rendered PNG

Before / After
Add your own example images here once you run the tool.