"""
Scene 02: 黎曼积分无限细分逼近 (Chalkboard 经典常春藤黑板粉笔主题)
展示:
1. Chalkboard 黑板粉笔质感配色
2. DynamicRiemannRig: 离散矩形向连续微积分面积的平滑极限逼近
3. OrganicMotion: 逼近完成时的高光呼吸
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import ChalkboardScene, DynamicRiemannRig, OrganicMotion

class RiemannChalkboardScene(ChalkboardScene):
    def construct(self):
        super().construct()

        # 1. 标题与引入
        self.play_show_title("微积分之源：黎曼和与无限逼近", "Riemann Sum Rig & Chalkboard Style")
        self.set_caption("经典黑板粉笔风格下，探寻离散矩形走向连续定积分的极限过程。")

        # 2. 坐标系与函数构建
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=7.0,
            y_length=4.5,
            axis_config={
                "color": self.theme.grid_color,
                "stroke_width": 2,
                "include_numbers": False
            }
        ).shift(DOWN * 0.4 + LEFT * 1.5)

        # 曲线 f(x) = -0.3*(x-1.8)^2 + 2.8
        func = lambda x: -0.35 * ((x - 1.8) ** 2) + 2.8
        graph = axes.plot(func, x_range=[0.3, 3.7], color=self.theme.primary, stroke_width=3.5)

        curve_label = self.make_math(r"y = f(x)", font_size=28, color=self.theme.primary)
        curve_label.next_to(axes.c2p(2.6, func(2.6)), UR, buff=0.15)

        self.play(Create(axes), Create(graph), FadeIn(curve_label), run_time=1.5)
        self.pause(0.5)

        # 3. 初始低细分矩形 (n = 4)
        self.set_caption("当我们将区间粗糙划分为 4 个矩形时，与真实面积存在明显锯齿误差。")
        n_tracker = ValueTracker(4)

        riemann_rig = DynamicRiemannRig(
            axes=axes,
            func=func,
            x_range=[0.5, 3.5],
            n_tracker=n_tracker,
            color_scheme=(self.theme.secondary, self.theme.success),
            fill_opacity=0.65,
            stroke_width=1.2,
            show_area_label=True
        )

        self.play(FadeIn(riemann_rig), run_time=1.0)
        self.pause(1.0)

        # 4. 动态细分：从 n=4 递增到 n=12
        self.set_caption("增加划分密度：矩形不断变窄，锯齿空隙迅速缩小。")
        self.play(n_tracker.animate.set_value(12), run_time=2.0, rate_func=smooth)
        self.pause(0.6)

        # 5. 极限逼近：从 n=12 递增到 n=40
        self.set_caption("当 n 逼近无穷，离散阶梯完全贴合光滑曲线——这便是定积分的诞生！")
        self.play(n_tracker.animate.set_value(40), run_time=3.0, rate_func=smooth)
        self.pause(0.5)

        # 6. 定积分公式顿悟展开
        integral_tex = self.make_math(r"\lim_{n \to \infty} \sum_{i=1}^n f(x_i)\Delta x = \int_a^b f(x)\,dx", font_size=26)
        self.colorize_formula(integral_tex, {
            r"\sum": self.theme.accent,
            r"\int": self.theme.secondary,
            r"f(x)": self.theme.primary
        })
        integral_tex.next_to(riemann_rig.status_label, DOWN, buff=0.4, aligned_edge=RIGHT)

        self.play(FadeIn(integral_tex, shift=UP * 0.2), run_time=1.0)
        self.play(OrganicMotion.spring_bounce(integral_tex, scale_factor=1.1, run_time=0.6))
        self.pause(1.5)

        # 优雅淡出
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(riemann_rig), FadeOut(curve_label), FadeOut(integral_tex), run_time=1.2)
