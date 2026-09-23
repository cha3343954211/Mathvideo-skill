"""
Scene 03: 高光顿悟与代数呼应 (The Aha! Moment & Synthesis)
剥离相同元素，留下终极公式，聚光灯强调。
"""
from manim import *
from theme_config import BaseMathScene, MathTheme

class Scene03Summary(BaseMathScene):
    def construct(self):
        super().construct()
        
        self.play_show_title("高光时刻：等量减等量，差必相等", "The Core Insight")
        self.set_caption("两边的大正方形面积完全相同，且各自包含 4 个完全一样的三角形...")
        
        # 居中展示核心公式的诞生
        eq_raw = MathTex(
            r"(a+b)^2 - 4 \times \frac{1}{2}ab",
            r"=",
            r"(a+b)^2 - 4 \times \frac{1}{2}ab",
            font_size=36
        )
        eq_raw.shift(UP * 0.8)
        
        self.play(Write(eq_raw), run_time=1.5)
        self.pause(1.2)
        
        self.set_caption("扣除 4 个三角形后，左侧剩下 c²，右侧剩下 a² + b²")
        
        # 转化为最终公式
        final_eq = MathTex(
            r"c^2", r"=", r"a^2", r"+", r"b^2",
            font_size=56
        )
        final_eq.shift(DOWN * 0.5)
        final_eq[0].set_color(MathTheme.YELLOW)
        final_eq[2].set_color(MathTheme.BLUE)
        final_eq[4].set_color(MathTheme.ORANGE)
        
        self.play(
            ReplacementTransform(eq_raw, final_eq),
            run_time=1.5
        )
        self.pause(1.0)
        
        # 高光聚光灯效果 (调用 BaseMathScene 的 focus_on 方法)
        self.set_caption("这就是流传千古的勾股定理：a² + b² = c²")
        self.focus_on(final_eq, color=MathTheme.YELLOW, scale_factor=1.12)
        self.pause(2.0)
        
        # 收尾谢幕
        thank_you = self.make_text("数学之美，在于一目了然的直觉", font_size=32, color=MathTheme.TEXT_MUTED)
        thank_you.next_to(final_eq, DOWN, buff=0.8)
        self.play(FadeIn(thank_you, shift=UP * 0.3), run_time=1.0)
        self.pause(2.5)
