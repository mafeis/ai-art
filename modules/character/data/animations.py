# animations.py
# 动画帧数据和元数据

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
    "attack": [
        # 攻击：蓄力(后退) -> 突刺(大幅前进) -> 恢复
        # Frame 1: Wind up (Back -45 deg)
        {
            "bob": 1,
            "leg_f": -1,
            "arm_f": -1,
            "offset_x": -2,
            "rot": -45,
        },
        # Frame 2: Ready (Back more -90 deg)
        {
            "bob": 2,
            "leg_f": -1,
            "arm_f": 1,
            "offset_x": -4,
            "rot": -90,
        },
        # Frame 3: SLASH! (Forward 45 deg) + VFX
        {
            "bob": -1,
            "leg_f": 2,
            "arm_f": 3,
            "offset_x": 8,
            "rot": 45,
            "vfx": "slash",
        },
        # Frame 4: Follow through (Forward 90 deg) + VFX Fade
        {
            "bob": 0,
            "leg_f": 1,
            "arm_f": 4,
            "offset_x": 4,
            "rot": 100,
            # "vfx": "slash", # Optional: keep showing slash or let it fade
        },
        # Frame 5: Recovery
        {"bob": 0, "leg_f": 0, "arm_f": 1, "offset_x": 0, "rot": 0},
    ],
    "attack_shoot": [
        # Shoot: Recoil -> Recovery
        # Frame 1: Aim
        {"bob": 0, "leg_f": 0, "arm_f": 3, "offset_x": 0, "rot": 0},
        # Frame 2: Shoot (Recoil back) + Muzzle Flash
        {
            "bob": 0,
            "leg_f": 0,
            "arm_f": 3,
            "offset_x": -2,
            "rot": 10,
            "vfx": "shoot_flash",
        },
        # Frame 3: Recovery
        {"bob": 0, "leg_f": 0, "arm_f": 3, "offset_x": -1, "rot": 5},
        # Frame 4: Steady
        {"bob": 0, "leg_f": 0, "arm_f": 3, "offset_x": 0, "rot": 0},
    ],
    "attack_cast": [
        # Cast: Raise staff -> Glow -> Lower
        # Frame 1: Raise Staff
        {"bob": 0, "leg_f": 0, "arm_f": 4, "offset_x": 0, "rot": -10},
        # Frame 2: Channeling (Higher)
        {
            "bob": -1,
            "leg_f": 0,
            "arm_f": 4,
            "offset_x": 0,
            "rot": -20,
            "vfx": "magic_circle",
        },
        # Frame 3: Release (Thrust forward slightly)
        {
            "bob": 0,
            "leg_f": 1,
            "arm_f": 3,
            "offset_x": 2,
            "rot": 10,
            "vfx": "magic_beam",
        },
        # Frame 4: Recovery
        {"bob": 0, "leg_f": 0, "arm_f": 4, "offset_x": 0, "rot": 0},
    ],
    "attack_heavy": [
        # Heavy Swing (Axe): Slower windup, bigger follow through
        # Frame 1: Wind up
        {"bob": 1, "leg_f": -1, "arm_f": -1, "offset_x": -2, "rot": -45},
        # Frame 2: Hold
        {"bob": 2, "leg_f": -1, "arm_f": 1, "offset_x": -4, "rot": -100},
        # Frame 3: Smash!
        {"bob": -2, "leg_f": 2, "arm_f": 3, "offset_x": 8, "rot": 60, "vfx": "impact"},
        # Frame 4: Heavy Landing
        {"bob": 1, "leg_f": 1, "arm_f": 4, "offset_x": 6, "rot": 110},
        # Frame 5: Recovery
        {"bob": 0, "leg_f": 0, "arm_f": 1, "offset_x": 2, "rot": 45},
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
        {"bob": -1, "leg_f": -1, "arm_f": 2, "offset_x": -8},  # 被打飞 (加大幅度)
        {"bob": 1, "leg_f": -1, "arm_f": 2, "offset_x": -12},  # 继续后退 (加大幅度)
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": -6},  # 落地滑行
        {"bob": 0, "leg_f": 0, "arm_f": 0, "offset_x": 0},
    ],
    "die": [
        {"bob": 0, "leg_f": 0, "arm_f": 0, "body_rot": 0},
        {
            "bob": 0,
            "leg_f": 0,
            "arm_f": 2,
            "offset_x": -2,
            "body_rot": -20,
        },  # Stumble back
        {
            "bob": 0,
            "leg_f": -1,
            "arm_f": -1,
            "offset_x": -4,
            "body_rot": -45,
        },  # Falling (Pivot handles height)
        {"bob": 0, "leg_f": -1, "arm_f": 0, "offset_x": -4, "body_rot": -90},  # Flat
        {"bob": 0, "leg_f": -1, "arm_f": 0, "offset_x": -4, "body_rot": -90},  # Dead
    ],
}

# Weapon Metadata for Animation Selection
# Pivot is in 64x64 coordinate space relative to weapon origin
WEAPON_METADATA = {
    # Melee
    "sword_iron": {"type": "slash", "pivot": (1, 23)},  # Hilt center
    "katana": {"type": "slash", "pivot": (1, 14)},
    "buster_sword": {"type": "heavy", "pivot": (1.5, 14.5)},
    # Magic
    "staff_magic": {"type": "cast", "pivot": (0, 0)},  # Center grip
    "star_wand": {"type": "cast", "pivot": (0, 0)},
    "book_spell": {"type": "cast", "pivot": (2, 4)},
    # Ranged
    "plasma_rifle": {"type": "shoot", "pivot": (0, 6)},
    # Misc
    "shield_round": {"type": "heavy", "pivot": (0, 0)},
    "tea_cup": {"type": "cast", "pivot": (0, 4)},  # Hold cup
    "none": {"type": "slash", "pivot": (0, 0)},
}
