# character_definitions.py

LAYER_ORDER = [
    "back",
    "legs_back",
    "body",
    "head",
    "eyes",
    "hair",
    "legs_front",
    "arms",
    "held",
]

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

PART_TAGS = {
    "head": {
        "human": ["generic", "xianxia", "western", "steampunk"],
        "elf": ["western", "xianxia"],
        "orc": ["western"],
        "dwarf": ["western", "steampunk"],
        "skeleton": ["western", "xianxia", "horror"],
        "robot": ["tech", "cyberpunk"],
        "pumpkin": ["western", "generic", "horror"],
        "sage_beard": ["xianxia", "western"],
        "cyborg_eye": ["tech", "cyberpunk"],
        "zombie": ["horror"],
        "gas_mask": ["steampunk", "tech"],
        "oni": ["xianxia", "western"],  # Japanese demon fits Xianxia/Western
    },
    "hair": {
        "bald": ["generic", "tech"],
        "short": ["generic", "modern"],
        "long": ["generic", "xianxia", "western"],
        "mohawk": ["tech", "western", "generic", "cyberpunk"],
        "ponytail": ["xianxia", "generic"],
        "afro": ["generic", "modern"],
        "wizard_hat": ["western"],
        "hood": ["western", "tech", "xianxia", "horror"],
        "bandana": ["western", "generic", "modern"],
        "topknot": ["xianxia"],
        "long_flowy": ["xianxia"],
        "helmet": ["tech", "western", "cyberpunk"],
        "mohawk_neon": ["cyberpunk", "tech"],
        "top_hat": ["steampunk", "western"],
        "brain_exposed": ["horror"],
    },
    "eyes": {
        "normal": ["generic"],
        "sunglasses": ["tech", "modern", "cyberpunk"],
        "cyclops": ["western", "tech"],
        "visipatch": ["tech", "cyberpunk"],
        "glowing": ["tech", "xianxia", "western", "cyberpunk", "horror"],
        "tired": ["generic", "modern", "horror"],
        "goggles": ["steampunk", "tech"],
    },
    "body": {
        "shirt": ["generic", "modern"],
        "armor": ["western", "xianxia"],
        "robe": ["xianxia", "western", "horror"],
        "jacket": ["modern", "tech", "cyberpunk"],
        "ribs": ["western", "xianxia", "horror"],
        "suit": ["modern", "tech", "steampunk"],
        "overalls": ["modern", "steampunk"],
        "hanfu_scholar": ["xianxia"],
        "hanfu_warrior": ["xianxia"],
        "mech_suit": ["tech", "cyberpunk"],
        "jacket_neon": ["cyberpunk"],
        "coat_brass": ["steampunk"],
        "ribs_gore": ["horror"],
    },
    "legs": {
        "pants": ["generic", "modern"],
        "skirt": ["generic", "xianxia", "western"],
        "shorts": ["modern", "generic"],
        "peg_leg": ["western", "steampunk"],
        "boots_high": ["tech", "western", "xianxia", "cyberpunk", "steampunk"],
        "robot_legs": ["tech", "cyberpunk"],
    },
    "held": {
        "none": ["generic"],
        "sword": ["western", "generic", "xianxia"],
        "staff": ["western", "xianxia"],
        "axe": ["western", "horror"],
        "shield": ["western", "tech"],
        "jian": ["xianxia"],
        "fan": ["xianxia"],
        "gourd": ["xianxia"],
        "laser_gun": ["tech", "cyberpunk"],
        "katana_laser": ["cyberpunk", "tech"],
        "wrench": ["steampunk", "modern"],
        "chainsaw": ["horror", "modern"],
        "butcher_knife": ["horror"],
    },
    "back": {
        "none": ["generic"],
        "cape": ["western", "xianxia", "horror"],
        "wings": ["western", "xianxia"],
        "backpack": ["modern", "western", "steampunk"],
        "jetpack": ["tech", "cyberpunk"],
        "flying_swords": ["xianxia"],
        "coffin": ["horror", "western"],
    },
}

PART_DEFINITIONS = {
    "back": {
        "none": [],
        "cape": [("rect", (8, 16, 16, 14), "shirt")],
        "wings": [
            ("rect", (4, 14, 8, 4), "white"),
            ("rect", (20, 14, 8, 4), "white"),
            ("pixel", (5, 13), "white"),
            ("pixel", (26, 13), "white"),
        ],
        "backpack": [
            ("rect", (8, 16, 16, 10), "wood"),
            ("rect", (10, 18, 12, 6), "pants"),
        ],
        "jetpack": [
            ("rect", (10, 16, 4, 10), "metal"),
            ("rect", (18, 16, 4, 10), "metal"),
            ("pixel", (11, 26), "highlight"),
            ("pixel", (19, 26), "highlight"),
        ],
        "flying_swords": [
            ("rect", (6, 10, 2, 10), "metal"),
            ("rect", (24, 10, 2, 10), "metal"),
            ("rect", (4, 12, 6, 2), "metal"),
            ("rect", (22, 12, 6, 2), "metal"),
        ],
        "coffin": [
            ("rect", (10, 12, 12, 18), "wood"),
            ("rect", (14, 16, 4, 10), "black"),
        ],  # Cross shape
    },
    "head": {
        "human": [("rect", (10, 4, 12, 12), "skin")],
        "elf": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("pixel", (9, 8), "skin"),
            ("pixel", (22, 8), "skin"),
        ],
        "orc": [
            ("rect", (9, 4, 14, 12), "skin"),
            ("rect", (11, 12, 2, 3), "tooth"),
            ("rect", (19, 12, 2, 3), "tooth"),
        ],
        "dwarf": [("rect", (10, 4, 12, 12), "skin"), ("rect", (10, 12, 12, 6), "hair")],
        "skeleton": [
            ("rect", (11, 5, 10, 10), "skin"),
            ("rect", (11, 12, 10, 3), "black"),
            ("rect", (13, 12, 1, 3), "skin"),
            ("rect", (15, 12, 1, 3), "skin"),
            ("rect", (17, 12, 1, 3), "skin"),
        ],
        "robot": [
            ("rect", (10, 4, 12, 12), "metal"),
            ("rect", (9, 9, 2, 2), "highlight"),
            ("rect", (21, 9, 2, 2), "highlight"),
        ],
        "pumpkin": [("rect", (9, 4, 14, 12), "hair"), ("rect", (15, 2, 2, 2), "wood")],
        "sage_beard": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("rect", (12, 14, 8, 6), "white"),
            ("rect", (13, 18, 6, 4), "white"),
        ],
        "cyborg_eye": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("rect", (11, 8, 4, 4), "metal"),
            ("pixel", (12, 9), "neon_pink"),
        ],
        "zombie": [
            ("rect", (10, 4, 12, 12), "zombie_skin"),
            ("rect", (11, 6, 3, 3), "blood"),
            ("pixel", (20, 10), "white"),
        ],  # Missing eye
        "gas_mask": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("rect", (11, 10, 10, 6), "leather"),
            ("rect", (13, 12, 2, 2), "brass"),
            ("rect", (17, 12, 2, 2), "brass"),
        ],
        "oni": [
            ("rect", (9, 4, 14, 12), "blood"),
            ("rect", (10, 2, 2, 3), "tooth"),
            ("rect", (20, 2, 2, 3), "tooth"),
        ],  # Red skin, horns
    },
    "hair": {
        "bald": [],
        "short": [
            ("rect", (10, 2, 12, 4), "hair"),
            ("rect", (9, 4, 1, 4), "hair"),
            ("rect", (22, 4, 1, 4), "hair"),
        ],
        "long": [
            ("rect", (10, 2, 12, 4), "hair"),
            ("rect", (8, 4, 2, 10), "hair"),
            ("rect", (22, 4, 2, 10), "hair"),
        ],
        "mohawk": [("rect", (14, 0, 4, 6), "hair")],
        "ponytail": [("rect", (10, 2, 12, 4), "hair"), ("rect", (6, 4, 4, 4), "hair")],
        "afro": [("rect", (8, 0, 16, 14), "hair")],
        "wizard_hat": [
            ("rect", (8, 6, 16, 2), "shirt"),
            ("polygon", [(11, 6), (16, -4), (21, 6)], "shirt"),
            ("rect", (11, 0, 10, 6), "shirt"),
            ("rect", (13, -4, 6, 4), "shirt"),
        ],
        "hood": [("rect", (9, 3, 14, 14), "shirt")],
        "bandana": [("rect", (9, 5, 14, 3), "shirt"), ("pixel", (8, 5), "shirt")],
        "topknot": [
            ("rect", (10, 2, 12, 4), "hair"),
            ("rect", (14, -2, 4, 4), "hair"),
            ("rect", (13, -1, 6, 1), "wood"),
        ],
        "long_flowy": [
            ("rect", (10, 2, 12, 4), "hair"),
            ("rect", (8, 4, 2, 14), "hair"),
            ("rect", (22, 4, 2, 14), "hair"),
            ("rect", (10, -2, 12, 2), "hair"),
        ],
        "helmet": [
            ("rect", (9, 3, 14, 14), "metal"),
            ("rect", (11, 8, 10, 3), "black"),
        ],
        "mohawk_neon": [("rect", (14, 0, 4, 6), "neon_pink")],
        "top_hat": [
            ("rect", (10, 2, 12, 2), "black"),
            ("rect", (11, -4, 10, 6), "black"),
            ("rect", (11, 1, 10, 1), "shirt"),
        ],  # Band
        "brain_exposed": [("rect", (11, 4, 10, 4), "blood")],
    },
    "eyes": {
        "normal": [("pixel", (12, 10), "eye_color"), ("pixel", (19, 10), "eye_color")],
        "sunglasses": [("rect", (11, 9, 10, 3), "black")],
        "cyclops": [("rect", (14, 9, 4, 4), "eye_color"), ("pixel", (15, 10), "black")],
        "visipatch": [
            ("rect", (11, 9, 10, 2), "metal"),
            ("pixel", (15, 9), "highlight"),
        ],
        "glowing": [
            ("rect", (12, 10, 2, 2), "highlight"),
            ("rect", (18, 10, 2, 2), "highlight"),
        ],
        "tired": [
            ("pixel", (12, 10), "eye_color"),
            ("pixel", (19, 10), "eye_color"),
            ("rect", (11, 11, 3, 1), "black"),
            ("rect", (18, 11, 3, 1), "black"),
        ],
        "goggles": [
            ("rect", (10, 9, 4, 4), "brass"),
            ("rect", (18, 9, 4, 4), "brass"),
            ("rect", (11, 10, 2, 2), "neon_blue"),
            ("rect", (19, 10, 2, 2), "neon_blue"),
        ],
    },
    "body": {
        "shirt": [("rect", (12, 16, 8, 8), "shirt")],
        "armor": [
            ("rect", (11, 16, 10, 8), "metal"),
            ("rect", (14, 18, 4, 4), "highlight"),
        ],
        "robe": [("rect", (11, 16, 10, 14), "shirt")],
        "jacket": [
            ("rect", (11, 16, 10, 10), "shirt"),
            ("rect", (15, 16, 2, 10), "white"),
        ],
        "ribs": [
            ("rect", (15, 16, 2, 8), "skin"),
            ("rect", (13, 17, 6, 1), "skin"),
            ("rect", (13, 19, 6, 1), "skin"),
            ("rect", (13, 21, 6, 1), "skin"),
        ],
        "suit": [
            ("rect", (12, 16, 8, 8), "black"),
            ("rect", (15, 16, 2, 4), "white"),
            ("rect", (15, 17, 2, 4), "shirt"),
        ],
        "overalls": [
            ("rect", (12, 16, 8, 8), "pants"),
            ("rect", (13, 18, 6, 4), "shirt"),
        ],
        "hanfu_scholar": [
            ("rect", (11, 16, 10, 14), "shirt"),
            ("rect", (11, 20, 10, 2), "black"),
            ("rect", (10, 16, 12, 14), "shirt"),
        ],
        "hanfu_warrior": [
            ("rect", (11, 16, 10, 12), "metal"),
            ("rect", (13, 18, 6, 6), "shirt"),
        ],
        "mech_suit": [
            ("rect", (10, 15, 12, 10), "metal"),
            ("rect", (14, 17, 4, 4), "neon_blue"),
            ("rect", (9, 15, 2, 6), "metal"),
            ("rect", (21, 15, 2, 6), "metal"),
        ],
        "jacket_neon": [
            ("rect", (11, 16, 10, 10), "black"),
            ("rect", (15, 16, 2, 10), "neon_pink"),
            ("rect", (11, 16, 1, 10), "neon_pink"),
            ("rect", (20, 16, 1, 10), "neon_pink"),
        ],
        "coat_brass": [
            ("rect", (11, 16, 10, 12), "leather"),
            ("rect", (13, 16, 2, 12), "brass"),
            ("rect", (17, 16, 2, 12), "brass"),
        ],
        "ribs_gore": [
            ("rect", (15, 16, 2, 8), "skin"),
            ("rect", (13, 17, 6, 1), "skin"),
            ("rect", (13, 19, 6, 1), "skin"),
            ("rect", (12, 16, 8, 8), "blood"),
        ],  # Bloody ribs
    },
    "legs": {
        "pants": [("rect", (0, 0, 3, 6), "pants")],
        "skirt": [("rect", (-1, 0, 5, 4), "pants")],
        "shorts": [("rect", (0, 0, 3, 3), "pants"), ("rect", (0, 3, 3, 3), "skin")],
        "peg_leg": [("rect", (1, 0, 1, 6), "wood")],
        "boots_high": [
            ("rect", (0, 0, 3, 3), "pants"),
            ("rect", (-1, 3, 5, 3), "boots"),
        ],
        "robot_legs": [
            ("rect", (0, 0, 3, 6), "metal"),
            ("rect", (1, 2, 1, 1), "highlight"),
        ],
    },
    "held": {
        "none": [],
        "sword": [
            ("rect", (0, -4, 2, 10), "metal"),
            ("rect", (-1, 4, 4, 1), "wood"),
            ("rect", (0, 5, 2, 3), "wood"),
        ],
        "staff": [
            ("rect", (0, -8, 2, 20), "wood"),
            ("rect", (-1, -10, 4, 4), "highlight"),
        ],
        "axe": [
            ("rect", (0, -4, 2, 14), "wood"),
            ("rect", (2, -4, 4, 6), "metal"),
            ("rect", (-2, -4, 4, 6), "metal"),
        ],
        "shield": [
            ("rect", (-2, -4, 8, 10), "metal"),
            ("rect", (0, -2, 4, 6), "shirt"),
        ],
        "jian": [
            ("rect", (0, -6, 2, 12), "metal"),
            ("rect", (-2, 6, 6, 1), "wood"),
            ("rect", (0, 7, 2, 3), "wood"),
            ("pixel", (0, 10), "highlight"),
        ],
        "fan": [
            ("polygon", [(0, 0), (-4, -4), (4, -4)], "white"),
            ("rect", (0, 0, 2, 4), "wood"),
        ],
        "gourd": [
            ("rect", (-2, -2, 6, 6), "wood"),
            ("rect", (0, -4, 2, 2), "wood"),
            ("rect", (-1, -6, 4, 2), "wood"),
        ],
        "laser_gun": [
            ("rect", (0, 0, 8, 2), "metal"),
            ("rect", (0, 2, 2, 4), "black"),
            ("rect", (2, -1, 4, 1), "neon_green"),
        ],
        "katana_laser": [
            ("rect", (0, -6, 2, 14), "neon_pink"),
            ("rect", (-1, 6, 4, 1), "black"),
            ("rect", (0, 7, 2, 3), "black"),
        ],
        "wrench": [
            ("rect", (0, -2, 2, 10), "metal"),
            ("rect", (-1, -4, 4, 2), "metal"),
        ],
        "chainsaw": [
            ("rect", (0, 0, 10, 4), "neon_pink"),
            ("rect", (0, 2, 4, 4), "black"),
        ],  # Simplified
        "butcher_knife": [
            ("rect", (0, -4, 4, 10), "metal"),
            ("rect", (0, 6, 2, 4), "wood"),
        ],
    },
}

THEME_MAPPINGS = {
    "xianxia": [],
    "tech": [],
    "western": [],
    "cyberpunk": [],
    "steampunk": [],
    "horror": [],
}

# Animation defs remain the same, just copied over to ensure file integrity if overwriting
ANIMATION_DEFINITIONS = {
    "idle": [{"bob": 0, "leg_f": 0, "arm_f": 0}, {"bob": 1, "leg_f": 0, "arm_f": 0}],
    "walk": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 1, "leg_f": -1, "arm_f": 1},
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 1, "leg_f": 1, "arm_f": -1},
    ],
    "run": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 2, "leg_f": -2, "arm_f": 2},
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 2, "leg_f": 2, "arm_f": 2},
    ],
    "attack": [
        {"bob": 0, "leg_f": 1, "arm_f": -1},
        {"bob": 0, "leg_f": 2, "arm_f": 2},
        {"bob": 1, "leg_f": 2, "arm_f": 2},
        {"bob": 0, "leg_f": 1, "arm_f": 0},
    ],
    "jump": [
        {"bob": 1, "leg_f": -1, "arm_f": -1},
        {"bob": -4, "leg_f": 0, "arm_f": 2},
        {"bob": -2, "leg_f": 0, "arm_f": 2},
        {"bob": 0, "leg_f": -1, "arm_f": 0},
    ],
    "hurt": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 0, "leg_f": -1, "arm_f": 2, "offset_x": -2},
        {"bob": 0, "leg_f": -1, "arm_f": 2, "offset_x": -1},
        {"bob": 0, "leg_f": 0, "arm_f": 0},
    ],
    "cheer": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -2, "leg_f": 0, "arm_f": 2},
        {"bob": 0, "leg_f": 0, "arm_f": 2},
        {"bob": -1, "leg_f": 0, "arm_f": 2},
    ],
    "die": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 4, "leg_f": -1, "arm_f": -1},
        {"bob": 8, "leg_f": -2, "arm_f": 0},
        {"bob": 8, "leg_f": -2, "arm_f": 0},
    ],
}
