import pytest
import sys
sys.path.insert(0, 'D:/mafei/vscode-workspace/pc/ai-art')
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_options_route(client):
    resp = client.get('/options')
    assert resp.status_code == 200
    data = resp.get_json()
    assert "head" in data
    assert "body" in data
    assert len(data["animations"]) > 0


def test_config_route(client):
    resp = client.get('/config')
    assert resp.status_code == 200
    data = resp.get_json()
    assert "parts" in data
    assert "palette" in data


def test_randomize_route(client):
    resp = client.get('/randomize')
    assert resp.status_code == 200
    data = resp.get_json()
    assert "parts" in data
    assert "palette" in data
    assert "render_mode" in data


def test_randomize_with_theme(client):
    for theme in ["fantasy", "scifi", "modern", "cute", "action"]:
        resp = client.get(f'/randomize?theme={theme}')
        assert resp.status_code == 200


def test_randomize_invalid_theme_returns_available(client):
    """Invalid theme should still work (fallback to 'all')"""
    resp = client.get('/randomize?theme=invalid_theme_xyz')
    assert resp.status_code == 200


def test_generate_endpoint(client):
    payload = {
        "parts": {
            "head": "base",
            "hair": "short_hero",
            "eyes": "anime_large",
            "body": "adventurer_coat",
            "legs": "pants_boots",
            "held": "sword_iron",
            "back": "none",
            "expression": "neutral",
            "face_wear": "none"
        },
        "palette": {},
        "action": "idle",
        "density": 1.0,
        "output_size": 64,
        "render_mode": "retro"
    }
    resp = client.post('/generate', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "results" in data
    assert "stats" in data


def test_generate_batch(client):
    payload = {
        "parts": {
            "head": "base",
            "hair": "short_hero",
            "eyes": "anime_large",
            "body": "adventurer_coat",
            "legs": "pants_boots",
            "held": "sword_iron",
            "back": "none",
            "expression": "neutral",
            "face_wear": "none"
        },
        "palette": {},
        "actions": ["idle", "walk"],
        "density": 1.0,
        "output_size": 64,
        "render_mode": "retro"
    }
    resp = client.post('/generate', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["results"]) == 2


def test_generate_no_config(client):
    resp = client.post('/generate')
    # Without Content-Type: application/json, Flask raises 415 which the
    # exception handler converts to 500
    assert resp.status_code == 500


def test_generate_invalid_part(client):
    """Invalid part style should return 400"""
    payload = {
        "parts": {
            "head": "nonexistent_style_xyz",
        },
        "palette": {},
        "action": "idle",
        "density": 1.0,
        "output_size": 64,
        "render_mode": "retro"
    }
    resp = client.post('/generate', json=payload)
    assert resp.status_code == 400


def test_generate_invalid_render_mode(client):
    """Invalid render_mode should return 400"""
    payload = {
        "parts": {
            "head": "base",
            "hair": "short_hero",
            "eyes": "anime_large",
            "body": "adventurer_coat",
            "legs": "pants_boots",
            "held": "sword_iron",
            "back": "none",
            "expression": "neutral",
            "face_wear": "none"
        },
        "palette": {},
        "action": "idle",
        "density": 1.0,
        "output_size": 64,
        "render_mode": "invalid_mode_xyz"
    }
    resp = client.post('/generate', json=payload)
    assert resp.status_code == 400