# Legacy & Experimental Modules (历史遗留与实验性模块)

此目录包含了一些实验性质的、早期的、或者未集成到主 Web 应用中的功能模块。
虽然它们不属于核心生产链路，但保留了许多有趣的想法和原型代码。

## 📂 文件列表与说明

### 🎨 矢量渲染实验 (Vector Rendering Experiments)

这些文件尝试使用 `pycairo` 库生成非像素风格（如手绘、矢量、平滑渐变）的游戏素材。

*   **`cairo_renderer.py`**
    *   **定义**: 矢量渲染器的基类及多种风格实现。
    *   **风格**:
        *   `DeadCellsRenderer`: 模拟《死亡细胞》的平滑渐变风格。
        *   `HollowKnightRenderer`: 模拟《空洞骑士》的粗描边手绘风格。
        *   `MonumentValleyRenderer`: 模拟《纪念碑谷》的极简几何风格。
    *   **作用**: 提供底层绘图 API。

*   **`game_character_gen.py`**
    *   **定义**: 高级矢量角色生成器。
    *   **作用**: 尝试使用程序化笔触（Tapered Brush）和简单的骨骼系统来生成更自然的动态角色。

*   **`test_cairo_renderer.py`**
    *   **定义**: 测试脚本。
    *   **作用**: 运行此脚本可生成上述三种风格的演示图片 (`.png`)。

### 🤖 AI 生成实验 (AI Generation Experiments)

这些文件尝试将程序化生成的配置与 Stable Diffusion 结合，生成高质量概念图。

*   **`ai_prompt.py`**
    *   **定义**: 提示词生成器。
    *   **作用**: 将像素角色的部件（如 "robot head", "laser gun"）翻译成详细的英文 Prompt（如 "mecha head, futuristic helmet, highly detailed..."）。

*   **`run_sd.py`**
    *   **定义**: Stable Diffusion 运行脚本。
    *   **作用**: 调用本地 AI 模型，根据 `ai_prompt.py` 生成的提示词生成高分辨率插画。需要 NVIDIA 显卡。

### 🧩 早期原型 (Early Prototypes)

*   **`gen_monster.py`**
    *   **定义**: 怪物生成器。
    *   **作用**: 独立脚本，生成史莱姆等简单怪物的像素动画。

*   **`gen_scene.py`**
    *   **定义**: 场景生成器。
    *   **作用**: 独立脚本，程序化生成 16-bit 风格的背景图（天空、云朵、草地）。

## ⚠️ 注意事项

1.  **依赖**: `cairo` 相关文件需要安装 `pycairo`。`run_sd.py` 需要安装 `torch` 和 `diffusers`。
2.  **状态**: 这些代码可能不再维护，仅供参考。
