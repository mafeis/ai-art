"""
测试 Cairo 渲染器 - 生成三种艺术风格的角色
"""

from cairo_renderer import (
    DeadCellsRenderer,
    HollowKnightRenderer,
    MonumentValleyRenderer,
)


def test_dead_cells_style():
    """测试死亡细胞风格"""
    print("生成 Dead Cells 风格角色...")
    renderer = DeadCellsRenderer(256, 256)

    # 清空背景（透明）
    renderer.clear(0, 0, 0, 0)

    # 绘制角色
    # 头部
    renderer.draw_character_head(128, 60, 35, (255, 210, 170))

    # 身体
    renderer.draw_character_body(128, 95, 45, 70, (80, 120, 200))

    # 手臂（胶囊形状）
    renderer.draw_capsule(
        95, 110, 70, 140, 10, (255, 210, 170), use_gradient=True
    )  # 左臂
    renderer.draw_capsule(
        160, 110, 185, 140, 10, (255, 210, 170), use_gradient=True
    )  # 右臂

    # 腿部
    renderer.draw_capsule(
        110, 165, 105, 220, 12, (60, 80, 120), use_gradient=True
    )  # 左腿
    renderer.draw_capsule(
        145, 165, 150, 220, 12, (60, 80, 120), use_gradient=True
    )  # 右腿

    # 保存
    img = renderer.to_pil_image()
    img.save("test_dead_cells.png")
    print("[OK] Saved: test_dead_cells.png")


def test_hollow_knight_style():
    """测试空洞骑士风格"""
    print("生成 Hollow Knight 风格角色...")
    renderer = HollowKnightRenderer(256, 256)

    # 清空背景（透明）
    renderer.clear(0, 0, 0, 0)

    # 绘制角色
    # 头部（标志性的大黑眼）
    renderer.draw_character_head(128, 70, 40, (240, 240, 245))

    # 身体（白色斗篷）
    renderer.draw_character_body(128, 110, 50, 75, (235, 235, 240))

    # 手臂
    renderer.draw_capsule(95, 125, 75, 155, 8, (230, 230, 235))
    renderer.draw_capsule(160, 125, 180, 155, 8, (230, 230, 235))

    # 腿部
    renderer.draw_capsule(110, 185, 108, 230, 10, (225, 225, 230))
    renderer.draw_capsule(145, 185, 147, 230, 10, (225, 225, 230))

    # 保存
    img = renderer.to_pil_image()
    img.save("test_hollow_knight.png")
    print("[OK] Saved: test_hollow_knight.png")


def test_monument_valley_style():
    """测试纪念碑谷风格"""
    print("生成 Monument Valley 风格角色...")
    renderer = MonumentValleyRenderer(256, 256)

    # 清空背景（浅色）
    renderer.clear(0.95, 0.93, 0.9, 1.0)

    # 绘制角色（极简几何）
    # 头部
    renderer.draw_character_head(128, 65, 32, (230, 180, 140))

    # 身体
    renderer.draw_character_body(128, 100, 40, 65, (200, 120, 100))

    # 手臂（简单矩形）
    renderer.ctx.set_source_rgb(0.85, 0.65, 0.5)
    renderer.ctx.rectangle(88, 110, 8, 40)
    renderer.ctx.fill()
    renderer.ctx.rectangle(159, 110, 8, 40)
    renderer.ctx.fill()

    # 腿部
    renderer.ctx.set_source_rgb(0.7, 0.4, 0.35)
    renderer.ctx.rectangle(108, 165, 12, 55)
    renderer.ctx.fill()
    renderer.ctx.rectangle(135, 165, 12, 55)
    renderer.ctx.fill()

    # 保存
    img = renderer.to_pil_image()
    img.save("test_monument_valley.png")
    print("[OK] Saved: test_monument_valley.png")


if __name__ == "__main__":
    print("=" * 50)
    print("Cairo 艺术渲染器测试")
    print("=" * 50)

    test_dead_cells_style()
    test_hollow_knight_style()
    test_monument_valley_style()

    print("\n" + "=" * 50)
    print("All done! Check generated images:")
    print("  - test_dead_cells.png (Smooth gradients)")
    print("  - test_hollow_knight.png (Thick black outlines)")
    print("  - test_monument_valley.png (Geometric flat)")
    print("=" * 50)
