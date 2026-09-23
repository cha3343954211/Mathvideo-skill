"""
Scene 01: 智能排版与包围盒碰撞检测器 (LayoutGuard 实战)
展示:
1. 空间碰撞雷达自动检测 (扫描重叠侵入并打印报告)
2. 安全视口边界收敛 (超长公式防切边溢出自动缩放)
3. 动态智能安全避让 (顺延推移直至完全脱离障碍物，实现自然留白)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import NordScene, LayoutGuard, OrganicMotion

class SafeLayoutScene(NordScene):
    def construct(self):
        super().construct()

        # 1. 标题与引入
        self.play_show_title("智能排版卫士：碰撞检测与边界守护", "LayoutGuard Collision Radar & Auto Avoidance")
        self.set_caption("数学视频的核心挑战之一：避免复杂公式、图表与字幕之间的相互遮挡。")

        # 2. 放置左侧核心图表 (Axes + Graph)
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 4, 1],
            x_length=5.5,
            y_length=4.0,
            axis_config={"color": self.theme.grid_color, "stroke_width": 2}
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)

        func = lambda x: 0.5 * (x**2) + 0.3
        graph = axes.plot(func, color=self.theme.primary, stroke_width=3.5)
        graph_label = self.make_math("y = f(x)", font_size=24, color=self.theme.primary)
        graph_label.next_to(axes.c2p(2.2, func(2.2)), UR, buff=0.1)

        chart_group = VGroup(axes, graph, graph_label)
        self.play(Create(axes), Create(graph), FadeIn(graph_label), run_time=1.2)
        self.pause(0.5)

        # 3. 引入超长泰勒展开公式 (演示自动安全边界防溢出)
        self.set_caption("防溢出机制：当遇到超长推导公式时，自动约束在屏幕安全边界内。")
        long_formula = self.make_math(
            r"f(x) = f(x_0) + f'(x_0)(x - x_0) + \frac{f''(x_0)}{2!}(x - x_0)^2 + \frac{f'''(x_0)}{3!}(x - x_0)^3 + \cdots + R_n(x)",
            font_size=32,
            color=self.theme.text_main
        )
        self.colorize_formula(long_formula, {
            r"f(x)": self.theme.primary,
            r"f'(x_0)": self.theme.secondary,
            r"f''(x_0)": self.theme.accent
        })
        long_formula.to_edge(UP, buff=1.3)

        # 调用 keep_in_bounds 进行安全约束
        self.keep_in_bounds(long_formula, safe_margin=0.6)
        self.play(FadeIn(long_formula, shift=DOWN * 0.2), run_time=1.0)
        self.pause(0.5)

        # 4. 演示元素碰撞检测 (故意生成一块与左侧图表重叠的解释卡片)
        self.set_caption("雷达扫描：当新生成的数学对象与已有图表发生空间侵入时，系统发出预警。")
        info_text = self.make_text("核心判据：二阶导数恒大于零，函数呈现严格凸性。", font_size=22, color=self.theme.accent)
        # 初始故意放在左侧图表上方区域，形成空间压盖
        info_text.move_to(axes.get_center() + UP * 0.5)

        self.play(FadeIn(info_text), run_time=0.8)
        self.pause(0.4)

        # 执行全场景空间碰撞扫描
        collisions = self.scan_collisions(verbose=True)
        if collisions:
            # 视觉上展示碰撞告警框
            alert_box = SurroundingRectangle(info_text, color=self.theme.alert, buff=0.1)
            self.play(Create(alert_box), run_time=0.4)
            self.play(OrganicMotion.wiggle_alert(info_text, run_time=0.8))
            self.pause(0.5)
            self.play(FadeOut(alert_box), run_time=0.3)

        # 5. 调用 avoid_overlap 进行智能避让推移
        self.set_caption("智能安全避让：算法自动将对象平滑推移至右侧安全无干扰空白区。")
        # 顺着 RIGHT 方向推移出 chart_group
        target_pos = self.avoid_overlap(info_text.copy(), [chart_group, long_formula], direction=RIGHT, buff=0.5)
        target_pos.to_edge(RIGHT, buff=0.8).shift(UP * 0.5)

        self.play(info_text.animate.move_to(target_pos.get_center()), run_time=1.2, rate_func=smooth)
        self.play(OrganicMotion.pulse_glow(info_text, color=self.theme.success, scale=1.06, run_time=0.6))
        self.pause(0.4)

        # 6. 在右侧追加结论推导 (再次自动保证上下间距)
        conclusion_tex = self.make_math(r"\implies \min f(x) = f(x_0)", font_size=30, color=self.theme.success)
        conclusion_tex.next_to(info_text, DOWN, buff=0.6)
        self.play(FadeIn(conclusion_tex, shift=UP * 0.2), run_time=0.8)
        self.pause(0.5)

        # 7. 再次执行碰撞雷达扫描：已恢复 100% 空间健康度
        self.set_caption("复检通过：全场景元素各自舒展，呈现极高可读性与呼吸感留白。")
        self.scan_collisions(verbose=True)
        self.pause(1.5)

        # 优雅淡出
        self.play(FadeOut(chart_group), FadeOut(long_formula), FadeOut(info_text), FadeOut(conclusion_tex), run_time=1.2)
