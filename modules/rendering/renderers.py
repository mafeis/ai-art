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


import colorsys


class HiBitRenderer(Renderer):
    """
    高位像素渲染器 (Hi-Bit Pixel Art Style)
    目标：达到类似《星露谷物语》或《蔚蓝》的精致像素质感。
    核心技术：
    1. 色彩偏移 (Hue Shifting): 亮部偏暖，暗部偏冷。
    2. 材质感知 (Material Aware): 金属、皮肤、布料使用不同的着色逻辑。
    3. 像素级描边 (Pixel-perfect Outline): 保持硬边缘，但增加内部细节。
    """

    def hue_shift(self, rgb, amount, shift_warm=True):
        """
        高级调色：改变亮度的同时改变色相
        """
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        # 亮度调整
        if shift_warm:
            l = min(1.0, l * (1.0 + amount))
            # 亮部向黄色/暖色偏移 (Hue 0.1-0.15 is yellow/orange)
            # 这里简单处理：稍微减少 Hue 如果是红色/紫色，稍微增加如果是绿色
            # 简化策略：亮部增加饱和度，暗部降低饱和度
            s = min(1.0, s * 1.1)
        else:
            l = max(0.0, l * (1.0 - amount))
            # 暗部向蓝色/紫色偏移
            # s = max(0.0, s * 0.9)
            # 增加一点冷色调通常意味着推向蓝色 (Hue 0.66)
            # 这里为了通用性，只降低亮度和微调饱和度

        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (int(r * 255), int(g * 255), int(b * 255))

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        base_color = self.get_color(color_key)

        # 强制取整，保证像素完美 (Pixel Perfect)
        sx = int(x * scale)
        sy = int(y * scale)
        sw = int(max(1, w * scale))
        sh = int(max(1, h * scale))
        x1 = int(offset_x + sx)
        y1 = int(offset_y + sy)

        # 1. 材质判断
        is_metal = color_key in ["metal", "gold", "brass", "sword", "shield"]
        is_skin = color_key in ["skin", "elf", "highlight"]  # highlight通常是皮肤高光
        is_hair = color_key in ["hair"]

        # === 高级密度细节处理 (Sub-pixel Detailing) ===
        # 只有在高清/超清模式 (scale >= 3) 下才启用，让"大颗粒"变成"细腻材质"
        if scale >= 3.0:
            # A. 材质纹理 (Texture)
            if is_metal:
                # 金属拉丝：绘制细微的斜线
                for i in range(0, sw + sh, 2):  # 间隔2物理像素
                    # 在矩形范围内绘制斜线 (简单点缀)
                    if i % 3 == 0:
                        px = x1 + (i % sw)
                        py = y1 + (i % sh)
                        draw.rectangle(
                            [px, py, px + 1, py + 1], fill=(255, 255, 255, 60)
                        )

            elif is_cloth:
                # 布料纹理：十字格或杂色
                noise_color = self.adjust_color(base_color, 0.9)  # 稍暗
                # 棋盘格纹理
                for py in range(0, sh, 2):
                    for px in range(0, sw, 2):
                        if (px + py) % 4 == 0:
                            draw.point((x1 + px, y1 + py), fill=noise_color)

            elif not is_skin:
                # 通用杂色 (Noise)
                for _ in range(int(sw * sh * 0.1)):  # 10% 密度
                    nx = x1 + int(random.random() * sw)
                    ny = y1 + int(random.random() * sh)
                    draw.point((nx, ny), fill=self.adjust_color(base_color, 0.95))

        # 2. 宏观光影 (Macro Shading) - 保持原来的立体感逻辑
        shadow_color = self.hue_shift(base_color, 0.3, shift_warm=False)
        shadow_width = max(1, int(scale * 0.15))

        # 右侧阴影
        draw.rectangle(
            [x1 + sw - shadow_width, y1, x1 + sw, y1 + sh], fill=shadow_color
        )
        # 底部阴影
        draw.rectangle(
            [x1, y1 + sh - shadow_width, x1 + sw, y1 + sh], fill=shadow_color
        )

        # [通用] 顶部和左侧高光 (Highlight) - 仅 1px 宽，保持精致
        highlight_color = self.hue_shift(base_color, 0.2, shift_warm=True)
        highlight_width = max(1, int(scale * 0.1))

        # 顶部高光
        draw.rectangle(
            [x1, y1, x1 + sw - shadow_width, y1 + highlight_width], fill=highlight_color
        )
        # 左侧高光
        draw.rectangle(
            [x1, y1, x1 + highlight_width, y1 + sh - shadow_width], fill=highlight_color
        )

        # 4. 材质特效 (Texture Effects)

        if is_metal:
            # 金属光泽：绘制一条 45 度的强高光带
            shine_color = (255, 255, 255, 180)
            # 简单的斜线模拟
            mid_x = x1 + sw // 2
            mid_y = y1 + sh // 2
            shine_w = max(1, int(scale * 0.2))
            # 绘制斜向矩形比较麻烦，用阶梯状像素模拟
            for i in range(min(sw, sh)):
                # 限制范围
                px = x1 + i
                py = y1 + sh - i - 1
                if 0 <= i < sw and 0 <= sh - i - 1 < sh:
                    draw.rectangle(
                        [px, py, px + shine_w, py + shine_w], fill=shine_color
                    )

        elif is_skin:
            # 皮肤：增加红润感 (Subsurface Scattering 模拟)
            # 在阴影和基色交界处加一点点饱和度高的红色
            warm_shadow = self.hue_shift(base_color, 0.1, shift_warm=False)
            # 这里简单地在脸颊位置画
            if w > 4 and h > 4:  # 只在大块皮肤上画
                # 腮红/红润
                blush_color = (255, 150, 150, 50)
                draw.rectangle(
                    [x1 + sw * 0.2, y1 + sh * 0.5, x1 + sw * 0.4, y1 + sh * 0.7],
                    fill=blush_color,
                )
                draw.rectangle(
                    [x1 + sw * 0.6, y1 + sh * 0.5, x1 + sw * 0.8, y1 + sh * 0.7],
                    fill=blush_color,
                )

        elif not is_hair:
            # 普通布料/物体：增加一点噪点纹理 (Noise)
            if scale >= 2.0:  # 只有像素足够大时才画纹理
                noise_color = (0, 0, 0, 20)
                if random.random() > 0.5:
                    nx = x1 + int(sw * 0.3)
                    ny = y1 + int(sh * 0.3)
                    draw.rectangle(
                        [nx, ny, nx + max(1, scale * 0.1), ny + max(1, scale * 0.1)],
                        fill=noise_color,
                    )

        # 5. 外部轮廓 (Pixel Outline) - 这里的轮廓要在物体内部画，还是外部？
        # 既然是 draw_rect，通常是在内部画。
        # 为了让物体之间有区分，我们加深最外圈的 1px
        border_color = self.hue_shift(base_color, 0.5, shift_warm=False)
        # 用 stroke 模拟
        # Pillow 的 rectangle outline 是向内还是向外？通常是居中或向内。
        # 手动画一个 1px 的框
        draw.rectangle([x1, y1, x1 + sw, y1 + sh], outline=border_color, width=1)


class PremiumRenderer(Renderer):
    """
    高端 2.5D 渲染器 (Premium 2.5D Style)
    特点：
    1. 伪 3D 光照 (Top-Left Highlight, Bottom-Right Shadow)
    2. 动态深色描边
    3. 内部高分辨率绘制，减少锯齿
    """

    def draw_rect(self, draw, x, y, w, h, color_key, offset_x, offset_y, scale):
        base_color = self.get_color(color_key)
        # 计算绘制坐标 (Internal High-Res Coords)
        sx, sy = x * scale, y * scale
        sw, sh = w * scale, h * scale
        x1, y1 = offset_x + sx, offset_y + sy

        # 1. 描边 (Outline) - 在底层绘制一个稍大的深色矩形
        outline_color = self.adjust_color(base_color, 0.4)  # 深色描边
        outline_width = max(1, scale * 0.1)
        draw.rounded_rectangle(
            [
                x1 - outline_width,
                y1 - outline_width,
                x1 + sw + outline_width,
                y1 + sh + outline_width,
            ],
            radius=scale * 0.2,
            fill=outline_color,
        )

        # 2. 主体填充 (Main Body)
        # 使用稍微深一点的基色作为阴影底
        shadow_color = self.adjust_color(base_color, 0.8)
        draw.rounded_rectangle(
            [x1, y1, x1 + sw, y1 + sh], radius=scale * 0.15, fill=shadow_color
        )

        # 3. 顶部高光面 (Top/Left Face - Highlight)
        # 模拟光源来自左上方，照亮物体的顶部和左侧
        highlight_color = self.adjust_color(base_color, 1.1)
        # 绘制一个稍微缩小并向左上偏移的矩形
        bevel_size = max(1, scale * 0.15)
        draw.rounded_rectangle(
            [x1, y1, x1 + sw - bevel_size, y1 + sh - bevel_size],
            radius=scale * 0.1,
            fill=highlight_color,
        )

        # 4. 镜面反光 (Specular Highlight) - 增加材质感
        # 在左上角加一个小点或线条
        specular_color = (255, 255, 255, 100)  # 半透明白
        draw.ellipse(
            [x1 + scale * 0.1, y1 + scale * 0.1, x1 + scale * 0.3, y1 + scale * 0.3],
            fill=specular_color,
        )


def get_renderer(mode, palette):
    if mode == "hibit":  # [New]
        return HiBitRenderer(palette)
    if mode == "premium":
        return PremiumRenderer(palette)
    if mode == "hd":
        return VectorRenderer(palette)
    if mode == "sketch":
        return SketchRenderer(palette)
    if mode == "neon":
        return NeonRenderer(palette)
    if mode == "ink":
        return InkRenderer(palette)
    return RetroRenderer(palette)
