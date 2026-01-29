"""
模块名称: 应用入口 (Application Entry Point)
文件路径: app.py

文件作用:
    这是整个 Web 应用程序的入口文件，基于 Flask 框架构建。
    它负责处理所有的 HTTP 请求，路由分发，以及连接前端页面与后端生成逻辑。

主要功能:
    1. 启动 Flask 服务器。
    2. 提供 Web 页面路由 ("/")。
    3. 提供 API 接口：
        - /options: 获取所有可用的角色部件、样式、主题配置。
        - /config: 读取当前的配置文件。
        - /randomize: 提供智能随机化逻辑，根据主题生成角色配置。
        - /generate: 核心接口，接收配置参数，调用生成模块生成 GIF 和 Sprite Sheet。

依赖模块:
    - modules.character.generator: 核心角色生成逻辑。
    - modules.character.definitions: 角色定义数据。
"""

from flask import Flask, render_template, jsonify, request, send_file
from modules.character import generator as gen_character
from modules.character import definitions as defs
import time  # For performance stats
import yaml
import io
import base64
import random
import colorsys

app = Flask(__name__)

CONFIG_PATH = "config/character_config.yaml"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/options", methods=["GET"])
def get_options():
    options = {}
    for part, styles in defs.PART_DEFINITIONS.items():
        options[part] = list(styles.keys())
    options["animations"] = list(defs.ANIMATION_DEFINITIONS.keys())
    options["themes"] = defs.THEME_MAPPINGS
    return jsonify(options)


@app.route("/config", methods=["GET"])
def get_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
        for k, v in defs.DEFAULT_PALETTE.items():
            if k not in config.get("palette", {}):
                if "palette" not in config:
                    config["palette"] = {}
                config["palette"][k] = v
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/randomize", methods=["GET"])
def randomize():
    """Smart Randomizer Logic (Strong Theme Enforcement)"""
    theme = request.args.get("theme", "all")

    # 1. Determine Actual Theme (if 'all', pick one)
    available_themes = [
        "xianxia",
        "tech",
        "western",
        "cyberpunk",
        "steampunk",
        "horror",
    ]
    if theme == "all":
        selected_theme = random.choice(available_themes)
    else:
        selected_theme = theme

    # 2. Theme Tags Strategy
    # Primary tag is the theme itself. Secondary tags are compatible ones.
    target_tags = [selected_theme, "generic"]

    # Some themes share tags (e.g. Cyberpunk includes Tech)
    if selected_theme == "cyberpunk":
        target_tags.append("tech")
    if selected_theme == "steampunk":
        target_tags.append("western")

    # 3. Pick Parts
    new_parts = {}
    for part_key, styles in defs.PART_DEFINITIONS.items():
        # 如果该部件没有任何样式定义，跳过
        if not styles:
            continue

        part_tags_map = defs.PART_TAGS.get(part_key, {})
        all_styles = list(styles.keys())

        # Categorize
        exact_matches = []
        compatible_matches = []
        generic_matches = []

        for style_name in all_styles:
            style_tags = part_tags_map.get(style_name, [])
            if not style_tags:
                generic_matches.append(style_name)
                continue

            if selected_theme in style_tags:
                exact_matches.append(style_name)
            elif any(t in target_tags for t in style_tags):
                compatible_matches.append(style_name)
            elif "generic" in style_tags:
                generic_matches.append(style_name)

        # 构建随机池
        pool = []

        if theme == "all":
            # 混合模式：完全随机
            pool = all_styles
        else:
            # 主题模式：加权随机
            if exact_matches:
                pool.extend(exact_matches * 50)  # 极大增加匹配主题的概率
            if compatible_matches:
                pool.extend(compatible_matches * 10)
            if generic_matches:
                pool.extend(generic_matches * 2)

            # 保底：加入所有选项，防止死锁，但权重极低
            pool.extend(all_styles * 1)

        # 再次检查 pool 是否为空（理论上不应该，因为加了 all_styles）
        if not pool:
            pool = all_styles

        new_parts[part_key] = random.choice(pool)

    # 4. Completely Random Palette (Smart HSV)
    new_palette = {}

    def random_hsv_color(min_s=0.4, max_s=0.9, min_v=0.6, max_v=1.0):
        """生成好看的随机颜色"""
        h = random.random()
        s = random.uniform(min_s, max_s)
        v = random.uniform(min_v, max_v)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return [int(r * 255), int(g * 255), int(b * 255)]

    for key in defs.DEFAULT_PALETTE.keys():
        if key == "skin":
            # 肤色逻辑: 80% 自然色, 20% 奇幻色
            if random.random() < 0.8:
                # 自然肤色 (偏黄/红)
                h = random.uniform(0.05, 0.12)
                s = random.uniform(0.2, 0.5)
                v = random.uniform(0.8, 1.0)
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                new_palette[key] = [int(r * 255), int(g * 255), int(b * 255)]
            else:
                # 奇幻肤色 (任意色相)
                new_palette[key] = random_hsv_color(min_s=0.3, max_s=0.6)

        elif key == "metal":
            # 金属逻辑: 银/灰/金/铜
            roll = random.random()
            if roll < 0.5:  # 银灰
                val = random.randint(150, 220)
                new_palette[key] = [val, val, val]
            elif roll < 0.75:  # 金色
                new_palette[key] = [255, 215, 0]
            else:  # 铜/锈
                new_palette[key] = [184, 115, 51]

        elif key in ["highlight", "outline"]:
            if key == "outline":
                new_palette[key] = random_hsv_color(max_v=0.3)  # 深色
            else:
                new_palette[key] = random_hsv_color(min_v=0.9, min_s=0.0)  # 亮色

        else:
            # 头发、衣服、鞋子等 -> 完全随机鲜艳色
            new_palette[key] = random_hsv_color()

    # 5. Recommended Render Mode
    rec_render_mode = defs.THEME_RENDER_MODES.get(
        selected_theme, "hibit"
    )  # Default to hibit for better look

    return jsonify(
        {
            "parts": new_parts,
            "palette": new_palette,
            "render_mode": rec_render_mode,
            "theme": selected_theme,
        }
    )


@app.route("/generate", methods=["POST"])
def generate_image():
    start_time = time.time()
    try:
        config = request.json
        if not config:
            return jsonify({"error": "No config provided"}), 400

        # Support for batch generation
        # Check if 'actions' (list) is provided in config.
        # If so, generate for all. If not, check 'action' (single).
        actions = config.get("actions", [])
        if not actions:
            # Fallback to single action mode (backward compatibility)
            single_action = config.get("action", "walk")
            actions = [single_action]

        # Deduplicate but keep order
        actions = list(dict.fromkeys(actions))

        # Limit batch size to prevent server overload
        if len(actions) > 8:
            actions = actions[:8]

        density = float(config.get("density", 1.0))
        # Default to 16-bit (1.0) if not specified, though user requested 16-bit default in UI
        # The UI sends the value.

        # [优化] 支持自定义输出尺寸 (512, 1024, 2048)
        output_size = int(config.get("output_size", 512))
        if output_size > 2048:
            output_size = 2048  # Cap for safety

        render_mode = config.get("render_mode", "retro")

        if render_mode == "hollow_knight":
            return jsonify({"error": "Mode moved to experimental"}), 400

        results = {}
        total_size_kb = 0

        # Loop through actions
        for act in actions:
            # Generate GIF (Preview)
            buf_gif = gen_character.create_character_gif(
                config_source=config,
                action=act,
                density=density,
                output_size=output_size,
                render_mode=render_mode,
            )
            gif_base64 = base64.b64encode(buf_gif.getvalue()).decode("utf-8")

            # Generate PNG (Sprite Sheet) for Download
            img_sheet = gen_character.create_character_spritesheet(
                filename=None,
                config_source=config,
                action=act,
                density=density,
                output_size=output_size,
                render_mode=render_mode,
            )
            buf_png = io.BytesIO()
            img_sheet.save(buf_png, format="PNG")
            buf_png.seek(0)
            png_bytes = buf_png.getvalue()
            png_base64 = base64.b64encode(png_bytes).decode("utf-8")

            size_kb = len(png_bytes) / 1024
            total_size_kb += size_kb

            results[act] = {
                "image": f"data:image/gif;base64,{gif_base64}",
                "download_data": f"data:image/png;base64,{png_base64}",
                "filename": f"character_{act}_{render_mode}.png",
                "size_kb": round(size_kb, 1),
            }

        duration = time.time() - start_time

        return jsonify(
            {
                "results": results,  # Map of action -> {image, download_data, ...}
                "stats": {
                    "duration": round(duration, 2),
                    "total_size_kb": round(total_size_kb, 1),
                    "width": output_size,
                    "height": output_size,
                    "count": len(actions),
                },
            }
        )

    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
