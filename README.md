# Pixel Forge (水浒像素工坊)

Pixel Forge 是一个强大的程序化像素角色生成器，最初以水浒传（Shuihu）角色风格为基础，现已扩展支持多种艺术风格（仙侠、赛博朋克、蒸汽朋克、恐怖等）。

项目包含一个基于 Flask 的 Web 界面，支持实时预览、多动作生成、图层定制以及多种渲染风格（标准像素、高清矢量、手绘草图、霓虹特效等）。

## ✨ 主要功能

*   **多风格支持**: 内置 仙侠 (Xianxia)、科技 (Tech)、赛博朋克 (Cyberpunk)、魔幻 (Western) 等多种主题配置。
*   **程序化生成**: 基于部件（头、发型、躯干、腿、手持物、背饰）的随机组合。
*   **实时渲染**: 支持调整像素密度（16-bit, 32-bit, 64-bit HD）。
*   **动作系统**: 包含 Idle, Walk, Run, Attack, Jump, Die 等多种动画序列。
*   **艺术滤镜**:
    *   **Retro**: 经典 CRT 像素风格。
    *   **Sketch**: 模拟手绘/草图线条效果。
    *   **Neon**: 赛博朋克发光特效。
    *   **Ink**: 水墨晕染风格。
    *   **HD**: 矢量化平滑处理。
*   **Web 工作台**: 现代化的 UI 设计，支持批量预览、配色调整、背景切换和序列帧下载。

## 🛠️ 安装与运行

### 环境要求
*   Python 3.8+

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用
```bash
python app.py
```

### 3. 访问
打开浏览器访问: `http://127.0.0.1:5000`

## 📂 项目结构

*   `app.py`: Flask 后端入口，处理 API 请求和页面路由。
*   `gen_character.py`: 核心角色生成逻辑，负责图层合成和绘制。
*   `character_definitions.py`: 角色部件、调色板、动画帧和主题的定义文件。
*   `post_effects.py`: 图像后处理模块（艺术滤镜）。
*   `texture_generator.py`: 程序化纹理生成工具（用于滤镜）。
*   `character_config.yaml`: 默认角色配置文件。
*   `templates/index.html`: 前端单页应用（Vue-like 交互，原生 JS）。

## 🎨 扩展指南

### 添加新部件
在 `character_definitions.py` 中的 `PART_DEFINITIONS` 字典中添加新的绘图指令。
指令格式：
*   `("rect", (x, y, w, h), "color_key")`
*   `("pixel", (x, y), "color_key")`
*   `("polygon", [(x1,y1), ...], "color_key")`

### 修改配色
在 `character_definitions.py` 的 `THEME_PALETTES` 或 `DEFAULT_PALETTE` 中定义新的颜色。

### 自定义滤镜
在 `post_effects.py` 中编写新的图像处理函数，并在 `get_post_effect_for_mode` 中注册。

## 📝 开发日志

*   **v1.0**: 基础像素生成。
*   **v2.0**: Web 界面集成，支持动画预览。
*   **v3.0**: 增加多风格（赛博、仙侠等）和艺术滤镜。
*   **v3.5 (Current)**: UI 重构为专业工坊模式，支持批量动作生成，自适应布局优化。

---
*Created by Antigravity / OpenCode*
