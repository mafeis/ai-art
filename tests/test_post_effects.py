import pytest
import sys
sys.path.insert(0, 'D:/mafei/vscode-workspace/pc/ai-art')
from PIL import Image
from modules.rendering import post_effects


@pytest.fixture
def sample_image():
    return Image.new("RGBA", (64, 64), (255, 100, 100, 255))


def test_all_effects_return_rgba(sample_image):
    modes = ["ink", "neon", "sketch", "retro", "hd", "hibit", "premium"]
    for mode in modes:
        func = post_effects.get_post_effect_for_mode(mode)
        result = func(sample_image)
        assert result.mode == "RGBA", f"Failed for mode: {mode}"
        assert result.size == sample_image.size


def test_alpha_channel_preserved(sample_image):
    for mode in ["ink", "neon", "sketch", "retro", "hd", "hibit", "premium"]:
        func = post_effects.get_post_effect_for_mode(mode)
        result = func(sample_image)
        r, g, b, a = result.split()
        assert a.getpixel((0, 0)) == 255


def test_chromatic_aberration():
    img = Image.new("RGB", (32, 32), (255, 0, 0))
    result = post_effects.apply_chromatic_aberration(img, offset=2)
    assert result.size == img.size
    assert result.mode == "RGB"


def test_get_post_effect_unknown_mode():
    """Unknown mode should return identity (pass-through)"""
    func = post_effects.get_post_effect_for_mode("unknown_mode_xyz")
    img = Image.new("RGBA", (32, 32), (100, 150, 200, 255))
    result = func(img)
    assert result.size == img.size