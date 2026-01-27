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

    def draw_part(self, draw, part_name, style, offset_x, offset_y, leg_offset=0):
        instructions = defs.PART_DEFINITIONS.get(part_name, {}).get(style, [])

        for cmd in instructions:
            type_ = cmd[0]

            if type_ == "rect":
                # ("rect", (x, y, w, h), color)
                x, y, w, h = cmd[1]
                color = self.get_color(cmd[2])
                draw.rectangle(
                    [
                        x + offset_x,
                        y + offset_y,
                        x + offset_x + w - 1,
                        y + offset_y + h - 1,
                    ],
                    fill=color,
                )

            elif type_ == "pixel":
                # ("pixel", (x, y), color)
                x, y = cmd[1]
                color = self.get_color(cmd[2])
                draw.point((x + offset_x, y + offset_y), fill=color)

            elif type_ == "polygon":
                # ("polygon", [(x,y), ...], color)
                points = [(p[0] + offset_x, p[1] + offset_y) for p in cmd[1]]
                color = self.get_color(cmd[2])
                draw.polygon(points, fill=color)

    def compose_frame(self, draw, offset_x, frame_config):
        bob = frame_config.get("bob", 0)
        leg_frame = frame_config.get("leg_f", 0)  # -1 left, 0 stand, 1 right, 2 wide
        arm_frame = frame_config.get("arm_f", 0)  # 0 idle, 1 swing, 2 raised
        global_x_off = frame_config.get("offset_x", 0)

        # Apply global offset for animations like "hurt"
        offset_x += global_x_off

        # Calculate Hand Positions (for Held items)
        # Base arm pos: x=10, y=17 (Left), x=20, y=17 (Right)
        # We track the RIGHT hand (front) for the weapon
        hand_x, hand_y = 20, 17 + bob
        if arm_frame == 1:
            hand_x += 2
            hand_y += 3  # Swing Fwd
        elif arm_frame == -1:
            hand_x += 1
            hand_y += 4  # Swing Back (less likely for right hand in walk?)
        elif arm_frame == 2:
            hand_x += 4
            hand_y -= 2  # Raised

        for layer in defs.LAYER_ORDER:
            part_key = layer
            if layer in ["legs_back", "legs_front"]:
                part_key = "legs"
            if layer == "arms":
                part_key = "body"

            style = self.selections.get(part_key, "none")

            # Default fallbacks
            if style == "none" and part_key in ["head", "body", "legs"]:
                if part_key == "head":
                    style = "human"
                if part_key == "body":
                    style = "shirt"
                if part_key == "legs":
                    style = "pants"

            # Back Layer
            if layer == "back":
                style = self.selections.get("back", "none")
                self.draw_part(draw, "back", style, offset_x, bob)

            # Legs
            elif layer == "legs_back":
                lx, ly = 12, 24 + bob
                if leg_frame == -1:
                    lx -= 1
                    ly -= 1
                if leg_frame == 1:
                    lx += 1
                if leg_frame == 2:
                    lx -= 2
                    ly += 1
                if leg_frame == -2:
                    lx -= 2
                    ly -= 4  # High knee
                self.draw_part(draw, "legs", style, offset_x + lx, ly)

            elif layer == "legs_front":
                rx, ry = 17, 24 + bob
                if leg_frame == -1:
                    rx += 1
                if leg_frame == 1:
                    rx -= 1
                    ry -= 1
                if leg_frame == 2:
                    rx += 2
                    ry += 1
                if leg_frame == -2:
                    rx += 1
                    ry -= 1
                self.draw_part(draw, "legs", style, offset_x + rx, ry)

            # Arms
            elif layer == "arms":
                color = self.get_color("shirt")
                ay = 17 + bob
                if arm_frame == 0:
                    draw.rectangle(
                        [offset_x + 10, ay, offset_x + 11, ay + 6], fill=color
                    )  # L
                    draw.rectangle(
                        [offset_x + 20, ay, offset_x + 21, ay + 6], fill=color
                    )  # R
                elif arm_frame == 1:
                    draw.rectangle(
                        [offset_x + 10, ay - 1, offset_x + 11, ay + 5], fill=color
                    )  # L Back
                    draw.rectangle(
                        [offset_x + 20, ay + 1, offset_x + 22, ay + 4], fill=color
                    )  # R Fwd
                elif arm_frame == -1:
                    draw.rectangle(
                        [offset_x + 10, ay + 1, offset_x + 12, ay + 4], fill=color
                    )  # L Fwd
                    draw.rectangle(
                        [offset_x + 20, ay - 1, offset_x + 21, ay + 5], fill=color
                    )  # R Back
                elif arm_frame == 2:
                    draw.rectangle(
                        [offset_x + 20, ay - 2, offset_x + 24, ay], fill=color
                    )  # R Raised
                    draw.rectangle(
                        [offset_x + 10, ay + 1, offset_x + 11, ay + 6], fill=color
                    )  # L Idle

            # Held Items (Weapons)
            elif layer == "held":
                style = self.selections.get("held", "none")
                if style != "none":
                    self.draw_part(draw, "held", style, offset_x + hand_x, hand_y)

            # Core Body Parts
            elif layer in ["body", "head", "eyes", "hair"]:
                self.draw_part(draw, part_key, style, offset_x, bob)


def create_character_spritesheet(
    filename=None, config_source="character_config.yaml", action="walk"
):
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )
    frames = len(anim_def)

    sheet_w = composer.width * frames
    sheet_h = composer.height

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for f in range(frames):
        config = anim_def[f]
        composer.compose_frame(draw, f * composer.width, config)

    if filename:
        img.save(filename)

    return img


def create_character_gif(config_source="character_config.yaml", action="walk"):
    composer = CharacterComposer(config_source)
    anim_def = defs.ANIMATION_DEFINITIONS.get(
        action, defs.ANIMATION_DEFINITIONS["walk"]
    )

    frames = []
    for f_config in anim_def:
        frame_img = Image.new("RGBA", (composer.width, composer.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        composer.compose_frame(draw, 0, f_config)
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
    create_character_spritesheet("character_sheet.png")
