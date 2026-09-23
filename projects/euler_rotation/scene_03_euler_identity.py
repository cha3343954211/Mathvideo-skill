"""
Scene 03: 数学皇冠上的明珠 (The Most Beautiful Formula)
Claude 浅色米纸风格 + 广角全景拉远 (Zoom Out) + 终极五常数升华。
"""
from manim import *
from theme_config import MovingCameraMathScene

class Scene03Euler(MovingCameraMathScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        
        self.play_show_title("数学皇冠上的明珠：欧拉恒等式", "Euler's Identity: The Pearl of Mathematics")
        self.set_caption("旋转半圈抵达 -1，只需轻轻移项，宇宙最奇妙的五大常数便完美相遇...")
        
        # 1. 核心大公式缓缓升起 (居中，深墨色与赤陶橙)
        euler_formula = self.make_math(
            r"e^{i\pi} \ + \ 1 \ = \ 0",
            font_size=64, color=self.theme.accent
        ).shift(UP * 0.4)
        
        self.play(DrawBorderThenFill(euler_formula), run_time=1.5)
        self.focus_on(euler_formula, color=self.theme.secondary, scale_factor=1.12)
        self.pause(1.2)
        
        # 2. 电影级广角拉远 (Zoom Out)：镜头平滑拉远，展示宏大空间留白
        self.set_caption("【广角拉远 Zoom Out】分析学、代数学、几何学、算术与虚无，在这一瞬间统一！")
        self.play(
            self.camera_frame.animate.set_width(self.default_frame_width * 1.25),
            run_time=2.0,
            rate_func=smooth
        )
        
        # 五大常数注解卡片排开
        c_e = self.make_text("e (自然对数)", font_size=18, color=self.theme.primary)
        c_i = self.make_text("i (虚数单位)", font_size=18, color=self.theme.secondary)
        c_pi = self.make_text("π (圆周率)", font_size=18, color=self.theme.success)
        c_1 = self.make_text("1 (算术之源)", font_size=18, color=self.theme.accent)
        c_0 = self.make_text("0 (平衡与虚无)", font_size=18, color=self.theme.text_muted)
        
        constants_row = VGroup(c_e, c_i, c_pi, c_1, c_0).arrange(RIGHT, buff=0.45).next_to(euler_formula, DOWN, buff=0.8)
        
        self.play(FadeIn(constants_row, shift=UP * 0.2), run_time=1.2)
        self.pause(2.0)
        
        # 3. 终章谢幕
        self.set_caption("看似不相干的概念，在旋转之舞中融为一体。这就是数学的终极浪漫。")
        
        outro_txt = self.make_text("—— 谨以此片致敬莱昂哈德·欧拉 (1707 - 1783) ——", font_size=20, color=self.theme.text_muted)
        outro_txt.next_to(constants_row, DOWN, buff=0.6)
        
        self.play(FadeIn(outro_txt), run_time=1.0)
        self.pause(2.5)
