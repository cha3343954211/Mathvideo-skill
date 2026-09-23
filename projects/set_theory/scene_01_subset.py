"""
Scene 01 (极简纯净 3b1b 风格): 高中核心 —— 包含与子集 (Subsets)
去除多余杂框，严格左右分区，彻底杜绝元素重叠。
"""
from manim import *
from theme_config import BaseMathScene, MathTheme

class Scene01Subset(BaseMathScene):
    def construct(self):
        super().construct()
        
        # 1. 顶部纯净标题
        self.play_show_title("集合间的基本关系", "Subsets & Inclusion")
        self.set_caption("集合是数学的底层语言。集合与集合之间，究竟存在怎样的关系？")
        
        # 2. 初始状态：屏幕中央两个分离的集合圆圈 A 与 B
        circ_a = Circle(radius=1.1, color=MathTheme.BLUE, fill_opacity=0.3, stroke_width=3)
        circ_a.shift(LEFT * 2.5 + DOWN * 0.2)
        lbl_a = MathTex("A", color=MathTheme.BLUE, font_size=36).next_to(circ_a, UP, buff=0.15)
        dot_a = Dot(circ_a.get_center(), color=MathTheme.BLUE, radius=0.08)
        grp_a = VGroup(circ_a, lbl_a, dot_a)
        
        circ_b = Circle(radius=1.8, color=MathTheme.ORANGE, fill_opacity=0.2, stroke_width=3)
        circ_b.shift(RIGHT * 2.2 + DOWN * 0.2)
        lbl_b = MathTex("B", color=MathTheme.ORANGE, font_size=36).next_to(circ_b, UP, buff=0.15)
        grp_b = VGroup(circ_b, lbl_b)
        
        self.play(FadeIn(grp_a), FadeIn(grp_b), run_time=1.0)
        self.pause(1.0)
        
        # 3. A 缓缓融入 B 内部，右侧形成纯净清晰的韦恩图
        self.set_caption("若集合 A 中的每个元素都属于 B，称 A 是 B 的子集，记作 A ⊆ B")
        
        target_b_pos = RIGHT * 2.2 + DOWN * 0.2
        target_a_pos = target_b_pos + LEFT * 0.4 + DOWN * 0.2
        
        self.play(
            circ_a.animate.scale(0.85).move_to(target_a_pos),
            lbl_a.animate.scale(0.85).move_to(target_a_pos + UP * 1.15),
            dot_a.animate.move_to(target_a_pos),
            run_time=1.5
        )
        
        # 左侧清晰陈列定义公式 (左右分屏，绝无交叉覆盖)
        f_all = MathTex(r"\forall x \in A \implies x \in B", font_size=32, color=MathTheme.TEXT_MAIN)
        f_sub = MathTex(r"A \subseteq B", font_size=46, color=MathTheme.YELLOW)
        lbl_sub = self.make_text("A 是 B 的子集", font_size=20, color=MathTheme.YELLOW)
        
        left_defs = VGroup(f_all, f_sub, lbl_sub).arrange(DOWN, buff=0.3).shift(LEFT * 3.2 + DOWN * 0.2)
        
        self.play(Write(f_all), Write(f_sub), FadeIn(lbl_sub), run_time=1.2)
        self.pause(1.2)
        
        # 4. 真子集：B 外部独有元素
        self.set_caption("若 B 中还有 A 所没有的元素，A 更是 B 的真子集：A ⊊ B")
        
        dot_extra = Dot(target_b_pos + RIGHT * 0.9 + UP * 0.4, color=MathTheme.ORANGE, radius=0.08)
        lbl_extra = self.make_text("B独有元素", font_size=16, color=MathTheme.ORANGE).next_to(dot_extra, UP, buff=0.1)
        
        f_psub = MathTex(r"A \subsetneqq B", font_size=46, color=MathTheme.ORANGE).move_to(f_sub)
        lbl_psub = self.make_text("A 是 B 的真子集", font_size=20, color=MathTheme.ORANGE).move_to(lbl_sub)
        
        self.play(FadeIn(dot_extra), FadeIn(lbl_extra), run_time=0.6)
        self.play(ReplacementTransform(f_sub, f_psub), ReplacementTransform(lbl_sub, lbl_psub), run_time=0.8)
        self.pause(1.2)
        
        # 彻底清场：将阶段一全部元素 FadeOut，准备第二阶段
        self.play(
            *[FadeOut(m) for m in [
                circ_a, lbl_a, dot_a, circ_b, lbl_b, dot_extra, lbl_extra,
                f_all, f_psub, lbl_psub
            ]],
            run_time=0.6
        )
        
        # 5. 空集哲学 (屏幕正中央，纯粹留白)
        self.set_caption("最特殊的空集 ∅：不含任何元素，却傲然作为任何集合的子集：∅ ⊆ A")
        
        sq = Square(side_length=1.4, color=MathTheme.YELLOW, stroke_width=2)
        dashed_sq = DashedVMobject(sq, num_dashes=16)
        txt_empty = MathTex(r"\emptyset", font_size=52, color=MathTheme.YELLOW).move_to(sq)
        rule_empty = MathTex(r"\emptyset \subseteq A", font_size=42, color=MathTheme.YELLOW)
        desc_empty = self.make_text("(空集是一切集合的子集)", font_size=20, color=MathTheme.TEXT_MUTED)
        
        center_empty_grp = VGroup(
            VGroup(dashed_sq, txt_empty),
            rule_empty,
            desc_empty
        ).arrange(DOWN, buff=0.25).shift(DOWN * 0.2)
        
        self.play(Create(dashed_sq), Write(txt_empty), run_time=1.0)
        self.play(Write(rule_empty), FadeIn(desc_empty), run_time=0.8)
        self.focus_on(rule_empty, color=MathTheme.YELLOW, scale_factor=1.12)
        self.pause(1.5)
        
        # 清除过渡
        self.clear_caption()
        self.play(
            FadeOut(center_empty_grp), FadeOut(self.title_mobject),
            run_time=0.6
        )
