# palettes.py
# 颜色定义

# Theme-specific Default Palettes (Overrides random generation)
THEME_PALETTES = {
    "fantasy": {
        "hair": (80, 40, 20),  # Warm brown
        "shirt": (230, 240, 255),  # White/Cyan Robe
        "pants": (50, 70, 90),  # Dark Blue
        "boots": (80, 50, 20),
        "skin": (255, 235, 220),  # Fair
        "eye_color": (0, 100, 180),
        "metal": (200, 200, 210),  # Silver
        "outline": (40, 50, 60),  # Ink Outline
        "gold": (255, 215, 0),
        "leather": (120, 70, 30),
    },
    "scifi": {
        "hair": (200, 200, 220),  # White/Grey
        "shirt": (20, 20, 25),  # Black Jacket
        "pants": (40, 40, 50),
        "boots": (0, 200, 200),  # Cyan Boots
        "skin": (220, 220, 255),  # Pale/Synth
        "eye_color": (0, 255, 0),  # Green LED
        "metal": (100, 100, 110),  # Chrome
        "neon_pink": (255, 0, 128),
        "neon_blue": (0, 200, 255),
        "outline": (0, 20, 40),
    },
    "modern": {
        "hair": (30, 20, 10),  # Dark brown/black
        "shirt": (255, 255, 255),  # White
        "pants": (50, 50, 60),
        "boots": (100, 80, 60),
        "skin": (255, 220, 180),
        "eye_color": (80, 60, 40),
        "metal": (180, 190, 200),
        "outline": (50, 60, 70),
        "leather": (100, 60, 30),
    },
    "cute": {
        "hair": (255, 180, 200),  # Pink
        "shirt": (255, 220, 230),  # Light pink
        "pants": (255, 240, 245),
        "boots": (255, 200, 220),
        "skin": (255, 230, 220),  # Rosy
        "eye_color": (180, 100, 150),
        "metal": (220, 220, 230),
        "outline": (200, 150, 170),
        "gold": (255, 215, 0),
    },
    "action": {
        "hair": (255, 100, 50),  # Orange/Red
        "shirt": (60, 60, 70),  # Dark grey
        "pants": (40, 40, 50),
        "boots": (80, 60, 40),
        "skin": (220, 180, 150),
        "eye_color": (200, 50, 50),
        "metal": (160, 170, 180),  # Steel
        "outline": (30, 30, 30),
        "leather": (100, 50, 20),
    },
}

# Theme-specific Recommended Render Modes
THEME_RENDER_MODES = {
    "fantasy": "ink",
    "scifi": "neon",
    "modern": "hd",
    "cute": "premium",
    "action": "retro",
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
    "red": (200, 50, 50),
}

THEME_MAPPINGS = {
    "fantasy": ["adventurer_coat", "wizard_robe", "cape_hero", "wings_angel", "staff_magic", "sword_iron", "round_face", "long_straight", "braided", "ball_gown", "dress_skirt", "star_wand"],
    "scifi": ["cyber_vest", "tactical_armor", "plasma_rifle", "shield_round", "spiky", "messy_shag", "katana", "angular_hero", "armored_greaves"],
    "modern": ["school_uniform", "casual_tee", "backpack_travel", "book_spell", "bob", "long_straight", "glasses_red"],
    "cute": ["maid_dress", "ball_gown", "tea_cup", "twin_tails", "braided", "long_curly", "round_face", "dress_skirt", "star_wand", "topknot"],
    "action": ["tactical_armor", "leather_jacket", "spiky", "messy_shag", "buster_sword", "katana", "angular_hero", "armored_legs", "armored_greaves", "boots_shorts"],
}