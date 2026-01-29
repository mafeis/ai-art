# palettes.py
# 颜色定义

# Theme-specific Default Palettes (Overrides random generation)
THEME_PALETTES = {
    "xianxia": {
        "hair": (20, 20, 20),  # Ink Black
        "shirt": (230, 240, 255),  # White/Cyan Robe
        "pants": (50, 70, 90),  # Dark Blue
        "boots": (30, 30, 30),
        "skin": (255, 235, 220),  # Fair
        "eye_color": (0, 0, 0),
        "metal": (200, 200, 210),  # Silver
        "outline": (40, 50, 60),  # Ink Outline
    },
    "cyberpunk": {
        "hair": (255, 0, 128),  # Neon Pink
        "shirt": (20, 20, 25),  # Black Jacket
        "pants": (40, 40, 50),
        "boots": (0, 255, 255),  # Cyan Boots
        "skin": (220, 220, 255),  # Pale/Synth
        "eye_color": (0, 255, 0),  # Green LED
        "metal": (100, 100, 110),  # Chrome
        "neon_pink": (255, 0, 128),
        "neon_blue": (0, 255, 255),
        "outline": (0, 20, 40),
    },
    "horror": {
        "hair": (50, 50, 50),  # Grey/Dead
        "shirt": (80, 0, 0),  # Blood Red
        "pants": (30, 30, 30),
        "boots": (20, 10, 10),
        "skin": (150, 160, 140),  # Rotting Green/Grey
        "eye_color": (255, 0, 0),  # Red Eyes
        "blood": (180, 0, 0),
        "zombie_skin": (100, 120, 100),
        "outline": (20, 0, 0),
    },
    "steampunk": {
        "hair": (100, 60, 20),  # Brown
        "shirt": (200, 180, 150),  # Beige
        "pants": (80, 50, 30),  # Leather
        "boots": (60, 40, 20),
        "skin": (240, 200, 160),
        "brass": (200, 150, 50),
        "leather": (120, 70, 30),
        "metal": (160, 140, 100),  # Bronze-ish
        "outline": (60, 40, 20),
    },
    "tech": {
        "hair": (200, 200, 200),  # White/Grey
        "shirt": (220, 220, 230),  # Lab coat white
        "pants": (50, 50, 60),
        "boots": (200, 200, 200),
        "skin": (255, 220, 180),
        "eye_color": (0, 100, 255),
        "metal": (180, 190, 200),
        "outline": (50, 60, 70),
    },
    "western": {
        "hair": (180, 140, 50),  # Blonde
        "shirt": (150, 150, 160),  # Chainmail
        "pants": (80, 60, 40),
        "boots": (100, 60, 20),
        "skin": (255, 210, 170),
        "metal": (160, 170, 180),  # Steel
        "outline": (30, 30, 30),
    },
}

# Theme-specific Recommended Render Modes
THEME_RENDER_MODES = {
    "xianxia": "ink",
    "cyberpunk": "neon",
    "horror": "sketch",
    "steampunk": "retro",
    "tech": "hd",
    "western": "retro",
}

# Expanded Palette with theme colors
DEFAULT_PALETTE = {
    "skin": (255, 200, 150),
    "hair": (100, 50, 0),
    "shirt": (0, 100, 255),
    "pants": (50, 50, 50),
    "boots": (100, 50, 0),
    "outline": (20, 20, 20),
    "eye_color": (50, 50, 50),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "metal": (150, 150, 160),
    "highlight": (200, 200, 220),
    "tooth": (240, 240, 220),
    "wood": (100, 60, 20),
    # New Colors
    "neon_green": (0, 255, 100),
    "neon_pink": (255, 0, 100),
    "neon_blue": (0, 200, 255),
    "brass": (180, 140, 60),
    "leather": (120, 70, 30),
    "blood": (180, 20, 20),
    "zombie_skin": (100, 130, 100),
    "jade": (0, 160, 100),
    "gold": (255, 215, 0),
}

THEME_MAPPINGS = {
    "xianxia": [],
    "tech": [],
    "western": [],
    "cyberpunk": [],
    "steampunk": [],
    "horror": [],
}
