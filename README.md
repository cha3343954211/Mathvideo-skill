# MathVideo Skill: 基于 Manim 的专业数学教学与科普视频工作流

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Manim Community v0.18+](https://img.shields.io/badge/manim-v0.18+-purple.svg)](https://www.manim.community/)
[![TTS Engine](https://img.shields.io/badge/TTS-Edge--TTS%20Neural-green.svg)](https://github.com/rany2/edge-tts)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **为数学教师、科普博主与 AI 协作智能体量身打造的顶级数学视频制作全流程套件。**  
> 内建 3Blue1Brown 传世级美学标准、严格的教学叙事安全门控、多主题换肤引擎、毫秒级声画同步与高阶几何直觉装置库。

> 📘 **完整实战指南**：深入的 API 手册与从零到一教程，请阅读 [👉 详细使用说明与开发者手册 (docs/USAGE_GUIDE.md)](docs/USAGE_GUIDE.md)

---

## 📖 目录

- [🌟 核心理念与防翻车双门控](#-核心理念与防翻车双门控)
- [✨ 十大核心突破与架构体系](#-十大核心突破与架构体系)
  - [1. 7 大顶级学术与科技美学主题家族](#1-7-大顶级学术与科技美学主题家族)
  - [2. 公式多项式智能着色与平滑渐变演化](#2-公式多项式智能着色与平滑渐变演化)
  - [3. 电影级动态运镜与 3D HUD 抬头显示屏](#3-电影级动态运镜与-3d-hud-抬头显示屏)
  - [4. LayoutGuard 智能排版与包围盒碰撞检测器](#4-layoutguard-智能排版与包围盒碰撞检测器)
  - [5. 毫秒级声画同步引擎 (AudioSync Engine)](#5-毫秒级声画同步引擎-audiosync-engine)
  - [6. 纯粹数学美学与单行优雅字幕规范](#6-纯粹数学美学与单行优雅字幕规范)
  - [7. 高阶数学直觉组件库 (Intuition Rigs)](#7-高阶数学直觉组件库-intuition-rigs)
  - [8. 秒级单帧质检与交互式 Web 故事板看板](#8-秒级单帧质检与交互式-web-故事板看板)
- [📂 代码库与 Skill 架构全景](#-代码库与-skill-架构全景)
- [🚀 极速上手：三步创作你的高品质数学视频](#-极速上手三步创作你的高品质数学视频)
- [🤖 AI 智能体协同范式 (Prompt & Directives)](#-ai-智能体协同范式-prompt--directives)
- [📄 开源协议](#-开源协议)

---

## 🌟 核心理念与防翻车双门控

传统的 Manim 视频制作与 AI 生成常面临致命痛点：
1. **“一上来就写代码”**：未理顺直觉逻辑，反复渲染返工耗时费力；
2. **“画面拥挤混乱”**：公式出界、文字叠在一起、白底白字隐形；
3. **“语画严重脱节”**：音频和画面各播各的，节奏生硬尴尬。

本套件在底层确立了**两条不可逾越的硬门控协议**：

```text
┌─────────────────────────────────────────────────────────────┐
│  【硬规则 0 (Rule 0)】时间轴脚本未审不写代码                │
│  在写任何 Manim 代码前，必须先生成分镜大纲与时间轴对照表    │
│  由人类创作者审核确认教学直觉无误后，才可进入编码阶段。     │
├─────────────────────────────────────────────────────────────┤
│  【硬规则 0.5 (Rule 0.5)】音频决策门控                      │
│  脚本审核通过后，必须明确决策制作模式：                     │
│  - 真人质感 TTS 神经网络语音解说 (Microsoft Yunxi / Xiaoxiao)│
│  - 极致沉浸纯净无声教学模式                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ 十大核心突破与架构体系

### 1. 7 大顶级学术与科技美学主题家族
彻底告别传统枯燥的纯黑背景与高饱和刺眼配色：
- **`3b1b_dark`**：3Blue1Brown 经典极客深空风 (`#121417`)
- **`claude_light`**：Claude 象牙暖米纸学术风（Quanta Magazine / 剑桥学刊质感，公式自动反色为深炭灰，绝无隐形）
- **`claude_dark`**：Claude 优雅深邃炭灰风
- **`nord`**：北极冰川深蓝极简风
- **`chalkboard`**：经典深绿教室黑板风（板书教学亲切感）
- **`solarized_light`**：日光清爽浅色纸张风
- **`cyberpunk_neon`**：赛博霓虹高对比深色系

```python
class MyScene(BaseMathScene):
    DEFAULT_THEME = "claude_light"  # 一键换肤，全套文字、网格、公式智能自适应
```

### 2. 公式多项式智能着色与平滑渐变演化
告别手动通过 `math_tex[0][2:5]` 调试切片索引的巨大痛苦：
```python
formula = self.make_math(r"\int_{a}^{b} f(x) \, dx = F(b) - F(a)")
self.colorize_formula(formula, {
    r"f(x)": BLUE,
    r"F(b)": GREEN,
    r"F(a)": RED
})
# 平滑公式继承与匹配演变
self.stepwise_tex_transform(old_formula, new_formula, run_time=1.2)
```

### 3. 电影级动态运镜与 3D HUD 抬头显示屏
- **`MovingCameraMathScene`**：平滑推镜聚焦 (`camera_zoom_to`)、平移追踪 (`camera_pan_to`)、镜头复位 (`camera_reset`)；
- **`ThreeDMathScene`**：原生支持 3D 曲面与**固定在视口正前方、不随三维摄影机旋转的 2D HUD 面板** (`add_fixed_in_frame_mobjects`)，并自带平滑轨道巡航环绕视角 (`start_orbital_flight`)。

### 4. LayoutGuard 智能排版与包围盒碰撞检测器
在渲染前或关键帧自动构建二维 AABB 包围盒树：
- **碰撞与重叠告警**：`self.scan_collisions()` 实时检测文字与几何对象是否叠压重叠；
- **视口越界拦截**：`LayoutGuard.keep_in_safe_bounds()` 强制将超出视口的对象推回安全可视区；
- **智能避让**：`self.avoid_overlap(target, obstacles, direction=DOWN)` 自动平滑排开元素，彻底实现无遮挡。

### 5. 毫秒级声画同步引擎 (AudioSync Engine)
搭载 Microsoft Neural TTS (云希/晓晓)，支持 MD5 纯本地音频持久化缓存：
```python
with self.voiceover("当旋转行进到圆周率派时，质点刚好精准抵达实轴负一。") as tracker:
    # 动画持续时间自动与实际人声物理音频毫秒级锁死，零冗余拖沓！
    self.play(dot.animate(run_time=tracker.duration).move_to(target_pos))
```

### 6. 纯粹数学美学与单行优雅字幕规范
- **去伪存真**：坚决摒弃粗暴的多层描边膨胀（Cheap Bloom）与游戏街机式冲击波，杜绝干扰数学心智思考的劣质配乐；
- **单行优雅规范 (Strict Single-Line)**：
  - 底部字幕保持利落纯单行，释放开阔留白空间；
  - 具备 **智能阶梯字号自适应**（短句 20pt、中句 17.5pt、长句 15.5pt）；
  - 配备 `scale_to_fit_width(11.2)` **100% 物理绝对边界防溢出保底**，永不出界切边。

### 7. 高阶数学直觉组件库 (Intuition Rigs)
开箱即用的高阶动态数学装置，全部基于参数驱动与 `always_redraw` 响应：
- **`DynamicTangentRig`**：动态导数切线装置，自带正交斜率直角三角形与数值实时追踪；
- **`DynamicRiemannRig`**：动态黎曼和切分柱状图，支持从 $N=4$ 平滑逼近到 $N=60$；
- **`LinearTransformRig`**：二维矩阵变换装置，网格动态剪切旋转，自带行列式面积守恒平行四边形；
- **`FourierCirclesRig`**：外轮旋转周转圆环级数组件；
- **`OrganicMotion.spring_bounce`**：物理弹簧阻尼速率缓动函数。

### 8. 秒级单帧质检与交互式 Web 故事板看板
- **毫秒级单帧快速切片质检**：`python skills/manim-video/scripts/fast_inspector.py scene.py MyScene`，0.5 秒内直出单帧 PNG 排版图；
- **独立交互式 Web 故事板看板**：`python skills/manim-video/scripts/storyboard_generator.py`，全自动扫描全片所有 Scene，提取关键帧与口播字幕，一键生成可在任何浏览器离线查看的响应式故事板看板。

---

## 📂 代码库与 Skill 架构全景

```text
mathvideo-skill/
├── .agents/skills/manim-video/     # Antigravity IDE 智能体标准技能根目录
│   ├── SKILL.md                    # 技能规范、门控协议与指令手册
│   ├── templates/                  # 核心资产库
│   │   ├── base_scene.py           # 7大主题、电影运镜、3D HUD、单行字幕基类
│   │   ├── audio_engine.py         # TTS 神经人声生成与音频管理
│   │   ├── layout_guard.py         # AABB 包围盒重叠与出界检测器
│   │   ├── math_rigs.py            # 切线、黎曼和、线性变换、傅里叶等直觉装置
│   │   ├── visual_fx.py            # 克制极简视效与暗场聚光引擎
│   │   ├── script_timeline_template.md # 时间轴与口播台词审核模板
│   │   └── storyboard_template.md  # 分镜设计模板
│   ├── references/                 # 最佳实践、审美配色与避坑指南
│   └── scripts/                    # 效能脚本套件 (check_env, fast_inspector, storyboard_generator, render_manager)
├── demo_project/                   # 经典样板工程：毕达哥拉斯勾股定理证明 (已调通)
├── projects/                       # 经典实战演示项目集 (欧拉公式几何正交、康托尔三分集、集合论等)
├── .gitignore                      # 工业级防膨胀过滤配置 (严禁大视频切片与缓存入库)
├── requirements.txt                # 核心依赖清单
└── README.md                       # 本说明文档
```

---

## 🚀 极速上手：三步创作你的高品质数学视频

### 1. 环境准备
确保已安装 Python 3.10+、Manim、FFmpeg 与 LaTeX。克隆本仓库并安装依赖：
```bash
git clone https://github.com/cha3343954211/Mathvideo-skill.git
cd Mathvideo-skill
pip install -r requirements.txt
```
运行环境自检：
```bash
python skills/manim-video/scripts/check_env.py
```

### 2. 作为 Antigravity / Claude 智能体技能加载
将 `skills/manim-video/` 复制到您的智能体配置根目录：
- **Antigravity 工作区技能**：放置在当前项目的 `.agents/skills/manim-video/`
- **全局用户技能**：放置在 `~/.gemini/config/skills/manim-video/`

在对话中输入：
> *"请基于 manim-video 技能，为我构思一个关于【欧拉公式几何本质】的视频，先出时间轴脚本供我审核。"*

### 3. 一键渲染、快速质检与批量拼接
```bash
# 0.5 秒提取关键帧快速检查排版
python skills/manim-video/scripts/fast_inspector.py demo_project/scene_01_intro.py Scene01Intro

# 一键批量高清渲染并无损合并
python skills/manim-video/scripts/render_manager.py --action pipeline --quality h \
  --scenes demo_project/scene_01_intro.py:Scene01Intro demo_project/scene_02_proof.py:Scene02Proof \
  --output final_pythagoras.mp4
```

---

## 🤖 AI 智能体协同范式 (Prompt & Directives)

当与 AI 结对编程数学动画时，推荐使用以下指令模板：

```text
你现在是一个顶尖的数学可视化导演，请使用 manim-video 技能执行任务：
1. 主题：傅里叶变换的几何直觉
2. 受众：理工科大学本科生
3. 视觉基调：3b1b_dark 极客风格，保持纯单行利落字幕，杜绝花里胡哨低级发光
4. 严格遵守 Rule 0：请先输出 script_and_timeline.md 供我审核确认，得到我的同意前不要生成任何 Manim 代码。
```

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。欢迎提交 Issue 与 Pull Request，共同推动数学与科学教育可视化美学走向新高度！
