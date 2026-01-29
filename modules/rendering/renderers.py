from PIL import Image, ImageDraw
import random


class Renderer:
    def __init__(self, palette):
        self.palette = palette

    def get_color(self, key):
        return self.palette.get(key, (255, 0, 255))

    def adjust_color(self, color, factor):
        r, g, b = color
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return (r, g, b)

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        raise NotImplementedError

    def draw_pixel(self, draw, x, y, color_key, offset_x, offset_y, scale):
        # Default to rect
        self.draw_rect(draw, x, y, 1, 1, color_key, offset_x, offset_y, scale)

    def draw_polygon(self, draw, points, color_key, offset_x, offset_y, scale):
        # Default implementation
        fill_color = self.get_color(color_key)
        scaled_points = [
            (p[0] * scale + offset_x, p[1] * scale + offset_y) for p in points
        ]
        draw.polygon(scaled_points, fill=fill_color)


class RetroRenderer(Renderer):
    """Classic Pixel Art"""

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        color = self.get_color(color_key)
        sx, sy = x * scale, y * scale
        sw, sh = w * scale, h * scale
        draw.rectangle(
            [offset_x + sx, offset_y + sy, offset_x + sx + sw, offset_y + sy + sh],
            fill=color,
        )


class VectorRenderer(Renderer):
    """HD Vector / Mobile Game Style"""

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        base_color = self.get_color(color_key)
        sx, sy, sw, sh = x * scale, y * scale, w * scale, h * scale
        x1, y1 = offset_x + sx, offset_y + sy

        # Roundness
        radius = min(sw, sh) * 0.3
        outline_color = self.adjust_color(base_color, 0.6)
        outline_width = int(max(1, scale * 0.15))

        draw.rounded_rectangle(
            [x1, y1, x1 + sw, y1 + sh],
            radius=radius,
            fill=base_color,
            outline=outline_color,
            width=outline_width,
        )

        # Highlight (Gradient sim)
        light_color = self.adjust_color(base_color, 1.2)
        inset = scale * 0.2
        if sh > inset * 2:
            draw.rounded_rectangle(
                [x1 + inset, y1 + inset, x1 + sw - inset, y1 + sh * 0.5],
                radius=radius * 0.8,
                fill=light_color,
            )

        # Shine
        highlight_size = min(sw, sh) * 0.25
        draw.ellipse(
            [
                x1 + sw * 0.1,
                y1 + sh * 0.1,
                x1 + sw * 0.1 + highlight_size,
                y1 + sh * 0.1 + highlight_size,
            ],
            fill=(255, 255, 255, 128),
        )


class SketchRenderer(Renderer):
    """Hand-drawn / Messy Style"""

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        base_color = self.get_color(color_key)
        sx, sy, sw, sh = x * scale, y * scale, w * scale, h * scale

        # Jitter base position
        jitter = scale * 0.15
        x1 = offset_x + sx + random.uniform(-jitter, jitter)
        y1 = offset_y + sy + random.uniform(-jitter, jitter)

        # Fill (Rough)
        draw.rectangle([x1, y1, x1 + sw, y1 + sh], fill=base_color)

        # Outline (Messy, multiple strokes)
        outline_color = self.adjust_color(base_color, 0.4)
        stroke_w = int(max(1, scale * 0.08))

        for _ in range(2):
            jx, jy = random.uniform(-jitter, jitter), random.uniform(-jitter, jitter)
            draw.rectangle(
                [
                    x1 + jx,
                    y1 + jy,
                    x1 + sw + random.uniform(-jitter, jitter),
                    y1 + sh + random.uniform(-jitter, jitter),
                ],
                outline=outline_color,
                width=stroke_w,
            )


class NeonRenderer(Renderer):
    """Cyberpunk / Glow Style"""

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        color = self.get_color(color_key)
        sx, sy, sw, sh = x * scale, y * scale, w * scale, h * scale
        x1, y1 = offset_x + sx, offset_y + sy

        # Draw Glow (Simulated by drawing larger, semi-transparent rects behind?
        # Pillow standard draw doesn't do alpha blend well on RGB. Assuming RGBA canvas.)

        # Since we can't easily blur, we draw outlines
        # Bright center
        bright_color = self.adjust_color(color, 1.5)

        # Outer glow (outline)
        glow_color = color  # Base color is the glow
        draw.rectangle(
            [x1, y1, x1 + sw, y1 + sh],
            fill=(0, 0, 0, 0),
            outline=glow_color,
            width=int(scale * 0.3),
        )

        # Core (Bright white/tint)
        draw.rectangle(
            [
                x1 + scale * 0.2,
                y1 + scale * 0.2,
                x1 + sw - scale * 0.2,
                y1 + sh - scale * 0.2,
            ],
            fill=bright_color,
        )


class InkRenderer(Renderer):
    """Xianxia / Sumi-e Style"""

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        base_color = self.get_color(color_key)
        # Desaturate slightly for ink look? Or rely on palette.

        sx, sy, sw, sh = x * scale, y * scale, w * scale, h * scale
        x1, y1 = offset_x + sx, offset_y + sy

        # Draw overlapping ellipses/circles to simulate brush stroke
        # Instead of a perfect rect, draw blobs
        steps = max(2, int(w))
        radius = sh / 2

        # Horizontal stroke simulation
        for i in range(steps):
            px = x1 + (i / steps) * sw
            jitter_y = random.uniform(-scale * 0.1, scale * 0.1)
            draw.ellipse(
                [px, y1 + jitter_y, px + radius * 2, y1 + sh + jitter_y],
                fill=base_color,
            )

        # Add "bleed" (faint specks)
        if random.random() < 0.3:
            bx = x1 + random.random() * sw
            by = y1 + random.random() * sh
            draw.ellipse(
                [bx, by, bx + scale, by + scale],
                fill=self.adjust_color(base_color, 0.8),
            )


def get_renderer(mode, palette):
    if mode == "hd":
        return VectorRenderer(palette)
    if mode == "sketch":
        return SketchRenderer(palette)
    if mode == "neon":
        return NeonRenderer(palette)
    if mode == "ink":
        return InkRenderer(palette)
    return RetroRenderer(palette)
