from flask import Flask, render_template, jsonify, request, send_file
import gen_character
import character_definitions as defs
import yaml
import io
import base64

app = Flask(__name__)

CONFIG_PATH = "character_config.yaml"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/options", methods=["GET"])
def get_options():
    """Returns the available parts and styles from definitions."""
    options = {}
    for part, styles in defs.PART_DEFINITIONS.items():
        options[part] = list(styles.keys())

    # Add animations to options
    options["animations"] = list(defs.ANIMATION_DEFINITIONS.keys())
    return jsonify(options)


@app.route("/config", methods=["GET"])
def get_config():
    """Returns the current configuration from file."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)

        # Ensure palette has defaults if missing
        for k, v in defs.DEFAULT_PALETTE.items():
            if k not in config.get("palette", {}):
                if "palette" not in config:
                    config["palette"] = {}
                config["palette"][k] = v

        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        config = request.json
        if not config:
            return jsonify({"error": "No config provided"}), 400

        action = config.get("action", "walk")

        # 1. Generate Spritesheet (PNG)
        img_sheet = gen_character.create_character_spritesheet(
            filename=None, config_source=config, action=action
        )
        buf_png = io.BytesIO()
        img_sheet.save(buf_png, format="PNG")
        buf_png.seek(0)
        png_base64 = base64.b64encode(buf_png.getvalue()).decode("utf-8")

        # 2. Generate Preview (GIF)
        buf_gif = gen_character.create_character_gif(
            config_source=config, action=action
        )
        gif_base64 = base64.b64encode(buf_gif.getvalue()).decode("utf-8")

        return jsonify(
            {
                "image": f"data:image/gif;base64,{gif_base64}",  # Preview uses GIF
                "download_data": f"data:image/png;base64,{png_base64}",  # Download uses PNG sheet
                "filename": f"character_{action}.png",
            }
        )

    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
