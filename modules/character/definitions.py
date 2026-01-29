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
        "cape": [
            ("rect", (6, 16, 20, 16), "shirt"),  # Main cape body
            ("rect", (8, 14, 16, 2), "shirt"),  # Shoulders
            ("rect", (10, 32, 4, 3), "shirt"),  # Ragged bottom
            ("rect", (18, 32, 4, 2), "shirt"),  # Ragged bottom
        ],
        "wings": [
            ("rect", (2, 12, 8, 4), "white"),  # L Wing top
            ("rect", (4, 16, 6, 6), "white"),  # L Wing mid
            ("rect", (6, 22, 2, 4), "white"),  # L Wing tip
            ("rect", (22, 12, 8, 4), "white"),  # R Wing top
            ("rect", (22, 16, 6, 6), "white"),  # R Wing mid
            ("rect", (24, 22, 2, 4), "white"),  # R Wing tip
        ],
        "backpack": [
            ("rect", (8, 14, 16, 12), "wood"),  # Main pack
            ("rect", (9, 15, 14, 10), "pants"),  # Inner fabric
            ("rect", (10, 20, 12, 4), "wood"),  # Pocket
            ("rect", (6, 16, 2, 8), "wood"),  # Strap L
            ("rect", (24, 16, 2, 8), "wood"),  # Strap R
        ],
        "jetpack": [
            ("rect", (10, 14, 5, 14), "metal"),  # L Thruster
            ("rect", (17, 14, 5, 14), "metal"),  # R Thruster
            ("rect", (11, 28, 3, 2), "neon_blue"),  # Flame L
            ("rect", (18, 28, 3, 2), "neon_blue"),  # Flame R
            ("rect", (12, 16, 8, 4), "metal"),  # Connector
        ],
        "flying_swords": [
            ("rect", (6, 8, 2, 14), "metal"),  # Sword 1
            ("rect", (24, 8, 2, 14), "metal"),  # Sword 2
            ("rect", (4, 12, 6, 1), "metal"),  # Guard 1
            ("rect", (22, 12, 6, 1), "metal"),  # Guard 2
            ("pixel", (6, 23), "highlight"),  # Tip sparkle
            ("pixel", (24, 23), "highlight"),
        ],
        "coffin": [
            ("rect", (10, 10, 12, 22), "wood"),  # Box
            ("rect", (12, 14, 8, 14), "black"),  # Cross inset
            ("rect", (14, 12, 4, 18), "wood"),  # Cross vertical
            ("rect", (11, 16, 10, 4), "wood"),  # Cross horizontal
        ],
    },
    "head": {
        "human": [
            ("rect", (9, 4, 14, 13), "skin"),  # Face Base
            # Eyes (Detailed)
            ("rect", (10, 9, 3, 2), "white"),  # L Sclera
            ("pixel", (11, 9), "eye_color"),  # L Pupil
            ("rect", (19, 9, 3, 2), "white"),  # R Sclera
            ("pixel", (20, 9), "eye_color"),  # R Pupil
            # Brows
            ("rect", (10, 7, 3, 1), "hair"),
            ("rect", (19, 7, 3, 1), "hair"),
            # Nose
            ("pixel", (15, 11), "outline"),  # Small nose shadow
            # Mouth
            ("rect", (14, 14, 4, 1), "outline"),
            # Ears
            ("rect", (8, 9, 1, 3), "skin"),
            ("rect", (23, 9, 1, 3), "skin"),
        ],
        "elf": [
            ("rect", (10, 4, 12, 13), "skin"),
            ("pixel", (11, 9), "eye_color"),
            ("pixel", (20, 9), "eye_color"),
            ("rect", (14, 14, 4, 1), "outline"),
            # Pointy Ears
            ("pixel", (9, 8), "skin"),
            ("pixel", (8, 7), "skin"),
            ("pixel", (22, 8), "skin"),
            ("pixel", (23, 7), "skin"),
        ],
        "orc": [
            ("rect", (9, 4, 14, 13), "skin"),  # Green skin
            # Angry Eyes
            ("rect", (10, 9, 3, 1), "white"),
            ("pixel", (11, 9), "black"),
            ("rect", (19, 9, 3, 1), "white"),
            ("pixel", (20, 9), "black"),
            ("rect", (10, 8, 4, 1), "black"),  # Brow
            ("rect", (18, 8, 4, 1), "black"),
            # Tusks
            ("rect", (11, 13, 1, 3), "tooth"),
            ("rect", (20, 13, 1, 3), "tooth"),
            ("rect", (13, 13, 6, 1), "black"),  # Mouth between tusks
        ],
        "dwarf": [
            ("rect", (9, 4, 14, 13), "skin"),
            ("rect", (10, 8, 4, 2), "white"),  # Big eyes
            ("pixel", (12, 8), "black"),
            ("rect", (18, 8, 4, 2), "white"),
            ("pixel", (19, 8), "black"),
            # Big Beard
            ("rect", (9, 11, 14, 8), "hair"),
            ("rect", (11, 10, 10, 2), "hair"),  # Mustache
        ],
        "skeleton": [
            ("rect", (10, 5, 12, 11), "skin"),  # Bone color
            # Hollow Eyes
            ("rect", (11, 8, 3, 3), "black"),
            ("rect", (18, 8, 3, 3), "black"),
            ("pixel", (12, 8), "white"),  # Eye glint
            # Nose hole
            ("rect", (15, 11, 2, 2), "black"),
            # Teeth
            ("rect", (11, 14, 10, 2), "skin"),
            ("rect", (11, 14, 1, 2), "outline"),
            ("rect", (13, 14, 1, 2), "outline"),
            ("rect", (15, 14, 1, 2), "outline"),
            ("rect", (17, 14, 1, 2), "outline"),
            ("rect", (19, 14, 1, 2), "outline"),
        ],
        "robot": [
            ("rect", (9, 4, 14, 13), "metal"),
            # Visor
            ("rect", (10, 8, 12, 3), "black"),
            ("rect", (11, 9, 10, 1), "neon_blue"),  # Glowing line
            # Vents
            ("rect", (11, 13, 2, 2), "outline"),
            ("rect", (14, 13, 2, 2), "outline"),
            ("rect", (17, 13, 2, 2), "outline"),
            # Antenna
            ("rect", (9, 2, 1, 4), "metal"),
            ("pixel", (9, 1), "neon_green"),
        ],
        "sage_beard": [
            ("rect", (10, 4, 12, 12), "skin"),
            # Wise Eyes
            ("rect", (11, 8, 2, 1), "black"),
            ("rect", (19, 8, 2, 1), "black"),
            # Long Beard
            ("rect", (11, 11, 10, 10), "white"),
            ("rect", (12, 21, 8, 3), "white"),
            # Eyebrows
            ("rect", (10, 6, 4, 2), "white"),
            ("rect", (18, 6, 4, 2), "white"),
        ],
        "cyborg_eye": [
            ("rect", (9, 4, 14, 13), "skin"),
            ("rect", (19, 9, 3, 2), "white"),  # R Normal Eye
            ("pixel", (20, 9), "black"),
            # Cyborg L Eye
            ("rect", (10, 7, 5, 6), "metal"),
            ("pixel", (12, 9), "neon_pink"),
            # Mouth
            ("rect", (14, 14, 4, 1), "outline"),
        ],
    },
    "hair": {
        "bald": [
            ("pixel", (8, 9), "skin"),  # Just ears
            ("pixel", (23, 9), "skin"),
        ],
        "short": [
            ("rect", (9, 2, 14, 6), "hair"),  # Top
            ("rect", (8, 6, 2, 4), "hair"),  # Sides
            ("rect", (22, 6, 2, 4), "hair"),
            ("rect", (14, 2, 4, 2), "highlight"),  # Shine
        ],
        "long": [
            ("rect", (9, 2, 14, 6), "hair"),
            ("rect", (7, 6, 3, 12), "hair"),  # Long sides
            ("rect", (22, 6, 3, 12), "hair"),
            ("rect", (10, 3, 12, 2), "highlight"),
        ],
        "mohawk": [
            ("rect", (14, 0, 4, 10), "hair"),  # Tall strip
            ("rect", (10, 4, 12, 2), "skin"),  # Shaved head base
        ],
        "ponytail": [
            ("rect", (9, 2, 14, 6), "hair"),
            ("rect", (22, 5, 2, 2), "hair"),  # Tie
            ("rect", (24, 6, 4, 8), "hair"),  # Tail
        ],
        "afro": [
            ("rect", (7, 0, 18, 14), "hair"),  # Big round
            (
                "pixel",
                (8, 1),
                "bg",
            ),  # Rounding corners (negative space logic via no-draw, but here we just draw rect)
            # Actually we can't erase. So we just draw shape.
            ("rect", (9, 2, 4, 4), "highlight"),  # Curls texture
            ("rect", (18, 4, 4, 4), "highlight"),
        ],
        "wizard_hat": [
            ("rect", (6, 6, 20, 2), "shirt"),  # Brim
            ("rect", (9, 2, 14, 4), "shirt"),  # Base
            ("rect", (11, -2, 10, 4), "shirt"),  # Mid
            ("rect", (13, -5, 6, 3), "shirt"),  # Tip
            ("rect", (9, 5, 14, 1), "outline"),  # Band
        ],
        "hood": [
            ("rect", (8, 3, 16, 14), "shirt"),  # Main hood
            ("rect", (10, 5, 12, 10), "black"),  # Face shadow
            # (Face will be drawn over this, so we need hood to be 'hair' layer but visually covering?)
            # Hair draws AFTER head. So this works as a cowl.
        ],
        "helmet": [
            ("rect", (8, 3, 16, 14), "metal"),
            ("rect", (14, 3, 4, 14), "highlight"),  # Crest shine
            ("rect", (10, 8, 12, 4), "black"),  # Visor slit
        ],
        "topknot": [
            ("rect", (9, 3, 14, 5), "hair"),
            ("rect", (14, 0, 4, 3), "hair"),  # Bun
            ("rect", (13, 1, 6, 1), "wood"),  # Stick
        ],
    },
    "body": {
        "shirt": [
            ("rect", (11, 16, 10, 10), "shirt"),
            ("rect", (11, 16, 10, 1), "highlight"),  # Collar
            ("rect", (15, 17, 2, 9), "outline"),  # Placket
            ("pixel", (16, 18), "white"),  # Button
            ("pixel", (16, 20), "white"),
            ("pixel", (16, 22), "white"),
        ],
        "armor": [
            ("rect", (10, 16, 12, 10), "metal"),  # Plate
            ("rect", (9, 16, 3, 4), "metal"),  # L Pauldron
            ("rect", (20, 16, 3, 4), "metal"),  # R Pauldron
            ("rect", (13, 19, 6, 4), "highlight"),  # Chest shine
            ("rect", (12, 24, 8, 2), "leather"),  # Belt
            ("pixel", (15, 24), "gold"),  # Buckle
        ],
        "robe": [
            ("rect", (10, 16, 12, 14), "shirt"),
            ("rect", (13, 16, 6, 14), "white"),  # Inner
            ("rect", (10, 16, 12, 2), "highlight"),  # Collar/Scarf
            ("rect", (10, 24, 12, 2), "outline"),  # Sash
        ],
        "jacket": [
            ("rect", (10, 16, 12, 10), "shirt"),
            ("rect", (14, 16, 4, 10), "white"),  # T-shirt under
            ("rect", (10, 16, 3, 8), "highlight"),  # Lapel L
            ("rect", (19, 16, 3, 8), "highlight"),  # Lapel R
            ("rect", (10, 24, 12, 2), "black"),  # Bottom hem
        ],
        "hanfu_scholar": [
            ("rect", (10, 16, 12, 14), "shirt"),  # Main Robe
            ("rect", (10, 16, 12, 14), "shirt"),  # Cross collar L
            ("rect", (10, 16, 4, 8), "highlight"),  # Collar trim
            ("rect", (11, 22, 10, 4), "black"),  # Wide belt
            ("rect", (14, 22, 4, 4), "jade"),  # Jade ornament
        ],
        "mech_suit": [
            ("rect", (9, 15, 14, 12), "metal"),  # Bulky chest
            ("rect", (13, 18, 6, 6), "neon_blue"),  # Core Reactor
            ("rect", (8, 15, 3, 6), "metal"),  # Shoulder L
            ("rect", (21, 15, 3, 6), "metal"),  # Shoulder R
            ("rect", (10, 25, 12, 2), "highlight"),  # Waist hydraulic
        ],
    },
    # [Fix] Removed 'arms' key as it is procedural and causes UI issues
    "legs": {
        "pants": [
            ("rect", (0, 0, 4, 8), "pants"),  # L Leg
            ("rect", (0, 7, 4, 1), "outline"),  # Cuff
        ],
    },
    "arms": {
        # Procedural arms usually, but we can define props here if needed.
        # This dict key is mostly unused by generator logic which draws rects procedurally.
        # But we will leave it for compatibility.
    },
    "legs": {
        "pants": [
            ("rect", (0, 0, 4, 8), "pants"),  # L Leg
            ("rect", (0, 7, 4, 1), "outline"),  # Cuff
        ],
        "shorts": [
            ("rect", (0, 0, 4, 4), "pants"),  # Shorts
            ("rect", (0, 4, 4, 4), "skin"),  # Bare leg
            ("rect", (0, 7, 4, 1), "boots"),  # Shoes
        ],
        "boots_high": [
            ("rect", (0, 0, 4, 3), "pants"),  # Thigh
            ("rect", (-1, 3, 6, 5), "boots"),  # Big Boot
            ("rect", (-1, 3, 6, 1), "highlight"),  # Boot cuff
        ],
        "skirt": [
            ("rect", (-1, 0, 6, 5), "pants"),  # Skirt body
            ("rect", (-1, 5, 6, 1), "highlight"),  # Hem
            ("rect", (1, 5, 2, 3), "skin"),  # Legs underneath
        ],
        "robot_legs": [
            ("rect", (1, 0, 2, 8), "metal"),  # Piston
            ("rect", (0, 2, 4, 2), "highlight"),  # Joint
            ("rect", (-1, 6, 6, 2), "metal"),  # Foot
        ],
    },
    "held": {
        "sword": [
            ("rect", (0, -8, 2, 16), "metal"),  # Blade
            ("rect", (-2, 8, 6, 1), "gold"),  # Guard
            ("rect", (-1, 9, 4, 3), "wood"),  # Hilt
            ("pixel", (0, 12), "gold"),  # Pommel
            ("rect", (0, -8, 1, 16), "highlight"),  # Blade Shine
        ],
        "staff": [
            ("rect", (0, -12, 2, 26), "wood"),  # Pole
            ("rect", (-2, -14, 6, 4), "gold"),  # Headpiece
            ("rect", (-1, -13, 4, 2), "neon_blue"),  # Gem
        ],
        "axe": [
            ("rect", (0, -6, 2, 18), "wood"),  # Handle
            ("rect", (2, -6, 6, 8), "metal"),  # Blade R
            ("rect", (-4, -6, 6, 8), "metal"),  # Blade L
            ("rect", (-4, -2, 12, 1), "highlight"),  # Edge
        ],
        "shield": [
            ("rect", (-4, -6, 10, 14), "metal"),  # Main plate
            ("rect", (-2, -4, 6, 10), "shirt"),  # Heraldry color
            ("rect", (-4, -6, 10, 14), "outline", "stroke"),  # Rim (simulated)
            ("rect", (-4, -6, 10, 1), "gold"),  # Rim Top
            ("rect", (-4, 7, 10, 1), "gold"),  # Rim Bottom
        ],
        "laser_gun": [
            ("rect", (0, 0, 10, 3), "metal"),  # Barrel
            ("rect", (-2, 2, 4, 5), "black"),  # Grip
            ("rect", (2, -1, 6, 1), "neon_green"),  # Energy rail
            ("rect", (8, 0, 2, 4), "metal"),  # Muzzle
        ],
        "jian": [
            ("rect", (0, -10, 2, 20), "metal"),  # Blade
            ("rect", (-3, 10, 8, 1), "gold"),  # Guard
            ("rect", (-1, 11, 4, 4), "wood"),  # Hilt
            ("rect", (0, 15, 2, 4), "highlight"),  # Tassel
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

# [优化] 重写动画定义，大幅增强动作差异性
ANIMATION_DEFINITIONS = {
    "idle": [
        # 呼吸感：轻微上下浮动，频率慢
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": 1, "leg_f": 0, "arm_f": 0},
        {"bob": 1, "leg_f": 0, "arm_f": 0},
    ],
    "walk": [
        # 走路：稳定的节奏，小幅度摆臂
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": 0},
        {"bob": -1, "leg_f": -1, "arm_f": 1, "offset_x": 0},  # 抬脚
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": 0},
        {"bob": -1, "leg_f": 1, "arm_f": -1, "offset_x": 0},  # 另一只脚
    ],
    "run": [
        # 跑步：大幅度跳跃感(bob -3)，身体前倾(通过offset_x模拟冲刺感)
        # 帧数减少以增加速度感
        {"bob": -1, "leg_f": 1, "arm_f": -1, "offset_x": 2},  # 冲刺前倾
        {"bob": -3, "leg_f": -2, "arm_f": 2, "offset_x": 0},  # 腾空，双腿大迈，手举高
        {"bob": -1, "leg_f": -1, "arm_f": 1, "offset_x": 2},  # 落地前倾
        {"bob": -3, "leg_f": 2, "arm_f": 2, "offset_x": 0},  # 腾空
    ],
    "attack": [
        # 攻击：蓄力(后退) -> 突刺(大幅前进) -> 恢复
        {"bob": 0, "leg_f": -1, "arm_f": 0, "offset_x": -2},  # 蓄力：向后退，手收回
        {"bob": 1, "leg_f": -1, "arm_f": 0, "offset_x": -4},  # 蓄力深蹲
        {
            "bob": -1,
            "leg_f": 2,
            "arm_f": 2,
            "offset_x": 8,
        },  # 突刺：大幅向前，手举起(挥刀)
        {"bob": 0, "leg_f": 1, "arm_f": 2, "offset_x": 4},  # 惯性
        {"bob": 0, "leg_f": 0, "arm_f": 1, "offset_x": 0},  # 恢复站姿
    ],
    "jump": [
        # 跳跃：下蹲蓄力 -> 升空 -> 滞空 -> 落地
        {"bob": 2, "leg_f": 0, "arm_f": 0},  # 蹲
        {"bob": -6, "leg_f": -2, "arm_f": 2},  # 起跳，腿缩起
        {"bob": -8, "leg_f": -2, "arm_f": 2},  # 最高点
        {"bob": -4, "leg_f": -1, "arm_f": 1},  # 下落
        {"bob": 1, "leg_f": 0, "arm_f": 0},  # 缓冲
    ],
    "hurt": [
        # 受击：剧烈震动，向后击退
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -1, "leg_f": -1, "arm_f": 2, "offset_x": -4},  # 被打飞
        {"bob": 1, "leg_f": -1, "arm_f": 2, "offset_x": -6},  # 继续后退
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": -3},  # 落地滑行
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": 0},
    ],
    "cheer": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -2, "leg_f": 0, "arm_f": 2},  # 跳起欢呼
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -2, "leg_f": 0, "arm_f": 2},
    ],
    "die": [
        {"bob": 0, "leg_f": 0, "arm_f": 0},
        {"bob": -2, "leg_f": 0, "arm_f": 2, "offset_x": -2},  # 痛苦
        {"bob": 4, "leg_f": -1, "arm_f": -1, "offset_x": -4},  # 倒下中
        {"bob": 10, "leg_f": -2, "arm_f": 0, "offset_x": -6},  # 躺平 (bob正值是向下)
        {"bob": 10, "leg_f": -2, "arm_f": 0, "offset_x": -6},  # 尸体帧
    ],
}
