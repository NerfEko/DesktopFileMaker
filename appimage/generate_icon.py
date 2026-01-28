#!/usr/bin/env python3
"""
Generate a simple icon for Desktop File Maker AppImage
Creates a 256x256 PNG icon
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create 256x256 image with transparent background
size = 256
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a rounded rectangle background (blue gradient)
background_color = (52, 152, 219)  # Blue
margin = 20
draw.rounded_rectangle(
    [margin, margin, size - margin, size - margin], radius=30, fill=background_color
)

# Draw a document icon (white)
doc_color = (255, 255, 255)
doc_margin = 60
doc_width = size - (doc_margin * 2)
doc_height = size - (doc_margin * 2)

# Document body
draw.rounded_rectangle(
    [doc_margin, doc_margin + 20, doc_margin + doc_width, doc_margin + doc_height],
    radius=10,
    fill=doc_color,
)

# Folded corner
corner_size = 30
draw.polygon(
    [
        (doc_margin + doc_width, doc_margin + 20),
        (doc_margin + doc_width - corner_size, doc_margin + 20),
        (doc_margin + doc_width, doc_margin + 20 + corner_size),
    ],
    fill=(230, 230, 230),
)

# Draw lines on the document (representing text)
line_color = (52, 152, 219)
line_start_y = doc_margin + 60
line_spacing = 25
line_width = 3

for i in range(4):
    y = line_start_y + (i * line_spacing)
    draw.line(
        [(doc_margin + 20, y), (doc_margin + doc_width - 20, y)],
        fill=line_color,
        width=line_width,
    )

# Save the icon
output_dir = os.path.join(os.path.dirname(__file__))
output_path = os.path.join(output_dir, "desktop-file-maker.png")
img.save(output_path, "PNG")

print(f"Icon created: {output_path}")
