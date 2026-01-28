#!/usr/bin/env python3
"""
Generate a simple icon for Desktop File Maker for use in desktop entries.
This creates a basic text-based icon if no proper icon is available.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 icon
img = Image.new('RGB', (256, 256), color='#f8f9fa')
draw = ImageDraw.Draw(img)

# Background gradient effect (simple version)
for i in range(256):
    opacity = int(255 * (1 - i/256) * 0.1)
    draw.line([(0, i), (255, i)], fill=(52, 152, 219, opacity))

# Draw main document shape
doc_color = (52, 152, 219)  # Blue
doc_margin = 40
doc_width = 176
doc_height = 200

# Main document rectangle
draw.rounded_rectangle(
    [doc_margin, doc_margin, doc_margin + doc_width, doc_margin + doc_height],
    radius=15,
    fill=doc_color,
)

# Window/app icon overlay
window_size = 60
window_x = doc_margin + doc_width - window_size - 20
window_y = doc_margin + 30
draw.rounded_rectangle(
    [window_x, window_y, window_x + window_size, window_y + window_size],
    radius=8,
    fill=(255, 255, 255),
)

# Small squares inside window (representing app interface)
for i, color in enumerate([(52, 152, 219), (46, 204, 113), (241, 196, 15)]):
    x = window_x + 10 + (i % 2) * 20
    y = window_y + 10 + (i // 2) * 20
    draw.rounded_rectangle(
        [x, y, x + 15, y + 15],
        radius=3,
        fill=color,
    )

# Gear/settings icon in corner
gear_x = doc_margin + doc_width - 35
gear_y = doc_margin + doc_height - 35
draw.ellipse([gear_x, gear_y, gear_x + 25, gear_y + 25], fill=(255, 255, 255))
draw.ellipse([gear_x + 5, gear_y + 5, gear_x + 20, gear_y + 20], fill=doc_color)

# Desktop entry text on document
try:
    # Try to use a monospace font
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
except:
    try:
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 14)
    except:
        font = ImageFont.load_default()

text_lines = ["[Desktop Entry]", "Type=Application", "Name=MyApp", "Exec=/usr/bin/"]
text_color = (255, 255, 255)

for i, line in enumerate(text_lines):
    y_pos = doc_margin + 40 + i * 20
    draw.text((doc_margin + 15, y_pos), line, fill=text_color, font=font)

# Save the icon
output_dir = os.path.join(os.path.dirname(__file__))
output_path = os.path.join(output_dir, "desktop-file-maker-icon.png")
img.save(output_path, "PNG")

print(f"Icon generated: {output_path}")