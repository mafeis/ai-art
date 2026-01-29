# character_definitions.py (Facade)
# 这个文件保留作为统一入口，防止破坏旧代码的 import

from modules.character.data.parts import LAYER_ORDER, PART_TAGS, PART_DEFINITIONS
from modules.character.data.palettes import (
    THEME_PALETTES,
    DEFAULT_PALETTE,
    THEME_RENDER_MODES,
    THEME_MAPPINGS,
)
from modules.character.data.animations import ANIMATION_DEFINITIONS, WEAPON_METADATA
