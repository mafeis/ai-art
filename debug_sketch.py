from PIL import Image
import post_effects


def test_sketch():
    print("Testing sketch effect...")
    # Create a dummy RGBA image
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))

    try:
        res = post_effects.apply_sketch_texture(img)
        print("Sketch effect success")
        res.save("test_sketch_debug.png")
    except Exception as e:
        print(f"Sketch effect failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_sketch()
