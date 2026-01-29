"""
模块名称: AI 提示词生成器 (AI Prompt Generator)
文件用途:
    负责将像素角色的部件配置 (Configuration) 翻译成自然语言提示词 (Prompt)。
    这些提示词用于输入给 Stable Diffusion 等 AI 模型，生成高质量的概念图或插画。

    包含:
    - PROMPT_MAPPINGS: 部件到英文描述的映射表。
    - build_prompt(): 核心函数，组装风格、部件和质量词。
"""

import random

# 将我们之前的部件 key 翻译成高质量的 AI 提示词 (Prompt)
PROMPT_MAPPINGS = {
    # Themes
    "themes": {
        "xianxia": "Chinese Xianxia fantasy style, ethereal, wuxia, flowy silk, ancient chinese aesthetics, cultivation world, intricate patterns",
        "tech": "Sci-fi style, high-tech, futuristic, clean surfaces, mechanical details, utopian",
        "cyberpunk": "Cyberpunk style, neon lights, dark gloomy background, chrome metal, high contrast, dystopia, Edgerunners style",
        "steampunk": "Steampunk style, brass and copper, gears and clockwork, victorian era clothing, steam smoke, industrial fantasy",
        "western": "Western fantasy style, D&D art style, medieval, rough textures, epic atmosphere",
        "horror": "Dark horror style, gloomy, bloodstained, eerie atmosphere, cinematic lighting, resident evil style",
    },
    # Parts (映射到英文描述)
    "head": {
        "robot": "mecha head, futuristic helmet, robotic face",
        "human": "handsome human face, detailed skin texture",
        "orc": "ferocious orc face, green skin, tusks",
        "skeleton": "terrifying skull face, undead",
        "sage_beard": "elderly face with long white beard, wise eyes",
        "cyborg_eye": "human face with glowing mechanical eye implant",
        "zombie": "rotten zombie face, pale skin, wounds",
        "oni": "japanese oni demon mask, red face, horns",
    },
    "hair": {
        "mohawk_neon": "glowing neon mohawk hair, punk style",
        "long_flowy": "long flowy black hair blowing in wind",
        "topknot": "traditional daoist topknot bun",
        "wizard_hat": "wearing a large pointed wizard hat",
        "helmet": "wearing a full-face tactical helmet",
        "hood": "wearing a mysterious hood casting shadows",
    },
    "body": {
        "mech_suit": "heavy mechanical power armor, exosuit",
        "hanfu_scholar": "elegant traditional chinese hanfu robe, silk fabric",
        "jacket_neon": "futuristic bomber jacket with glowing led strips",
        "coat_brass": "vintage leather trench coat with brass gears",
        "armor": "plate metal armor, knight gear",
        "ribs_gore": "exposed ribcage, gore, zombie body",
    },
    "held": {
        "laser_gun": "holding a high-tech laser rifle",
        "jian": "holding a mystical chinese jian sword, glowing rune blade",
        "katana_laser": "holding a glowing beam katana",
        "chainsaw": "holding a rusty bloody chainsaw",
        "fan": "holding a folding paper fan",
        "flying_swords": "surrounded by floating spiritual swords",
    },
}

QUALITY_TAGS = "masterpiece, best quality, 8k resolution, highly detailed, cinematic lighting, unreal engine 5 render, trending on artstation"
NEGATIVE_PROMPT = "low quality, bad anatomy, worst quality, lowres, blurry, pixelated, deformed, ugly, bad hands, extra limbs"


def build_prompt(config):
    """
    根据前端传来的 config (parts, theme) 生成 AI 提示词
    """
    theme = config.get("theme_key", "generic")  # 假设前端会传这个

    # 1. 基础风格
    prompt_parts = []
    base_style = PROMPT_MAPPINGS["themes"].get(theme, "")
    if base_style:
        prompt_parts.append(base_style)

    # 2. 部件描述
    parts = config.get("parts", {})

    # 组合身体描述
    body_desc = []
    if "head" in parts:
        body_desc.append(PROMPT_MAPPINGS["head"].get(parts["head"], parts["head"]))
    if "hair" in parts:
        body_desc.append(PROMPT_MAPPINGS["hair"].get(parts["hair"], parts["hair"]))
    if "body" in parts:
        body_desc.append(PROMPT_MAPPINGS["body"].get(parts["body"], parts["body"]))
    if "held" in parts and parts["held"] != "none":
        body_desc.append(PROMPT_MAPPINGS["held"].get(parts["held"], parts["held"]))

    # 将身体描述加入 Prompt
    prompt_parts.append(f"Solo character, full body shot, {', '.join(body_desc)}")

    # 3. 质量词
    prompt_parts.append(QUALITY_TAGS)

    return ", ".join(prompt_parts)


if __name__ == "__main__":
    # Test
    test_config = {
        "theme_key": "cyberpunk",
        "parts": {
            "head": "cyborg_eye",
            "body": "jacket_neon",
            "held": "katana_laser",
            "hair": "mohawk_neon",
        },
    }
    print(build_prompt(test_config))
