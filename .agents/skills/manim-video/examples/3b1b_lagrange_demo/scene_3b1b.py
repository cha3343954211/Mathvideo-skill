"""
scene_3b1b.py: 3Blue1Brown 标志性视觉美学示范场景
《拉格朗日中值定理：动态几何与算式共鸣》
包含 3b1b 核心支柱：
1. 暗黑微调底色 (#171717) 与柔和坐标网格
2. 四原色精准映射：天青蓝曲线/割线、明黄水平差与标尺、鲜红高度差与标尺、翡翠绿瞬时切线
3. 几何与算式像素级色彩对应
4. Dynamic Rig: ValueTracker + always_redraw 切线动态平滑扫掠与实时斜率读数
5. 瞬时平行共振高光脉冲 (Flash & Pulse)
6. 手绘聚焦圆角矩形 SurroundingRectangle 与弧线箭头 CurvedArrow
7. 电影级平滑聚焦运镜
8. 零破壁解说词，纯数学沉浸
"""
import sys
import numpy as np
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_TEMPLATES = REPO_ROOT / "skills" / "manim-video" / "templates"
sys.path.insert(0, str(SKILL_TEMPLATES))

from manim import *
from base_scene import MovingCameraMathScene, THEMES
from math_rigs import OrganicMotion

# 3Blue1Brown 经典色彩定义
COLOR_BG = "#171717"
COLOR_CURVE = "#58C4DD"       # 3b1b 天青蓝 (Blue C)
COLOR_SECANT = "#38BDF8"      # 割线明蓝
COLOR_DX = "#FACC15"          # 3b1b 明黄 (Yellow C - 水平底边与分母)
COLOR_DY = "#FC6255"          # 3b1b 珊瑚红 (Red C - 垂直对边与分子)
COLOR_TANGENT = "#83C167"     # 3b1b 翡翠绿 (Green C - 瞬时切线与导数)
COLOR_FOCUS = "#FBBF24"       # 金黄高光


class Scene3B1BLagrangeDemo(MovingCameraMathScene):
    DEFAULT_THEME = "3b1b_dark"
    ENABLE_VOICEOVER = True
    TTS_ENGINE = "voxcpm"
    VOICE_NAME = "zh-CN-YunyangNeural-Style (专业新闻纪录片男播音员，三十多岁，字正腔圆，沉稳大气)"

    def construct(self):
        super().construct()
        # 强制设置 3b1b 经典暗黑画布
        self.camera.background_color = COLOR_BG

        # =========================================================================
        # 0. 坐标系与函数定义
        # =========================================================================
        axes = Axes(
            x_range=[0, 7.0, 1],
            y_range=[0, 5.0, 1],
            x_length=8.2,
            y_length=4.6,
            axis_config={
                "color": "#4A5568",
                "stroke_width": 2,
                "include_tip": True,
                "tip_width": 0.16,
                "tip_height": 0.16,
            }
        ).to_corner(DL, buff=0.8).shift(UP * 0.1)

        # 3b1b 风格的微积分光滑凸起曲线 f(x)
        def func(x):
            return 0.5 + 2.2 * np.sin(0.48 * (x - 0.5)) + 0.18 * (x - 1.0)

        def dfunc(x):
            return 2.2 * 0.48 * np.cos(0.48 * (x - 0.5)) + 0.18

        curve = axes.plot(func, x_range=[0.8, 6.2], color=COLOR_CURVE, stroke_width=4.0)
        curve_label = MathTex("f(x)", color=COLOR_CURVE, font_size=32).next_to(
            axes.c2p(6.2, func(6.2)), UR, buff=0.15
        )

        # 端点 a 与 b
        xA, xB = 1.2, 5.5
        pA = axes.c2p(xA, func(xA))
        pB = axes.c2p(xB, func(xB))
        secant_slope = (func(xB) - func(xA)) / (xB - xA)

        dotA = Dot(pA, radius=0.08, color=COLOR_CURVE)
        dotB = Dot(pB, radius=0.08, color=COLOR_CURVE)
        labelA = MathTex("a", font_size=24, color=WHITE).next_to(axes.c2p(xA, 0), DOWN, buff=0.12)
        labelB = MathTex("b", font_size=24, color=WHITE).next_to(axes.c2p(xB, 0), DOWN, buff=0.12)
        v_lineA = DashedLine(axes.c2p(xA, 0), pA, color="#718096", stroke_width=1.5, dash_length=0.08)
        v_lineB = DashedLine(axes.c2p(xB, 0), pB, color="#718096", stroke_width=1.5, dash_length=0.08)

        # 割线
        secant_line = Line(
            pA - normalize(pB - pA) * 0.4,
            pB + normalize(pB - pA) * 0.4,
            color=COLOR_SECANT,
            stroke_width=3.2
        )

        # =========================================================================
        # 1. 第一幕：宏观平均变化率与几何割线
        # =========================================================================
        t1 = "对于闭区间 a 到 b 上平滑可导的函数 f，连接两端点的割线，其几何斜率刻画了函数在这段区间的平均变化率。"
        with self.voiceover(t1) as v1:
            self.play(Create(axes), run_time=1.2)
            self.play(Create(curve), FadeIn(curve_label), run_time=1.4)
            self.play(
                FadeIn(dotA, scale=0.5), FadeIn(dotB, scale=0.5),
                Create(v_lineA), Create(v_lineB),
                Write(labelA), Write(labelB),
                run_time=1.0
            )
            self.play(Create(secant_line), run_time=1.2)

        # =========================================================================
        # 2. 第二幕：3b1b 标志性色彩对应 (直角三角形 + Brace 标尺 + 割线公式)
        # =========================================================================
        # 直角三角形顶点 (xB, func(xA))
        pCorner = axes.c2p(xB, func(xA))
        line_dx = DashedLine(pA, pCorner, color=COLOR_DX, stroke_width=2.5, dash_length=0.08)
        line_dy = DashedLine(pCorner, pB, color=COLOR_DY, stroke_width=2.5, dash_length=0.08)

        # 大括号标尺
        brace_dx = Brace(line_dx, DOWN, buff=0.12, color=COLOR_DX)
        brace_dx_text = brace_dx.get_tex("b - a", buff=0.1)
        brace_dx_text.set_color(COLOR_DX).scale(0.8)

        brace_dy = Brace(line_dy, RIGHT, buff=0.12, color=COLOR_DY)
        brace_dy_text = brace_dy.get_tex("f(b) - f(a)", buff=0.1)
        brace_dy_text.set_color(COLOR_DY).scale(0.8)

        # 右上方公式：纯正 3b1b 色彩对应 (拆解式精准色彩映射)
        formula_avg = MathTex(
            r"\text{Average Slope} = \frac{",
            r"f(b) - f(a)",
            r"}{",
            r"b - a",
            r"}",
            font_size=34
        ).to_corner(UR, buff=0.7).shift(DOWN * 0.2)
        formula_avg[0].set_color("#E2E8F0")
        formula_avg[1].set_color(COLOR_DY)
        formula_avg[2].set_color("#E2E8F0")
        formula_avg[3].set_color(COLOR_DX)
        formula_avg[4].set_color("#E2E8F0")

        t2 = "垂直增量 f(b) 减 f(a) 除以水平跨度 b 减 a，在代数上给出了差商，与割线斜率严格对应。"
        with self.voiceover(t2) as v2:
            self.play(
                Create(line_dx),
                Create(brace_dx),
                FadeIn(brace_dx_text, shift=UP * 0.1),
                run_time=1.2
            )
            self.play(
                Create(line_dy),
                Create(brace_dy),
                FadeIn(brace_dy_text, shift=LEFT * 0.1),
                run_time=1.2
            )
            self.play(Write(formula_avg), run_time=1.4)

        # =========================================================================
        # 3. 第三幕：动态机械联动 (ValueTracker 切线平滑扫掠 + 实时斜率读数)
        # =========================================================================
        # 寻找斜率相等的理论点 xi_exact
        # dfunc(x) = secant_slope => 解出 xi
        xi_val = 3.12  # 在凸峰稍偏右侧处导数等于割线斜率
        tracker = ValueTracker(1.5)

        # 动点与切线装置
        dot_tan = always_redraw(lambda: Dot(
            axes.c2p(tracker.get_value(), func(tracker.get_value())),
            radius=0.08,
            color=COLOR_TANGENT
        ))

        def get_tangent_line():
            x = tracker.get_value()
            p0 = axes.c2p(x, func(x))
            slope = dfunc(x)
            p_right = axes.c2p(x + 0.5, func(x) + slope * 0.5)
            tangent_dir = normalize(p_right - p0)
            return Line(
                p0 - tangent_dir * 1.6,
                p0 + tangent_dir * 1.6,
                color=COLOR_TANGENT,
                stroke_width=3.2
            )

        dynamic_tangent = always_redraw(get_tangent_line)

        v_proj_tan = always_redraw(lambda: DashedLine(
            axes.c2p(tracker.get_value(), 0),
            axes.c2p(tracker.get_value(), func(tracker.get_value())),
            color=COLOR_TANGENT,
            stroke_width=1.5,
            dash_length=0.07
        ))

        # 实时斜率动态徽标
        slope_badge = always_redraw(lambda: MathTex(
            f"f'(x) = {dfunc(tracker.get_value()):.2f}",
            font_size=24,
            color=COLOR_TANGENT
        ).next_to(
            axes.c2p(tracker.get_value(), func(tracker.get_value())),
            UL,
            buff=0.15
        ))

        t3 = "在区间内部取一点滑动观察，每个位置切线的倾斜程度，恰好是函数在该点的瞬时导数 f'(x)。"
        with self.voiceover(t3) as v3:
            self.play(
                FadeIn(dot_tan, scale=0.6),
                Create(dynamic_tangent),
                Create(v_proj_tan),
                FadeIn(slope_badge),
                run_time=1.2
            )
            # 连续平滑扫描：从 1.5 滑动到 2.4，切线角度连续倾斜改变
            self.play(tracker.animate.set_value(2.4), run_time=2.2, rate_func=linear)

        # =========================================================================
        # 4. 第四幕：捕获平行共鸣与拉格朗日终极公式
        # =========================================================================
        t4 = "容易注意到，必然存在一个点 xi，那里的切线与割线完全平行，也就是瞬时导数精确等于平均斜率。"
        with self.voiceover(t4) as v4:
            # 平滑滑向平行点 xi_val = 3.12
            self.play(tracker.animate.set_value(xi_val), run_time=1.8, rate_func=smooth)
            self.wait(0.2)

            # 瞬时共振：切线与割线爆发脉冲呼吸高光！
            p_xi = axes.c2p(xi_val, func(xi_val))
            label_xi = MathTex(r"\xi", font_size=28, color=COLOR_TANGENT).next_to(
                axes.c2p(xi_val, 0), DOWN, buff=0.12
            )

            # 平行几何双斜杠标记
            p_mid_sec = (pA + pB) / 2
            p_mid_tan = p_xi
            parallel_mark1 = MathTex(r"\parallel", font_size=32, color=COLOR_FOCUS).move_to(
                (p_mid_sec + p_mid_tan) / 2 + RIGHT * 0.4
            )

            self.play(
                Write(label_xi),
                FadeIn(parallel_mark1, scale=1.2),
                OrganicMotion.pulse_glow(secant_line, color=COLOR_FOCUS, run_time=0.8),
                OrganicMotion.pulse_glow(dynamic_tangent, color=COLOR_FOCUS, run_time=0.8),
            )

        # 镜头平滑微推聚焦到平行接触面
        t5 = "这就是拉格朗日中值定理：它将局部的瞬时导数值，与区间的整体差商紧密统一了起来。"
        with self.voiceover(t5) as v5:
            # 运镜微推 (3b1b 经典微观聚焦)
            self.camera_zoom_to(p_xi, scale_factor=0.8, run_time=1.2)

            # 终极公式演进与手绘圆角矩形聚焦
            formula_lagrange = MathTex(
                r"f'(\xi)",
                r" = \frac{",
                r"f(b) - f(a)",
                r"}{",
                r"b - a",
                r"}",
                font_size=38
            ).move_to(formula_avg.get_center())
            formula_lagrange[0].set_color(COLOR_TANGENT)
            formula_lagrange[1].set_color(WHITE)
            formula_lagrange[2].set_color(COLOR_DY)
            formula_lagrange[3].set_color(WHITE)
            formula_lagrange[4].set_color(COLOR_DX)
            formula_lagrange[5].set_color(WHITE)

            # 镜头拉回全景
            self.camera_reset(run_time=1.2)

            self.play(
                ReplacementTransform(formula_avg, formula_lagrange),
                run_time=1.2
            )

            # 3b1b 手绘感聚焦圆角矩形
            focus_box = SurroundingRectangle(
                formula_lagrange,
                color=COLOR_FOCUS,
                buff=0.18,
                corner_radius=0.12,
                stroke_width=2.5
            )

            # 优雅弧线箭头 CurvedArrow 从公式直指平行切点
            arrow_to_tangent = CurvedArrow(
                focus_box.get_left() + LEFT * 0.1,
                p_xi + UR * 0.25,
                angle=-0.4,
                color=COLOR_FOCUS,
                stroke_width=2.5,
                tip_length=0.18
            )

            self.play(
                Create(focus_box),
                Create(arrow_to_tangent),
                run_time=1.4
            )
            self.wait(1.5)
