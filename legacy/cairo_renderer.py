"""
模块名称: Cairo 矢量渲染器基类 (Cairo Renderer Base)
文件用途:
    提供基于 PyCairo 的 2D 矢量绘图基础类和特定风格实现。

    包含以下类:
    1. CairoCharacterRenderer: 基础渲染器，封装了常用的矢量绘图操作（画圆、圆角矩形、胶囊体、渐变等）。
    2. DeadCellsRenderer: 《死亡细胞》风格渲染器，使用平滑渐变和动态身体曲线。
    3. HollowKnightRenderer: 《空洞骑士》风格渲染器，特点是粗黑描边和手绘感。
    4. MonumentValleyRenderer: 《纪念碑谷》风格渲染器，特点是极简几何和扁平配色。

    此模块属于实验性质，旨在探索非像素风格的程序化生成。
"""

import cairo
from PIL import Image
import io
import math


class CairoCharacterRenderer:
    """Cairo 艺术渲染器基类"""

    def __init__(self, width=256, height=256, style="dead_cells"):
        self.width = width
        self.height = height
        self.style = style
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context(self.surface)

        # 设置最高质量抗锯齿
        self.ctx.set_antialias(cairo.ANTIALIAS_BEST)

        # 设置默认线条样式
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    def clear(self, r=0, g=0, b=0, a=0):
        """清空画布"""
        self.ctx.set_source_rgba(r, g, b, a)
        self.ctx.paint()

    def rgb_to_cairo(self, color):
        """转换 RGB (0-255) 到 Cairo (0.0-1.0)"""
        if isinstance(color, tuple) and len(color) >= 3:
            return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
        return (1.0, 0.0, 1.0)  # 默认洋红色

    def draw_ellipse(self, x, y, width, height, color, fill=True, stroke_width=0):
        """绘制椭圆"""
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(width / 2.0, height / 2.0)
        self.ctx.arc(0, 0, 1, 0, 2 * math.pi)
        self.ctx.restore()

        r, g, b = self.rgb_to_cairo(color)

        if fill:
            self.ctx.set_source_rgb(r, g, b)
            self.ctx.fill_preserve()

        if stroke_width > 0:
            self.ctx.set_line_width(stroke_width)
            self.ctx.set_source_rgb(r * 0.7, g * 0.7, b * 0.7)
            self.ctx.stroke()
        else:
            self.ctx.new_path()

    def draw_rounded_rect(
        self, x, y, width, height, radius, color, fill=True, stroke_width=0
    ):
        """绘制圆角矩形"""
        self.ctx.new_path()
        self.ctx.arc(x + radius, y + radius, radius, math.pi, 3 * math.pi / 2)
        self.ctx.arc(x + width - radius, y + radius, radius, 3 * math.pi / 2, 0)
        self.ctx.arc(x + width - radius, y + height - radius, radius, 0, math.pi / 2)
        self.ctx.arc(x + radius, y + height - radius, radius, math.pi / 2, math.pi)
        self.ctx.close_path()

        r, g, b = self.rgb_to_cairo(color)

        if fill:
            self.ctx.set_source_rgb(r, g, b)
            self.ctx.fill_preserve()

        if stroke_width > 0:
            self.ctx.set_line_width(stroke_width)
            self.ctx.set_source_rgb(r * 0.6, g * 0.6, b * 0.6)
            self.ctx.stroke()
        else:
            self.ctx.new_path()

    def draw_gradient_ellipse(self, x, y, width, height, color):
        """绘制带渐变的椭圆（用于Dead Cells风格）"""
        cx, cy = x, y

        # 径向渐变（中心亮，边缘暗）
        gradient = cairo.RadialGradient(
            cx, cy - height * 0.2, 0, cx, cy, max(width, height) / 2
        )
        r, g, b = self.rgb_to_cairo(color)

        gradient.add_color_stop_rgb(
            0, min(1.0, r * 1.3), min(1.0, g * 1.3), min(1.0, b * 1.3)
        )
        gradient.add_color_stop_rgb(1, r * 0.7, g * 0.7, b * 0.7)

        self.ctx.save()
        self.ctx.translate(cx, cy)
        self.ctx.scale(width / 2.0, height / 2.0)
        self.ctx.arc(0, 0, 1, 0, 2 * math.pi)
        self.ctx.restore()

        self.ctx.set_source(gradient)
        self.ctx.fill()

    def draw_capsule(self, x1, y1, x2, y2, thickness, color, use_gradient=False):
        """绘制胶囊形状（用于四肢）"""
        # 计算方向
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)

        if length < 0.1:
            return

        angle = math.atan2(dy, dx)

        self.ctx.save()
        self.ctx.translate(x1, y1)
        self.ctx.rotate(angle)

        # 绘制矩形主体
        r, g, b = self.rgb_to_cairo(color)

        if use_gradient:
            # 线性渐变（上亮下暗）
            gradient = cairo.LinearGradient(0, -thickness / 2, 0, thickness / 2)
            gradient.add_color_stop_rgb(
                0, min(1.0, r * 1.2), min(1.0, g * 1.2), min(1.0, b * 1.2)
            )
            gradient.add_color_stop_rgb(1, r * 0.8, g * 0.8, b * 0.8)
            self.ctx.set_source(gradient)
        else:
            self.ctx.set_source_rgb(r, g, b)

        self.ctx.rectangle(0, -thickness / 2, length, thickness)
        self.ctx.fill()

        # 两端的圆形
        self.ctx.arc(0, 0, thickness / 2, 0, 2 * math.pi)
        self.ctx.fill()
        self.ctx.arc(length, 0, thickness / 2, 0, 2 * math.pi)
        self.ctx.fill()

        self.ctx.restore()

    def to_pil_image(self):
        """转换为 PIL Image"""
        buf = io.BytesIO()
        self.surface.write_to_png(buf)
        buf.seek(0)
        return Image.open(buf).convert("RGBA")


class DeadCellsRenderer(CairoCharacterRenderer):
    """死亡细胞风格：流畅曲线 + 细腻渐变"""

    def __init__(self, width=256, height=256):
        super().__init__(width, height, style="dead_cells")

    def draw_character_head(self, x, y, size, skin_color):
        """绘制头部（椭圆+渐变）"""
        self.draw_gradient_ellipse(x, y, size, size * 1.2, skin_color)

        # 高光
        highlight_size = size * 0.3
        self.draw_ellipse(
            x - size * 0.2,
            y - size * 0.3,
            highlight_size,
            highlight_size,
            (255, 255, 255),
            fill=True,
        )

        # 眼睛（简单黑点）
        eye_size = size * 0.15
        self.draw_ellipse(x - size * 0.25, y, eye_size, eye_size, (40, 40, 40))
        self.draw_ellipse(x + size * 0.25, y, eye_size, eye_size, (40, 40, 40))

    def draw_character_body(self, x, y, width, height, body_color):
        """绘制身体（梯形+渐变）"""
        # 用贝塞尔曲线绘制平滑的身体轮廓
        self.ctx.new_path()

        # 肩部宽，腰部窄
        shoulder_w = width
        waist_w = width * 0.7

        # 顶部（肩膀）
        self.ctx.move_to(x - shoulder_w / 2, y)
        self.ctx.curve_to(
            x - shoulder_w / 2,
            y + height * 0.3,
            x - waist_w / 2,
            y + height * 0.7,
            x - waist_w / 2,
            y + height,
        )

        # 底部
        self.ctx.line_to(x + waist_w / 2, y + height)

        # 右侧
        self.ctx.curve_to(
            x + waist_w / 2,
            y + height * 0.7,
            x + shoulder_w / 2,
            y + height * 0.3,
            x + shoulder_w / 2,
            y,
        )

        self.ctx.close_path()

        # 线性渐变（上亮下暗）
        r, g, b = self.rgb_to_cairo(body_color)
        gradient = cairo.LinearGradient(x, y, x, y + height)
        gradient.add_color_stop_rgb(
            0, min(1.0, r * 1.2), min(1.0, g * 1.2), min(1.0, b * 1.2)
        )
        gradient.add_color_stop_rgb(0.5, r, g, b)
        gradient.add_color_stop_rgb(1, r * 0.7, g * 0.7, b * 0.7)

        self.ctx.set_source(gradient)
        self.ctx.fill()


class HollowKnightRenderer(CairoCharacterRenderer):
    """空洞骑士风格：手绘感 + 粗黑描边"""

    def __init__(self, width=256, height=256):
        super().__init__(width, height, style="hollow_knight")

    def draw_character_head(self, x, y, size, base_color):
        """绘制头部（白色+粗黑边）"""
        # 主体（白色或浅色）
        self.draw_ellipse(x, y, size, size * 1.1, (240, 240, 240), fill=True)

        # 粗黑描边
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(size / 2.0, size * 1.1 / 2.0)
        self.ctx.arc(0, 0, 1, 0, 2 * math.pi)
        self.ctx.restore()

        self.ctx.set_line_width(4)
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.stroke()

        # 黑色眼睛（空洞骑士标志性大黑眼）
        eye_w, eye_h = size * 0.35, size * 0.45
        self.draw_ellipse(x - size * 0.2, y + size * 0.1, eye_w, eye_h, (30, 30, 30))
        self.draw_ellipse(x + size * 0.2, y + size * 0.1, eye_w, eye_h, (30, 30, 30))

        # 眼睛高光
        highlight_size = eye_w * 0.3
        self.draw_ellipse(
            x - size * 0.2 - eye_w * 0.15,
            y + size * 0.05,
            highlight_size,
            highlight_size,
            (200, 200, 255),
        )
        self.draw_ellipse(
            x + size * 0.2 - eye_w * 0.15,
            y + size * 0.05,
            highlight_size,
            highlight_size,
            (200, 200, 255),
        )

    def draw_character_body(self, x, y, width, height, body_color):
        """绘制身体（简洁+粗描边）"""
        # 圆角矩形身体
        radius = width * 0.2
        self.draw_rounded_rect(
            x - width / 2, y, width, height, radius, (230, 230, 230), fill=True
        )

        # 粗黑描边
        self.ctx.new_path()
        self.ctx.arc(
            x - width / 2 + radius, y + radius, radius, math.pi, 3 * math.pi / 2
        )
        self.ctx.arc(x + width / 2 - radius, y + radius, radius, 3 * math.pi / 2, 0)
        self.ctx.arc(
            x + width / 2 - radius, y + height - radius, radius, 0, math.pi / 2
        )
        self.ctx.arc(
            x - width / 2 + radius, y + height - radius, radius, math.pi / 2, math.pi
        )
        self.ctx.close_path()

        self.ctx.set_line_width(4)
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.stroke()

        # 斗篷阴影（半透明黑色）
        shadow_gradient = cairo.LinearGradient(x, y + height * 0.3, x, y + height)
        shadow_gradient.add_color_stop_rgba(0, 0.2, 0.2, 0.3, 0)
        shadow_gradient.add_color_stop_rgba(1, 0.1, 0.1, 0.2, 0.4)

        self.ctx.rectangle(
            x - width / 2 + radius, y + height * 0.4, width - 2 * radius, height * 0.6
        )
        self.ctx.set_source(shadow_gradient)
        self.ctx.fill()


class MonumentValleyRenderer(CairoCharacterRenderer):
    """纪念碑谷风格：几何扁平 + 纯色"""

    def __init__(self, width=256, height=256):
        super().__init__(width, height, style="monument_valley")

    def draw_character_head(self, x, y, size, color):
        """绘制头部（简单圆形+极简）"""
        # 纯色圆形
        self.draw_ellipse(x, y, size, size, color, fill=True)

        # 细线描边（可选）
        self.ctx.save()
        self.ctx.translate(x, y)
        self.ctx.scale(size / 2.0, size / 2.0)
        self.ctx.arc(0, 0, 1, 0, 2 * math.pi)
        self.ctx.restore()

        r, g, b = self.rgb_to_cairo(color)
        self.ctx.set_line_width(1.5)
        self.ctx.set_source_rgb(r * 0.7, g * 0.7, b * 0.7)
        self.ctx.stroke()

        # 极简眼睛（两个小点）
        dot_size = size * 0.1
        self.draw_ellipse(x - size * 0.2, y, dot_size, dot_size, (50, 50, 50))
        self.draw_ellipse(x + size * 0.2, y, dot_size, dot_size, (50, 50, 50))

    def draw_character_body(self, x, y, width, height, color):
        """绘制身体（简单矩形）"""
        # 纯色矩形
        r, g, b = self.rgb_to_cairo(color)
        self.ctx.set_source_rgb(r, g, b)
        self.ctx.rectangle(x - width / 2, y, width, height)
        self.ctx.fill()

        # 细线描边
        self.ctx.rectangle(x - width / 2, y, width, height)
        self.ctx.set_line_width(1.5)
        self.ctx.set_source_rgb(r * 0.7, g * 0.7, b * 0.7)
        self.ctx.stroke()
