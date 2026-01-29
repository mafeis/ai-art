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

    # 3. Pick Parts (Priority: Exact Match > Compatible > Generic)
    new_parts = {}
    for part_key, styles in defs.PART_DEFINITIONS.items():
        part_tags_map = defs.PART_TAGS.get(part_key, {})

        # Categorize styles by match level
        exact_matches = []
        compatible_matches = []
        generic_matches = []

        for style_name in styles.keys():
            style_tags = part_tags_map.get(style_name, [])
            if not style_tags:  # Assume generic if no tags
                generic_matches.append(style_name)
                continue

            if selected_theme in style_tags:
                exact_matches.append(style_name)
            elif any(t in target_tags for t in style_tags):
                compatible_matches.append(style_name)
            elif "generic" in style_tags:
                generic_matches.append(style_name)

        # Selection Strategy: 70% Exact, 20% Compatible, 10% Generic (if available)
        pool = []
        if exact_matches:
            pool.extend(exact_matches * 10)  # Weighted heavily
        if compatible_matches:
            pool.extend(compatible_matches * 3)
        if generic_matches:
            pool.extend(generic_matches * 1)

        if not pool:
            # Fallback to anything
            pool = list(styles.keys())

        new_parts[part_key] = random.choice(pool)

    # 4. Enforce Theme Palette
    # If theme defines a palette, use it. Otherwise random.
    theme_palette_def = defs.THEME_PALETTES.get(selected_theme, {})
    new_palette = {}

    for key, default_val in defs.DEFAULT_PALETTE.items():
        if key in theme_palette_def:
            # Use fixed theme color WITH JITTER (+/- 30)
            # This ensures "Random Palette" still produces variations even in strict themes
            base_rgb = theme_palette_def[key]
            new_palette[key] = [
                max(0, min(255, c + random.randint(-30, 30))) for c in base_rgb
            ]
        else:
            # Randomize variations for non-critical colors?
            # Or stick to default? Let's add slight variation to default to keep it alive
            # But for theme consistency, fixed is better.
            new_palette[key] = default_val

    # 5. Recommended Render Mode
    rec_render_mode = defs.THEME_RENDER_MODES.get(selected_theme, "retro")

    return jsonify(
        {
            "parts": new_parts,
            "palette": new_palette,
            "render_mode": rec_render_mode,
            "theme": selected_theme,  # Return actual theme used (for UI update)
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

        output_size = 512
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
