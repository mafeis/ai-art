"""
模块名称: 怪物生成脚本 (Monster Generator)
文件用途:
    一个独立的脚本，用于程序化生成像素风格的怪物（如史莱姆）。
    包含简单的动画帧生成逻辑（如史莱姆的蠕动动画）。

    此脚本未集成到主 Web 应用中，仅作为早期的原型验证。
"""

from PIL import Image, ImageDraw
import random
import math


def create_monster_spritesheet(filename="monster_sheet.png"):
    # Monster palette (greens and purples)
    colors = {
        "body": (50, 150, 50),
        "highlight": (100, 200, 100),
        "eye": (255, 255, 0),
        "pupil": (0, 0, 0),
        "outline": (20, 50, 20),
    }

    # Frame size
    w, h = 32, 32
    frames = 4
    sheet_w = w * frames
    sheet_h = h

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for f in range(frames):
        offset_x = f * w

        # Slime pulsating animation
        squish = 0
        if f == 0:
            squish = 0
        elif f == 1:
            squish = 2
        elif f == 2:
            squish = 0
        elif f == 3:
            squish = -2

        cx, cy = offset_x + 16, 24
        radius = 10

        # Draw Blob body (using polygon for pixel look or simple shapes)
        # Using rectangles to simulate pixels for 16-bit look

        # Main body
        x1, y1 = cx - radius - squish, cy - radius + squish
        x2, y2 = cx + radius + squish, cy + radius

        draw.rectangle([x1, y1, x2, y2], fill=colors["body"], outline=colors["outline"])

        # Highlight (shiny slime)
        draw.rectangle([x1 + 4, y1 + 4, x1 + 8, y1 + 8], fill=colors["highlight"])

        # Eye (cyclops)
        eye_y = y1 + 6
        draw.rectangle(
            [cx - 4, eye_y, cx + 4, eye_y + 6],
            fill=colors["eye"],
            outline=colors["outline"],
        )
        draw.rectangle([cx - 1, eye_y + 2, cx + 1, eye_y + 4], fill=colors["pupil"])

    img.save(filename)
    print(f"Monster spritesheet saved to {filename}")


if __name__ == "__main__":
    create_monster_spritesheet()
