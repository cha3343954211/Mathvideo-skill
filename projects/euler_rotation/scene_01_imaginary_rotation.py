"""
Scene 01: 乘以 i 本质是旋转 (Multiplying by i is Rotation)
Claude 浅色米纸风格 + 电影级推镜聚焦 (Zoom In)。
"""
from manim import *
from theme_config import MovingCameraMathScene

class Scene01Rotation(MovingCameraMathScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        
        # 1. 全景开场：标题与水平实数轴
        self.play_show_title("打破一维枷锁：乘以 i 是旋转", "Multiplying by i is Rotation")
        self.set_caption("在实数轴上，乘以正数是伸缩，乘以负数是翻转。连续两次什么操作会等于 -1？")
        
        # 水平实数轴
        real_axis = NumberLine(
            x_range=[-3.5, 3.5, 1], length=7,
            color=self.theme.primary, stroke_width=2.5,
            include_numbers=True, font_size=24
        ).shift(DOWN * 0.2)
        
        lbl_r = self.make_math(r"\mathbb{R}", font_size=32, color=self.theme.primary).next_to(real_axis, RIGHT, buff=0.2)
        
        # 从原点指向 1 的赤陶橙基准向量
        vec_start = real_axis.n2p(0)
        vec_end = real_axis.n2p(1)
        v = Arrow(start=vec_start, end=vec_end, buff=0, color=self.theme.secondary, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        lbl_v = self.make_math("1", font_size=28, color=self.theme.secondary).next_to(v, UP, buff=0.1)
        
        self.play(Create(real_axis), Write(lbl_r), run_time=1.0)
        self.play(GrowArrow(v), FadeIn(lbl_v), run_time=0.8)
        self.pause(1.0)
        
        # 2. 电影级推镜 (Zoom In)：特写原点局部，垂直虚轴破土升起
        self.set_caption("答案不是在线上硬挤，而是跨出维度！乘以虚数 i，本质是逆时针旋转 90 度！")
        
        # 平滑推近聚焦到原点局部
        self.camera_zoom_to(v, scale_factor=0.65, buff=1.2, run_time=1.6)
        
        # 垂直虚数轴升起
        imag_axis = NumberLine(
            x_range=[-2.2, 2.2, 1], length=4.4, rotation=90 * DEGREES,
            color=self.theme.text_muted, stroke_width=2.0
        ).move_to(vec_start)
        lbl_i_axis = self.make_math(r"\mathbb{I}", font_size=28, color=self.theme.text_muted).next_to(imag_axis, UP, buff=0.15)
        
        lbl_i_pos = self.make_math("i", font_size=26, color=self.theme.accent).next_to(imag_axis.n2p(1), LEFT, buff=0.1)
        lbl_neg1_pos = self.make_math("-1", font_size=26, color=self.theme.text_main).next_to(real_axis.n2p(-1), DOWN, buff=0.15)
        
        self.play(Create(imag_axis), FadeIn(lbl_i_axis), run_time=1.0)
        self.pause(0.6)
        
        # 3. 第一次旋转 90 度到达 i
        arc1 = Arc(radius=1.0, start_angle=0, angle=PI / 2, arc_center=vec_start, color=self.theme.accent, stroke_width=2.5)
        txt_times_i1 = self.make_math(r"\times i", font_size=24, color=self.theme.secondary).move_to(vec_start + UR * 0.9)
        
        self.play(
            Rotate(v, angle=PI / 2, about_point=vec_start),
            Create(arc1), FadeIn(txt_times_i1),
            ReplacementTransform(lbl_v, lbl_i_pos),
            run_time=1.5
        )
        self.pause(0.8)
        
        # 4. 第二次旋转 90 度到达 -1
        self.set_caption("再次乘以 i，再旋转 90 度，自然指向 -1！因此 i × i = -1 是旋转的必然！")
        
        arc2 = Arc(radius=1.0, start_angle=PI / 2, angle=PI / 2, arc_center=vec_start, color=self.theme.accent, stroke_width=2.5)
        txt_times_i2 = self.make_math(r"\times i", font_size=24, color=self.theme.secondary).move_to(vec_start + UL * 0.9)
        
        lbl_minus1 = self.make_math("-1", font_size=28, color=self.theme.secondary).next_to(real_axis.n2p(-1), UP, buff=0.1)
        
        self.play(
            Rotate(v, angle=PI / 2, about_point=vec_start),
            Create(arc2), FadeIn(txt_times_i2),
            ReplacementTransform(lbl_i_pos, lbl_minus1),
            run_time=1.5
        )
        self.pause(1.0)
        
        # 核心恒等式特写
        f_i2 = self.make_math(r"i^2 \ = \ -1", font_size=42, color=self.theme.accent).move_to(vec_start + DOWN * 1.4)
        self.play(Write(f_i2), run_time=0.8)
        self.focus_on(f_i2, color=self.theme.secondary, scale_factor=1.12)
        self.pause(1.8)
        
        # 重置相机与清场
        self.clear_caption()
        self.camera_reset(run_time=1.2)
        self.play(
            *[FadeOut(m) for m in [
                real_axis, imag_axis, lbl_r, lbl_i_axis,
                v, arc1, arc2, txt_times_i1, txt_times_i2,
                lbl_neg1_pos, lbl_minus1, f_i2, self.title_mobject
            ]],
            run_time=0.6
        )
