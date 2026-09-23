"""
Scene 02 (Claude 典雅人文风格): 集合相等的双向奔赴 (Proving A = B)
石板蓝 + 赤陶橙 -> 鼠尾草绿优雅融合，暖琥珀金充要法则。
"""
from manim import *
from theme_config import ClaudeScene, ClaudeTheme

class Scene02Equality(ClaudeScene):
    def construct(self):
        super().construct()
        
        self.play_show_title("集合相等的本质：双向奔赴", "Two-Way Inclusion: Proving A = B")
        self.set_caption("两个集合怎样才算真正相等？在数学证明中，必须完成一场‘双向奔赴’...")
        
        # 1. 左右两个纯粹集合圆
        c_left = Circle(radius=1.2, color=ClaudeTheme.SLATE_BLUE, fill_opacity=0.35, stroke_width=3)
        c_left.shift(LEFT * 3.0 + DOWN * 0.2)
        txt_l = MathTex(r"A \subseteq B", font_size=38, color=ClaudeTheme.SLATE_BLUE).next_to(c_left, UP, buff=0.25)
        grp_l = VGroup(c_left, txt_l)
        
        c_right = Circle(radius=1.2, color=ClaudeTheme.TERRACOTTA, fill_opacity=0.35, stroke_width=3)
        c_right.shift(RIGHT * 3.0 + DOWN * 0.2)
        txt_r = MathTex(r"B \subseteq A", font_size=38, color=ClaudeTheme.TERRACOTTA).next_to(c_right, UP, buff=0.25)
        grp_r = VGroup(c_right, txt_r)
        
        self.play(FadeIn(grp_l), FadeIn(grp_r), run_time=1.0)
        self.pause(1.2)
        
        # 2. 两个圆向中心聚拢，重合融合成一个鼠尾草绿大圆
        self.set_caption("若 A 包含于 B，同时 B 也包含于 A，则两者的边界完全重合！")
        
        c_green = Circle(radius=1.4, color=ClaudeTheme.SAGE_GREEN, fill_color=ClaudeTheme.SAGE_GREEN, fill_opacity=0.4, stroke_width=3.5)
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
        
        # 3. 左右分屏：鼠尾草绿圆平移至左侧，右侧优雅展开核心充要条件
        self.set_caption("高中证明 A = B 永恒的核心范式：分两步证明 A ⊆ B 与 B ⊆ A！")
        
        target_circle_pos = LEFT * 3.2 + DOWN * 0.2
        lbl_circle = MathTex("A = B", color=ClaudeTheme.SAGE_GREEN, font_size=38).move_to(target_circle_pos)
        
        f_cond1 = MathTex(r"A \subseteq B", font_size=38, color=ClaudeTheme.SLATE_BLUE)
        f_and = MathTex(r"\land", font_size=34, color=ClaudeTheme.TEXT_MUTED)
        f_cond2 = MathTex(r"B \subseteq A", font_size=38, color=ClaudeTheme.TERRACOTTA)
        top_row = VGroup(f_cond1, f_and, f_cond2).arrange(RIGHT, buff=0.25)
        
        arrow_down = MathTex(r"\Updownarrow", font_size=44, color=ClaudeTheme.WARM_AMBER)
        f_final = MathTex(r"A = B", font_size=56, color=ClaudeTheme.WARM_AMBER)
        
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
        self.focus_on(f_final, color=ClaudeTheme.WARM_AMBER, scale_factor=1.15)
        self.pause(1.8)
        
        # 清除过渡
        self.clear_caption()
        self.play(
            *[FadeOut(m) for m in [c_green, lbl_circle, right_logic, self.title_mobject]],
            run_time=0.6
        )
