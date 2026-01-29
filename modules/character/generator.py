from PIL import Image, ImageDraw
import yaml
import sys
from modules.character import definitions as defs
from modules.rendering import post_effects  # 艺术滤镜系统
import io
import random


class CharacterComposer:
    def __init__(self, config_source="character_config.yaml"):
        if isinstance(config_source, dict):
            config = config_source
        else:
            try:
                with open(config_source, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
            except (FileNotFoundError, yaml.YAMLError) as e:
                print(f"Error loading config: {e}")
                config = {}

        self.width = config.get("canvas", {}).get("width", 32)
        self.height = config.get("canvas", {}).get("height", 32)
        self.selections = config.get("parts", {})
        self.palette = defs.DEFAULT_PALETTE.copy()
        user_palette = config.get("palette", {})
        for k, v in user_palette.items():
            self.palette[k] = tuple(v) if isinstance(v, (list, tuple)) else v

    def get_color(self, key):
        return self.palette.get(key, (255, 0, 255))

    def adjust_color(self, color, factor):
        # Unpack explicitly to handle potential RGBA inputs gracefully
        if len(color) >= 3:
            r, g, b = color[:3]
            a = color[3] if len(color) > 3 else None
        else:
            # Fallback for weird data
            r, g, b = 0, 0, 0
            a = None

        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))

        if a is not None:
            return (r, g, b, a)
        return (r, g, b)

    def draw_part(
        self, draw, part_name, style, offset_x, offset_y, scale=1.0, render_mode="retro"
    ):
        instructions = defs.PART_DEFINITIONS.get(part_name, {}).get(style, [])

        is_hd = (render_mode == "hd") and (scale >= 4.0)
        is_sketch = render_mode == "sketch"

        for cmd in instructions:
            type_ = cmd[0]

            if type_ == "rect":
                x, y, w, h = cmd[1]
                base_color = self.get_color(cmd[2])

                sx, sy = x * scale, y * scale
                sw, sh = w * scale, h * scale
                x1, y1 = offset_x + sx, offset_y + sy

                if is_sketch:
                    # Sketch Logic: Jitter and messy lines
                    jitter = scale * 0.1
                    x1 += random.uniform(-jitter, jitter)
                    y1 += random.uniform(-jitter, jitter)
                    # Draw multiple lines to simulate stroke? Or just a slightly rotated/offset rect
                    # Simple approach: Draw outline slightly offset from fill

                    # Fill
                    draw.rectangle([x1, y1, x1 + sw, y1 + sh], fill=base_color)

                    # Outline (Wobbly)
                    outline_color = self.adjust_color(base_color, 0.5)
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
                    outline_color = self.adjust_color(base_color, 0.6)
                    radius = min(sw, sh) * 0.3
                    draw.rounded_rectangle(
                        [x1, y1, x1 + sw, y1 + sh],
                        radius=radius,
                        fill=base_color,
                        outline=outline_color,
                        width=int(outline_width),
                    )
                    light_color = self.adjust_color(base_color, 1.2)
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
                base_color = self.get_color(cmd[2])
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
                base_color = self.get_color(cmd[2])

                if is_hd:
                    outline_color = self.adjust_color(base_color, 0.6)
                    draw.polygon(points, fill=base_color, outline=outline_color)
                else:
                    draw.polygon(points, fill=base_color)

    def compose_frame(
        self, draw, offset_x, frame_config, scale=1.0, render_mode="retro"
    ):
        bob = frame_config.get("bob", 0) * scale
        leg_frame = frame_config.get("leg_f", 0)
        arm_frame = frame_config.get("arm_f", 0)
        global_x_off = frame_config.get("offset_x", 0) * scale

        offset_x += global_x_off

        def s(val):
            return val * scale

        hand_x_base, hand_y_base = 20, 17
        hand_x, hand_y = s(hand_x_base), s(hand_y_base) + bob

        if arm_frame == 1:
            hand_x += s(2)
            hand_y += s(3)
        elif arm_frame == -1:
            hand_x += s(1)
            hand_y += s(4)
        elif arm_frame == 2:
            hand_x += s(4)
            hand_y -= s(2)

        for layer in defs.LAYER_ORDER:
            part_key = layer
            if layer in ["legs_back", "legs_front"]:
                part_key = "legs"
            if layer == "arms":
                part_key = "body"

            style = self.selections.get(part_key, "none")

            if style == "none" and part_key in ["head", "body", "legs"]:
                if part_key == "head":
                    style = "human"
                if part_key == "body":
                    style = "shirt"
                if part_key == "legs":
                    style = "pants"

            if layer == "back":
                style = self.selections.get("back", "none")
                self.draw_part(draw, "back", style, offset_x, bob, scale, render_mode)

            elif layer == "legs_back":
                lx, ly = s(12), s(24) + bob
                if leg_frame == -1:
                    lx -= s(1)
                    ly -= s(1)
                if leg_frame == 1:
                    lx += s(1)
                if leg_frame == 2:
                    lx -= s(2)
                    ly += s(1)
                if leg_frame == -2:
                    lx -= s(2)
                    ly -= s(4)
                self.draw_part(
                    draw, "legs", style, offset_x + lx, ly, scale, render_mode
                )

            elif layer == "legs_front":
                rx, ry = s(17), s(24) + bob
                if leg_frame == -1:
                    rx += s(1)
                if leg_frame == 1:
                    rx -= s(1)
                    ry -= s(1)
                if leg_frame == 2:
                    rx += s(2)
                    ry += s(1)
                if leg_frame == -2:
                    rx += s(1)
                    ry -= s(1)
                self.draw_part(
                    draw, "legs", style, offset_x + rx, ry, scale, render_mode
                )

            elif layer == "arms":
                color = self.get_color("shirt")
                ay = s(17) + bob

                is_hd = (render_mode == "hd") and (scale >= 4.0)
                is_sketch = render_mode == "sketch"

                rect_func = draw.rectangle
                kwargs = {"fill": color}

                if is_hd:
                    radius = scale * 0.4
                    outline_color = self.adjust_color(color, 0.6)
                    kwargs = {
                        "radius": radius,
                        "fill": color,
                        "outline": outline_color,
                        "width": int(max(1, scale * 0.15)),
                    }
                    rect_func = draw.rounded_rectangle
                elif is_sketch:
                    kwargs = {"fill": color, "outline": self.adjust_color(color, 0.5)}
                    # rect_func remains draw.rectangle but we rely on simple draw for procedural arms
                    # Arms in sketch mode might look too clean. Let's apply jitter manually?
                    # For now, just use standard rect

                # Arm Coords
                l_rect = [offset_x + s(10), ay, offset_x + s(11), ay + s(6)]
                r_rect = [offset_x + s(20), ay, offset_x + s(21), ay + s(6)]

                if arm_frame == 1:
                    l_rect = [offset_x + s(10), ay - s(1), offset_x + s(11), ay + s(5)]
                    r_rect = [offset_x + s(20), ay + s(1), offset_x + s(22), ay + s(4)]
                elif arm_frame == -1:
                    l_rect = [offset_x + s(10), ay + s(1), offset_x + s(12), ay + s(4)]
                    r_rect = [offset_x + s(20), ay - s(1), offset_x + s(21), ay + s(5)]
                elif arm_frame == 2:
                    r_rect = [offset_x + s(20), ay - s(2), offset_x + s(24), ay]
                    l_rect = [offset_x + s(10), ay + s(1), offset_x + s(11), ay + s(6)]

                rect_func(l_rect, **kwargs)
                rect_func(r_rect, **kwargs)

            elif layer == "held":
                style = self.selections.get("held", "none")
                if style != "none":
                    self.draw_part(
                        draw,
                        "held",
                        style,
                        offset_x + hand_x,
                        hand_y,
                        scale,
                        render_mode,
                    )

            elif layer in ["body", "head", "eyes", "hair"]:
                self.draw_part(draw, part_key, style, offset_x, bob, scale, render_mode)


def create_character_spritesheet(
    filename=None,
    config_source="character_config.yaml",
    action="walk",
    density=1.0,
    output_size=512,
    render_mode="retro",
):
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )
    frames = len(anim_def)
    base_w, base_h = composer.width, composer.height
    internal_scale = density
    draw_w = int(base_w * internal_scale)
    draw_h = int(base_h * internal_scale)
    sheet_w = draw_w * frames
    sheet_h = draw_h

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for f in range(frames):
        config = anim_def[f]
        composer.compose_frame(
            draw, f * draw_w, config, scale=internal_scale, render_mode=render_mode
        )

    target_h = output_size
    target_w = int(target_h * (sheet_w / sheet_h))

    resample_mode = (
        Image.Resampling.LANCZOS if density >= 4.0 else Image.Resampling.NEAREST
    )
    img = img.resize((target_w, target_h), resample_mode)

    # 应用艺术滤镜后处理
    effect_func = post_effects.get_post_effect_for_mode(render_mode)
    img = effect_func(img)

    if filename:
        img.save(filename)
    return img


def create_character_gif(
    config_source="character_config.yaml",
    action="walk",
    density=1.0,
    output_size=512,
    render_mode="retro",
):
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )
    base_w, base_h = composer.width, composer.height
    internal_scale = density
    draw_w = int(base_w * internal_scale)
    draw_h = int(base_h * internal_scale)

    frames = []
    for f_config in anim_def:
        frame_img = Image.new("RGBA", (draw_w, draw_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        composer.compose_frame(
            draw, 0, f_config, scale=internal_scale, render_mode=render_mode
        )

        target_h = output_size
        target_w = int(target_h * (draw_w / draw_h))
        resample_mode = (
            Image.Resampling.LANCZOS if density >= 4.0 else Image.Resampling.NEAREST
        )
        frame_img = frame_img.resize((target_w, target_h), resample_mode)

        # 应用艺术滤镜（每一帧都处理）
        effect_func = post_effects.get_post_effect_for_mode(render_mode)
        frame_img = effect_func(frame_img)

        frames.append(frame_img)

    buf = io.BytesIO()
    frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=150,
        loop=0,
        transparency=0,
        disposal=2,
    )
    buf.seek(0)
    return buf


if __name__ == "__main__":
    create_character_spritesheet(
        "test_sketch.png", density=8.0, output_size=512, render_mode="sketch"
    )
