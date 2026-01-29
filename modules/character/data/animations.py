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

# Weapon Metadata for Animation Selection
WEAPON_METADATA = {
    "sword": {"type": "slash", "pivot": (0, 10)},
    "blade": {"type": "slash", "pivot": (0, 10)},
    "katana": {"type": "slash", "pivot": (0, 10)},
    "axe": {"type": "heavy", "pivot": (0, 10)},
    "staff": {"type": "cast", "pivot": (0, 0)},
    "wand": {"type": "cast", "pivot": (0, 0)},
    "spear": {"type": "slash", "pivot": (0, 0)},  # Or thrust
    "jian": {"type": "slash", "pivot": (0, 10)},
    "fan": {"type": "cast", "pivot": (0, 10)},
    "gourd": {"type": "cast", "pivot": (0, 5)},
    "laser_gun": {"type": "shoot", "pivot": (-2, 4)},
    "katana_laser": {"type": "slash", "pivot": (0, 10)},
    "wrench": {"type": "heavy", "pivot": (0, 10)},
    "chainsaw": {"type": "heavy", "pivot": (-4, 4)},
    "butcher_knife": {"type": "slash", "pivot": (0, 8)},
    "shield": {"type": "heavy", "pivot": (0, 0)},  # Bash
    "none": {"type": "slash", "pivot": (0, 0)},  # Punch
}
