from PIL import Image, ImageChops
import os, shutil

out = os.path.expanduser("~/shared/research/automation-impact")

# Load and auto-crop whitespace
img = Image.open("/tmp/ai-impact-tight.png").convert("RGB")
bg = Image.new("RGB", img.size, (255, 255, 255))
diff = ImageChops.difference(img, bg)
bbox = diff.getbbox()
if bbox:
    # Add small padding
    pad = 4
    bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(img.width, bbox[2]+pad), min(img.height, bbox[3]+pad))
    img = img.crop(bbox)

w, h = img.size
print(f"Cropped image: {w}x{h}")

# Save full
img.save(os.path.join(out, "full.png"))

# Split into ~1100px sections
chunk = 1100
y, i = 0, 1
while y < h:
    bottom = min(y + chunk, h)
    section = img.crop((0, y, w, bottom))
    path = os.path.join(out, f"section-{i}.png")
    section.save(path)
    print(f"  section-{i}.png: {w}x{bottom-y}")
    y = bottom
    i += 1

print("Done.")
