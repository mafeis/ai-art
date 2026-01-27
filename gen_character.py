from PIL import Image, ImageDraw
import yaml
import sys
import character_definitions as defs
import io


class CharacterComposer:
    """
    Composes a character from modular parts defined in character_definitions.py.
    """

    def __init__(self, config_source="character_config.yaml"):
        # Load config
        if isinstance(config_source, dict):
            config = config_source
        else:
            try:
                with open(config_source, "r") as f:
                    config = yaml.safe_load(f)
            except (FileNotFoundError, yaml.YAMLError) as e:
                print(f"Error loading config: {e}")
                config = {}  # Fallback to empty

        self.width = config.get("canvas", {}).get("width", 32)
        self.height = config.get("canvas", {}).get("height", 32)

        # Load selections (which style to use for each part)
        self.selections = config.get("parts", {})

        # Load Palette
        self.palette = defs.DEFAULT_PALETTE.copy()
        user_palette = config.get("palette", {})
        for k, v in user_palette.items():
            self.palette[k] = tuple(v) if isinstance(v, (list, tuple)) else v

    def get_color(self, key):
        return self.palette.get(key, (255, 0, 255))  # Magenta default for missing

    def draw_part(self, draw, part_name, style, offset_x, offset_y, scale=1):
        instructions = defs.PART_DEFINITIONS.get(part_name, {}).get(style, [])

        for cmd in instructions:
            type_ = cmd[0]

            if type_ == "rect":
                # ("rect", (x, y, w, h), color)
                x, y, w, h = cmd[1]
                color = self.get_color(cmd[2])
                # Scale coordinates
                sx, sy, sw, sh = x * scale, y * scale, w * scale, h * scale
                draw.rectangle(
                    [
                        offset_x + sx,
                        offset_y + sy,
                        offset_x + sx + sw - 1,
                        offset_y + sy + sh - 1,
                    ],
                    fill=color,
                )

            elif type_ == "pixel":
                # ("pixel", (x, y), color)
                x, y = cmd[1]
                color = self.get_color(cmd[2])
                sx, sy = x * scale, y * scale
                # A pixel scaled up is a rect of size scale x scale
                draw.rectangle(
                    [
                        offset_x + sx,
                        offset_y + sy,
                        offset_x + sx + scale - 1,
                        offset_y + sy + scale - 1,
                    ],
                    fill=color,
                )

            elif type_ == "polygon":
                # ("polygon", [(x,y), ...], color)
                points = [
                    (p[0] * scale + offset_x, p[1] * scale + offset_y) for p in cmd[1]
                ]
                color = self.get_color(cmd[2])
                draw.polygon(points, fill=color)

    def compose_frame(self, draw, offset_x, frame_config, scale=1):
        # Frame config values are in base 32px units
        bob = frame_config.get("bob", 0) * scale
        leg_frame = frame_config.get("leg_f", 0)
        arm_frame = frame_config.get("arm_f", 0)
        global_x_off = frame_config.get("offset_x", 0) * scale

        offset_x += global_x_off

        # Hand Logic (scaled)
        hand_x_base, hand_y_base = 20, 17
        hand_x, hand_y = hand_x_base * scale, (hand_y_base * scale) + bob

        if arm_frame == 1:
            hand_x += 2 * scale
            hand_y += 3 * scale
        elif arm_frame == -1:
            hand_x += 1 * scale
            hand_y += 4 * scale
        elif arm_frame == 2:
            hand_x += 4 * scale
            hand_y -= 2 * scale

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

            # Helper to scale logic
            def s(val):
                return val * scale

            if layer == "back":
                style = self.selections.get("back", "none")
                self.draw_part(draw, "back", style, offset_x, bob, scale)

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
                self.draw_part(draw, "legs", style, offset_x + lx, ly, scale)

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
                self.draw_part(draw, "legs", style, offset_x + rx, ry, scale)

            elif layer == "arms":
                color = self.get_color("shirt")
                ay = s(17) + bob
                if arm_frame == 0:
                    draw.rectangle(
                        [offset_x + s(10), ay, offset_x + s(11), ay + s(6)], fill=color
                    )
                    draw.rectangle(
                        [offset_x + s(20), ay, offset_x + s(21), ay + s(6)], fill=color
                    )
                elif arm_frame == 1:
                    draw.rectangle(
                        [offset_x + s(10), ay - s(1), offset_x + s(11), ay + s(5)],
                        fill=color,
                    )
                    draw.rectangle(
                        [offset_x + s(20), ay + s(1), offset_x + s(22), ay + s(4)],
                        fill=color,
                    )
                elif arm_frame == -1:
                    draw.rectangle(
                        [offset_x + s(10), ay + s(1), offset_x + s(12), ay + s(4)],
                        fill=color,
                    )
                    draw.rectangle(
                        [offset_x + s(20), ay - s(1), offset_x + s(21), ay + s(5)],
                        fill=color,
                    )
                elif arm_frame == 2:
                    draw.rectangle(
                        [offset_x + s(20), ay - s(2), offset_x + s(24), ay], fill=color
                    )
                    draw.rectangle(
                        [offset_x + s(10), ay + s(1), offset_x + s(11), ay + s(6)],
                        fill=color,
                    )

            elif layer == "held":
                style = self.selections.get("held", "none")
                if style != "none":
                    self.draw_part(
                        draw, "held", style, offset_x + hand_x, hand_y, scale
                    )

            elif layer in ["body", "head", "eyes", "hair"]:
                self.draw_part(draw, part_key, style, offset_x, bob, scale)


def create_character_spritesheet(
    filename=None,
    config_source="character_config.yaml",
    action="walk",
    resolution=128,
    render_mode="retro",
):
    """
    render_mode: 'retro' (scale after), 'hd' (scale coords)
    """
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )
    frames = len(anim_def)

    # Base dimensions
    base_w, base_h = composer.width, composer.height  # 32x32

    scale_factor = 1
    if render_mode == "hd":
        scale_factor = max(1, resolution // base_h)
        draw_w, draw_h = base_w * scale_factor, base_h * scale_factor
    else:
        draw_w, draw_h = base_w, base_h

    sheet_w = draw_w * frames
    sheet_h = draw_h

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for f in range(frames):
        config = anim_def[f]
        composer.compose_frame(draw, f * draw_w, config, scale=scale_factor)

    # Post-process resize for Retro mode
    if render_mode == "retro" and resolution != base_h:
        # Scale whole sheet
        target_scale = resolution / base_h
        new_w = int(sheet_w * target_scale)
        new_h = int(sheet_h * target_scale)
        img = img.resize((new_w, new_h), Image.NEAREST)

    if filename:
        img.save(filename)

    return img


def create_character_gif(
    config_source="character_config.yaml",
    action="walk",
    resolution=128,
    render_mode="retro",
):
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )

    base_w, base_h = composer.width, composer.height

    scale_factor = 1
    if render_mode == "hd":
        scale_factor = max(1, resolution // base_h)
        draw_w, draw_h = base_w * scale_factor, base_h * scale_factor
    else:
        draw_w, draw_h = base_w, base_h

    frames = []
    for f_config in anim_def:
        frame_img = Image.new("RGBA", (draw_w, draw_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        composer.compose_frame(draw, 0, f_config, scale=scale_factor)

        if render_mode == "retro" and resolution != base_h:
            target_scale = resolution / base_h
            new_w = int(draw_w * target_scale)
            new_h = int(draw_h * target_scale)
            frame_img = frame_img.resize((new_w, new_h), Image.NEAREST)

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
    # Test
    create_character_spritesheet("test_hd.png", resolution=128, render_mode="hd")
