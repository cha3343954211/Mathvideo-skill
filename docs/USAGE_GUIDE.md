# MathVideo Skill 详细使用说明与实战开发者手册

欢迎阅读 **MathVideo Skill** 详细使用指南！本手册旨在帮助数学老师、科研人员、科普创作者以及 AI 结对智能体，从零到一掌握基于 Manim 的工业级数学视频制作全流程。

---

## 目录

1. [环境安装与全套配置](#1-环境安装与全套配置)
2. [AI 协同创作范式 (双门控工作流)](#2-ai-协同创作范式-双门控工作流)
3. [核心组件与场景 API 详解](#3-核心组件与场景-api-详解)
   - [3.1 7 大美学主题一键换肤](#31-7-大美学主题一键换肤)
   - [3.2 公式智能多项式着色与渐变演进](#32-公式智能多项式着色与渐变演进)
   - [3.3 纯粹单行自适应字幕与毫秒级语画同步](#33-纯粹单行自适应字幕与毫秒级语画同步)
   - [3.4 电影级动态运镜与 3D HUD 抬头显示屏](#34-电影级动态运镜与-3d-hud-抬头显示屏)
   - [3.5 LayoutGuard 空间碰撞与视口越界防护](#35-layoutguard-空间碰撞与视口越界防护)
   - [3.6 高阶数学直觉装置库 (Intuition Rigs)](#36-高阶数学直觉装置库-intuition-rigs)
4. [生产与效能工具链](#4-生产与效能工具链)
   - [4.1 0.5秒单帧快速质检 (Fast Inspector)](#41-05秒单帧快速质检-fast-inspector)
   - [4.2 离线交互式 Web 故事板看板 (Storyboard Generator)](#42-离线交互式-web-故事板看板-storyboard-generator)
   - [4.3 批量全自动渲染与无损拼接 (Render Manager)](#43-批量全自动渲染与无损拼接-render-manager)
5. [实战样板全流程教学 (从零到成片)](#5-实战样板全流程教学-从零到成片)
6. [常见疑难排查与避坑指南 (FAQ)](#6-常见疑难排查与避坑指南-faq)

---

## 1. 环境安装与全套配置

### 1.1 依赖总览
- **操作系统**：Windows / macOS / Linux
- **Python 环境**：Python 3.10+
- **核心软件**：
  - `manim` (Manim Community Edition $\ge$ v0.18.0)
  - `FFmpeg` (音视频转码与合并必需)
  - `MiKTeX` 或 `TeX Live` (LaTeX 公式渲染必需)
  - `edge-tts` (微软云端神经人声配音)

### 1.2 极速安装步骤

```bash
# 1. 克隆代码仓库
git clone https://github.com/cha3343954211/Mathvideo-skill.git
cd Mathvideo-skill

# 2. 安装 Python 核心依赖
pip install -r requirements.txt
```

### 1.3 运行环境诊断脚本
项目内建了全自动自检诊断脚本，运行即可检查缺少哪个组件：
```bash
python skills/manim-video/scripts/check_env.py
```
> 若诊断通过，将显示 `[OK] 全部核心依赖检测通过！`。如果提示缺少 FFmpeg 或 LaTeX，请根据提示安装并配置环境变量。

---

## 2. AI 协同创作范式 (双门控工作流)

当你在 Antigravity IDE、Cursor、Claude Desktop 或终端中使用 AI 辅助制作数学视频时，必须要求 AI 遵守本套件的**两条底层防翻车硬规则**：

### 阶段一：时间轴脚本审核 (Rule 0)
- **硬性约定**：在写任何 Manim 动画代码之前，**必须先输出时间轴脚本供人类审核**。
- **模板参考**：`skills/manim-video/templates/script_timeline_template.md`
- **内容包含**：
  - 分幕规划（通常一个 2~3 分钟的视频解耦为 3~4 幕）；
  - 每一幕的预估时间戳、口播解说词、核心动画动作、涉及公式。
- **创作者角色**：审核教学直觉是否准确、节奏是否舒服，确认无误后方可让 AI 编码。

### 阶段二：音频决策门控 (Rule 0.5)
时间轴脚本审核通过后，AI **必须显式向你确认**：
> *"请问本视频是采用真人质感 TTS 神经网络语音解说？还是采用纯净无声教学模式？"*
- 若选择 **有声模式**：AI 将在类中声明 `ENABLE_VOICEOVER = True`，并在渲染时自动生成 Microsoft Yunxi 语音并毫秒级锁死时长；
- 若选择 **无声模式**：AI 将保持纯净无声，依据字符数智能设置视觉停留时间。

---

## 3. 核心组件与场景 API 详解

所有核心组件均可在你的场景脚本中直接继承引用：
```python
from base_scene import BaseMathScene, MovingCameraMathScene, ThreeDMathScene
```

### 3.1 7 大美学主题一键换肤
彻底告别死板的纯黑背景，在场景类中声明 `DEFAULT_THEME` 即可自动适配全套文字、网格、坐标系与公式反色：
- `"3b1b_dark"`：3Blue1Brown 经典深空色 (`#121417`)
- `"claude_light"`：Claude 象牙暖米纸学术风（公式自动转深炭灰，绝无白底白字隐形）
- `"claude_dark"`：优雅深邃现代炭灰
- `"nord"`：北极冰川深蓝极简风
- `"chalkboard"`：经典教室深绿黑板风
- `"solarized_light"`：日光清爽浅色纸张风
- `"cyberpunk_neon"`：赛博高对比极客风

```python
class MyScene(BaseMathScene):
    DEFAULT_THEME = "claude_light"  # 一键切换为顶级学刊质感
```

### 3.2 公式智能多项式着色与渐变演进
不再需要手动数字符下标调试 `tex[0][1:4]`：
```python
formula = self.make_math(r"e^{i\pi} + 1 = 0")
self.colorize_formula(formula, {
    r"e^{i\pi}": self.theme.primary,
    r"1": self.theme.secondary,
    r"0": self.theme.accent
})

# 平滑无缝变形转换
self.stepwise_tex_transform(old_formula, new_formula, run_time=1.2)
```

### 3.3 纯粹单行自适应字幕与毫秒级语画同步
- **单行规范 (Strict Single-Line)**：底部字幕永远保持纯粹单行，杜绝笨重的双行占用纵向画面；
- **智能自适应字号**：
  - $\le 22$ 字：`20pt` 标准典雅
  - $22 \sim 30$ 字：`17.5pt` 精致小巧
  - $> 30$ 字：`15.5pt` 紧凑内敛
  - 底层配备 `scale_to_fit_width(11.2)`，**从物理上 100% 杜绝文字超出屏幕**。
- **语画同步用法**：
```python
with self.voiceover("当时间行进到圆周率派，动点刚好抵达实轴负一。") as tracker:
    # 动画时长自动与实际语音音频时长完全对齐！
    self.play(dot.animate(run_time=tracker.duration).move_to(target_pos))
```

### 3.4 电影级动态运镜与 3D HUD 抬头显示屏
- **`MovingCameraMathScene`**：
  ```python
  self.camera_zoom_to(target_mobject, scale_factor=0.6, run_time=1.5)  # 平滑特写推镜
  self.camera_pan_to(another_mobject, run_time=1.2)                     # 平移追踪
  self.camera_reset(run_time=1.0)                                       # 镜头拉回避全景
  ```
- **`ThreeDMathScene` (3D 沉浸式曲面)**：
  - `add_fixed_in_frame_mobjects(title, hud_panel)`：将 2D 标题、计分板、参数 HUD 牢牢锁定在屏幕前，不随 3D 摄像机翻转；
  - `start_orbital_flight(speed=0.15)`：摄像机如无人机般环绕 3D 曲面平滑巡航巡检。

### 3.5 LayoutGuard 空间碰撞与视口越界防护
```python
# 1. 扫描当前屏幕是否发生元素重叠
self.scan_collisions()

# 2. 自动边界防护：若目标被动画移出屏幕外，自动将其推回安全边界内
self.keep_in_bounds(formula)

# 3. 智能避让：顺着 DOWN 方向将 formula 推开，直到完全脱离 obstacles
self.avoid_overlap(formula, [axes, circle], direction=DOWN, buff=0.35)
```

### 3.6 高阶数学直觉组件库 (Intuition Rigs)
位于 `skills/manim-video/templates/math_rigs.py`：
- **`DynamicTangentRig`**：动态切线追踪装置（支持斜率直角三角形跟随与数值更新）；
- **`DynamicRiemannRig`**：动态黎曼和柱状分割（支持从矩形到极限曲线平滑过渡）；
- **`LinearTransformRig`**：二维矩阵网格动态剪切/旋转变形，带面积守恒平行四边形；
- **`FourierCirclesRig`**：傅里叶周转圆环串联装置；
- **`OrganicMotion.spring_bounce`**：自然弹簧阻尼速率。

---

## 4. 生产与效能工具链

### 4.1 0.5秒单帧快速质检 (Fast Inspector)
开发排版过程中，无需花费数十秒等待完整视频渲染，0.5 秒直接输出末帧或指定帧排版图片：
```bash
python skills/manim-video/scripts/fast_inspector.py demo_project/scene_01_intro.py Scene01Intro
```
图片将保存在 `media/images/...` 下，便于秒级核验文字是否出界或重合。

### 4.2 离线交互式 Web 故事板看板 (Storyboard Generator)
一键扫描指定分幕，自动提取所有 Scene 的关键帧缩略图与口播字幕台词，生成一个完全独立的响应式 HTML 看板：
```bash
python skills/manim-video/scripts/storyboard_generator.py \
  --scenes demo_project/scene_01_intro.py:Scene01Intro demo_project/scene_02_proof.py:Scene02Proof \
  --output storyboard.html
```
双击生成的 `storyboard.html`，即可在任何浏览器中像电影分镜墙一样审阅整部视频的视觉与解说流！

### 4.3 批量全自动渲染与无损拼接 (Render Manager)
告别手动合成多段视频：
```bash
# 低清快速拼接预览 (-ql)
python skills/manim-video/scripts/render_manager.py --action pipeline --quality l \
  --scenes scene_01.py:Scene01 scene_02.py:Scene02 --output preview.mp4

# 高清母带级导出 (-qh, 1080p 60fps)
python skills/manim-video/scripts/render_manager.py --action pipeline --quality h \
  --scenes scene_01.py:Scene01 scene_02.py:Scene02 --output master_final.mp4
```

---

## 5. 实战样板全流程教学 (从零到成片)

以经典的 **毕达哥拉斯勾股定理证明** 为例（完整源码见 `demo_project/`）：

1. **分幕解耦**：
   - `scene_01_intro.py` (Scene01Intro)：引入直角三角形与三边正方形；
   - `scene_02_proof.py` (Scene02Proof)：边长 $(a+b)$ 的大正方形几何重拼对称消去；
   - `scene_03_summary.py` (Scene03Summary)：高光顿悟时刻，$a^2 + b^2 = c^2$ 聚焦。
2. **执行一键高清渲染**：
   ```bash
   cd demo_project
   python ../skills/manim-video/scripts/render_manager.py --action pipeline --quality h \
     --scenes scene_01_intro.py:Scene01Intro scene_02_proof.py:Scene02Proof scene_03_summary.py:Scene03Summary \
     --output demo_pythagoras.mp4
   ```
3. **输出成品**：得到无损拼接的高清最终成片 `demo_pythagoras.mp4`！

---

## 6. 常见疑难排查与避坑指南 (FAQ)

### Q1: 中文字体显示为方块或乱码怎么办？
- **原因**：Manim 默认的英文字体不包含中文字库。
- **解法**：`BaseMathScene` 已经默认注入了 `font="Microsoft YaHei"`（Windows）与通用中文字体后备。如果在 Linux 或 macOS 环境，请确保系统已安装 `Noto Sans CJK SC` 或 `PingFang SC`。

### Q2: 公式编译报错 `LaTeX Error` 或找不到 `dvisvgm`？
- **解法**：
  1. 运行 `python skills/manim-video/scripts/check_env.py` 检查 LaTeX 状态；
  2. 确保已安装 MiKTeX 或 TeX Live，且 `latex` 与 `dvisvgm` 所在路径已添加到系统 `PATH` 环境变量中。

### Q3: 为什么不建议在数学视频中加嘈杂的背景音乐？
- **答**：根据 3Blue1Brown 及认知科学研究，复杂的数学公式推导对观众的心智带宽要求极高。劣质或旋律突兀的背景音乐会严重分散注意力。本套件倡导纯净人声解说与克制几何动态，直击数学本质。

### Q4: 怎样给仓库贡献新的数学 Rig 装置？
- 非常欢迎！请在 `skills/manim-video/templates/math_rigs.py` 中编写基于 `VGroup` 与 `always_redraw` 的参数化装置，并在 `projects/` 下提交对应的测试场景，发起 Pull Request 即可。

---

*让严谨的数学规律在动态几何与代码的交融中，展现出最动人心魄的美！*
