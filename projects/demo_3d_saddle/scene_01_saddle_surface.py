"""
Scene 01: 鞍点之美与双曲抛物面 (ThreeDMathScene 实战)
展示:
1. HUD 固定视口字幕与标题 (无论相机如何旋转，字幕永不镜像变形)
2. 视角平滑升维过渡 (从 2D 俯视无缝旋入 3D 黄金角)
3. 渐变深度着色曲面 GradientSurface
4. 空间动点投影与环绕巡航漫游
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import ThreeDMathScene, GradientSurface, Dynamic3DCursorRig, OrganicMotion

class SaddlePoint3DScene(ThreeDMathScene):
    def construct(self):
        super().construct()

        # 1. 初始相机设为 2D 俯视视角 (phi=0, theta=-90度)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # 2. 纯净 HUD 固定标题与字幕
        self.play_show_title("多元微积分之奇：马鞍面与鞍点", "3D Gradient Surface & Saddle Point")
        self.set_caption("在二维俯视图中，它只是一组对称的双曲线等高线。")

        # 3. 构建三维空间坐标系与马鞍曲面
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-2.5, 2.5, 1],
            x_length=6.0,
            y_length=6.0,
            z_length=4.5,
            axis_config={"color": self.theme.grid_color, "stroke_width": 2}
        )

        # 双曲抛物面 z = 0.5 * (x^2 - y^2)
        saddle_func = lambda u, v: 0.45 * (u**2 - v**2)

        surface = GradientSurface(
            func=saddle_func,
            u_range=(-2.0, 2.0),
            v_range=(-2.0, 2.0),
            resolution=(30, 30),
            color_gradient=(self.theme.secondary, self.theme.primary, self.theme.accent),
            opacity=0.82
        )

        # 公式卡片放在 HUD 层
        formula_hud = self.make_math(r"z = \frac{1}{2}(x^2 - y^2)", font_size=28)
        self.colorize_formula(formula_hud, {
            r"z": self.theme.accent,
            r"x^2": self.theme.primary,
            r"y^2": self.theme.secondary
        })
        formula_hud.to_corner(UR, buff=0.8)
        self.add_hud(formula_hud)

        self.play(Create(axes), FadeIn(formula_hud), run_time=1.2)
        self.play(Create(surface), run_time=1.8)
        self.pause(0.6)

        # 4. 电影级平滑升维：从 2D 俯视平滑旋入 3D 黄金立体视角！
        self.set_caption("打破二维平面的局限：摄影机平滑俯仰，升维进入三维空间。")
        self.smooth_camera_orientation(
            phi=68 * DEGREES,
            theta=-42 * DEGREES,
            zoom=0.95,
            run_time=3.0,
            rate_func=smooth
        )
        self.pause(0.5)

        # 5. 装配曲面空间动点装置 Dynamic3DCursorRig
        self.set_caption("空间动点沿 x 方向滑动：从高处降至原点，此处为局部极小值。")
        u_track = ValueTracker(1.8)
        v_track = ValueTracker(0.0)

        cursor_rig = Dynamic3DCursorRig(
            axes=axes,
            func=saddle_func,
            u_tracker=u_track,
            v_tracker=v_track,
            dot_color=self.theme.accent,
            line_color=self.theme.alert,
            radius=0.10
        )

        self.play(FadeIn(cursor_rig), run_time=0.8)
        # 沿 x 轴向原点滑动
        self.play(u_track.animate.set_value(0.0), run_time=2.2, rate_func=smooth)
        self.pause(0.4)

        # 6. 再沿 y 轴滑动：凸显鞍点本质
        self.set_caption("然而沿 y 方向看，原点却是两侧山峰的最高峰（局部极大值）！")
        self.play(v_track.animate.set_value(1.8), run_time=2.2, rate_func=smooth)
        self.pause(0.4)

        # 7. 开启 3D 慢速空间轨道环绕巡航漫游！
        self.set_caption("极大与极小在此处交汇坍缩——这便是多元函数最壮丽的‘鞍点’。")
        self.start_orbital_flight(rate=0.10)
        self.play(v_track.animate.set_value(0.0), run_time=2.0, rate_func=smooth)
        self.play(OrganicMotion.pulse_glow(cursor_rig.dot, color=self.theme.alert, scale=1.6, run_time=1.0))
        self.pause(2.5)

        # 8. 停止巡航并优雅淡出
        self.stop_orbital_flight()
        self.set_caption("3D HUD 正交层与深度渐变曲面，让多元几何的直觉触手可及。")
        self.pause(1.2)
        self.play(FadeOut(axes), FadeOut(surface), FadeOut(cursor_rig), FadeOut(formula_hud), run_time=1.2)
