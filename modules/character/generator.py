from PIL import Image, ImageDraw
import yaml
import time
from modules.character import definitions as defs
from modules.rendering import post_effects  # 艺术滤镜系统
from modules.character.renderer import CharacterRenderer
import io


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

        self.width = config.get("canvas", {}).get("width", 64)
        self.height = config.get("canvas", {}).get("height", 64)

        # 居中偏移量
        design_w, design_h = 32, 32
        self.base_offset_x = (self.width - design_w) // 2
        self.base_offset_y = (self.height - design_h) // 2

        self.selections = config.get("parts", {})
        self.palette = defs.DEFAULT_PALETTE.copy()
        user_palette = config.get("palette", {})
        for k, v in user_palette.items():
            self.palette[k] = tuple(v) if isinstance(v, (list, tuple)) else v

        # 初始化渲染器，将自身作为颜色提供者
        self.renderer = CharacterRenderer(self)

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

    def compose_frame(
        self,
        draw,
        offset_x,
        frame_config,
        scale=1.0,
        render_mode="retro",
        canvas=None,
    ):
        """
        组合每一帧的画面
        """
        # 动画帧的基础位移
        bob = frame_config.get("bob", 0) * scale
        leg_frame = frame_config.get("leg_f", 0)
        arm_frame = frame_config.get("arm_f", 0)
        global_x_off = frame_config.get("offset_x", 0) * scale
        rotation = frame_config.get("rot", 0)
        vfx = frame_config.get("vfx", None)

        # 应用全局居中偏移量
        current_base_x = offset_x + (self.base_offset_x * scale) + global_x_off
        current_base_y = (self.base_offset_y * scale) + bob

        def s(val):
            return val * scale

        # 手部基准位置修正 (基于居中后的坐标)
        # 原逻辑是 hand_x_base = 20, hand_y_base = 17 (在 32x32 网格中)
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
        elif arm_frame == 3:
            hand_x += s(8)
            hand_y -= s(4)
        elif arm_frame == 4:
            hand_x += s(6)
            hand_y -= s(6)

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

            # 获取部件的具体绘制指令
            instructions = defs.PART_DEFINITIONS.get(part_key, {}).get(style, [])

            # 绘制各个部件
            if layer == "back":
                style = self.selections.get("back", "none")
                # Need to re-fetch instructions because style changed
                back_instructions = defs.PART_DEFINITIONS.get("back", {}).get(style, [])
                self.renderer.draw_part(
                    draw,
                    back_instructions,
                    current_base_x,
                    current_base_y,
                    scale,
                    render_mode,
                    canvas=canvas,
                )

            elif layer == "legs_back":
                lx, ly = s(12), s(24)
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

                self.renderer.draw_part(
                    draw,
                    instructions,
                    current_base_x + lx,
                    current_base_y + s(24) - bob + (ly - s(24)) + bob,
                    scale,
                    render_mode,
                    canvas=canvas,
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

                final_x = offset_x + (self.base_offset_x * scale) + global_x_off + rx
                final_y = (self.base_offset_y * scale) + ry

                self.renderer.draw_part(
                    draw,
                    instructions,
                    final_x,
                    final_y,
                    scale,
                    render_mode,
                    canvas=canvas,
                )

            elif layer == "arms":
                color = self.get_color("shirt")
                ay = (self.base_offset_y * scale) + s(17) + bob
                ax_base = offset_x + (self.base_offset_x * scale) + global_x_off

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

                # Arm Procedural Drawing (Still handled here as it is not a static part definition)
                l_rect = [ax_base + s(10), ay, ax_base + s(11), ay + s(6)]
                r_rect = [ax_base + s(20), ay, ax_base + s(21), ay + s(6)]

                if arm_frame == 1:
                    l_rect = [ax_base + s(10), ay - s(1), ax_base + s(11), ay + s(5)]
                    r_rect = [ax_base + s(20), ay + s(1), ax_base + s(22), ay + s(4)]
                elif arm_frame == -1:
                    l_rect = [ax_base + s(10), ay + s(1), ax_base + s(12), ay + s(4)]
                    r_rect = [ax_base + s(20), ay - s(1), ax_base + s(21), ay + s(5)]
                elif arm_frame == 2:
                    r_rect = [ax_base + s(20), ay - s(2), ax_base + s(24), ay]
                    l_rect = [ax_base + s(10), ay + s(1), ax_base + s(11), ay + s(6)]
                elif arm_frame == 3:
                    r_rect = [
                        ax_base + s(20),
                        ay - s(4),
                        ax_base + s(28),
                        ay - s(2),
                    ]  # Stretch
                    l_rect = [ax_base + s(10), ay + s(2), ax_base + s(12), ay + s(6)]
                elif arm_frame == 4:
                    r_rect = [
                        ax_base + s(20),
                        ay - s(6),
                        ax_base + s(26),
                        ay - s(4),
                    ]  # Up high
                    l_rect = [ax_base + s(10), ay + s(1), ax_base + s(11), ay + s(6)]

                rect_func(l_rect, **kwargs)
                rect_func(r_rect, **kwargs)

            elif layer == "held":
                style = self.selections.get("held", "none")
                if style != "none":
                    final_hand_x = (
                        offset_x + (self.base_offset_x * scale) + global_x_off + hand_x
                    )
                    final_hand_y = (self.base_offset_y * scale) + hand_y

                    wp_meta = defs.WEAPON_METADATA.get(style, {"pivot": (0, 0)})
                    pivot = wp_meta.get("pivot", (0, 0))

                    held_instructions = defs.PART_DEFINITIONS.get("held", {}).get(
                        style, []
                    )

                    self.renderer.draw_part(
                        draw,
                        held_instructions,
                        final_hand_x,
                        final_hand_y,
                        scale,
                        render_mode,
                        canvas=canvas,
                        rotation=rotation,
                        pivot_offset=pivot,
                    )

            elif layer in ["body", "head", "eyes", "hair"]:
                self.renderer.draw_part(
                    draw,
                    instructions,
                    current_base_x,
                    current_base_y,
                    scale,
                    render_mode,
                    canvas=canvas,
                )

        # Draw VFX on top
        if vfx and canvas:
            vfx_x = offset_x + (self.base_offset_x * scale) + global_x_off + hand_x
            vfx_y = (self.base_offset_y * scale) + hand_y
            vfx_x += s(16)  # In front of player
            self.renderer.draw_vfx(canvas, vfx, vfx_x, vfx_y, scale, render_mode)


def create_character_spritesheet(
    filename=None,
    config_source="character_config.yaml",
    action="walk",
    density=1.0,
    output_size=512,
    render_mode="retro",
):
    if render_mode == "premium" and density < 8.0:
        density = 8.0
    elif render_mode == "hibit" and density < 4.0:
        density = 4.0

    composer = CharacterComposer(config_source)

    # Resolve sub-animation for attack based on weapon
    final_action = action
    if action == "attack":
        weapon = composer.selections.get("held", "none")
        weapon_info = defs.WEAPON_METADATA.get(weapon, {"type": "slash"})
        attack_type = weapon_info.get("type", "slash")

        candidate_action = f"attack_{attack_type}"
        if candidate_action in defs.ANIMATION_DEFINITIONS:
            final_action = candidate_action
        else:
            final_action = "attack"

    anim_def = defs.ANIMATION_DEFINITIONS.get(
        final_action, defs.ANIMATION_DEFINITIONS["walk"]
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
            draw,
            f * draw_w,
            config,
            scale=internal_scale,
            render_mode=render_mode,
            canvas=img,
        )

    target_h = output_size
    target_w = int(target_h * (sheet_w / sheet_h))

    resample_mode = (
        Image.Resampling.LANCZOS if density >= 4.0 else Image.Resampling.NEAREST
    )
    img = img.resize((target_w, target_h), resample_mode)

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
    if render_mode == "premium" and density < 8.0:
        density = 8.0
    elif render_mode == "hibit" and density < 4.0:
        density = 4.0

    composer = CharacterComposer(config_source)

    final_action = action
    if action == "attack":
        weapon = composer.selections.get("held", "none")
        weapon_info = defs.WEAPON_METADATA.get(weapon, {"type": "slash"})
        attack_type = weapon_info.get("type", "slash")

        candidate_action = f"attack_{attack_type}"
        if candidate_action in defs.ANIMATION_DEFINITIONS:
            final_action = candidate_action
        else:
            final_action = "attack"

    anim_def = defs.ANIMATION_DEFINITIONS.get(
        final_action, defs.ANIMATION_DEFINITIONS["walk"]
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
            draw,
            0,
            f_config,
            scale=internal_scale,
            render_mode=render_mode,
            canvas=frame_img,
        )

        target_h = output_size
        target_w = int(target_h * (draw_w / draw_h))
        resample_mode = (
            Image.Resampling.LANCZOS if density >= 4.0 else Image.Resampling.NEAREST
        )
        frame_img = frame_img.resize((target_w, target_h), resample_mode)

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
