# parts.py
# 像素本位 - 64x64 HD Q版 (Pixel-Perfect Chibi HD)
# Rule 1: Base Resolution is 64x64 (Double Precision).
# Rule 2: High Detail via pixel placement.

LAYER_ORDER = [
    "back",
    "arm_back",  # 后手 (New)
    "legs_back",
    "body",
    "head",
    "eyes",
    "expression",
    "face_wear",
    "hair",
    "legs_front",
    "arm_front",  # 前手 (New)
    "held",  # 武器在手前? 通常武器柄在手心，武器身在手后/前。简单起见：手覆盖武器柄。
    "hand_front",  # 前手掌 (覆盖武器柄)
]

PART_TAGS = {
    "head": {"base": ["generic"]},
    "hair": {
        "short_hero": ["male", "generic"],
        "long_straight": ["female", "generic"],
        "twin_tails": ["female", "cute"],
        "messy_shag": ["male", "action"],
        "bob": ["female", "modern"],
    },
    "eyes": {
        "anime_large": ["cute"],
        "sharp_focus": ["cool"],
        "gentle_droop": ["calm"],
        "cat_eye": ["active"],
    },
    "expression": {
        "smile": ["happy"],
        "pout": ["angry"],
        "neutral": ["calm"],
        "surprised": ["shock"],
    },
    "face_wear": {
        "none": ["generic"],
        "glasses_red": ["smart"],
        "bandage": ["action"],
        "cat_ears_headset": ["cute"],
    },
    "body": {
        "adventurer_coat": ["fantasy"],
        "school_uniform": ["modern"],
        "maid_dress": ["cute"],
        "cyber_vest": ["scifi"],
        "wizard_robe": ["fantasy"],
    },
    "legs": {
        "boots_shorts": ["action"],
        "skirt_socks": ["cute"],
        "pants_boots": ["generic"],
        "armored_legs": ["fantasy"],
    },
    "held": {
        "sword_iron": ["action"],
        "staff_magic": ["fantasy"],
        "book_spell": ["smart"],
        "shield_round": ["defense"],
        "tea_cup": ["cute"],
        "none": ["generic"],
    },
    "back": {
        "none": ["generic"],
        "cape_hero": ["fantasy"],
        "wings_angel": ["fantasy"],
        "backpack_travel": ["modern"],
    },
}

PART_DEFINITIONS = {
    "head": {
        "base": [
            # 64x64 Scale Head (approx 24x22 pixels)
            # Main Shape
            ("rect", (20, 12, 24, 20), "skin"),
            # Rounding (2px steps)
            ("rect", (22, 10, 20, 2), "skin"),
            ("rect", (24, 8, 16, 2), "skin"),
            ("rect", (18, 14, 2, 16), "skin"),
            ("rect", (44, 14, 2, 16), "skin"),
            # Chin
            ("rect", (20, 32, 24, 2), "skin"),
            ("rect", (22, 34, 20, 2), "skin"),
            # Chin Shadow
            ("rect", (24, 35, 16, 1), "outline"),
            # Blush (4x2 dithered)
            ("rect", (18, 24, 4, 2), "highlight"),
            ("rect", (42, 24, 4, 2), "highlight"),
            # Ears
            ("rect", (14, 20, 4, 6), "skin"),
            ("rect", (16, 22, 2, 2), "outline"),  # Inner
            ("rect", (46, 20, 4, 6), "skin"),
            ("rect", (46, 22, 2, 2), "outline"),
        ],
    },
    "eyes": {
        "anime_large": [
            # 8x10 Eyes (Huge detail)
            # Sclera
            ("rect", (20, 18, 8, 10), "white"),
            ("rect", (36, 18, 8, 10), "white"),
            # Iris (6x8)
            ("rect", (22, 18, 6, 8), "eye_color"),
            ("rect", (38, 18, 6, 8), "eye_color"),
            # Pupil (2x4)
            ("rect", (24, 20, 2, 4), "black"),
            ("rect", (40, 20, 2, 4), "black"),
            # Highlight Main (2x2)
            ("rect", (22, 18, 2, 2), "white"),
            ("rect", (38, 18, 2, 2), "white"),
            # Highlight Secondary (1x1)
            ("pixel", (26, 24), "highlight"),
            ("pixel", (42, 24), "highlight"),
        ],
        "sharp_focus": [
            ("rect", (20, 18, 8, 6), "white"),
            ("rect", (36, 18, 8, 6), "white"),
            ("rect", (22, 18, 4, 6), "eye_color"),
            ("rect", (38, 18, 4, 6), "eye_color"),
            ("rect", (23, 18, 2, 6), "black"),
            ("rect", (39, 18, 2, 6), "black"),
        ],
        "gentle_droop": [
            ("rect", (20, 20, 8, 8), "white"),
            ("rect", (36, 20, 8, 8), "white"),
            ("rect", (22, 20, 4, 6), "eye_color"),
            ("rect", (38, 20, 4, 6), "eye_color"),
            # Lid
            ("rect", (20, 18, 8, 2), "skin"),
            ("rect", (36, 18, 8, 2), "skin"),
        ],
        "cat_eye": [
            ("rect", (20, 18, 8, 8), "white"),
            ("rect", (36, 18, 8, 8), "white"),
            ("rect", (22, 18, 4, 8), "gold"),
            ("rect", (38, 18, 4, 8), "gold"),
            ("rect", (23, 18, 2, 8), "black"),  # Slit
            ("rect", (39, 18, 2, 8), "black"),
        ],
    },
    "expression": {
        "neutral": [
            ("rect", (28, 32, 8, 1), "outline"),  # Thin line
        ],
        "smile": [
            # Brows
            ("rect", (20, 14, 6, 1), "hair"),
            ("rect", (38, 14, 6, 1), "hair"),
            # Smile
            ("pixel", (26, 30), "outline"),
            ("rect", (28, 32, 8, 2), "outline"),
            ("pixel", (36, 30), "outline"),
        ],
        "pout": [
            # Angry Brows
            ("pixel", (20, 16), "hair"),
            ("pixel", (22, 17), "hair"),
            ("pixel", (24, 18), "hair"),
            ("pixel", (42, 16), "hair"),
            ("pixel", (40, 17), "hair"),
            ("pixel", (38, 18), "hair"),
            # Pout dot
            ("rect", (30, 32, 4, 2), "outline"),
        ],
        "surprised": [
            ("rect", (20, 12, 6, 1), "hair"),
            ("rect", (38, 12, 6, 1), "hair"),
            ("rect", (28, 30, 8, 6), "outline"),
            ("rect", (30, 32, 4, 2), "black"),
        ],
    },
    "hair": {
        "short_hero": [
            # 64x64 HD Hair
            ("rect", (16, 4, 32, 12), "hair"),
            ("rect", (20, 6, 24, 2), "highlight"),
            # Spikes (2px steps)
            ("rect", (24, 2, 4, 2), "hair"),
            ("rect", (32, 0, 4, 4), "hair"),
            ("rect", (40, 2, 4, 2), "hair"),
            # Bangs
            ("rect", (18, 12, 4, 6), "hair"),
            ("rect", (28, 12, 8, 4), "hair"),
            ("rect", (42, 12, 4, 6), "hair"),
            # Sideburns
            ("rect", (14, 16, 4, 8), "hair"),
            ("rect", (46, 16, 4, 8), "hair"),
        ],
        "long_straight": [
            ("rect", (18, 4, 28, 12), "hair"),
            ("rect", (20, 6, 24, 2), "highlight"),
            ("rect", (20, 12, 24, 4), "hair"),  # Bangs
            # Sides (Long)
            ("rect", (14, 12, 6, 24), "hair"),
            ("rect", (44, 12, 6, 24), "hair"),
            # Back
            ("rect", (20, 16, 24, 16), "hair"),
        ],
        "twin_tails": [
            ("rect", (18, 4, 28, 12), "hair"),
            ("rect", (20, 6, 24, 2), "highlight"),
            # Tails
            ("rect", (6, 8, 10, 24), "hair"),
            ("rect", (48, 8, 10, 24), "hair"),
            # Ties
            ("rect", (10, 6, 6, 4), "white"),
            ("rect", (48, 6, 6, 4), "white"),
        ],
        "messy_shag": [
            ("rect", (16, 6, 32, 12), "hair"),
            ("rect", (24, 2, 6, 4), "hair"),  # Ahoge
            ("pixel", (14, 14), "hair"),
            ("pixel", (48, 14), "hair"),
            ("rect", (18, 12, 6, 8), "hair"),
            ("rect", (40, 12, 6, 6), "hair"),
        ],
        "bob": [
            ("rect", (16, 4, 32, 20), "hair"),
            ("rect", (18, 6, 28, 2), "highlight"),
            ("rect", (18, 24, 4, 2), "hair"),  # Curl
            ("rect", (42, 24, 4, 2), "hair"),
            ("rect", (20, 14, 24, 10), "skin"),  # Face cutout
        ],
    },
    "body": {
        "adventurer_coat": [
            # 64x64 Body (approx 24x18)
            ("rect", (20, 32, 24, 18), "shirt"),
            ("rect", (28, 32, 8, 18), "white"),  # Inner
            ("rect", (20, 46, 24, 4), "leather"),  # Belt
            ("rect", (30, 46, 4, 4), "gold"),  # Buckle
            ("rect", (20, 32, 6, 14), "highlight"),  # Lapel L
            ("rect", (38, 32, 6, 14), "highlight"),  # Lapel R
        ],
        "school_uniform": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (28, 32, 8, 8), "white"),
            ("rect", (30, 36, 4, 8), "red"),  # Tie
            ("rect", (20, 48, 24, 2), "outline"),  # Hem
            ("pixel", (22, 38), "gold"),
        ],
        "maid_dress": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (24, 32, 16, 16), "white"),  # Apron
            ("rect", (24, 32, 16, 4), "white"),  # Frill
            ("rect", (14, 32, 6, 6), "white"),  # Sleeve L
            ("rect", (44, 32, 6, 6), "white"),  # Sleeve R
        ],
        "cyber_vest": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (22, 36, 20, 2), "neon_blue"),
            ("rect", (22, 42, 20, 2), "neon_blue"),
            ("rect", (16, 32, 4, 8), "metal"),  # Pads
            ("rect", (44, 32, 4, 8), "metal"),
        ],
        "wizard_robe": [
            ("rect", (20, 32, 24, 28), "shirt"),
            ("rect", (26, 32, 12, 28), "highlight"),
            ("rect", (20, 32, 24, 6), "gold"),
        ],
    },
    "legs": {
        "pants_boots": [
            ("rect", (2, 0, 8, 12), "pants"),
            ("rect", (0, 12, 10, 4), "boots"),
            ("rect", (0, 16, 10, 2), "black"),
        ],
        "skirt_socks": [
            ("rect", (-2, 0, 14, 8), "pants"),  # Skirt
            ("rect", (2, 8, 6, 6), "skin"),
            ("rect", (2, 14, 6, 4), "white"),
            ("rect", (2, 18, 6, 2), "boots"),
        ],
        "boots_shorts": [
            ("rect", (2, 0, 8, 6), "pants"),  # Shorts
            ("rect", (2, 6, 6, 6), "skin"),
            ("rect", (0, 12, 10, 6), "boots"),
        ],
        "armored_legs": [
            ("rect", (2, 0, 8, 10), "metal"),
            ("rect", (4, 4, 4, 4), "highlight"),
            ("rect", (0, 10, 10, 8), "metal"),
        ],
    },
    "held": {
        "sword_iron": [
            ("rect", (0, -20, 6, 36), "metal"),
            ("rect", (2, -20, 2, 36), "highlight"),
            ("rect", (-4, 16, 14, 4), "gold"),
            ("rect", (-2, 20, 6, 6), "wood"),
        ],
        "staff_magic": [
            ("rect", (0, -24, 4, 52), "wood"),
            ("rect", (-4, -28, 12, 12), "gold"),
            ("rect", (-2, -26, 8, 8), "neon_blue"),
        ],
        "book_spell": [
            ("rect", (-4, -8, 20, 24), "leather"),
            ("rect", (0, -4, 12, 16), "white"),
            ("rect", (6, 4, 4, 4), "neon_blue"),
        ],
        "shield_round": [
            ("rect", (-8, -8, 24, 24), "metal"),
            ("rect", (-6, -6, 20, 20), "shirt"),
            ("rect", (-8, -8, 24, 24), "outline", "stroke"),
        ],
        "tea_cup": [
            ("rect", (0, 0, 12, 16), "white"),
            ("pixel", (4, 6), "outline"),
            ("rect", (4, -6, 2, 6), "black"),
        ],
        "none": [],
    },
    "back": {
        "none": [],
        "cape_hero": [
            ("rect", (12, 32, 40, 28), "shirt"),
            ("rect", (20, 32, 24, 28), "highlight"),
        ],
        "wings_angel": [
            ("rect", (4, 24, 16, 12), "white"),
            ("rect", (44, 24, 16, 12), "white"),
            ("pixel", (8, 28), "highlight"),
        ],
        "backpack_travel": [
            ("rect", (16, 28, 32, 24), "wood"),
            ("rect", (20, 36, 24, 12), "highlight"),
            ("rect", (30, 28, 4, 24), "outline"),
        ],
    },
    "face_wear": {
        "none": [],
        "glasses_red": [
            ("rect", (20, 20, 8, 4), "red", "stroke"),
            ("rect", (36, 20, 8, 4), "red", "stroke"),
            ("rect", (28, 22, 8, 2), "red"),
        ],
        "bandage": [
            ("rect", (20, 24, 6, 4), "white"),
            ("pixel", (22, 26), "blood"),
        ],
        "cat_ears_headset": [
            ("rect", (18, 6, 28, 2), "black"),
            ("polygon", [(14, 6), (10, 0), (18, 4)], "black"),
            ("polygon", [(46, 6), (50, 0), (42, 4)], "black"),
            ("rect", (14, 16, 4, 12), "neon_blue"),
            ("rect", (46, 16, 4, 12), "neon_blue"),
        ],
    },
}
