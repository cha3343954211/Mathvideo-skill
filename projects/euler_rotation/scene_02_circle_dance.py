"""
Scene 02: 速度垂直于位置的圆周之舞 (Velocity Perpendicular to Position)
Claude 浅色米纸风格 + 电影级横移镜头追踪 (Pan & Tracking)。
"""
from manim import *
from theme_config import MovingCameraMathScene

class Scene02Dance(MovingCameraMathScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        
        self.play_show_title("速度垂直于位置：圆周之舞", "Euler's Trajectory & Rotation")
        self.set_caption("当变量持续流动，e^(it) 的导数是 i·e^(it)：速度永远垂直于位置！")
        
        # 1. 复平面网格与单位圆 (全景)
        origin = DOWN * 0.2
        r = 1.8
        
        c_unit = Circle(radius=r, color=self.theme.success, stroke_width=3).move_to(origin)
        r_axis = Line(start=origin + LEFT * 3.2, end=origin + RIGHT * 3.2, color=self.theme.grid_color, stroke_width=1.5)
        i_axis = Line(start=origin + DOWN * 2.3, end=origin + UP * 2.3, color=self.theme.grid_color, stroke_width=1.5)
        
        lbl_1 = self.make_math("1", font_size=26, color=self.theme.text_muted).next_to(origin + RIGHT * r, DOWN + RIGHT, buff=0.1)
        lbl_neg1 = self.make_math("-1", font_size=26, color=self.theme.text_muted).next_to(origin + LEFT * r, DOWN + LEFT, buff=0.1)
        
        self.play(Create(r_axis), Create(i_axis), Create(c_unit), run_time=1.0)
        self.play(FadeIn(lbl_1), FadeIn(lbl_neg1), run_time=0.6)
        self.pause(0.8)
        
        # 2. 动点与切线速度箭头
        self.set_caption("速度永远垂直于位移，意味着它绝不膨胀、绝不坍缩，只能在圆周上恒速奔跑！")
        
        t_tracker = ValueTracker(0.0)
        
        # 径向位置向量 (赤陶橙)
        pos_vec = always_redraw(lambda:
            Arrow(
                start=origin,
                end=origin + np.array([r * np.cos(t_tracker.get_value()), r * np.sin(t_tracker.get_value()), 0]),
                buff=0, color=self.theme.secondary, stroke_width=3.5, max_tip_length_to_length_ratio=0.25
            )
        )
        
        # 切向速度向量 (暖琥珀金，逆时针 90 度)
        vel_vec = always_redraw(lambda:
            Arrow(
                start=origin + np.array([r * np.cos(t_tracker.get_value()), r * np.sin(t_tracker.get_value()), 0]),
                end=origin + np.array([r * np.cos(t_tracker.get_value()), r * np.sin(t_tracker.get_value()), 0])
                   + np.array([-1.0 * np.sin(t_tracker.get_value()), 1.0 * np.cos(t_tracker.get_value()), 0]),
                buff=0, color=self.theme.accent, stroke_width=3.0, max_tip_length_to_length_ratio=0.3
            )
        )
        
        dot = always_redraw(lambda:
            Dot(
                origin + np.array([r * np.cos(t_tracker.get_value()), r * np.sin(t_tracker.get_value()), 0]),
                color=self.theme.secondary, radius=0.08
            )
        )
        
        self.add(pos_vec, vel_vec, dot)
        self.pause(0.6)
        
        # 3. 电影级横移镜头追踪 (Pan Tracking)
        # 随着动点从 0 运动到 PI，镜头平滑向左横移聚焦到达 -1 终点
        self.set_caption("当走过 π 的弧度，质点不偏不倚，恰好降落在实数轴的 -1 上！")
        
        self.play(
            t_tracker.animate.set_value(PI),
            self.camera_frame.animate.shift(LEFT * 1.0).set_width(9.5),
            run_time=3.5,
            rate_func=linear
        )
        self.pause(1.2)
        
        # 定格在 -1
        f_step = self.make_math(r"e^{i\pi} \ = \ -1", font_size=42, color=self.theme.accent).move_to(origin + UP * 1.5 + LEFT * 1.0)
        self.play(Write(f_step), run_time=1.0)
        self.focus_on(f_step, color=self.theme.secondary, scale_factor=1.15)
        self.pause(1.8)
        
        # 相机重置与清场
        self.clear_caption()
        self.camera_reset(run_time=1.0)
        self.play(
            *[FadeOut(m) for m in [
                r_axis, i_axis, c_unit, lbl_1, lbl_neg1,
                pos_vec, vel_vec, dot, f_step, self.title_mobject
            ]],
            run_time=0.6
        )
