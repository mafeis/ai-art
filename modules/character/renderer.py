# renderer.py
# 核心渲染逻辑 (Draw calls, Geometry, VFX)

from PIL import Image, ImageDraw
import random


class CharacterRenderer:
    def __init__(self, color_provider):
        """
        :param color_provider: 一个对象，具有 get_color(key) 和 adjust_color(color, factor) 方法
        """
        self.provider = color_provider

    def _render_instructions(
        self, draw, instructions, offset_x, offset_y, scale, render_mode
    ):
        is_hd = (render_mode == "hd") and (scale >= 4.0)
        is_sketch = render_mode == "sketch"

        for cmd in instructions:
            type_ = cmd[0]

            if type_ == "rect":
                x, y, w, h = cmd[1]
                base_color = self.provider.get_color(cmd[2])
                extra_args = cmd[3:] if len(cmd) > 3 else []
                is_stroke = "stroke" in extra_args

                sx, sy = x * scale, y * scale
                sw, sh = w * scale, h * scale
                x1, y1 = offset_x + sx, offset_y + sy

                if is_stroke:
                    # Stroke logic (used for shield rim)
                    outline_width = int(max(1, scale * 0.1))
                    rx1, ry1 = x1, y1
                    rx2, ry2 = x1 + sw, y1 + sh
                    # Normalize so x2>=x1 and y2>=y1 (PIL requirement)
                    if rx2 < rx1:
                        rx1, rx2 = rx2, rx1
                    if ry2 < ry1:
                        ry1, ry2 = ry2, ry1
                    draw.rectangle(
                        [rx1, ry1, rx2, ry2],
                        outline=base_color,
                        width=outline_width,
                    )
                    continue

                if is_sketch:
                    # Sketch Logic: Jitter and messy lines
                    jitter = scale * 0.1
                    x1 += random.uniform(-jitter, jitter)
                    y1 += random.uniform(-jitter, jitter)

                    # Fill
                    draw.rectangle([x1, y1, x1 + sw, y1 + sh], fill=base_color)

                    # Outline (Wobbly)
                    outline_color = self.provider.adjust_color(base_color, 0.5)
                    outline_width = int(max(1, scale * 0.1))
                    draw.rectangle(
                        [
                            x1 + random.uniform(-1, 1),
                            y1 + random.uniform(-1, 1),
                            x1 + sw + random.uniform(-1, 1),
                            y1 + sh + random.uniform(-1, 1),
                        ],
                        outline=outline_color,
                        width=outline_width,
                    )

                if is_hd:
                    # HD Render: Material-based Shading & Micro-Texture
                    color_key = cmd[2]
                    is_metal = (
                        "metal" in color_key
                        or "gold" in color_key
                        or "silver" in color_key
                    )
                    is_skin = "skin" in color_key
                    is_hair = "hair" in color_key
                    is_glowing = "neon" in color_key or "light" in color_key

                    # 1. Base Fill
                    draw.rectangle([x1, y1, x1 + sw, y1 + sh], fill=base_color)

                    if is_glowing:
                        # Glow: Inner white core
                        if sw > 4 and sh > 4:
                            core_col = (255, 255, 255, 128)
                            draw.rectangle(
                                [x1 + 2, y1 + 2, x1 + sw - 2, y1 + sh - 2],
                                fill=core_col,
                            )

                    elif is_metal:
                        # Metal: High Contrast Glare
                        highlight = self.provider.adjust_color(base_color, 1.4)
                        shadow = self.provider.adjust_color(base_color, 0.6)

                        # Diagonal Sheen
                        draw.rectangle(
                            [x1, y1, x1 + sw, y1 + max(1, scale * 0.5)], fill=highlight
                        )  # Top rim
                        draw.rectangle(
                            [x1, y1, x1 + max(1, scale * 0.5), y1 + sh], fill=highlight
                        )  # Left rim

                        # Deep Shadow
                        draw.rectangle(
                            [x1, y1 + sh - max(1, scale * 0.5), x1 + sw, y1 + sh],
                            fill=shadow,
                        )  # Bot
                        draw.rectangle(
                            [x1 + sw - max(1, scale * 0.5), y1, x1 + sw, y1 + sh],
                            fill=shadow,
                        )  # Right

                    elif is_skin:
                        # Skin: Soft Subsurface Scattering (Reddish shadow)
                        shadow = self.provider.adjust_color(
                            base_color, 0.9
                        )  # Very subtle
                        draw.rectangle(
                            [x1, y1 + sh - max(1, scale * 0.5), x1 + sw, y1 + sh],
                            fill=shadow,
                        )

                    else:  # Cloth / Hair / Wood
                        # Matte Texture with Noise
                        highlight = self.provider.adjust_color(base_color, 1.1)
                        shadow = self.provider.adjust_color(base_color, 0.85)

                        # Rim Light
                        draw.rectangle(
                            [x1, y1, x1 + sw, y1 + max(1, scale * 0.5)], fill=highlight
                        )

                        # Soft Shadow
                        draw.rectangle(
                            [x1, y1 + sh - max(1, scale * 0.5), x1 + sw, y1 + sh],
                            fill=shadow,
                        )

                        # Procedural Noise (Dithering)
                        if sw > 4 and sh > 4:
                            noise_density = 0.05
                            noise_count = int(sw * sh * noise_density)
                            noise_col = self.provider.adjust_color(base_color, 0.95)
                            for _ in range(noise_count):
                                nx = x1 + random.random() * sw
                                ny = y1 + random.random() * sh
                                draw.point((nx, ny), fill=noise_col)

                else:
                    # Retro
                    draw.rectangle([x1, y1, x1 + sw, y1 + sh], fill=base_color)

            elif type_ == "pixel":
                x, y = cmd[1]
                base_color = self.provider.get_color(cmd[2])
                sx, sy = x * scale, y * scale

                if is_sketch:
                    draw.rectangle(
                        [
                            offset_x + sx,
                            offset_y + sy,
                            offset_x + sx + scale,
                            offset_y + sy + scale,
                        ],
                        fill=base_color,
                    )
                elif is_hd:
                    radius = scale * 0.4
                    draw.rounded_rectangle(
                        [
                            offset_x + sx,
                            offset_y + sy,
                            offset_x + sx + scale,
                            offset_y + sy + scale,
                        ],
                        radius=radius,
                        fill=base_color,
                    )
                else:
                    draw.rectangle(
                        [
                            offset_x + sx,
                            offset_y + sy,
                            offset_x + sx + scale,
                            offset_y + sy + scale,
                        ],
                        fill=base_color,
                    )

            elif type_ == "polygon":
                points = [
                    (p[0] * scale + offset_x, p[1] * scale + offset_y) for p in cmd[1]
                ]
                base_color = self.provider.get_color(cmd[2])

                if is_hd:
                    # HD Polygon: Fill
                    draw.polygon(points, fill=base_color)

                    # Material Edge Definition
                    color_key = cmd[2]
                    is_metal = "metal" in color_key or "gold" in color_key

                    if is_metal:
                        # Sharp Highlight Edge
                        edge_col = self.provider.adjust_color(base_color, 1.3)
                        draw.line(points + [points[0]], fill=edge_col, width=1)
                    else:
                        # Subtle Definition
                        edge_col = self.provider.adjust_color(base_color, 0.9)
                        draw.line(points + [points[0]], fill=edge_col, width=1)
                else:
                    draw.polygon(points, fill=base_color)

            elif type_ == "ellipse":
                # ("ellipse", (x, y, w, h), "color")
                x, y, w, h = cmd[1]
                base_color = self.provider.get_color(cmd[2])

                sx, sy = x * scale, y * scale
                sw, sh = w * scale, h * scale
                x1, y1 = offset_x + sx, offset_y + sy

                if is_hd:
                    # HD mode: Subtle gradient or rim light simulation could go here
                    # For now, just clean anti-aliased ellipse
                    outline_color = self.provider.adjust_color(
                        base_color, 0.8
                    )  # Subtle outline
                    draw.ellipse(
                        [x1, y1, x1 + sw, y1 + sh], fill=base_color
                    )  # Outline off for smoothness?
                else:
                    draw.ellipse([x1, y1, x1 + sw, y1 + sh], fill=base_color)

            elif type_ == "circle":
                # ("circle", (cx, cy, r), "color")
                cx, cy, r = cmd[1]
                base_color = self.provider.get_color(cmd[2])

                scx, scy = cx * scale, cy * scale
                sr = r * scale

                x1 = offset_x + scx - sr
                y1 = offset_y + scy - sr
                x2 = offset_x + scx + sr
                y2 = offset_y + scy + sr

                draw.ellipse([x1, y1, x2, y2], fill=base_color)

    def _draw_part_rotated(
        self,
        canvas,
        instructions,
        offset_x,
        offset_y,
        scale,
        render_mode,
        rotation,
        pivot_offset=(0, 0),
    ):
        # Create a temp image large enough to hold the rotated weapon
        size = int(64 * scale)
        temp_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        # Pivot at center of temp image
        pivot_x, pivot_y = size // 2, size // 2

        wp_pivot_x = pivot_offset[0] * scale
        wp_pivot_y = pivot_offset[1] * scale

        draw_start_x = pivot_x - wp_pivot_x
        draw_start_y = pivot_y - wp_pivot_y

        # Render instructions relative to pivot
        self._render_instructions(
            temp_draw, instructions, draw_start_x, draw_start_y, scale, render_mode
        )

        # Rotate
        rotated_img = temp_img.rotate(
            rotation, resample=Image.Resampling.BICUBIC, expand=True
        )

        # Paste back onto canvas
        w, h = rotated_img.size
        paste_x = int(offset_x - w // 2)
        paste_y = int(offset_y - h // 2)

        canvas.alpha_composite(rotated_img, (paste_x, paste_y))

    def draw_vfx(self, canvas, vfx_type, offset_x, offset_y, scale, render_mode):
        draw = ImageDraw.Draw(canvas)

        if vfx_type == "slash":
            color = (200, 200, 255, 180)
            start_angle = -60
            end_angle = 60
            radius = 20 * scale
            size = int(64 * scale)
            temp_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            center = size // 2
            bbox = [center - radius, center - radius, center + radius, center + radius]
            temp_draw.arc(
                bbox, start=start_angle, end=end_angle, fill=color, width=int(3 * scale)
            )
            w, h = temp_img.size
            paste_x = int(offset_x - w // 2)
            paste_y = int(offset_y - h // 2)
            canvas.alpha_composite(temp_img, (paste_x, paste_y))

        elif vfx_type == "shoot_flash":
            color = (255, 255, 200, 240)
            cx, cy = offset_x, offset_y
            r = 6 * scale
            draw.polygon(
                [(cx, cy - r), (cx + r * 2, cy), (cx, cy + r), (cx + r * 0.5, cy)],
                fill=color,
            )

        elif vfx_type == "magic_circle":
            color = (100, 200, 255, 100)
            r = 12 * scale
            draw.ellipse(
                [offset_x - r, offset_y - r, offset_x + r, offset_y + r],
                fill=None,
                outline=color,
                width=int(2 * scale),
            )

        elif vfx_type == "magic_beam":
            color = (100, 255, 255, 180)
            cx, cy = offset_x, offset_y
            draw.ellipse(
                [cx, cy - 4 * scale, cx + 30 * scale, cy + 4 * scale], fill=color
            )

        elif vfx_type == "impact":
            color = (255, 255, 200, 200)
            r = 10 * scale
            draw.ellipse(
                [offset_x - r, offset_y - r, offset_x + r, offset_y + r], fill=color
            )

    def draw_part(
        self,
        draw,
        part_definitions,  # Pass the specific definition dict/list
        offset_x,
        offset_y,
        scale=1.0,
        render_mode="retro",
        canvas=None,
        rotation=0,
        pivot_offset=(0, 0),
    ):
        """
        Generic draw part function.
        part_definitions: List of drawing instructions (rects, pixels, etc.)
        """
        instructions = part_definitions

        if rotation != 0 and canvas:
            self._draw_part_rotated(
                canvas,
                instructions,
                offset_x,
                offset_y,
                scale,
                render_mode,
                rotation,
                pivot_offset,
            )
            return

        # [Fix] Apply pivot offset even if not rotating
        # The pivot point on the sprite (pivot_offset) should align with the anchor (offset_x, offset_y)
        # So we shift the drawing by -pivot
        px = pivot_offset[0] * scale
        py = pivot_offset[1] * scale

        draw_x = offset_x - px
        draw_y = offset_y - py

        self._render_instructions(
            draw, instructions, draw_x, draw_y, scale, render_mode
        )
