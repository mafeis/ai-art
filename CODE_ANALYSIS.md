# Pixel Forge 代码分析文档

> 项目：水浒像素工坊 (AI-Art) | 技术栈：Python + Flask + Pillow

---

## 一、项目概览

Pixel Forge 是一个**程序化像素角色生成器**，通过组合预定义的像素部件（头、身、发型、武器等）实时生成角色动画（GIF）和精灵图（PNG）。

### 核心能力
- 多主题角色生成（仙侠、赛博朋克、蒸汽朋克、恐怖、科技、西部）
- 8 种动作动画（Idle、Walk、Run、Attack、Jump、Hurt、Cheer、Die）
- 7 种渲染风格（Retro、Sketch、Neon、Ink、HD、HiBit、Premium）
- Web 界面实时预览 + 批量导出

---

## 二、目录结构

```
ai-art/
├── app.py                          # Flask 入口，API 路由
├── config/
│   └── character_config.yaml       # 默认角色配置（部件+配色）
├── debug_sketch.py                 # 调试脚本
├── modules/
│   ├── character/
│   │   ├── definitions.py          # 【核心】部件/动画/主题定义
│   │   └── generator.py            # 【核心】角色合成引擎
│   ├── rendering/
│   │   ├── post_effects.py         # 艺术滤镜后处理
│   │   ├── renderers.py            # 各渲染器实现
│   │   └── texture_generator.py    # 程序化纹理生成
│   └── config/
│       └── __init__.py
├── templates/
│   └── index.html                  # 前端 SPA 界面
├── tests/                          # 测试目录（空）
├── legacy/                         # 历史废弃代码
│   ├── cairo_renderer.py           # Cairo 渲染实验（未使用）
│   ├── game_character_gen.py
│   ├── gen_monster.py
│   ├── gen_scene.py
│   ├── ai_prompt.py
│   ├── run_sd.py                   # Stable Diffusion 调用（未集成）
│   └── test_cairo_renderer.py
└── requirements.txt                # 依赖：Flask, Pillow, PyYAML
```

---

## 三、核心模块详解

### 3.1 `modules/character/definitions.py` — 数据定义层

这是项目的**数据心脏**，定义了所有可组合的元素。

#### 关键数据结构

| 数据结构 | 用途 |
|---------|------|
| `LAYER_ORDER` | 渲染层级顺序（back → front，共 9 层） |
| `PART_DEFINITIONS` | 每个部件的所有样式及其像素绘制指令 |
| `PART_TAGS` | 每个样式的标签体系（用于主题匹配） |
| `ANIMATION_DEFINITIONS` | 每种动作的关键帧参数 |
| `DEFAULT_PALETTE` | 全局调色板（20+ 颜色键） |
| `THEME_PALETTES` | 6 个主题各自的专属配色 |
| `THEME_RENDER_MODES` | 主题推荐的默认渲染模式 |

#### 部件层级（LAYER_ORDER）

```
back → legs_back → body → head → eyes → hair → legs_front → arms → held
```

#### 部件与样式数量

| 部件 | 样式数量 | 示例样式 |
|------|---------|---------|
| back | 6 | none, cape, wings, backpack, jetpack, flying_swords, coffin |
| head | 10 | human, elf, orc, dwarf, skeleton, robot, sage_beard, cyborg_eye, zombie, gas_mask, oni |
| hair | 13 | bald, short, long, mohawk, ponytail, afro, wizard_hat, hood, helmet, topknot, brain_exposed |
| body | 11 | shirt, armor, robe, jacket, hanfu_scholar, hanfu_warrior, mech_suit, ribs_gore |
| legs | 5 | pants, shorts, boots_high, skirt, robot_legs |
| held | 11 | sword, staff, axe, shield, laser_gun, katana_laser, wrench, chainsaw, jian, fan, gourd |

#### 绘制指令格式

三种指令类型，定义在每个样式的 `PART_DEFINITIONS` 中：

```python
# rect: 矩形填充
("rect", (x, y, w, h), "color_key")

# pixel: 单像素
("pixel", (x, y), "color_key")

# polygon: 多边形
("polygon", [(x1,y1), (x2,y2), ...], "color_key")
```

坐标基于 **32×32 网格**（设计坐标系），实际渲染时会乘以 `scale` 放大。

#### 动画帧参数

每帧由以下参数控制角色姿态：

| 参数 | 含义 |
|------|------|
| `bob` | 身体上下浮动（负值=上升，正值=下沉） |
| `leg_f` | 腿部帧索引（-2~2，控制抬腿幅度） |
| `arm_f` | 手臂帧索引（-1~2，控制摆臂幅度） |
| `offset_x` | 整体水平位移（用于冲刺、击退等） |

#### 主题系统

6 个主题，每个主题有独立配色 + 推荐渲染模式：

| 主题 | 推荐渲染 | 特色配色 |
|------|---------|---------|
| xianxia | ink | 水墨黑发、白袍、青玉 |
| cyberpunk | neon | 霓虹粉发、青蓝靴、绿眼 |
| horror | sketch | 灰色死发、血红衣、僵尸绿皮 |
| steampunk | retro | 棕发、黄铜色、皮质 |
| tech | hd | 白发白靴、蓝眼、金属银 |
| western | retro | 金发、链甲、钢甲 |

---

### 3.2 `modules/character/generator.py` — 合成引擎

#### `CharacterComposer` 类

核心合成器，负责将部件配置渲染到画布上。

**初始化流程：**
1. 加载 YAML 配置（或直接接收 dict）
2. 设置画布尺寸（默认 64×64，比设计大 2 倍，防止动作溢出）
3. 计算居中偏移量：`base_offset = (64 - 32) / 2 = 16`
4. 合并用户配色覆盖默认调色板

**关键方法：**

- `get_color(key)` — 从调色板获取颜色，未定义返回品红 `(255, 0, 255)` 作为调试色
- `adjust_color(color, factor)` — 按系数调整颜色亮度（用于高光/阴影）
- `draw_part(...)` — 执行单个部件的绘制指令，支持三种渲染模式
- `compose_frame(...)` — 组合单帧画面，按 `LAYER_ORDER` 依次绘制各层

**绘制坐标系统：**

```
画布坐标系: 64×64
设计坐标系: 32×32（原始像素部件定义在此空间）
实际坐标 = base_offset + 设计坐标 × scale + 动画偏移
```

#### 两个导出函数

| 函数 | 输出 | 用途 |
|------|------|------|
| `create_character_gif()` | BytesIO (GIF) | 前端预览动画 |
| `create_character_spritesheet()` | PIL.Image (PNG) | 用户下载精灵图 |

两者共享相同的渲染管线，区别在于：
- GIF：逐帧渲染，每帧独立 resize 后打包
- PNG：将所有帧水平拼接成一张条带图

**渲染管线：**
```
配置解析 → 逐帧绘制（compose_frame）→ 缩放（LANCZOS/NEAREST）→ 艺术滤镜后处理
```

**密度（density）与缩放：**
- `density` 控制内部渲染分辨率
- `output_size` 控制最终输出尺寸
- `density ≥ 4.0` 时使用 LANCZOS 插值（高清），否则 NEAREST（像素锐利）

---

### 3.3 `modules/rendering/post_effects.py` — 艺术滤镜

在主渲染完成后对图像进行后处理，通过 `get_post_effect_for_mode()` 分发。

| 滤镜 | 效果描述 | 实现方式 |
|------|---------|---------|
| `ink` | 水墨晕染 | 高斯模糊(0.8) + 混合(0.4) + 降饱和(0.7) + 增对比(1.2) |
| `neon` | 霓虹发光 | 增对比(1.4) + 高斯模糊(4) + 混合(0.5) + 增饱和(1.4) |
| `sketch` | 手绘质感 | 边缘强化 + 锐化 + 降饱和(0.5) + 增亮(1.1) |
| `retro` | CRT 复古 | 色差偏移(2px) + 模糊(0.4) + 增对比(1.1) |
| `hd` | 矢量抛光 | 平滑模糊(0.3) + 增对比(1.15) + 增饱和(1.1) + 锐化 |
| `hibit` | Hi-Bit 纯净 | 无滤镜，保持像素纯净 |
| `premium` | 高端抛光 | 锐化(1.2) + 增饱和(1.1) |

**Alpha 通道保护机制：** `_apply_effect_with_alpha_mask()` 确保透明区域不被滤镜污染。

---

### 3.4 `modules/rendering/renderers.py` — 渲染器实现

定义了 6 种渲染器类，继承自 `Renderer` 基类：

| 渲染器 | 特点 |
|-------|------|
| `RetroRenderer` | 纯色矩形，像素风 |
| `VectorRenderer` | 圆角矩形 + 内高光 + 镜面点（HD 风格） |
| `SketchRenderer` | 抖动偏移 + 多次描边模拟手绘 |
| `NeonRenderer` | 外发光描边 + 亮核（但实际发光效果有限） |
| `InkRenderer` | 椭圆笔触叠加模拟毛笔效果 |
| `HiBitRenderer` | **最复杂**：材质感知 + 亚像素纹理 + 四向光影 + 像素描边 |
| `PremiumRenderer` | 伪 3D 光照（左上高光、右下阴影）+ 圆角描边 |

> ⚠️ **注意**：`HiBitRenderer` 第 263 行存在未定义变量 `is_cloth`，会导致运行时错误。

---

### 3.5 `modules/rendering/texture_generator.py` — 程序化纹理

提供 6 种程序化纹理生成函数，当前**未被主流程调用**（仅作备用）：

- `generate_paper_texture()` — 米黄纸张噪点
- `generate_scanline_texture()` — CRT 扫描线
- `generate_noise_texture()` — 颗粒噪点
- `generate_gradient_texture()` — 线性渐变
- `generate_metal_texture()` — 拉丝金属
- `apply_vignette()` — 暗角效果

---

### 3.6 `app.py` — Flask Web 服务

#### API 路由

| 路由 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 渲染 `templates/index.html` |
| `/options` | GET | 返回所有可用部件样式、动画、主题列表 |
| `/config` | GET | 读取并返回 `character_config.yaml` |
| `/randomize` | GET | 智能随机生成角色配置（支持主题加权） |
| `/generate` | POST | 核心生成接口，接收配置返回 GIF+PNG |

#### `/randomize` 智能随机化逻辑

1. 确定主题（`all` 时随机选一个）
2. 构建标签池：主标签 + 兼容标签（如 cyberpunk 包含 tech）
3. 对每个部件分类：精确匹配 → 兼容匹配 → 泛型匹配
4. 加权随机抽取：精确匹配权重 ×50，兼容 ×10，泛型 ×2
5. 配色智能生成：肤色（HSV）、金属色（银/金/铜）、轮廓（深色）、其他（鲜艳随机）

#### `/generate` 批处理

- 支持 `actions` 数组批量生成（最多 8 个动作）
- 支持 `output_size`（512/1024/2048，上限 2048）
- 支持 `render_mode` 指定渲染风格
- 返回每动作的 GIF（base64）和 PNG 下载数据（base64）

---

## 四、前端（templates/index.html）

单页 Vue-like 应用（原生 JS），主要功能：
- 部件选择面板（每个部件的下拉选择）
- 配色编辑器（各颜色通道调整）
- 主题快捷切换
- 动作批量选择
- 渲染模式选择
- 实时预览区（GIF 显示）
- 下载按钮（PNG 精灵图）
- 随机生成按钮

---

## 五、技术债务与问题

### 已知 Bug

| 问题 | 位置 | 严重度 |
|------|------|--------|
| `is_cloth` 未定义 | `renderers.py:263` | 🔴 运行时报错 |
| `PART_DEFINITIONS["legs"]` 定义了两次（第 468 行和第 479 行） | `definitions.py` | 🟡 后定义覆盖前定义 |
| `debug_sketch.py` 导入 `post_effects` 但工作目录不对（应从 `modules.rendering` 导入） | `debug_sketch.py:2` | 🟡 无法独立运行 |
| `hollow_knight` 模式返回 400 错误提示"已移至 experimental"，但代码中没有 experimental 模式 | `app.py:245` | 🟢 遗留提示 |

### 架构问题

1. **渲染器未被真正使用**：`generator.py` 的 `draw_part()` 自己实现了 retro/sketch/hd 三种渲染逻辑，`renderers.py` 中的 6 个渲染器类是独立实现但未被调用
2. **`texture_generator.py` 未集成**：所有纹理生成函数都是孤立的，主流程没有使用
3. **`legacy/` 目录混乱**：包含多个废弃文件和 Stable Diffusion 集成实验代码
4. **无测试**：tests 目录为空，无任何单元测试
5. **配置分散**：部分逻辑硬编码在 `generator.py` 中（如 `density` 强制提升逻辑）

---

## 六、数据流总图

```
用户操作（前端）
    ↓ JSON 配置
/app.py POST /generate
    ↓
generator.py: create_character_gif() / create_character_spritesheet()
    ↓
CharacterComposer.__init__() — 加载配置 + 合并调色板
    ↓
逐帧循环：
    compose_frame() — 按 LAYER_ORDER 绘制 9 层
        draw_part() — 执行绘制指令（rect/pixel/polygon）
            根据 render_mode 应用不同渲染逻辑
    ↓
resize — LANCZOS 或 NEAREST
    ↓
post_effects — 艺术滤镜后处理
    ↓
GIF 打包 或 PNG 保存
    ↓
base64 编码 → JSON 响应
```