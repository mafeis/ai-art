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
                    draw.rectangle(
                        [x1, y1, x1 + sw, y1 + sh],
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

                elif is_hd:
                    # HD Render
                    outline_width = max(1, scale * 0.15)
                    outline_color = self.provider.adjust_color(base_color, 0.6)
                    radius = min(sw, sh) * 0.3
                    draw.rounded_rectangle(
                        [x1, y1, x1 + sw, y1 + sh],
                        radius=radius,
                        fill=base_color,
                        outline=outline_color,
                        width=int(outline_width),
                    )
                    light_color = self.provider.adjust_color(base_color, 1.2)
                    inset = scale * 0.2
                    if sh > inset * 2:
                        draw.rounded_rectangle(
                            [x1 + inset, y1 + inset, x1 + sw - inset, y1 + sh * 0.5],
                            radius=radius * 0.8,
                            fill=light_color,
                        )
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
                    outline_color = self.provider.adjust_color(base_color, 0.6)
                    draw.polygon(points, fill=base_color, outline=outline_color)
                else:
                    draw.polygon(points, fill=base_color)

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

        self._render_instructions(
            draw, instructions, offset_x, offset_y, scale, render_mode
        )
