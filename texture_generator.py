"""
程序化纹理生成器
用于为像素角色添加艺术质感（纸张、金属、噪点、扫描线等）
"""

import random
from PIL import Image, ImageDraw


def generate_paper_texture(size, grain_intensity=0.3):
    """
    生成纸张纹理（程序化噪点）
    适用于水墨、手绘风格
    """
    width, height = size
    texture = Image.new("RGB", size, (245, 240, 230))  # 米黄纸底
    pixels = texture.load()

    for y in range(height):
        for x in range(width):
            # 添加随机噪点模拟纸张纤维
            noise = random.randint(-15, 15)
            base = 240
            r = max(0, min(255, base + int(noise * grain_intensity)))
            g = max(0, min(255, base - 5 + int(noise * grain_intensity)))
            b = max(0, min(255, base - 10 + int(noise * grain_intensity)))
            pixels[x, y] = (r, g, b)

    return texture


def generate_scanline_texture(size, line_spacing=2, orientation="horizontal"):
    """
    生成扫描线纹理（CRT/赛博效果）
    适用于复古、赛博朋克风格
    """
    width, height = size
    texture = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)

    if orientation == "horizontal":
        for y in range(0, height, line_spacing):
            # 深色扫描线
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, 60), width=1)
    else:  # vertical
        for x in range(0, width, line_spacing):
            draw.line([(x, 0), (x, height)], fill=(0, 0, 0, 60), width=1)

    return texture


def generate_noise_texture(size, intensity=0.2):
    """
    生成噪点纹理（随机颗粒）
    适用于复古、电影质感
    """
    width, height = size
    texture = Image.new("RGB", size, (128, 128, 128))
    pixels = texture.load()

    for y in range(height):
        for x in range(width):
            noise_val = random.randint(0, 255)
            alpha = int(255 * intensity)
            pixels[x, y] = (noise_val, noise_val, noise_val)

    return texture


def generate_gradient_texture(size, color_start, color_end, direction="vertical"):
    """
    生成渐变纹理
    适用于矢量、现代风格
    """
    width, height = size
    texture = Image.new("RGB", size)
    draw = ImageDraw.Draw(texture)

    if direction == "vertical":
        for y in range(height):
            ratio = y / height
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return texture


def generate_metal_texture(size):
    """
    生成金属质感纹理（用于蒸汽朋克）
    模拟拉丝金属效果
    """
    width, height = size
    texture = Image.new("RGB", size, (120, 120, 130))
    pixels = texture.load()

    # 垂直拉丝效果
    for x in range(width):
        brush_variation = random.randint(-20, 20)
        for y in range(height):
            base = 130
            val = max(0, min(255, base + brush_variation + random.randint(-5, 5)))
            pixels[x, y] = (val - 10, val - 10, val)

    return texture


def apply_vignette(image, intensity=0.3):
    """
    添加暗角效果（四周渐暗）
    增强艺术感和聚焦
    """
    width, height = image.size
    vignette = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(vignette)

    # 中心点
    cx, cy = width // 2, height // 2
    max_radius = ((width**2 + height**2) ** 0.5) / 2

    for y in range(height):
        for x in range(width):
            # 计算距离中心的距离
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            ratio = dist / max_radius
            darkness = int(255 * (1 - ratio * intensity))
            darkness = max(0, min(255, darkness))

    # 简化版：用椭圆渐变模拟
    for i in range(10):
        scale = 1 - (i / 10) * intensity
        ellipse_box = [
            int(cx - width * scale / 2),
            int(cy - height * scale / 2),
            int(cx + width * scale / 2),
            int(cy + height * scale / 2),
        ]
        alpha = int(255 * (1 - i / 10 * intensity))
        draw.ellipse(ellipse_box, fill=alpha)

    return Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), vignette)
