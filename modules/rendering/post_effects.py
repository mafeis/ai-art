"""
艺术滤镜后处理系统
为像素角色添加各种艺术效果（发光、水墨、手绘、复古等）
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from modules.rendering import texture_generator as tex
import random


def _ensure_rgba(image):
    if image.mode != "RGBA":
        return image.convert("RGBA")
    return image


def _apply_effect_with_alpha_mask(original, processed):
    """
    Apply the processed RGB effect back to the original Alpha channel.
    This preserves transparency.
    """
    if original.mode != "RGBA":
        return processed

    r, g, b, a = original.split()

    if processed.mode != "RGB":
        processed = processed.convert("RGB")

    if processed.size != original.size:
        processed = processed.resize(original.size)

    r_p, g_p, b_p = processed.split()
    return Image.merge("RGBA", (r_p, g_p, b_p, a))


def apply_ink_effect(image):
    """
    水墨效果：墨迹扩散 + 对比度增强
    """
    image = _ensure_rgba(image)
    rgb_img = image.convert("RGB")

    # 1. 轻微模糊模拟墨迹晕染
    blurred = rgb_img.filter(ImageFilter.GaussianBlur(radius=0.8))

    # 2. 混合原图和模糊图
    result = Image.blend(rgb_img, blurred, alpha=0.4)

    # 3. 轻微降低饱和度
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(0.7)

    # 4. 增强对比度
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.2)

    return _apply_effect_with_alpha_mask(image, result)


def apply_neon_glow(image):
    """
    霓虹发光：外发光
    """
    image = _ensure_rgba(image)

    # Extract alpha to create a glow mask?
    # For now, simple glow within bounds, but we want glow to extend?
    # Since we can't easily expand the canvas here without breaking spritesheets,
    # we will apply internal glow/bloom to the RGB channels and keep alpha.

    rgb_img = image.convert("RGB")

    # 1. 增强对比度
    contrast = ImageEnhance.Contrast(rgb_img)
    enhanced = contrast.enhance(1.4)

    # 2. 应用高斯模糊制造发光
    glow = enhanced.filter(ImageFilter.GaussianBlur(radius=4))

    # 3. 叠加
    result = Image.blend(rgb_img, glow, alpha=0.5)

    # 4. 增强饱和度
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.4)

    return _apply_effect_with_alpha_mask(image, result)


def apply_sketch_texture(image):
    """
    手绘质感：边缘强化
    """
    image = _ensure_rgba(image)
    rgb_img = image.convert("RGB")

    # 1. 强化边缘
    edges = rgb_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    edges = edges.filter(ImageFilter.SHARPEN)

    # 2. 降低饱和度
    enhancer = ImageEnhance.Color(edges)
    result = enhancer.enhance(0.5)

    # 3. 增强亮度
    brightness = ImageEnhance.Brightness(result)
    result = brightness.enhance(1.1)

    return _apply_effect_with_alpha_mask(image, result)


def apply_retro_crt(image):
    """
    复古 CRT：色差 + 模糊
    """
    image = _ensure_rgba(image)
    rgb_img = image.convert("RGB")

    # 1. RGB 色差
    result = apply_chromatic_aberration(rgb_img, offset=2)

    # 2. 轻微模糊
    result = result.filter(ImageFilter.GaussianBlur(radius=0.4))

    # 3. 增强对比度
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.1)

    return _apply_effect_with_alpha_mask(image, result)


def apply_vector_polish(image):
    """
    矢量抛光
    """
    image = _ensure_rgba(image)
    rgb_img = image.convert("RGB")

    # 1. 轻微模糊
    smoothed = rgb_img.filter(ImageFilter.GaussianBlur(radius=0.3))

    # 2. 增强对比度
    contrast = ImageEnhance.Contrast(smoothed)
    result = contrast.enhance(1.15)

    # 3. 增强饱和度
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.1)

    # 4. 锐化
    result = result.filter(ImageFilter.SHARPEN)

    # 5. 亮度
    brightness = ImageEnhance.Brightness(result)
    result = brightness.enhance(1.05)

    return _apply_effect_with_alpha_mask(image, result)


def apply_chromatic_aberration(image, offset=2):
    r, g, b = image.split()

    r_shifted = Image.new("L", image.size)
    g_shifted = Image.new("L", image.size)
    b_shifted = Image.new("L", image.size)

    r_shifted.paste(r, (offset, 0))
    g_shifted.paste(g, (0, 0))
    b_shifted.paste(b, (-offset, 0))

    return Image.merge("RGB", (r_shifted, g_shifted, b_shifted))


def apply_premium_polish(image):
    """
    高端模式抛光：锐化 + 微调对比度
    """
    image = _ensure_rgba(image)
    rgb_img = image.convert("RGB")

    # 1. 轻微锐化，突出描边细节
    sharpener = ImageEnhance.Sharpness(rgb_img)
    result = sharpener.enhance(1.2)

    # 2. 增强色彩饱和度，使其看起来更鲜艳
    color_enhancer = ImageEnhance.Color(result)
    result = color_enhancer.enhance(1.1)

    return _apply_effect_with_alpha_mask(image, result)


def get_post_effect_for_mode(render_mode):
    effects = {
        "ink": apply_ink_effect,
        "neon": apply_neon_glow,
        "sketch": apply_sketch_texture,
        "retro": apply_retro_crt,
        "hd": apply_vector_polish,
        "premium": apply_premium_polish,
        "hibit": lambda x: x,  # Hi-Bit 保持像素纯净，不加滤镜
    }
    return effects.get(render_mode, lambda x: x)
