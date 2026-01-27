# character_definitions.py

# Drawing Instructions Format:
# ("rect", (x, y, w, h), color_key)
# ("pixel", (x, y), color_key)
# Coordinates are based on a 32x32 grid.

# Order of drawing:
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

PART_DEFINITIONS = {
    "back": {
        "none": [],
        "cape": [
            ("rect", (8, 16, 16, 14), "shirt"),  # Wide cape
        ],
        "wings": [
            ("rect", (4, 14, 8, 4), "white"),  # Wing L
            ("rect", (20, 14, 8, 4), "white"),  # Wing R
            ("pixel", (5, 13), "white"),
            ("pixel", (26, 13), "white"),
        ],
        "backpack": [
            ("rect", (8, 16, 16, 10), "wood"),  # Leather pack
            ("rect", (10, 18, 12, 6), "pants"),  # Pocket
        ],
        "jetpack": [
            ("rect", (10, 16, 4, 10), "metal"),  # Tank L
            ("rect", (18, 16, 4, 10), "metal"),  # Tank R
            ("pixel", (11, 26), "highlight"),  # Flame?
            ("pixel", (19, 26), "highlight"),
        ],
    },
    "head": {
        "human": [
            ("rect", (10, 4, 12, 12), "skin"),
        ],
        "elf": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("pixel", (9, 8), "skin"),  # Left Ear
            ("pixel", (22, 8), "skin"),  # Right Ear
        ],
        "orc": [
            ("rect", (9, 4, 14, 12), "skin"),  # Wider head
            ("rect", (11, 12, 2, 3), "tooth"),  # Tusk
            ("rect", (19, 12, 2, 3), "tooth"),  # Tusk
        ],
        "dwarf": [
            ("rect", (10, 4, 12, 12), "skin"),
            ("rect", (10, 12, 12, 6), "hair"),  # Beard
        ],
        "skeleton": [
            ("rect", (11, 5, 10, 10), "skin"),  # Skull
            ("rect", (11, 12, 10, 3), "black"),  # Mouth
            ("rect", (13, 12, 1, 3), "skin"),  # Tooth
            ("rect", (15, 12, 1, 3), "skin"),  # Tooth
            ("rect", (17, 12, 1, 3), "skin"),  # Tooth
        ],
        "robot": [
            ("rect", (10, 4, 12, 12), "metal"),
            ("rect", (9, 9, 2, 2), "highlight"),  # Ear bolts
            ("rect", (21, 9, 2, 2), "highlight"),
        ],
        "pumpkin": [
            (
                "rect",
                (9, 4, 14, 12),
                "hair",
            ),  # Orange head (mapped to hair color usually orange)
            ("rect", (15, 2, 2, 2), "wood"),  # Stem
        ],
    },
    "hair": {
        "bald": [],
        "short": [
            ("rect", (10, 2, 12, 4), "hair"),  # Top
            ("rect", (9, 4, 1, 4), "hair"),  # Side L
            ("rect", (22, 4, 1, 4), "hair"),  # Side R
        ],
        "long": [
            ("rect", (10, 2, 12, 4), "hair"),  # Top
            ("rect", (8, 4, 2, 10), "hair"),  # Side L long
            ("rect", (22, 4, 2, 10), "hair"),  # Side R long
        ],
        "mohawk": [
            ("rect", (14, 0, 4, 6), "hair"),  # Spike
        ],
        "ponytail": [
            ("rect", (10, 2, 12, 4), "hair"),  # Top
            ("rect", (6, 4, 4, 4), "hair"),  # Ponytail
        ],
        "afro": [
            ("rect", (8, 0, 16, 14), "hair"),  # Big afro
        ],
        "wizard_hat": [
            ("rect", (8, 6, 16, 2), "shirt"),  # Brim
            ("polygon", [(11, 6), (16, -4), (21, 6)], "shirt"),  # Cone
            ("rect", (11, 0, 10, 6), "shirt"),  # Cone base
            ("rect", (13, -4, 6, 4), "shirt"),  # Cone tip
        ],
        "hood": [
            ("rect", (9, 3, 14, 14), "shirt"),  # Hood covers head
        ],
        "bandana": [
            ("rect", (9, 5, 14, 3), "shirt"),  # Bandana strip
            ("pixel", (8, 5), "shirt"),  # Knot
        ],
    },
    "eyes": {
        "normal": [
            ("pixel", (12, 10), "eye_color"),
            ("pixel", (19, 10), "eye_color"),
        ],
        "sunglasses": [
            ("rect", (11, 9, 10, 3), "black"),
        ],
        "cyclops": [
            ("rect", (14, 9, 4, 4), "eye_color"),
            ("pixel", (15, 10), "black"),  # Pupil
        ],
        "visipatch": [
            ("rect", (11, 9, 10, 2), "metal"),  # Visor
            ("pixel", (15, 9), "highlight"),
        ],
        "glowing": [
            ("rect", (12, 10, 2, 2), "highlight"),
            ("rect", (18, 10, 2, 2), "highlight"),
        ],
        "tired": [
            ("pixel", (12, 10), "eye_color"),
            ("pixel", (19, 10), "eye_color"),
            ("rect", (11, 11, 3, 1), "black"),  # Bags
            ("rect", (18, 11, 3, 1), "black"),
        ],
    },
    "body": {
        "shirt": [
            ("rect", (12, 16, 8, 8), "shirt"),
        ],
        "armor": [
            ("rect", (11, 16, 10, 8), "metal"),  # Bulky
            ("rect", (14, 18, 4, 4), "highlight"),  # Shiny center
        ],
        "robe": [
            ("rect", (11, 16, 10, 14), "shirt"),  # Long robe (covers legs partially)
        ],
        "jacket": [
            ("rect", (11, 16, 10, 10), "shirt"),  # Open jacket logic simulated
            ("rect", (15, 16, 2, 10), "white"),  # Inner shirt
        ],
        "ribs": [
            ("rect", (15, 16, 2, 8), "skin"),  # Spine
            ("rect", (13, 17, 6, 1), "skin"),  # Rib 1
            ("rect", (13, 19, 6, 1), "skin"),  # Rib 2
            ("rect", (13, 21, 6, 1), "skin"),  # Rib 3
        ],
        "suit": [
            ("rect", (12, 16, 8, 8), "black"),  # Jacket
            ("rect", (15, 16, 2, 4), "white"),  # Shirt
            ("rect", (15, 17, 2, 4), "shirt"),  # Tie (using shirt color)
        ],
        "overalls": [
            ("rect", (12, 16, 8, 8), "pants"),  # Denim color
            ("rect", (13, 18, 6, 4), "shirt"),  # Shirt under
        ],
    },
    "legs": {
        "pants": [
            ("rect", (0, 0, 3, 6), "pants"),
        ],
        "skirt": [
            ("rect", (-1, 0, 5, 4), "pants"),
        ],
        "shorts": [
            ("rect", (0, 0, 3, 3), "pants"),
            ("rect", (0, 3, 3, 3), "skin"),
        ],
        "peg_leg": [
            ("rect", (1, 0, 1, 6), "wood"),
        ],
        "boots_high": [
            ("rect", (0, 0, 3, 3), "pants"),
            ("rect", (-1, 3, 5, 3), "boots"),  # Thick boots
        ],
    },
    "held": {
        "none": [],
        "sword": [
            ("rect", (0, -4, 2, 10), "metal"),  # Blade
            ("rect", (-1, 4, 4, 1), "wood"),  # Guard
            ("rect", (0, 5, 2, 3), "wood"),  # Hilt
        ],
        "staff": [
            ("rect", (0, -8, 2, 20), "wood"),  # Staff
            ("rect", (-1, -10, 4, 4), "highlight"),  # Gem
        ],
        "axe": [
            ("rect", (0, -4, 2, 14), "wood"),  # Handle
            ("rect", (2, -4, 4, 6), "metal"),  # Blade R
            ("rect", (-2, -4, 4, 6), "metal"),  # Blade L
        ],
        "shield": [
            ("rect", (-2, -4, 8, 10), "metal"),  # Shield
            ("rect", (0, -2, 4, 6), "shirt"),  # Emblem
        ],
    },
}

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
        {"bob": 2, "leg_f": -2, "arm_f": 2},  # High knees
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 2, "leg_f": 2, "arm_f": 2},
    ],
    "attack": [
        {"bob": 0, "leg_f": 1, "arm_f": -1},  # Wind up
        {"bob": 0, "leg_f": 2, "arm_f": 2},  # Strike
        {"bob": 1, "leg_f": 2, "arm_f": 2},  # Hold
        {"bob": 0, "leg_f": 1, "arm_f": 0},  # Recover
    ],
    "jump": [
        {"bob": 1, "leg_f": -1, "arm_f": -1},  # Crouch
        {"bob": -4, "leg_f": 0, "arm_f": 2},  # Up
        {"bob": -2, "leg_f": 0, "arm_f": 2},  # Peak
        {"bob": 0, "leg_f": -1, "arm_f": 0},  # Land
    ],
    "hurt": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 0, "leg_f": -1, "arm_f": 2, "offset_x": -2},  # Push back
        {"bob": 0, "leg_f": -1, "arm_f": 2, "offset_x": -1},
        {"bob": 0, "leg_f": 0, "arm_f": 0},
    ],
    "cheer": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -2, "leg_f": 0, "arm_f": 2},  # Jump up
        {"bob": 0, "leg_f": 0, "arm_f": 2},  # Land arms up
        {"bob": -1, "leg_f": 0, "arm_f": 2},  # Bounce
    ],
    "die": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 4, "leg_f": -1, "arm_f": -1},  # Drop
        {"bob": 8, "leg_f": -2, "arm_f": 0},  # Floor
        {"bob": 8, "leg_f": -2, "arm_f": 0},
    ],
}

# Semantic Color Defaults (Fallback)
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
}
