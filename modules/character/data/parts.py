# parts.py
# 像素本位 - 纯净Q版 (Pixel-Perfect Chibi)
# Rule 1: Integers ONLY. No floats.
# Rule 2: High Detail via pixel placement.

LAYER_ORDER = [
    "back",
    "legs_back",
    "body",
    "head",
    "eyes",
    "expression",
    "face_wear",
    "hair",
    "legs_front",
    "arms",
    "held",
]

# 核心标签
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
            # 完美的像素圆脸 (Integer coordinates)
            # 核心方块
            ("rect", (10, 6, 12, 10), "skin"),
            # 顶部圆角
            ("rect", (11, 5, 10, 1), "skin"),
            ("rect", (12, 4, 8, 1), "skin"),
            # 脸颊扩充
            ("rect", (9, 7, 1, 8), "skin"),
            ("rect", (22, 7, 1, 8), "skin"),
            # 下巴收缩
            ("rect", (10, 16, 12, 1), "skin"),
            ("rect", (11, 17, 10, 1), "skin"),
            # 下巴阴影
            ("rect", (12, 17, 8, 1), "outline"),
            # 腮红 (2x2 像素块)
            ("rect", (9, 12, 2, 1), "highlight"),
            ("rect", (21, 12, 2, 1), "highlight"),
            # 耳朵
            ("rect", (7, 10, 2, 3), "skin"),
            ("pixel", (8, 11), "outline"),  # 耳蜗
            ("rect", (23, 10, 2, 3), "skin"),
            ("pixel", (23, 11), "outline"),
        ],
    },
    "eyes": {
        "anime_large": [
            # 典型的大眼萌
            # 眼白
            ("rect", (10, 9, 4, 5), "white"),
            ("rect", (18, 9, 4, 5), "white"),
            # 虹膜 (3x4)
            ("rect", (11, 9, 3, 4), "eye_color"),
            ("rect", (19, 9, 3, 4), "eye_color"),
            # 瞳孔 (1x2)
            ("rect", (12, 10, 1, 2), "black"),
            ("rect", (20, 10, 1, 2), "black"),
            # 高光点 (1px)
            ("pixel", (11, 9), "white"),
            ("pixel", (19, 9), "white"),
            # 次高光
            ("pixel", (13, 12), "highlight"),
            ("pixel", (21, 12), "highlight"),
        ],
        "sharp_focus": [
            # 扁平锐利的眼神
            ("rect", (10, 9, 4, 3), "white"),
            ("rect", (18, 9, 4, 3), "white"),
            ("rect", (11, 9, 2, 3), "eye_color"),
            ("rect", (19, 9, 2, 3), "eye_color"),
            ("pixel", (11, 9), "black"),
            ("pixel", (19, 9), "black"),
        ],
        "gentle_droop": [
            # 下垂眼
            ("rect", (10, 10, 4, 4), "white"),
            ("rect", (18, 10, 4, 4), "white"),
            ("rect", (11, 10, 2, 3), "eye_color"),
            ("rect", (19, 10, 2, 3), "eye_color"),
            # 眼皮遮挡
            ("rect", (10, 9, 4, 1), "skin"),
            ("rect", (18, 9, 4, 1), "skin"),
        ],
        "cat_eye": [
            # 猫瞳
            ("rect", (10, 9, 4, 4), "white"),
            ("rect", (18, 9, 4, 4), "white"),
            ("rect", (11, 9, 2, 4), "gold"),
            ("rect", (19, 9, 2, 4), "gold"),
            ("rect", (12, 9, 1, 4), "black"),  # 竖瞳
            ("rect", (20, 9, 1, 4), "black"),
        ],
    },
    "expression": {
        "neutral": [
            ("rect", (14, 16, 4, 1), "outline"),  # 一字嘴
        ],
        "smile": [
            # 眉毛
            ("pixel", (10, 7), "hair"),
            ("pixel", (11, 7), "hair"),
            ("pixel", (12, 8), "hair"),
            ("pixel", (21, 7), "hair"),
            ("pixel", (20, 7), "hair"),
            ("pixel", (19, 8), "hair"),
            # 笑嘴
            ("pixel", (13, 15), "outline"),
            ("rect", (14, 16, 4, 1), "outline"),
            ("pixel", (18, 15), "outline"),
        ],
        "pout": [
            # 生气眉
            ("pixel", (10, 8), "hair"),
            ("pixel", (11, 9), "hair"),
            ("pixel", (12, 9), "hair"),
            ("pixel", (21, 8), "hair"),
            ("pixel", (20, 9), "hair"),
            ("pixel", (19, 9), "hair"),
            # 撇嘴
            ("pixel", (15, 16), "outline"),
            ("pixel", (16, 16), "outline"),
        ],
        "surprised": [
            # 高眉
            ("rect", (10, 6, 3, 1), "hair"),
            ("rect", (19, 6, 3, 1), "hair"),
            # O嘴
            ("rect", (14, 15, 4, 3), "outline"),
            ("rect", (15, 16, 2, 1), "black"),
        ],
    },
    "hair": {
        "short_hero": [
            # 勇者短发
            ("rect", (8, 2, 16, 6), "hair"),  # 主体
            ("rect", (10, 3, 12, 1), "highlight"),  # 光环
            # 刺猬头
            ("pixel", (12, 1), "hair"),
            ("pixel", (16, 0), "hair"),
            ("pixel", (20, 1), "hair"),
            # 刘海 (块状)
            ("rect", (9, 6, 2, 3), "hair"),
            ("rect", (14, 6, 4, 2), "hair"),  # 中间刘海
            ("rect", (21, 6, 2, 3), "hair"),
            # 鬓角
            ("rect", (7, 8, 2, 4), "hair"),
            ("rect", (23, 8, 2, 4), "hair"),
        ],
        "long_straight": [
            # 姬发式
            ("rect", (9, 2, 14, 6), "hair"),  # 顶
            ("rect", (10, 3, 12, 1), "highlight"),
            # 齐刘海
            ("rect", (10, 6, 12, 2), "hair"),
            # 侧发
            ("rect", (7, 6, 3, 12), "hair"),
            ("rect", (22, 6, 3, 12), "hair"),
            # 后发
            ("rect", (10, 8, 12, 8), "hair"),
        ],
        "twin_tails": [
            # 双马尾
            ("rect", (9, 2, 14, 6), "hair"),
            ("rect", (10, 3, 12, 1), "highlight"),
            # 左右马尾 (大块面)
            ("rect", (3, 4, 5, 12), "hair"),
            ("rect", (24, 4, 5, 12), "hair"),
            # 发圈
            ("rect", (5, 3, 3, 2), "white"),
            ("rect", (24, 3, 3, 2), "white"),
        ],
        "messy_shag": [
            # 凌乱发型
            ("rect", (8, 3, 16, 6), "hair"),
            ("rect", (12, 1, 3, 2), "hair"),  # 呆毛
            ("pixel", (7, 7), "hair"),
            ("pixel", (24, 7), "hair"),
            ("rect", (9, 6, 3, 4), "hair"),  # 长刘海
            ("rect", (20, 6, 3, 3), "hair"),
        ],
        "bob": [
            # 波波头
            ("rect", (8, 2, 16, 10), "hair"),
            ("rect", (9, 3, 14, 1), "highlight"),
            # 内扣
            ("rect", (9, 12, 2, 1), "hair"),
            ("rect", (21, 12, 2, 1), "hair"),
            # 脸部镂空
            ("rect", (10, 7, 12, 5), "skin"),
        ],
    },
    "body": {
        "adventurer_coat": [
            ("rect", (10, 16, 12, 9), "shirt"),  # 外套
            ("rect", (14, 16, 4, 9), "white"),  # 内衬
            ("rect", (10, 23, 12, 2), "leather"),  # 腰带
            ("pixel", (15, 23), "gold"),  # 扣子
            ("rect", (10, 16, 3, 7), "highlight"),  # 翻领 L
            ("rect", (19, 16, 3, 7), "highlight"),  # 翻领 R
        ],
        "school_uniform": [
            ("rect", (10, 16, 12, 8), "black"),  # 制服黑
            ("rect", (14, 16, 4, 4), "white"),  # 衬衫领
            ("rect", (15, 18, 2, 4), "red"),  # 领带
            ("rect", (10, 24, 12, 1), "outline"),  # 下摆
            ("pixel", (11, 19), "gold"),  # 校徽
        ],
        "maid_dress": [
            ("rect", (10, 16, 12, 8), "black"),
            ("rect", (12, 16, 8, 8), "white"),  # 围裙
            ("rect", (12, 16, 8, 2), "white"),  # 领口花边
            ("rect", (14, 20, 4, 4), "white"),  # 围裙兜
            ("rect", (7, 16, 3, 3), "white"),  # 泡泡袖 L
            ("rect", (22, 16, 3, 3), "white"),  # 泡泡袖 R
        ],
        "cyber_vest": [
            ("rect", (10, 16, 12, 8), "black"),
            ("rect", (11, 18, 10, 1), "neon_blue"),  # 发光条
            ("rect", (11, 21, 10, 1), "neon_blue"),
            ("rect", (8, 16, 2, 4), "metal"),  # 肩甲
            ("rect", (22, 16, 2, 4), "metal"),
        ],
        "wizard_robe": [
            ("rect", (10, 16, 12, 14), "shirt"),  # 长袍
            ("rect", (13, 16, 6, 14), "highlight"),  # 中间条纹
            ("rect", (10, 16, 12, 3), "gold"),  # 金领
        ],
    },
    "legs": {
        "pants_boots": [
            ("rect", (1, 0, 4, 6), "pants"),
            ("rect", (0, 6, 5, 2), "boots"),
            ("rect", (0, 8, 5, 1), "black"),  # 鞋底
        ],
        "skirt_socks": [
            ("rect", (-1, 0, 7, 4), "pants"),  # 裙子 (pants color)
            ("rect", (1, 4, 3, 3), "skin"),  # 腿
            ("rect", (1, 7, 3, 2), "white"),  # 堆堆袜
            ("rect", (1, 9, 3, 1), "boots"),  # 鞋
        ],
        "boots_shorts": [
            ("rect", (1, 0, 4, 3), "pants"),  # 短裤
            ("rect", (1, 3, 3, 3), "skin"),
            ("rect", (0, 6, 5, 3), "boots"),  # 大靴子
        ],
        "armored_legs": [
            ("rect", (1, 0, 4, 5), "metal"),
            ("rect", (2, 2, 2, 2), "highlight"),  # 膝盖反光
            ("rect", (0, 5, 5, 4), "metal"),  # 铁靴
        ],
    },
    "held": {
        "sword_iron": [
            ("rect", (0, -10, 3, 18), "metal"),  # 宽剑刃
            ("rect", (1, -10, 1, 18), "highlight"),  # 血槽
            ("rect", (-2, 8, 7, 2), "gold"),  # 护手
            ("rect", (-1, 10, 3, 3), "wood"),  # 剑柄
        ],
        "staff_magic": [
            ("rect", (0, -12, 2, 26), "wood"),
            ("rect", (-2, -14, 6, 6), "gold"),  # 法杖头
            ("rect", (-1, -13, 4, 4), "neon_blue"),  # 宝石
        ],
        "shield_round": [
            ("rect", (-4, -4, 12, 12), "metal"),
            ("rect", (-3, -3, 10, 10), "shirt"),  # 涂装
            ("rect", (-4, -4, 12, 12), "outline", "stroke"),  # 边框
        ],
        "book_spell": [
            ("rect", (-2, -4, 10, 12), "leather"),  # 书皮
            ("rect", (0, -2, 6, 8), "white"),  # 纸张
            ("pixel", (3, 2), "neon_blue"),  # 符文
        ],
        "tea_cup": [
            ("rect", (0, 0, 6, 8), "white"),  # 杯子
            ("pixel", (2, 3), "outline"),  # 标志
            ("rect", (2, -3, 1, 3), "black"),  # 吸管
        ],
        "none": [],
    },
    "back": {
        "none": [],
        "cape_hero": [
            ("rect", (6, 16, 20, 14), "shirt"),
            ("rect", (10, 16, 12, 14), "highlight"),  # 中间亮
        ],
        "wings_angel": [
            ("rect", (2, 12, 8, 6), "white"),
            ("rect", (22, 12, 8, 6), "white"),
            ("pixel", (4, 14), "highlight"),
        ],
        "backpack_travel": [
            ("rect", (8, 14, 16, 12), "wood"),  # 棕色包
            ("rect", (10, 18, 12, 6), "highlight"),  # 前袋
            ("rect", (15, 14, 2, 12), "outline"),  # 拉链
        ],
    },
    "face_wear": {
        "none": [],
        "glasses_red": [
            ("rect", (10, 10, 4, 2), "red", "stroke"),
            ("rect", (18, 10, 4, 2), "red", "stroke"),
            ("rect", (14, 11, 4, 1), "red"),
        ],
        "bandage": [
            ("rect", (10, 12, 3, 2), "white"),
            ("pixel", (11, 13), "blood"),
        ],
        "cat_ears_headset": [
            ("rect", (9, 3, 14, 1), "black"),  # 头带
            ("polygon", [(7, 3), (5, 0), (9, 2)], "black"),  # 耳朵L
            ("polygon", [(23, 3), (25, 0), (21, 2)], "black"),  # 耳朵R
            ("rect", (7, 8, 2, 6), "neon_blue"),  # 耳机
            ("rect", (23, 8, 2, 6), "neon_blue"),
        ],
    },
}
