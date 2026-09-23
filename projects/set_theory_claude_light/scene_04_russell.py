"""
Scene 04 (Claude 标志性浅色米纸风格): 罗素悖论与公理基石 (Russell's Paradox & ZFC)
理发师两难 -> 砖石焦红死锁警报 -> 笔记本网格与琥珀金核心法则。
"""
from manim import *
from theme_config import ClaudeLightScene, ClaudeLightTheme

class Scene04Russell(ClaudeLightScene):
    def construct(self):
        super().construct()
        
        self.play_show_title("第三次数学危机：罗素悖论的死锁", "Russell's Paradox & The Axiomatic Foundation")
        self.set_caption("理发师宣告：‘我只给城里所有不给自己刮胡子的人刮胡子！’那他给自己刮吗？")
        
        # 1. 阶段一：理发师问题与罗素集合 (深墨色与灰褐)
        txt_barber = self.make_text("“若给自己刮，便违反规定；若不给自己刮，便必须给自己刮！”", font_size=22, color=ClaudeLightTheme.TEXT_MUTED)
        txt_barber.shift(UP * 1.5)
        
        r_formula = self.make_math(r"R = \{ x \mid x \notin x \}", font_size=48, color=ClaudeLightTheme.TEXT_INK)
        r_desc = self.make_text("由所有不属于自身的集合构成的罗素集合 R", font_size=20, color=ClaudeLightTheme.TEXT_MUTED).next_to(r_formula, DOWN, buff=0.2)
        r_group = VGroup(r_formula, r_desc).shift(DOWN * 0.2)
        
        self.play(FadeIn(txt_barber), run_time=0.8)
        self.play(Write(r_formula), FadeIn(r_desc), run_time=1.0)
        self.pause(1.2)
        
        # 2. 阶段二：彻底清场，呈现砖石焦红色的逻辑死锁
        self.set_caption("质问：R 是否属于自身？无论何种选择，都会立即推出荒谬矛盾！")
        
        self.play(
            FadeOut(txt_barber),
            FadeOut(r_desc),
            r_formula.animate.shift(UP * 1.6).scale(0.8),
            run_time=0.6
        )
        
        t_if1 = self.make_text("若", font_size=26, color=ClaudeLightTheme.CORAL_RED)
        f_if1 = self.make_math(r"R \in R \ \implies \ R \notin R", font_size=36, color=ClaudeLightTheme.CORAL_RED)
        row1 = VGroup(t_if1, f_if1).arrange(RIGHT, buff=0.15)
        
        t_if2 = self.make_text("若", font_size=26, color=ClaudeLightTheme.CORAL_RED)
        f_if2 = self.make_math(r"R \notin R \ \implies \ R \in R", font_size=36, color=ClaudeLightTheme.CORAL_RED)
        row2 = VGroup(t_if2, f_if2).arrange(RIGHT, buff=0.15)
        
        dead_rows = VGroup(row1, row2).arrange(DOWN, buff=0.35).shift(DOWN * 0.2)
        alert_box = SurroundingRectangle(dead_rows, color=ClaudeLightTheme.CORAL_RED, buff=0.3, stroke_width=2)
        
        self.play(Write(row1), run_time=0.8)
        self.play(Write(row2), run_time=0.8)
        self.play(Create(alert_box), run_time=0.6)
        self.pause(1.5)
        
        # 3. 阶段三：清场，公理系统降临与终极升华
        self.set_caption("数学家确立了严格的公理系统（如 ZFC），为集合圈定安全围墙，守护了数学大厦！")
        
        self.play(
            FadeOut(r_formula), FadeOut(dead_rows), FadeOut(alert_box),
            run_time=0.6
        )
        
        # 笔记本浅米坐标格线与琥珀金核心符号
        grid = NumberPlane(
            x_range=[-3.5, 3.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=7.5, y_length=2.5,
            background_line_style={"stroke_color": "#DCD5C9", "stroke_width": 1.2, "stroke_opacity": 0.8}
        ).shift(DOWN * 0.2)
        
        zfc_title = self.make_text("ZFC 公理化集合论：现代数学的稳固地基", font_size=22, color=ClaudeLightTheme.WARM_AMBER)
        zfc_title.next_to(grid, UP, buff=0.25)
        
        final_sym = self.make_math(r"A \subseteq B", font_size=64, color=ClaudeLightTheme.WARM_AMBER).move_to(grid.get_center())
        
        self.play(Create(grid), FadeIn(zfc_title), run_time=1.0)
        self.play(DrawBorderThenFill(final_sym), run_time=1.0)
        self.pause(0.8)
        
        # 终章致敬
        self.set_caption("从课本上小小的子集符号 ⊆，到叩问宇宙无穷与理性边界。这正是数学的魅力！")
        self.focus_on(final_sym, color=ClaudeLightTheme.TERRACOTTA, scale_factor=1.12)
        self.pause(2.0)
        
        outro = self.make_text("—— 致敬人类永不熄灭的理性之光 ——", font_size=20, color=ClaudeLightTheme.TEXT_MUTED)
        outro.next_to(grid, DOWN, buff=0.3)
        self.play(FadeIn(outro), run_time=0.8)
        self.pause(2.5)
