# Pixel Forge Ver2 代码分析文档

> 项目：ai-art | 分支：ver2 | 技术栈：Python + Flask + Pillow

---

## 一、与 Main 分支的核心差异

| 维度 | Main | Ver2 |
|------|------|------|
| **设计分辨率** | 32×32 | 64×64（翻倍精度） |
| **画布尺寸** | 64×64 | 128×128（更大缓冲） |
| **数据组织** | 单文件 `definitions.py` | 拆分为 `data/` 子包（parts/palettes/animations） |
| **渲染架构** | `generator.py` 内嵌渲染逻辑 | 独立 `renderer.py`（`CharacterRenderer` 类） |
| **渲染器使用** | `renderers.py` 中的类**未被调用** | `CharacterRenderer` **实际被使用** |
| **主题系统** | 6 个主题（xianxia/cyberpunk/horror/steampunk/tech/western） | 5 个主题（fantasy/scifi/modern/cute/action） |
| **动画数量** | 8 种 | 12 种（含 4 种武器特化攻击动画） |
| **武器系统** | 无武器元数据 | 新增 `WEAPON_METADATA`（pivot/type） |
| **武器旋转** | 无 | 支持 `rotation` 参数 + 枢轴点旋转 |
| **VFX 系统** | 无 | 支持 5 种特效（slash/shoot_flash/magic_circle/magic_beam/impact） |
| **手臂渲染** | 简单矩形 | 前后手臂分离 + 多边形连接 + 握拳细节 |
| **缩放算法** | density≥4 用 LANCZOS | **全部用 NEAREST**（保像素锐利） |
| **随机化模式** | 强制 `hibit` | 仍强制 `hibit`（未改） |
| **/config API** | 读 YAML 文件 | 直接从代码定义构建（始终同步） |

---

## 二、目录结构

```
ai-art/
├── app.py                              # Flask 入口（314行，比 main 多 5 行）
├── modules/
│   ├── character/
│   │   ├── definitions.py              # 【Facade】统一导入，防止破坏旧 import
│   │   ├── generator.py                # 【重构】合成引擎（534行，比 main 少 37 行）
│   │   ├── renderer.py                 # 【新增】独立渲染器类（391行）
│   │   └── data/                       # 【新增】拆分的子模块
│   │       ├── parts.py                # LAYER_ORDER + PART_TAGS + PART_DEFINITIONS
│   │       ├── palettes.py             # THEME_PALETTES + DEFAULT_PALETTE + THEME_MAPPINGS
│   │       └── animations.py           # ANIMATION_DEFINITIONS + WEAPON_METADATA
│   └── rendering/
│       ├── post_effects.py             # 艺术滤镜（未变，203行）
│       ├── renderers.py                # 渲染器类（未变，433行，但未被主流程调用）
│       └── texture_generator.py        # 程序化纹理（未变，150行）
├── templates/
│   └── index.html                      # 前端（1066行，比 main 更精致）
├── config/                             # 【已删除】不再需要 YAML 配置文件
├── legacy/                             # 历史废弃代码（8个文件，同 main）
└── requirements.txt                    # 依赖（同 main）
```

---

## 三、核心模块详解

### 3.1 `modules/character/data/parts.py` — 64×64 HD 像素定义

**设计规则：** Base Resolution = 64×64，所有坐标翻倍。

#### 新层级顺序（12 层，比 main 多 4 层）

```
back → arm_back → legs_back → body → head → eyes → expression → face_wear → hair → legs_front → arm_front → held → hand_front
```

新增层：
- `arm_back` — 后手（左手，通常不持武器）
- `arm_front` — 前手（右手，持武器），用多边形连接肩部和手腕
- `expression` — 表情层（smile/pout/neutral/surprised）
- `face_wear` — 面饰层（glasses_red/bandage/cat_ears_headset）
- `hand_front` — 前手掌（覆盖武器柄，绘制握拳细节）

#### 部件与样式（精简但更精致）

| 部件 | 样式数 | 示例 |
|------|--------|------|
| head | 1 | base（详细的头部形状，含耳廓、下颚阴影、腮红） |
| eyes | 4 | anime_large（大眼）、sharp_focus、gentle_droop、cat_eye |
| expression | 4 | smile、pout、neutral、surprised |
| hair | 5 | short_hero、long_straight、twin_tails、messy_shag、bob |
| face_wear | 3 | glasses_red、bandage、cat_ears_headset |
| body | 5 | adventurer_coat、school_uniform、maid_dress、cyber_vest、wizard_robe |
| legs | 4 | pants_boots、skirt_socks、boots_shorts、armored_legs |
| held | 6 | sword_iron、staff_magic、book_spell、shield_round、tea_cup、none |
| back | 3 | none、cape_hero、wings_angel、backpack_travel |

#### 新增绘制指令类型

| 类型 | 格式 | 用途 |
|------|------|------|
| `ellipse` | `("ellipse", (x,y,w,h), "color")` | 椭圆（眼睛、圆形装饰） |
| `circle` | `("circle", (cx,cy,r), "color")` | 正圆 |
| `stroke` | `("rect", (x,y,w,h), "color", "stroke")` | 仅描边（眼镜框、盾牌边框） |

#### 64×64 坐标示例（头部）

```python
# 主脸型
("rect", (20, 12, 24, 20), "skin"),   # 主体
("rect", (22, 10, 20, 2), "skin"),    # 圆角过渡
("rect", (24, 8, 16, 2), "skin"),     # 顶部圆角
# 腮红（4x2 像素）
("rect", (18, 24, 4, 2), "highlight"),
("rect", (42, 24, 4, 2), "highlight"),
# 耳朵
("rect", (14, 20, 4, 6), "skin"),
("rect", (16, 22, 2, 2), "outline"),  # 耳道
```

---

### 3.2 `modules/character/data/animations.py` — 动画与武器元数据

#### 12 种动画

| 动画 | 帧数 | 特性 |
|------|------|------|
| idle | 4 | 呼吸感，轻微 bob |
| walk | 4 | 稳定节奏，交替抬腿 |
| run | 4 | 大幅度 bob(-3)，offset_x 冲刺感 |
| attack | 5 | **武器旋转** -45°→-90°→45°→100°，含 vfx |
| attack_shoot | 4 | **武器射击**，后坐力，muzzle flash |
| attack_cast | 4 | **魔法施放**，staff 上扬，magic_circle + magic_beam |
| attack_heavy | 5 | **重型挥砍**，更大旋转角度，impact VFX |
| jump | 5 | 蓄力→腾空→落地 |
| hurt | 5 | 向后击退 |
| cheer | 4 | 跳起欢呼 |
| die | 5 | 倒地 |
| *(原有)* | | |

#### 武器元数据（WEAPON_METADATA）

```python
"sword_iron": {"type": "slash", "pivot": (1, 23)},   # 斩击型，剑柄中心为轴
"staff_magic": {"type": "cast", "pivot": (0, 0)},    # 施法型，握把中心
"plasma_rifle": {"type": "shoot", "pivot": (0, 6)},  # 射击型
```

**自动动画选择逻辑**（`generator.py`）：
```
用户选择 "attack" → 读取 held 武器类型 → 查找 attack_{type}
→ attack_shoot / attack_cast / attack_heavy / attack（默认）
```

#### 帧参数扩展

| 参数 | 含义 |
|------|------|
| `bob` | 身体上下浮动 |
| `leg_f` | 腿部帧（-2~2） |
| `arm_f` | 手臂帧（-1~4，新增 3 和 4） |
| `offset_x` | 水平位移 |
| `rot` | **武器旋转角度**（新增） |
| `vfx` | **视觉特效类型**（新增） |

---

### 3.3 `modules/character/renderer.py` — 独立渲染引擎

`CharacterRenderer` 类是 ver2 的核心渲染抽象，从 `generator.py` 中提取出来。

#### 核心方法

| 方法 | 职责 |
|------|------|
| `draw_part()` | 入口：处理旋转/枢轴偏移，然后分发给 `_render_instructions` |
| `_render_instructions()` | 执行绘制指令列表（rect/pixel/polygon/ellipse/circle） |
| `_draw_part_rotated()` | 武器旋转：在临时画布渲染 → rotate(BICUBIC) → alpha_composite 回原画布 |
| `draw_vfx()` | 绘制 5 种特效（slash arc / shoot_flash / magic_circle / magic_beam / impact） |

#### 材质感知渲染（HD 模式）

```python
is_metal = "metal" in color_key or "gold" in color_key
is_skin = "skin" in color_key
is_hair = "hair" in color_key
is_glowing = "neon" in color_key or "light" in color_key
```

不同材质应用不同光影策略：
- **金属**：高对比度镜面高光 + 四向阴影
- **皮肤**：柔和底部阴影 + 腮红红润
- **布料/头发**：顶部边缘光 + 柔和阴影 + 程序化噪点
- **发光体**：白色核心

#### 武器旋转实现

```python
# 1. 创建临时画布
temp_img = Image.new("RGBA", (size, size), (0,0,0,0))
# 2. 以枢轴点为中心渲染
draw_start_x = pivot_x - wp_pivot_x
draw_start_y = pivot_y - wp_pivot_y
# 3. BICUBIC 旋转（expand=True 自动扩展画布）
rotated_img = temp_img.rotate(rotation, resample=BICUBIC, expand=True)
# 4. alpha_composite 回原画布
canvas.alpha_composite(rotated_img, (paste_x, paste_y))
```

#### VFX 系统

| VFX | 实现 | 触发时机 |
|-----|------|---------|
| slash | `arc` 弧线（-60°~60°） | attack 帧 3 |
| shoot_flash | 四边形多边形（菱形） | attack_shoot 帧 2 |
| magic_circle | 空心椭圆环 | attack_cast 帧 2 |
| magic_beam | 椭圆形光束 | attack_cast 帧 3 |
| impact | 实心椭圆 | attack_heavy 帧 3 |

---

### 3.4 `modules/character/generator.py` — 合成引擎（重构）

#### 关键变化

1. **画布扩大**：128×128（main 是 64×64），设计坐标系 64×64，居中偏移 `(32, 48)`
2. **手臂分层渲染**：
   - `arm_back`：左手简单矩形 + 椭圆手掌
   - `arm_front`：右手多边形连接（肩→腕）+ 手掌覆盖武器柄
   - `hand_front`：握拳细节（拇指叠加 + 阴影 + 高光）
3. **武器旋转传递**：通过 `rotation` + `pivot_offset` 参数传给 `renderer.draw_part()`
4. **VFX 绘制**：在 `compose_frame` 末尾调用 `renderer.draw_vfx()`
5. **自动动画选择**：attack 动作根据武器类型路由到对应子动画
6. **全 NEAREST 缩放**：移除 LANCZOS，始终保持像素锐利

#### 武器-手部同步

武器位置和手部位置使用完全相同的计算逻辑（arm_frame 偏移链），确保武器始终握在手中：

```python
wp_x, wp_y = s(hand_x_base), s(hand_y_base) + bob
if arm_frame == 1: wp_x+=s(4); wp_y+=s(6)
elif arm_frame == 2: wp_x+=s(8); wp_y-=s(4)
elif arm_frame == 3: wp_x+=s(16); wp_y-=s(8)  # 攻击伸展
elif arm_frame == 4: wp_x+=s(12); wp_y-=s(12) # 高举
```

---

### 3.5 `app.py` — Web API（小幅改动）

| 变化点 | 说明 |
|--------|------|
| `/config` API | 不再读 YAML，直接从 `defs` 构建，确保与代码同步 |
| `/randomize` 主题 | 改为 fantasy/scifi/modern/cute/action（5个） |
| `/randomize` 模式 | 仍强制 `hibit`（未改） |
| 其他 API | 基本不变 |

---

### 3.6 `modules/rendering/` — 未变

`post_effects.py`、`renderers.py`、`texture_generator.py` 与 main 分支**完全相同**。

值得注意的是：`renderers.py` 中的 6 个渲染器类（Retro/Vector/Sketch/Neon/Ink/HiBit/Premium）仍然**未被主流程调用**。主流程使用的是 `renderer.py` 中的 `CharacterRenderer._render_instructions()` 内联逻辑。

---

## 四、技术债务与问题

### 已知 Bug

| 问题 | 位置 | 严重度 |
|------|------|--------|
| `is_cloth` 未定义 | `renderers.py:263`（HiBitRenderer） | 🔴 运行时报 NameError |
| `renderers.py` 仍未被使用 | `renderers.py` 整体 | 🟡 代码冗余 |
| `bob` 逻辑不一致 | `generator.py:169` legs_back 坐标计算 | 🟡 可读性差 |
| `PART_TAGS` 过于简化 | `parts.py` 只有 generic/male/female 等标签 | 🟡 随机化退化为主题无关 |
| `bob` 在 `legs_front` 中包含但在 `legs_back` 中处理混乱 | `generator.py:165-173` | 🟡 腿部动画可能不平滑 |

### 架构观察

1. **双渲染系统并存**：`renderer.py` 的 `CharacterRenderer` 和 `renderers.py` 的 6 个 Renderer 类是两套独立的渲染实现，前者被使用，后者是死代码
2. **数据拆分不彻底**：`definitions.py` 只是 Facade 转发，实际数据在 `data/` 子包中，但旧代码的 `from modules.character import definitions` 导入路径仍然有效
3. **无测试**：tests 目录仍然为空
4. **前端未分析**：`index.html`（1066行）包含完整的 SPA UI，但本次分析未深入

---

## 五、数据流总图

```
用户操作（前端）
    ↓ JSON 配置
app.py POST /generate
    ↓
generator.py: create_character_gif() / create_character_spritesheet()
    ├─ 武器类型检测 → 选择 attack_{type} 动画
    ↓
CharacterComposer.__init__()
    └─ 初始化 CharacterRenderer
    ↓
逐帧循环：
    compose_frame()
        ├─ 计算 bob / leg_f / arm_f / offset_x / rot / vfx
        ├─ 按 LAYER_ORDER 绘制 12 层
        │   ├─ back / arm_back / legs_back / body / head / eyes
        │   ├─ expression / face_wear / hair / legs_front
        │   ├─ arm_front（多边形连接）→ held（支持旋转）→ hand_front（握拳）
        │   └─ VFX 层（可选）
        └─ renderer.draw_vfx() ← 特效绘制
    ↓
resize（始终 NEAREST）
    ↓
post_effects — 艺术滤镜
    ↓
GIF 打包 或 PNG 保存
    ↓
base64 → JSON 响应
```