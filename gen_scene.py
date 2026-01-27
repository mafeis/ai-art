from PIL import Image, ImageDraw
import random


def create_scene_background(filename="scene_bg.png"):
    # 16-bit landscape palette
    colors = {
        "sky_top": (0, 0, 100),
        "sky_bottom": (100, 150, 255),
        "cloud": (255, 255, 255),
        "grass_dark": (0, 100, 0),
        "grass_light": (50, 150, 50),
        "dirt": (100, 50, 0),
    }

    w, h = 320, 240  # Retro resolution
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # 1. Sky Gradient (dithering or bands for 16-bit feel)
    for y in range(h // 2):
        ratio = y / (h // 2)
        r = int(colors["sky_top"][0] * (1 - ratio) + colors["sky_bottom"][0] * ratio)
        g = int(colors["sky_top"][1] * (1 - ratio) + colors["sky_bottom"][1] * ratio)
        b = int(colors["sky_top"][2] * (1 - ratio) + colors["sky_bottom"][2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # 2. Clouds (procedural blobs)
    for _ in range(5):
        cx = random.randint(0, w)
        cy = random.randint(20, 80)
        width = random.randint(30, 60)
        draw.rectangle([cx, cy, cx + width, cy + 10], fill=colors["cloud"])
        draw.rectangle([cx + 10, cy - 10, cx + width - 10, cy], fill=colors["cloud"])

    # 3. Ground (tiled look)
    ground_y = h // 2
    draw.rectangle([0, ground_y, w, h], fill=colors["dirt"])

    # Grass layer
    draw.rectangle([0, ground_y, w, ground_y + 20], fill=colors["grass_dark"])

    # Grass blades/texture
    for x in range(0, w, 4):
        h_grass = random.randint(2, 5)
        draw.rectangle(
            [x, ground_y - h_grass, x + 2, ground_y], fill=colors["grass_light"]
        )

    # 4. Mountains (background)
    # Simple triangles
    mount_y = ground_y
    for i in range(3):
        mx = random.randint(0, w)
        mw = random.randint(50, 100)
        mh = random.randint(40, 80)
        # Using polygon
        points = [(mx, mount_y), (mx + mw // 2, mount_y - mh), (mx + mw, mount_y)]
        draw.polygon(points, fill=(80, 80, 100), outline=(50, 50, 80))

    img.save(filename)
    print(f"Scene background saved to {filename}")


if __name__ == "__main__":
    create_scene_background()
