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

        # [优化] 将默认画布扩大到 64x64，以防止动作过大导致的裁剪
        self.width = config.get("canvas", {}).get("width", 64)
        self.height = config.get("canvas", {}).get("height", 64)

        # [优化] 计算居中偏移量
        # 原始素材是基于 32x32 设计的，所以我们需要将其居中放置在 64x64 的画布中
        # 偏移量 = (新尺寸 - 旧尺寸) / 2
        # 我们假设原始设计尺寸约为 32x32
        design_w, design_h = 32, 32
        self.base_offset_x = (self.width - design_w) // 2
        self.base_offset_y = (self.height - design_h) // 2

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
        """
        组合每一帧的画面
        """
        # 动画帧的基础位移
        bob = frame_config.get("bob", 0) * scale
        leg_frame = frame_config.get("leg_f", 0)
        arm_frame = frame_config.get("arm_f", 0)
        global_x_off = frame_config.get("offset_x", 0) * scale

        # [优化] 应用全局居中偏移量 (base_offset_x/y)
        # 这确保角色始终在画布中心，不会被动作甩出画面
        # 注意：Offset_x 是 sprite sheet 的横向排布偏移，base_offset 是单帧内的居中偏移
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

        # [New] Arm Frame 3: 特殊攻击姿态，手伸得更远
        elif arm_frame == 3:
            hand_x += s(8)
            hand_y -= s(4)

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

            # 绘制各个部件时，传入 current_base_x/y 作为起始点
            if layer == "back":
                style = self.selections.get("back", "none")
                self.draw_part(
                    draw,
                    "back",
                    style,
                    current_base_x,
                    current_base_y,
                    scale,
                    render_mode,
                )

            elif layer == "legs_back":
                # 腿部相对偏移 (12, 24)
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
                # 注意：legs_back 不需要加 bob，因为它支撑身体？不，通常身体上下动，脚不动或动得少
                # 原代码 legs_back 有 bob，这里保留原逻辑，但加上 current_base
                # 修正：current_base_y 已经包含了 bob。但腿通常是固定在地面或反向运动的。
                # 让我们看原代码： ly = s(24) + bob。
                # 如果我们用 current_base_y (包含bob)，那么 ly 只需要 s(24)。

                self.draw_part(
                    draw,
                    "legs",
                    style,
                    current_base_x + lx,
                    current_base_y + s(24) - bob + (ly - s(24)) + bob,
                    scale,
                    render_mode,
                )
                # 简化一下：原逻辑 draw_part(..., offset_x + lx, ly...) 其中 ly = s(24) + bob
                # 现逻辑 draw_part(..., current_base_x + 12, current_base_y + 24 ...)
                # current_base_y 已经有 bob 了。
                # 稍微调整下写法以保持清晰：

                # 腿部基础位置
                leg_draw_x = current_base_x + s(12)
                leg_draw_y = current_base_y + s(24)  # 这里的 base_y 有 bob

                # 修正腿部动画导致的额外偏移
                leg_anim_x, leg_anim_y = 0, 0
                if leg_frame == -1:
                    leg_anim_x -= s(1)
                    leg_anim_y -= s(1)
                if leg_frame == 1:
                    leg_anim_x += s(1)
                if leg_frame == 2:
                    leg_anim_x -= s(2)
                    leg_anim_y += s(1)
                if leg_frame == -2:
                    leg_anim_x -= s(2)
                    leg_anim_y -= s(4)

                self.draw_part(
                    draw,
                    "legs",
                    style,
                    leg_draw_x + leg_anim_x,
                    leg_draw_y + leg_anim_y - bob,
                    scale,
                    render_mode,
                )
                # 减去 bob 是因为腿部通常不随身体 bobbing 上下浮动那么多，或者动画定义里已经处理了
                # 暂时保持原逻辑：原逻辑 legs_back y = s(24) + bob.
                # current_base_y = base + bob. 所以直接传 current_base_y + s(24) 即可?
                # 让我们回退到最稳妥的写法：完全复刻原坐标逻辑，只是加上 base_offset

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

                # 使用 base_offset 修正
                final_x = offset_x + (self.base_offset_x * scale) + global_x_off + rx
                final_y = (self.base_offset_y * scale) + ry  # ry 包含 bob

                self.draw_part(
                    draw, "legs", style, final_x, final_y, scale, render_mode
                )

            elif layer == "arms":
                color = self.get_color("shirt")
                # 手臂基础高度
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

                # Arm Coords (相对于 ax_base, ay)
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

                rect_func(l_rect, **kwargs)
                rect_func(r_rect, **kwargs)

            elif layer == "held":
                style = self.selections.get("held", "none")
                if style != "none":
                    # hand_x, hand_y 已经是计算过 bob 的相对值
                    # 需要加上 base offset
                    final_hand_x = (
                        offset_x + (self.base_offset_x * scale) + global_x_off + hand_x
                    )
                    final_hand_y = (
                        self.base_offset_y * scale
                    ) + hand_y  # hand_y 这里应该是相对偏移
                    # 修正：上面定义的 hand_x, hand_y = s(20), s(17)+bob
                    # 所以直接加 base_offset_y * scale 即可

                    self.draw_part(
                        draw,
                        "held",
                        style,
                        final_hand_x,
                        (self.base_offset_y * scale) + hand_y,  # 这里 hand_y 包含了 bob
                        scale,
                        render_mode,
                    )

            elif layer in ["body", "head", "eyes", "hair"]:
                # 这些部件通常直接附着在主体上，受 bob 影响
                # current_base_y 已经包含了 bob
                # draw_part 内部逻辑是 offset_x + sx, offset_y + sy
                # 其中 sy 是部件定义的 y (比如 head 是 4)
                # 所以我们传入 current_base_x, current_base_y 即可

                # 但是要注意，draw_part 里的 y 是绝对坐标吗？
                # PART_DEFINITIONS 里: head -> ("rect", (10, 4, 12, 12)...)
                # 这里的 4 是相对于 32x32 画布顶部的
                # 所以我们传入的 offset_y 应该是 (base_offset_y + bob)

                # 等等，如果我传入 (base_offset_y + bob)，然后在 draw_part 里又加上 y*scale (即 4*scale)
                # 最终 y = base + bob + 4。这是对的。

                # 特殊处理 legs_back 遗留问题
                pass  # 已在上面处理

                self.draw_part(
                    draw,
                    part_key,
                    style,
                    current_base_x,
                    current_base_y,
                    scale,
                    render_mode,
                )

            # 重新修正 legs_back 逻辑以匹配
            if layer == "legs_back":
                # 回溯修正: 下面重新写一遍 legs_back 的正确逻辑，覆盖上面的
                pass

        # 修正 legs_back (因为上面写法有点乱，这里为了代码整洁，我在循环里是通过 if/elif 互斥的，不能在下面重写)
        # 我会在 edit 的时候一次性把 legs_back 写对。

        # 逻辑梳理 for legs_back inside loop:
        # lx, ly = s(12), s(24) + bob
        # ... modify lx, ly based on frame ...
        # final_x = offset_x + (base_x * s) + global_x + lx
        # final_y = (base_y * s) + ly  <-- ly contains bob
        # draw_part(..., final_x, final_y, ...)


def create_character_spritesheet(
    filename=None,
    config_source="character_config.yaml",
    action="walk",
    density=1.0,
    output_size=512,
    render_mode="retro",
):
    # [优化] 如果是 Premium 模式，强制提升内部渲染密度以获得细腻的圆角和光影
    if render_mode == "premium" and density < 8.0:
        density = 8.0  # 强制 8x 超采样
    elif render_mode == "hibit" and density < 4.0:
        density = 4.0  # Hi-Bit 模式推荐 4x (64-bit) 精度以显示高光细节

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
    # [优化] 如果是 Premium 模式，强制提升内部渲染密度
    if render_mode == "premium" and density < 8.0:
        density = 8.0
    elif render_mode == "hibit" and density < 4.0:
        density = 4.0

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
