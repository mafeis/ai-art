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
            # 64x64 Scale Head (Refined Shape)
            # Main Shape
            ("rect", (20, 12, 24, 20), "skin"),
            # Shading (Left/Right edges)
            ("rect", (20, 12, 2, 20), "skin_shadow"),
            ("rect", (42, 12, 2, 20), "skin_shadow"),
            # Rounding (2px steps)
            ("rect", (22, 10, 20, 2), "skin"),
            ("rect", (24, 8, 16, 2), "skin"),
            ("rect", (18, 14, 2, 16), "skin"),
            ("rect", (44, 14, 2, 16), "skin"),
            # Chin
            ("rect", (20, 32, 24, 2), "skin"),
            ("rect", (22, 34, 20, 2), "skin"),
            # Chin Shadow (Hard line)
            ("rect", (24, 35, 16, 1), "outline"),
            ("rect", (22, 36, 20, 2), "skin_shadow"),  # Neck shadow area
            # Blush (Dithered look)
            ("pixel", (19, 25), "highlight"),
            ("pixel", (21, 26), "highlight"),
            ("pixel", (43, 25), "highlight"),
            ("pixel", (45, 26), "highlight"),
            # Ears (Detailed)
            ("rect", (14, 20, 4, 6), "skin"),
            ("rect", (14, 21, 2, 4), "skin_shadow"),  # Inner ear shadow
            ("rect", (16, 22, 2, 2), "outline"),  # Ear hole
            ("rect", (46, 20, 4, 6), "skin"),
            ("rect", (48, 21, 2, 4), "skin_shadow"),
            ("rect", (46, 22, 2, 2), "outline"),
        ],
    },
    "eyes": {
        "anime_large": [
            # 8x10 Eyes (Super Detailed)
            # Sclera
            ("rect", (20, 18, 8, 10), "white"),
            ("rect", (36, 18, 8, 10), "white"),
            # Sclera Shadow (Top)
            ("rect", (20, 18, 8, 2), "white_shadow"),
            ("rect", (36, 18, 8, 2), "white_shadow"),
            # Iris (6x8)
            ("rect", (22, 18, 6, 8), "eye_color"),
            ("rect", (38, 18, 6, 8), "eye_color"),
            # Iris Gradient (Bottom lighter)
            ("rect", (22, 24, 6, 2), "eye_color_light"),
            ("rect", (38, 24, 6, 2), "eye_color_light"),
            # Pupil (2x4)
            ("rect", (24, 20, 2, 4), "black"),
            ("rect", (40, 20, 2, 4), "black"),
            # Highlight Main (2x2)
            ("rect", (22, 18, 2, 2), "white"),
            ("rect", (38, 18, 2, 2), "white"),
            # Highlight Secondary (1x1)
            ("pixel", (26, 24), "highlight"),
            ("pixel", (42, 24), "highlight"),
            # Highlight Sparkle
            ("pixel", (24, 25), "white"),
            ("pixel", (40, 25), "white"),
        ],
        "sharp_focus": [
            ("rect", (20, 18, 8, 6), "white"),
            ("rect", (36, 18, 8, 6), "white"),
            ("rect", (20, 18, 8, 2), "white_shadow"),
            ("rect", (36, 18, 8, 2), "white_shadow"),
            ("rect", (22, 18, 4, 6), "eye_color"),
            ("rect", (38, 18, 4, 6), "eye_color"),
            ("rect", (23, 18, 2, 6), "black"),
            ("rect", (39, 18, 2, 6), "black"),
            # Eyeliner
            ("rect", (19, 17, 10, 1), "black"),
            ("rect", (35, 17, 10, 1), "black"),
        ],
        "gentle_droop": [
            ("rect", (20, 20, 8, 8), "white"),
            ("rect", (36, 20, 8, 8), "white"),
            ("rect", (20, 20, 8, 2), "white_shadow"),
            ("rect", (36, 20, 8, 2), "white_shadow"),
            ("rect", (22, 20, 4, 6), "eye_color"),
            ("rect", (38, 20, 4, 6), "eye_color"),
            # Lid
            ("rect", (20, 18, 8, 2), "skin"),
            ("rect", (36, 18, 8, 2), "skin"),
            ("rect", (20, 19, 8, 1), "skin_shadow"),  # Lid crease
            ("rect", (36, 19, 8, 1), "skin_shadow"),
        ],
        "cat_eye": [
            ("rect", (20, 18, 8, 8), "white"),
            ("rect", (36, 18, 8, 8), "white"),
            ("rect", (22, 18, 4, 8), "gold"),
            ("rect", (38, 18, 4, 8), "gold"),
            ("rect", (23, 18, 2, 8), "black"),  # Slit
            ("rect", (39, 18, 2, 8), "black"),
            # Eyeliner Wings
            ("pixel", (19, 17), "black"),
            ("pixel", (44, 17), "black"),
        ],
    },
    "expression": {
        "neutral": [
            ("rect", (28, 32, 8, 1), "outline"),
            ("pixel", (28, 33), "outline"),  # Corner
            ("pixel", (35, 33), "outline"),
        ],
        "smile": [
            # Brows
            ("rect", (20, 14, 6, 1), "hair_dark"),
            ("rect", (38, 14, 6, 1), "hair_dark"),
            # Smile
            ("pixel", (26, 30), "outline"),
            ("rect", (28, 32, 8, 2), "outline"),
            ("pixel", (36, 30), "outline"),
            # Teeth
            ("rect", (29, 32, 6, 1), "white"),
        ],
        "pout": [
            # Angry Brows
            ("pixel", (20, 16), "hair_dark"),
            ("pixel", (22, 17), "hair_dark"),
            ("pixel", (24, 18), "hair_dark"),
            ("pixel", (42, 16), "hair_dark"),
            ("pixel", (40, 17), "hair_dark"),
            ("pixel", (38, 18), "hair_dark"),
            # Pout dot
            ("rect", (30, 32, 4, 2), "outline"),
            ("pixel", (34, 33), "skin_shadow"),
        ],
        "surprised": [
            ("rect", (20, 12, 6, 1), "hair_dark"),
            ("rect", (38, 12, 6, 1), "hair_dark"),
            ("rect", (28, 30, 8, 6), "outline"),
            ("rect", (30, 32, 4, 2), "black"),
        ],
    },
    "hair": {
        "short_hero": [
            # 64x64 HD Hair
            ("rect", (16, 4, 32, 12), "hair"),
            # Highlight Band (Broken up)
            ("rect", (20, 6, 6, 2), "highlight"),
            ("rect", (28, 6, 8, 2), "highlight"),
            ("rect", (38, 6, 6, 2), "highlight"),
            # Spikes (2px steps) - Add shadow to tips
            ("rect", (24, 2, 4, 2), "hair"),
            ("rect", (32, 0, 4, 4), "hair"),
            ("rect", (40, 2, 4, 2), "hair"),
            # Bangs
            ("rect", (18, 12, 4, 6), "hair"),
            ("rect", (28, 12, 8, 4), "hair"),
            ("rect", (42, 12, 4, 6), "hair"),
            # Bang Shadows
            ("rect", (18, 18, 4, 1), "hair_shadow"),
            ("rect", (28, 16, 8, 1), "hair_shadow"),
            ("rect", (42, 18, 4, 1), "hair_shadow"),
            # Sideburns
            ("rect", (14, 16, 4, 8), "hair"),
            ("rect", (46, 16, 4, 8), "hair"),
        ],
        "long_straight": [
            ("rect", (18, 4, 28, 12), "hair"),
            # Highlight
            ("rect", (20, 6, 6, 2), "highlight"),
            ("rect", (30, 6, 10, 2), "highlight"),
            ("rect", (20, 12, 24, 4), "hair"),  # Bangs
            ("rect", (20, 16, 24, 1), "hair_shadow"),  # Bang shadow
            # Sides (Long)
            ("rect", (14, 12, 6, 24), "hair"),
            ("rect", (44, 12, 6, 24), "hair"),
            # Side Highlights
            ("pixel", (14, 14), "highlight"),
            ("pixel", (49, 14), "highlight"),
        ],
        "twin_tails": [
            ("rect", (18, 4, 28, 12), "hair"),
            ("rect", (22, 6, 4, 2), "highlight"),
            ("rect", (38, 6, 4, 2), "highlight"),
            # Tails
            ("rect", (6, 8, 10, 24), "hair"),
            ("rect", (48, 8, 10, 24), "hair"),
            # Tail Shadow
            ("rect", (6, 32, 10, 2), "hair_shadow"),
            ("rect", (48, 32, 10, 2), "hair_shadow"),
            # Ties
            ("rect", (10, 6, 6, 4), "white"),
            ("rect", (48, 6, 6, 4), "white"),
            ("rect", (12, 8, 2, 2), "white_shadow"),  # Tie knot
            ("rect", (50, 8, 2, 2), "white_shadow"),
        ],
        "messy_shag": [
            ("rect", (16, 6, 32, 12), "hair"),
            ("rect", (24, 2, 6, 4), "hair"),  # Ahoge
            ("pixel", (26, 3), "highlight"),
            ("pixel", (14, 14), "hair"),
            ("pixel", (48, 14), "hair"),
            ("rect", (18, 12, 6, 6), "hair"),
            ("rect", (40, 12, 6, 6), "hair"),
            # Texture
            ("pixel", (20, 8), "hair_dark"),
            ("pixel", (35, 10), "hair_dark"),
        ],
        "bob": [
            ("rect", (16, 4, 32, 10), "hair"),  # Top Main
            ("rect", (16, 14, 4, 10), "hair"),  # Side L
            ("rect", (44, 14, 4, 10), "hair"),  # Side R
            ("rect", (18, 6, 8, 2), "highlight"),
            ("rect", (38, 6, 8, 2), "highlight"),
            ("rect", (18, 24, 4, 2), "hair"),  # Curl
            ("rect", (42, 24, 4, 2), "hair"),
        ],
    },
    "body": {
        "adventurer_coat": [
            # 64x64 Body (approx 24x18)
            ("rect", (20, 32, 24, 18), "shirt"),
            ("rect", (20, 32, 24, 18), "shirt_shadow", "stroke"),  # Outline for depth
            ("rect", (28, 32, 8, 18), "white"),  # Inner
            ("rect", (31, 34, 2, 2), "white_shadow"),  # Button
            ("rect", (31, 38, 2, 2), "white_shadow"),  # Button
            ("rect", (20, 46, 24, 4), "leather"),  # Belt
            ("rect", (20, 48, 24, 2), "leather_shadow"),  # Belt depth
            ("rect", (30, 46, 4, 4), "gold"),  # Buckle
            ("pixel", (31, 47), "white"),  # Shine
            ("rect", (20, 32, 6, 14), "highlight"),  # Lapel L
            ("rect", (38, 32, 6, 14), "highlight"),  # Lapel R
            ("rect", (24, 32, 2, 14), "shirt_shadow"),  # Lapel shadow
            ("rect", (38, 32, 2, 14), "shirt_shadow"),
        ],
        "school_uniform": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (28, 32, 8, 8), "white"),  # Shirt collar area
            ("rect", (30, 36, 4, 8), "red"),  # Tie
            ("rect", (31, 36, 2, 6), "red_light"),  # Tie highlight
            ("rect", (20, 48, 24, 2), "outline"),  # Hem
            ("pixel", (22, 38), "gold"),  # Pin
            # Collar
            ("rect", (20, 32, 8, 4), "black_light"),
            ("rect", (36, 32, 8, 4), "black_light"),
        ],
        "maid_dress": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (24, 32, 16, 16), "white"),  # Apron
            ("rect", (26, 34, 12, 12), "white_shadow"),  # Apron texture
            ("rect", (24, 32, 16, 4), "white"),  # Frill
            ("pixel", (26, 32), "white_shadow"),  # Frill detail
            ("pixel", (30, 32), "white_shadow"),
            ("pixel", (34, 32), "white_shadow"),
            ("rect", (14, 32, 6, 6), "white"),  # Sleeve L
            ("rect", (44, 32, 6, 6), "white"),  # Sleeve R
        ],
        "cyber_vest": [
            ("rect", (20, 32, 24, 16), "black"),
            ("rect", (20, 32, 24, 16), "black_light", "stroke"),  # Panel lines
            ("rect", (22, 36, 20, 2), "neon_blue"),
            ("rect", (22, 37, 20, 1), "neon_blue_light"),  # Core glow
            ("rect", (22, 42, 20, 2), "neon_blue"),
            ("rect", (16, 32, 4, 8), "metal"),  # Pads
            ("rect", (17, 33, 2, 6), "metal_light"),
            ("rect", (44, 32, 4, 8), "metal"),
            ("rect", (45, 33, 2, 6), "metal_light"),
        ],
        "wizard_robe": [
            ("rect", (20, 32, 24, 28), "shirt"),
            ("rect", (22, 34, 20, 24), "shirt_dark"),  # Folds
            ("rect", (26, 32, 12, 28), "highlight"),  # Center strip
            ("rect", (20, 32, 24, 6), "gold"),  # Collar
            ("rect", (22, 33, 20, 2), "gold_light"),
            # Runes
            ("pixel", (28, 40), "gold"),
            ("pixel", (34, 44), "gold"),
        ],
    },
    "legs": {
        "pants_boots": [
            ("rect", (2, 0, 8, 12), "pants"),
            ("rect", (2, 0, 1, 12), "pants_shadow"),  # Side seam
            ("rect", (0, 12, 10, 4), "boots"),
            ("rect", (2, 12, 6, 2), "boots_light"),  # Toe shine
            ("rect", (0, 16, 10, 2), "black"),  # Sole
            ("rect", (0, 17, 10, 1), "black_shadow"),  # Bottom shadow
        ],
        "skirt_socks": [
            ("rect", (-2, 0, 14, 8), "pants"),  # Skirt
            ("rect", (-2, 6, 14, 2), "pants_shadow"),  # Skirt shadow
            ("rect", (2, 8, 6, 6), "skin"),
            ("rect", (2, 14, 6, 4), "white"),  # Socks
            ("rect", (2, 14, 6, 1), "white_shadow"),  # Sock rim
            ("rect", (2, 18, 6, 2), "boots"),  # Shoes
            ("pixel", (3, 18), "boots_light"),
        ],
        "boots_shorts": [
            ("rect", (2, 0, 8, 6), "pants"),  # Shorts
            ("rect", (2, 5, 8, 1), "pants_shadow"),
            ("rect", (2, 6, 6, 6), "skin"),
            ("rect", (0, 12, 10, 6), "boots"),
            ("rect", (2, 12, 2, 6), "boots_light"),  # Laces area
            ("rect", (0, 12, 10, 1), "boots_shadow"),  # Boot top
        ],
        "armored_legs": [
            ("rect", (2, 0, 8, 10), "metal"),
            ("rect", (4, 4, 4, 4), "highlight"),  # Knee Plate
            ("rect", (5, 5, 2, 2), "white"),  # Specular
            ("rect", (0, 10, 10, 8), "metal"),
            ("rect", (0, 16, 10, 2), "metal_shadow"),  # Foot shadow
        ],
    },
    "held": {
        "sword_iron": [
            ("rect", (0, -20, 6, 36), "metal"),
            ("rect", (2, -20, 2, 36), "highlight"),  # Edge
            ("rect", (1, -18, 1, 32), "white"),  # Sharp edge shine
            ("rect", (-4, 16, 14, 4), "gold"),  # Crossguard
            ("rect", (-2, 17, 10, 2), "gold_light"),
            ("rect", (-2, 20, 6, 6), "wood"),  # Pommel
        ],
        "staff_magic": [
            ("rect", (0, -24, 4, 52), "wood"),
            ("rect", (3, -24, 1, 52), "wood_shadow"),  # Staff rounding
            ("rect", (-4, -28, 12, 12), "gold"),  # Head
            ("rect", (-2, -26, 8, 8), "neon_blue"),  # Gem
            ("rect", (0, -24, 4, 4), "white"),  # Gem shine
        ],
        "book_spell": [
            ("rect", (-4, -8, 20, 24), "leather"),  # Cover
            ("rect", (-4, -8, 2, 24), "leather_light"),  # Spine
            ("rect", (0, -4, 12, 16), "white"),  # Pages
            ("rect", (2, -2, 8, 1), "black_light"),  # Text line
            ("rect", (2, 2, 8, 1), "black_light"),
            ("rect", (6, 4, 4, 4), "neon_blue"),  # Rune
        ],
        "shield_round": [
            ("rect", (-8, -8, 24, 24), "metal"),
            ("rect", (-4, -4, 16, 16), "metal_light"),  # Center boss
            ("rect", (-6, -6, 20, 20), "shirt"),  # Heraldry bg
            ("rect", (-2, -2, 12, 12), "shirt_light"),  # Emblem
            ("rect", (-8, -8, 24, 24), "outline", "stroke"),  # Rim
            ("rect", (-8, -8, 24, 24), "metal_light", "stroke"),  # Inner rim highlight
        ],
        "tea_cup": [
            ("rect", (0, 0, 12, 16), "white"),
            ("rect", (2, 2, 8, 12), "white_shadow"),  # Cup volume
            ("pixel", (4, 6), "outline"),  # Pattern
            ("rect", (4, -6, 2, 6), "black"),  # Steam/Liquid?
        ],
        "none": [],
    },
    "back": {
        "none": [],
        "cape_hero": [
            ("rect", (12, 32, 40, 28), "shirt"),
            ("rect", (14, 32, 36, 28), "shirt_light"),  # Folds
            ("rect", (20, 32, 24, 28), "highlight"),
            ("rect", (12, 58, 40, 2), "shirt_shadow"),  # Bottom tatter
        ],
        "wings_angel": [
            ("rect", (4, 24, 16, 12), "white"),
            ("rect", (4, 30, 16, 2), "white_shadow"),  # Feather layer
            ("rect", (44, 24, 16, 12), "white"),
            ("rect", (44, 30, 16, 2), "white_shadow"),
            ("pixel", (8, 28), "highlight"),
        ],
        "backpack_travel": [
            ("rect", (16, 28, 32, 24), "wood"),  # Brown bag
            ("rect", (16, 28, 32, 2), "wood_light"),  # Top flap
            ("rect", (20, 36, 24, 12), "highlight"),  # Pocket
            ("rect", (22, 38, 20, 8), "highlight_shadow"),
            ("rect", (30, 28, 4, 24), "outline"),  # Strap
            ("rect", (31, 40, 2, 2), "gold"),  # Buckle
        ],
    },
    "face_wear": {
        "none": [],
        "glasses_red": [
            ("rect", (20, 20, 8, 4), "red", "stroke"),
            ("rect", (36, 20, 8, 4), "red", "stroke"),
            ("rect", (28, 22, 8, 2), "red"),  # Bridge
            ("pixel", (20, 20), "white"),  # Glint
            ("pixel", (36, 20), "white"),
        ],
        "bandage": [
            ("rect", (20, 24, 6, 4), "white"),
            ("rect", (21, 25, 4, 2), "white_shadow"),  # Texture
            ("pixel", (22, 26), "blood"),
        ],
        "cat_ears_headset": [
            ("rect", (18, 6, 28, 2), "black"),
            ("polygon", [(14, 6), (10, 0), (18, 4)], "black"),
            ("polygon", [(12, 4), (11, 2), (16, 5)], "neon_blue"),  # Inner glow
            ("polygon", [(46, 6), (50, 0), (42, 4)], "black"),
            ("polygon", [(48, 4), (49, 2), (44, 5)], "neon_blue"),
            ("rect", (14, 16, 4, 12), "neon_blue"),
            ("rect", (46, 16, 4, 12), "neon_blue"),
            ("pixel", (15, 18), "white"),  # LED
        ],
    },
}
