"""
Scene 02 (Claude 标志性浅色米纸风格): 集合相等的双向奔赴 (Proving A = B)
浅米背景 + 石板蓝与赤陶橙 -> 鼠尾草绿融合 + 暖金琥珀法则。
"""
from manim import *
from theme_config import ClaudeLightScene, ClaudeLightTheme

class Scene02Equality(ClaudeLightScene):
    def construct(self):
        super().construct()
        
        self.play_show_title("集合相等的本质：双向奔赴", "Two-Way Inclusion: Proving A = B")
        self.set_caption("两个集合怎样才算真正相等？在数学证明中，必须完成一场‘双向奔赴’...")
        
        # 1. 左右两个纯粹集合圆
        c_left = Circle(radius=1.2, color=ClaudeLightTheme.SLATE_BLUE, fill_opacity=0.2, stroke_width=3)
        c_left.shift(LEFT * 3.0 + DOWN * 0.2)
        txt_l = self.make_math(r"A \subseteq B", font_size=38, color=ClaudeLightTheme.SLATE_BLUE).next_to(c_left, UP, buff=0.25)
        grp_l = VGroup(c_left, txt_l)
        
        c_right = Circle(radius=1.2, color=ClaudeLightTheme.TERRACOTTA, fill_opacity=0.2, stroke_width=3)
        c_right.shift(RIGHT * 3.0 + DOWN * 0.2)
        txt_r = self.make_math(r"B \subseteq A", font_size=38, color=ClaudeLightTheme.TERRACOTTA).next_to(c_right, UP, buff=0.25)
        grp_r = VGroup(c_right, txt_r)
        
        self.play(FadeIn(grp_l), FadeIn(grp_r), run_time=1.0)
        self.pause(1.2)
        
        # 2. 两个圆向中心聚拢，重合融合成一个鼠尾草绿大圆
        self.set_caption("若 A 包含于 B，同时 B 也包含于 A，则两者的边界完全重合！")
        
        c_green = Circle(radius=1.4, color=ClaudeLightTheme.SAGE_GREEN, fill_color=ClaudeLightTheme.SAGE_GREEN, fill_opacity=0.25, stroke_width=3.5)
        c_green.shift(DOWN * 0.2)
        
        self.play(
            c_left.animate.move_to(DOWN * 0.2).scale(1.15),
            c_right.animate.move_to(DOWN * 0.2).scale(1.15),
            txt_l.animate.shift(RIGHT * 1.5 + UP * 0.8),
            txt_r.animate.shift(LEFT * 1.5 + UP * 0.8),
            run_time=1.4
        )
        self.play(
            FadeIn(c_green),
            FadeOut(c_left), FadeOut(c_right),
            run_time=0.6
        )
        self.pause(0.8)
        
        # 3. 左右分屏：鼠尾草绿圆平移至左侧，右侧展开核心充要条件
        self.set_caption("高中证明 A = B 永恒的核心范式：分两步证明 A ⊆ B 与 B ⊆ A！")
        
        target_circle_pos = LEFT * 3.2 + DOWN * 0.2
        lbl_circle = self.make_math("A = B", color=ClaudeLightTheme.SAGE_GREEN, font_size=38).move_to(target_circle_pos)
        
        f_cond1 = self.make_math(r"A \subseteq B", font_size=38, color=ClaudeLightTheme.SLATE_BLUE)
        f_and = self.make_math(r"\land", font_size=34, color=ClaudeLightTheme.TEXT_MUTED)
        f_cond2 = self.make_math(r"B \subseteq A", font_size=38, color=ClaudeLightTheme.TERRACOTTA)
        top_row = VGroup(f_cond1, f_and, f_cond2).arrange(RIGHT, buff=0.25)
        
        arrow_down = self.make_math(r"\Updownarrow", font_size=44, color=ClaudeLightTheme.WARM_AMBER)
        f_final = self.make_math(r"A = B", font_size=56, color=ClaudeLightTheme.WARM_AMBER)
        
        right_logic = VGroup(top_row, arrow_down, f_final).arrange(DOWN, buff=0.35).shift(RIGHT * 2.2 + DOWN * 0.2)
        
        self.play(
            FadeOut(txt_l), FadeOut(txt_r),
            c_green.animate.move_to(target_circle_pos),
            run_time=0.8
        )
        self.play(Write(lbl_circle), Write(top_row), run_time=1.0)
        self.play(Write(arrow_down), Write(f_final), run_time=1.0)
        self.pause(0.8)
        
        # 暖金琥珀聚焦
        self.focus_on(f_final, color=ClaudeLightTheme.TERRACOTTA, scale_factor=1.15)
        self.pause(1.8)
        
        # 清除过渡
        self.clear_caption()
        self.play(
            *[FadeOut(m) for m in [c_green, lbl_circle, right_logic, self.title_mobject]],
            run_time=0.6
        )
