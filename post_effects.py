"""
艺术滤镜后处理系统
为像素角色添加各种艺术效果（发光、水墨、手绘、复古等）
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import texture_generator as tex
import random


def apply_ink_effect(image):
    """
    水墨效果：墨迹扩散 + 对比度增强 (去除噪点)
    适用于仙侠风格
    """
    # 确保是 RGB 模式
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # 1. 轻微模糊模拟墨迹晕染
    blurred = image.filter(ImageFilter.GaussianBlur(radius=0.8))

    # 2. 混合原图和模糊图 (代替复杂的纸张纹理)
    result = Image.blend(image, blurred, alpha=0.4)

    # 3. 轻微降低饱和度，增加水墨感
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(0.7)

    # 4. 增强对比度
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.2)

    return result


def apply_neon_glow(image):
    """
    霓虹发光：外发光 (去除扫描线)
    适用于赛博朋克风格
    """
    # 确保是 RGB 模式
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 1. 找到明亮区域，制造发光效果
    # 先增强对比度，让亮部更亮
    contrast = ImageEnhance.Contrast(image)
    enhanced = contrast.enhance(1.4)

    # 2. 应用高斯模糊制造发光
    glow = enhanced.filter(ImageFilter.GaussianBlur(radius=4))

    # 3. 叠加原图 + 发光层
    result = Image.blend(image, glow, alpha=0.5)

    # 4. 增强饱和度（赛博朋克色彩更鲜艳）
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.4)

    return result


def apply_sketch_texture(image):
    """
    手绘质感：边缘强化 (去除噪点纹理)
    适用于素描、手绘风格
    """
    # 确保是 RGB 模式
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 1. 强化边缘 (更强烈的线条感)
    edges = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # 再次强化以模拟铅笔硬朗感
    edges = edges.filter(ImageFilter.SHARPEN)

    # 2. 降低饱和度
    enhancer = ImageEnhance.Color(edges)
    result = enhancer.enhance(0.5)

    # 3. 增强亮度 (模拟白纸背景，但不加纹理)
    brightness = ImageEnhance.Brightness(result)
    result = brightness.enhance(1.1)

    return result


def apply_retro_crt(image):
    """
    复古 CRT：色差 + 模糊 (去除噪点和扫描线)
    适用于 80 年代像素风
    """
    # 确保是 RGB 模式
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 1. RGB 色差效果（模拟 CRT 屏幕）
    result = apply_chromatic_aberration(image, offset=2)

    # 2. 轻微降低锐度（模拟 CRT 荧光粉扩散）
    result = result.filter(ImageFilter.GaussianBlur(radius=0.4))

    # 3. 增强对比度
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.1)

    return result


def apply_vector_polish(image):
    """
    矢量抛光：光滑渐变 + 光泽效果
    适用于现代矢量风格
    """
    # 确保是 RGB 模式
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 1. 轻微模糊制造光滑感
    smoothed = image.filter(ImageFilter.GaussianBlur(radius=0.3))

    # 2. 增强对比度
    contrast = ImageEnhance.Contrast(smoothed)
    result = contrast.enhance(1.15)

    # 3. 增强饱和度
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.1)

    # 4. 锐化边缘
    result = result.filter(ImageFilter.SHARPEN)

    # 5. 增加亮度（矢量风格更明亮）
    brightness = ImageEnhance.Brightness(result)
    result = brightness.enhance(1.05)

    return result


def apply_chromatic_aberration(image, offset=2):
    """
    色差效果（RGB 通道偏移）
    用于复古、故障艺术风格
    """
    # 分离 RGB 通道
    r, g, b = image.split()

    # 创建新的通道位置
    r_shifted = Image.new("L", image.size)
    g_shifted = Image.new("L", image.size)
    b_shifted = Image.new("L", image.size)

    # 红色通道向右偏移
    r_shifted.paste(r, (offset, 0))
    # 绿色通道不变
    g_shifted.paste(g, (0, 0))
    # 蓝色通道向左偏移
    b_shifted.paste(b, (-offset, 0))

    # 合并通道
    result = Image.merge("RGB", (r_shifted, g_shifted, b_shifted))
    return result


def apply_watercolor_effect(image):
    """
    水彩效果：色彩晕染 + 纸质纹理
    适用于艺术插画风格
    """
    # 1. 强烈模糊模拟颜料扩散
    blurred = image.filter(ImageFilter.GaussianBlur(radius=1.5))

    # 2. 边缘检测
    edges = image.filter(ImageFilter.FIND_EDGES)

    # 3. 混合模糊图和边缘
    result = Image.blend(blurred, edges, alpha=0.1)

    # 4. 添加纸质纹理
    paper = tex.generate_paper_texture(image.size, grain_intensity=0.6)
    result = Image.blend(result, paper, alpha=0.25)

    # 5. 增强饱和度（水彩色彩鲜艳）
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.2)

    return result


def apply_steampunk_metal(image):
    """
    蒸汽朋克金属质感
    适用于蒸汽朋克风格
    """
    # 1. 降低饱和度（金属感偏冷色调）
    enhancer = ImageEnhance.Color(image)
    desaturated = enhancer.enhance(0.7)

    # 2. 叠加金属纹理
    metal = tex.generate_metal_texture(image.size)
    result = Image.blend(desaturated, metal, alpha=0.15)

    # 3. 增强对比度（金属高光）
    contrast = ImageEnhance.Contrast(result)
    result = contrast.enhance(1.25)

    # 4. 锐化边缘
    result = result.filter(ImageFilter.SHARPEN)

    # 5. 轻微暗角（工业感）
    result = tex.apply_vignette(result, intensity=0.3)

    return result


def get_post_effect_for_mode(render_mode):
    """
    根据渲染模式返回对应的后处理函数
    """
    effects = {
        "ink": apply_ink_effect,
        "neon": apply_neon_glow,
        "sketch": apply_sketch_texture,
        "retro": apply_retro_crt,
        "hd": apply_vector_polish,
    }
    return effects.get(render_mode, lambda x: x)  # 默认不处理
