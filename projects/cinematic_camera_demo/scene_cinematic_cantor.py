"""
SceneCinematicCantor: 电影级运镜与主题自适应实战
演示平滑推近聚焦 (Zoom In)、横移追踪 (Pan)、广角拉远 (Zoom Out) 以及一键主题切换。
"""
from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "manim-video", "templates")))
from base_scene import MovingCameraMathScene

class SceneCinematicCantor(MovingCameraMathScene):
    # 支持一键换肤：只需切换 'claude_light' / '3b1b_dark' / 'claude_dark'
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        
        # 1. 全景开场：展开标题与两行数字
        self.play_show_title("电影级运镜：探索无限的世界", "Cinematic Camera & Spatial Intuition")
        self.set_caption("当摄影机缓缓推近，我们得以窥见数学微观结构与宏观宇宙...")
        
        y_top = 0.6
        y_bot = -0.8
        
        lbl_nat = self.make_math(r"\mathbb{N}:", font_size=38, color=self.theme.primary).move_to(LEFT * 5.0 + UP * y_top)
        lbl_even = self.make_math(r"2\mathbb{N}:", font_size=38, color=self.theme.secondary).move_to(LEFT * 5.0 + UP * y_bot)
        
        nums_n = [1, 2, 3, 4, 5]
        nums_e = [2, 4, 6, 8, 10]
        
        m_nat = []
        m_even = []
        arrows = []
        
        for i in range(5):
            x = -3.4 + i * 1.5
            tn = self.make_math(str(nums_n[i]), font_size=38, color=self.theme.text_main).move_to(RIGHT * x + UP * y_top)
            te = self.make_math(str(nums_e[i]), font_size=38, color=self.theme.text_main).move_to(RIGHT * x + UP * y_bot)
            arr = DoubleArrow(
                start=RIGHT * x + UP * (y_top - 0.35),
                end=RIGHT * x + UP * (y_bot + 0.35),
                color=self.theme.success, stroke_width=2.5, tip_length=0.15
            )
            m_nat.append(tn)
            m_even.append(te)
            arrows.append(arr)
            
        dots_nat = self.make_math(r"\dots \ n", font_size=34, color=self.theme.text_muted).move_to(RIGHT * 4.3 + UP * y_top)
        dots_even = self.make_math(r"\dots \ 2n", font_size=34, color=self.theme.text_muted).move_to(RIGHT * 4.3 + UP * y_bot)
        dots_arr = DoubleArrow(
            start=RIGHT * 4.3 + UP * (y_top - 0.35),
            end=RIGHT * 4.3 + UP * (y_bot + 0.35),
            color=self.theme.success, stroke_width=2.5, tip_length=0.15
        )
        
        self.play(FadeIn(lbl_nat), *[Write(m) for m in m_nat], Write(dots_nat), run_time=1.0)
        self.play(FadeIn(lbl_even), *[Write(m) for m in m_even], Write(dots_even), run_time=1.0)
        self.play(*[GrowArrow(a) for a in arrows], GrowArrow(dots_arr), run_time=1.0)
        self.pause(0.8)
        
        # 2. 电影级推镜 (Zoom In)：平滑特写到 1 <-> 2 配对的微观细节
        pair_micro = VGroup(m_nat[0], arrows[0], m_even[0])
        self.set_caption("【推镜 Zoom In】镜头缓缓推进，聚焦微观一一对应双射：1 ↔ 2")
        self.camera_zoom_to(pair_micro, scale_factor=0.45, buff=1.2, run_time=1.8)
        self.pause(1.2)
        
        # 3. 电影级摇镜横移 (Pan)：镜头平移追踪至无穷远处的 n <-> 2n
        pair_macro = VGroup(dots_nat, dots_arr, dots_even)
        self.set_caption("【横移 Pan】摄影机横向穿梭追踪，掠过无限漫长的对应链路，抵达 n ↔ 2n")
        self.camera_pan_to(pair_macro.get_center(), run_time=2.0)
        self.pause(1.2)
        
        # 4. 电影级广角拉远 (Zoom Out & Reset)：俯瞰整个宏观宇宙
        self.set_caption("【拉远 Zoom Out】镜头拉回全景，俯瞰康托尔阿列夫零的无限苍穹！")
        self.camera_reset(run_time=1.8)
        self.pause(0.5)
        
        # 终极公式居中升起
        self.play(
            FadeOut(lbl_nat), FadeOut(lbl_even),
            FadeOut(dots_nat), FadeOut(dots_even), FadeOut(dots_arr),
            *[FadeOut(m) for m in m_nat + m_even + arrows],
            run_time=0.6
        )
        
        f_final = self.make_math(r"|\mathbb{N}| \ = \ |2\mathbb{N}| \ = \ \aleph_0", font_size=52, color=self.theme.accent)
        desc_final = self.make_text("(无穷也分等级：实数的无穷比自然数庞大得多！)", font_size=20, color=self.theme.text_muted)
        end_grp = VGroup(f_final, desc_final).arrange(DOWN, buff=0.3).shift(DOWN * 0.2)
        
        self.play(Write(f_final), FadeIn(desc_final), run_time=1.2)
        self.focus_on(f_final, color=self.theme.accent, scale_factor=1.15)
        self.pause(2.0)
