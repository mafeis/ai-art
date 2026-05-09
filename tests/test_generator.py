import pytest
import sys
sys.path.insert(0, 'D:/mafei/vscode-workspace/pc/ai-art')
from modules.character.generator import CharacterComposer, create_character_gif, create_character_spritesheet
from modules.character import definitions as defs


@pytest.fixture
def sample_config():
    return {
        "parts": {
            "head": "base",
            "hair": "short_hero",
            "eyes": "anime_large",
            "body": "adventurer_coat",
            "legs": "pants_boots",
            "held": "sword_iron",
            "back": "none",
            "expression": "neutral",
            "face_wear": "none",
        },
        "palette": dict(defs.DEFAULT_PALETTE),
    }


def test_composer_init_with_dict(sample_config):
    composer = CharacterComposer(sample_config)
    assert composer.width == 128
    assert composer.height == 128


def test_composer_get_color(sample_config):
    composer = CharacterComposer(sample_config)
    skin = composer.get_color("skin")
    assert isinstance(skin, tuple)
    assert len(skin) >= 3


def test_composer_adjust_color(sample_config):
    composer = CharacterComposer(sample_config)
    color = (100, 100, 100)
    adjusted = composer.adjust_color(color, 1.5)
    assert adjusted[0] >= color[0]


def test_calc_hand_position_helper(sample_config):
    """Test the extracted _calc_hand_position helper method"""
    composer = CharacterComposer(sample_config)
    # Basic call
    x, y = composer._calc_hand_position(40, 34, 0, 0, 1.0)
    assert isinstance(x, int)
    assert isinstance(y, int)
    # With arm_frame variations
    for af in [-1, 0, 1, 2, 3, 4]:
        x, y = composer._calc_hand_position(40, 34, af, 0, 1.0)
        assert isinstance(x, int)


def test_create_character_gif_basic(sample_config):
    buf = create_character_gif(
        config_source=sample_config,
        action="idle",
        density=1.0,
        output_size=64,
        render_mode="retro"
    )
    assert buf.getbuffer().nbytes > 0


def test_create_character_gif_all_actions(sample_config):
    for action in defs.ANIMATION_DEFINITIONS.keys():
        buf = create_character_gif(
            config_source=sample_config,
            action=action,
            density=1.0,
            output_size=64,
            render_mode="retro"
        )
        assert buf.getbuffer().nbytes > 0, f"Failed for action: {action}"


def test_create_character_spritesheet_basic(sample_config):
    img = create_character_spritesheet(
        filename=None,
        config_source=sample_config,
        action="walk",
        density=1.0,
        output_size=64,
        render_mode="retro"
    )
    assert img.width > 0
    assert img.height > 0


def test_create_character_spritesheet_all_render_modes(sample_config):
    modes = ["retro", "hd", "sketch", "neon", "ink", "hibit", "premium"]
    for mode in modes:
        img = create_character_spritesheet(
            filename=None,
            config_source=sample_config,
            action="idle",
            density=1.0,
            output_size=64,
            render_mode=mode
        )
        assert img.width > 0, f"Failed for mode: {mode}"


def test_attack_routes_to_weapon_type(sample_config):
    """Attack action should route to weapon-specific animation"""
    for weapon in ["sword_iron", "staff_magic", "book_spell", "shield_round", "tea_cup"]:
        config = dict(sample_config)
        config["parts"]["held"] = weapon
        buf = create_character_gif(
            config_source=config,
            action="attack",
            density=1.0,
            output_size=64,
            render_mode="retro"
        )
        assert buf.getbuffer().nbytes > 0, f"Failed for weapon: {weapon}"