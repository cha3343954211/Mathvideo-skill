"""
Scene 01: 动切线追踪与导数极值探索 (Nord 极光主题)
展示:
1. DynamicTangentRig: 动点与切线自适应追踪，导数数值实时计算与联动
2. FormulaRig: 公式智能局部着色与平滑推导演化
3. OrganicMotion: 极值点处的弹性物理回弹
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import NordScene, DynamicTangentRig, OrganicMotion

class DynamicDerivativeScene(NordScene):
    def construct(self):
        super().construct()

        # 1. 标题与引入
        self.play_show_title("微积分之眼：动态切线与瞬时变化率", "Dynamic Tangent Rig & Nord Theme")
        self.set_caption("导数的本质，是切线斜率随着曲线上点位置的瞬时演变。")

        # 2. 坐标系与函数构建
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 4, 1],
            x_length=7.5,
            y_length=5.0,
            axis_config={
                "color": self.theme.grid_color,
                "stroke_width": 2,
                "include_numbers": False
            }
        ).shift(DOWN * 0.4 + LEFT * 1.5)

        # 曲线 f(x) = 0.25*x^3 - x + 0.5
        func = lambda x: 0.25 * (x**3) - x + 0.5
        graph = axes.plot(func, x_range=[-2.8, 2.8], color=self.theme.primary, stroke_width=3.5)
        
        # 函数标签 (智能公式着色)
        func_label = self.make_math(r"f(x) = \frac{1}{4}x^3 - x + \frac{1}{2}", font_size=28)
        self.colorize_formula(func_label, {
            r"f(x)": self.theme.primary,
            r"x^3": self.theme.accent,
            r"x": self.theme.secondary
        })
        func_label.to_corner(UR, buff=0.8).shift(LEFT * 0.5)

        self.play(Create(axes), Create(graph), FadeIn(func_label, shift=LEFT * 0.3), run_time=1.5)
        self.pause(0.5)

        # 3. 装配 DynamicTangentRig (数学交互装置)
        self.set_caption("装配动切线机械装置：切线方向与斜率数值随动点实时联动。")
        x_tracker = ValueTracker(-2.2)

        rig = DynamicTangentRig(
            axes=axes,
            func=func,
            tracker=x_tracker,
            tangent_length=3.2,
            tangent_color=self.theme.secondary,  # 冰河深蓝 / 暖调对比
            dot_color=self.theme.accent,         # 极光金黄
            show_slope_label=True,
            show_projections=True,
            decimal_places=2
        )

        self.play(FadeIn(rig), run_time=1.0)
        self.pause(0.5)

        # 4. 连续滑动动点：展现斜率动态演变
        self.set_caption("当动点沿曲线向右滑动，切线斜率 k 连续平滑变化。")
        self.play(x_tracker.animate.set_value(-1.15), run_time=2.5, rate_func=linear)

        # 5. 到达局部极大值点 (极值处 k ≈ 0)
        self.set_caption("在极大值极值点处，切线完全水平，瞬时导数斜率降为零！")
        self.play(x_tracker.animate.set_value(-1.1547), run_time=0.8, rate_func=smooth)
        self.pause(0.4)

        # 触发 OrganicMotion 弹性冲激与高亮
        self.play(OrganicMotion.spring_bounce(rig.dot, scale_factor=1.6, run_time=0.7))
        self.pause(0.6)

        # 6. 继续滑动穿过拐点到达极小值点
        self.set_caption("穿越拐点，切线迅速由负转正，再次在极小值点归零。")
        self.play(x_tracker.animate.set_value(1.1547), run_time=3.0, rate_func=smooth)
        self.play(OrganicMotion.pulse_glow(rig.dot, color=self.theme.alert, scale=1.5, run_time=0.8))
        self.pause(0.5)

        # 7. 公式平滑渐变演化 (stepwise_tex_transform)
        self.set_caption("这就是导数公式的几何真理：f'(x) 严丝合缝地描述了切线斜率。")
        deriv_label = self.make_math(r"f'(x) = \frac{3}{4}x^2 - 1", font_size=28)
        self.colorize_formula(deriv_label, {
            r"f'(x)": self.theme.secondary,
            r"x^2": self.theme.accent
        })
        self.stepwise_tex_transform(func_label, deriv_label, run_time=1.4)
        self.pause(1.2)

        # 优雅淡出
        self.set_caption("高阶机械装置与动态物理质感，赋予数学公式鲜活的生命力。")
        self.pause(1.0)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(rig), FadeOut(deriv_label), run_time=1.2)
