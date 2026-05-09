# Pixel Forge (水浒像素工坊)

A procedural pixel character generator with 64x64 HD resolution, supporting multiple themes, animations, and rendering styles.

## Features

- **64x64 HD Resolution**: Double precision pixel art
- **12 Animations**: idle, walk, run, attack (+ weapon-specific variants), jump, hurt, cheer, die
- **7 Render Modes**: retro, hd, sketch, neon, ink, hibit, premium
- **Weapon System**: Weapons rotate with attack animations, VFX effects
- **5 Themes**: fantasy, scifi, modern, cute, action
- **Batch Generation**: Generate up to 8 animations at once
- **Web Interface**: Real-time preview with customizable palette

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000
```

## API Reference

### GET /options
Returns all available part styles, animations, and themes.

### GET /config
Returns default character configuration.

### GET /randomize?theme=<theme>
Generates random character configuration.
- `theme`: fantasy | scifi | modern | cute | action | all (default)

### POST /generate
Generates character GIF and sprite sheet.

Request body:
```json
{
  "parts": {
    "head": "base",
    "hair": "short_hero",
    "eyes": "anime_large",
    "body": "adventurer_coat",
    "legs": "pants_boots",
    "held": "sword_iron",
    "back": "none",
    "expression": "neutral",
    "face_wear": "none"
  },
  "palette": {
    "skin": [255, 200, 150],
    "hair": [100, 50, 0]
  },
  "actions": ["idle", "walk"],
  "density": 1.0,
  "output_size": 512,
  "render_mode": "hibit"
}
```

Response:
```json
{
  "results": {
    "idle": {
      "image": "data:image/gif;base64,...",
      "download_data": "data:image/png;base64,...",
      "filename": "character_idle_hibit.png",
      "size_kb": 12.3
    }
  },
  "stats": {
    "duration": 1.23,
    "total_size_kb": 24.6,
    "width": 512,
    "height": 512,
    "count": 1
  }
}
```

## Architecture

- `modules/character/data/parts.py` - Part definitions and layer order
- `modules/character/data/animations.py` - Animation frames and weapon metadata
- `modules/character/data/palettes.py` - Color palettes and theme mappings
- `modules/character/generator.py` - Character composition engine
- `modules/character/renderer.py` - Rendering engine with material-aware shading
- `modules/rendering/post_effects.py` - Post-processing filters

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```