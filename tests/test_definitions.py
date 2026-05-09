import pytest
import sys
sys.path.insert(0, 'D:/mafei/vscode-workspace/pc/ai-art')
from modules.character import definitions as defs


def test_layer_order_exists():
    assert len(defs.LAYER_ORDER) > 0
    assert "body" in defs.LAYER_ORDER
    assert "head" in defs.LAYER_ORDER


def test_part_definitions_has_required_parts():
    required = ["head", "body", "legs", "held"]
    for part in required:
        assert part in defs.PART_DEFINITIONS
        assert len(defs.PART_DEFINITIONS[part]) > 0


def test_part_definitions_structure():
    for part, styles in defs.PART_DEFINITIONS.items():
        for style_name, instructions in styles.items():
            assert isinstance(instructions, list)
            for cmd in instructions:
                assert cmd[0] in ["rect", "pixel", "polygon", "ellipse", "circle"]


def test_default_palette_complete():
    required_colors = ["skin", "hair", "shirt", "pants", "boots", "outline", "eye_color"]
    for color in required_colors:
        assert color in defs.DEFAULT_PALETTE


def test_animation_definitions_valid():
    for action, frames in defs.ANIMATION_DEFINITIONS.items():
        assert len(frames) > 0
        for frame in frames:
            assert isinstance(frame, dict)
            assert "bob" in frame
            assert "leg_f" in frame
            assert "arm_f" in frame


def test_weapon_metadata_has_pivot():
    for weapon, meta in defs.WEAPON_METADATA.items():
        assert "type" in meta
        assert "pivot" in meta
        assert isinstance(meta["pivot"], tuple)
        assert len(meta["pivot"]) == 2


def test_part_tags_match_definitions():
    """Every style in PART_DEFINITIONS should have a tag entry"""
    for part, styles in defs.PART_DEFINITIONS.items():
        if part in defs.PART_TAGS:
            for style_name in styles.keys():
                assert style_name in defs.PART_TAGS[part], f"Missing tag for {part}.{style_name}"


def test_theme_mappings_not_empty():
    """THEME_MAPPINGS should have non-empty arrays"""
    for theme, styles in defs.THEME_MAPPINGS.items():
        assert len(styles) > 0, f"Theme {theme} has empty mappings"


def test_theme_palettes_keys_match_themes():
    """THEME_PALETTES keys should match THEME_MAPPINGS keys"""
    assert set(defs.THEME_MAPPINGS.keys()) == set(defs.THEME_PALETTES.keys())