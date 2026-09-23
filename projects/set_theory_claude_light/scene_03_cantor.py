"""
Scene 03 (Claude 标志性浅色米纸风格): 康托尔与无穷的深渊 (Cantor & Infinity)
学术图书排版风格 + 墨水双色数字序列 + 鼠尾草绿对应连线 + 琥珀金基数。
"""
from manim import *
from theme_config import ClaudeLightScene, ClaudeLightTheme

class Scene03Cantor(ClaudeLightScene):
    def construct(self):
        super().construct()
        
        self.play_show_title("颠覆常识的飞跃：康托尔与无穷", "Georg Cantor: Journey into the Infinite")
        self.set_caption("直觉告诉你：偶数只有自然数的一半！但无限的世界里，部分竟然等于整体？！")
        
        # 1. 康托尔名言纯文本 (灰褐墨水)
        quote = self.make_text("“数学的本质，在于它的绝对自由。” —— 格奥尔格·康托尔", font_size=23, color=ClaudeLightTheme.TEXT_MUTED)
        quote.shift(UP * 1.5)
        self.play(FadeIn(quote, shift=DOWN * 0.2), run_time=1.0)
        self.pause(1.2)
        
        # 2. 自然数行与偶数行展示 (双色墨水行)
        self.set_caption("康托尔提出了颠覆性的法宝：‘一一对应’！只要能严密配对，数量就完全相同！")
        
        y_top = 0.5
        y_bot = -1.0
        
        lbl_nat = self.make_math(r"\mathbb{N}:", font_size=38, color=ClaudeLightTheme.SLATE_BLUE).move_to(LEFT * 5.0 + UP * y_top)
        lbl_even = self.make_math(r"2\mathbb{N}:", font_size=38, color=ClaudeLightTheme.TERRACOTTA).move_to(LEFT * 5.0 + UP * y_bot)
        
        nums_n = [1, 2, 3, 4, 5]
        nums_e = [2, 4, 6, 8, 10]
        
        m_nat = []
        m_even = []
        arrows = []
        
        for i in range(5):
            x = -3.4 + i * 1.5
            tn = self.make_math(str(nums_n[i]), font_size=38, color=ClaudeLightTheme.TEXT_INK).move_to(RIGHT * x + UP * y_top)
            te = self.make_math(str(nums_e[i]), font_size=38, color=ClaudeLightTheme.TEXT_INK).move_to(RIGHT * x + UP * y_bot)
            arr = DoubleArrow(
                start=RIGHT * x + UP * (y_top - 0.35),
                end=RIGHT * x + UP * (y_bot + 0.35),
                color=ClaudeLightTheme.SAGE_GREEN, stroke_width=2.5, tip_length=0.15
            )
            m_nat.append(tn)
            m_even.append(te)
            arrows.append(arr)
            
        dots_nat = self.make_math(r"\dots \ n", font_size=34, color=ClaudeLightTheme.TEXT_MUTED).move_to(RIGHT * 4.3 + UP * y_top)
        dots_even = self.make_math(r"\dots \ 2n", font_size=34, color=ClaudeLightTheme.TEXT_MUTED).move_to(RIGHT * 4.3 + UP * y_bot)
        dots_arr = DoubleArrow(
            start=RIGHT * 4.3 + UP * (y_top - 0.35),
            end=RIGHT * 4.3 + UP * (y_bot + 0.35),
            color=ClaudeLightTheme.SAGE_GREEN, stroke_width=2.5, tip_length=0.15
        )
        
        self.play(FadeIn(lbl_nat), *[Write(m) for m in m_nat], Write(dots_nat), run_time=1.0)
        self.play(FadeIn(lbl_even), *[Write(m) for m in m_even], Write(dots_even), run_time=1.0)
        
        # 依次生长出鼠尾草绿连线
        for i in range(5):
            self.play(
                GrowArrow(arrows[i]),
                m_nat[i].animate.set_color(ClaudeLightTheme.SAGE_GREEN),
                m_even[i].animate.set_color(ClaudeLightTheme.SAGE_GREEN),
                run_time=0.25
            )
        self.play(GrowArrow(dots_arr), run_time=0.3)
        self.pause(1.2)
        
        # 3. 彻底清场：中央展示核心公式
        self.set_caption("每一个自然数 n 都有唯一偶数 2n 配对：偶数与自然数一样多！阿列夫零 ℵ₀！")
        
        self.play(
            FadeOut(quote),
            FadeOut(lbl_nat), FadeOut(lbl_even),
            FadeOut(dots_nat), FadeOut(dots_even), FadeOut(dots_arr),
            *[FadeOut(m) for m in m_nat + m_even + arrows],
            run_time=0.6
        )
        
        # 屏幕中心大字高光展示 (暖金琥珀)
        f_aleph = self.make_math(r"|\mathbb{N}| \ = \ |2\mathbb{N}| \ = \ \aleph_0", font_size=52, color=ClaudeLightTheme.WARM_AMBER)
        desc_aleph = self.make_text("(无穷也分阶梯：实数的无穷比自然数庞大得多！)", font_size=20, color=ClaudeLightTheme.TEXT_MUTED)
        aleph_group = VGroup(f_aleph, desc_aleph).arrange(DOWN, buff=0.3).shift(DOWN * 0.2)
        
        self.play(Write(f_aleph), FadeIn(desc_aleph), run_time=1.2)
        self.focus_on(f_aleph, color=ClaudeLightTheme.TERRACOTTA, scale_factor=1.15)
        self.pause(2.0)
        
        # 清除过渡
        self.clear_caption()
        self.play(FadeOut(aleph_group), FadeOut(self.title_mobject), run_time=0.6)
