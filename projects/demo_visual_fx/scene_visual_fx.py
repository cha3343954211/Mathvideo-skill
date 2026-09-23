"""
3Blue1Brown Canonical Style: Geometric Intuition of Euler's Formula
===================================================================
严格遵守【短句化纯单行美学规范】：
每句台词严格控制在 14~22 字，字字珠玑、节奏干脆，100% 纯粹优雅单行！
"""

import sys
import os
import numpy as np
from manim import *

# 引用模板库
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "manim-video", "templates")))
from base_scene import BaseMathScene


class PureMathEulerScene(BaseMathScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()

        # 1. 纯净学术标题
        title = self.play_show_title("欧拉公式的几何本质", "为什么虚指数对应着圆周旋转？")

        # 2. 纤细精密的复平面坐标系
        axes = Axes(
            x_range=[-1.8, 1.8, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=6.0,
            y_length=4.6,
            axis_config={"color": self.theme.grid_color, "stroke_width": 1.5},
        ).shift(LEFT * 2.2 + DOWN * 0.4)

        labels = axes.get_axis_labels(
            x_label=MathTex(r"\mathrm{Re}", color=self.theme.text_muted, font_size=20),
            y_label=MathTex(r"\mathrm{Im}", color=self.theme.text_muted, font_size=20)
        )

        unit_len = axes.coords_to_point(1, 0)[0] - axes.coords_to_point(0, 0)[0]
        center_pt = axes.c2p(0, 0)
        unit_circle = Circle(radius=unit_len, color=self.theme.grid_color, stroke_width=1.2, stroke_opacity=0.6)
        unit_circle.move_to(center_pt)

        # 纯单行短句 1
        with self.voiceover("初学欧拉公式，常困惑于虚数为何对应着旋转。") as tracker:
            self.play(Create(axes), Write(labels), Create(unit_circle), run_time=tracker.duration * 0.8)
            self.wait(tracker.duration * 0.2)

        # 3. 右侧核心数学逻辑推导面板
        formula_group = VGroup()
        f1 = self.make_math(r"z(t) = e^{i t}", font_size=32).move_to(RIGHT * 2.8 + UP * 1.5)
        self.colorize_formula(f1, {r"z(t)": self.theme.primary, r"e^{i t}": self.theme.primary})

        f2 = self.make_math(r"\frac{dz}{dt} = i \cdot e^{i t} = i \cdot z(t)", font_size=28).next_to(f1, DOWN, buff=0.45, aligned_edge=LEFT)
        self.colorize_formula(f2, {r"\frac{dz}{dt}": self.theme.secondary, r"i": self.theme.accent, r"z(t)": self.theme.primary})

        note = self.make_text("乘 i 的几何含义：逆时针旋转 90°", font_size=18, color=self.theme.text_muted).next_to(f2, DOWN, buff=0.35, aligned_edge=LEFT)
        conclusion_box = self.make_math(r"\vec{v}(t) \perp \vec{z}(t)", font_size=32, color=self.theme.accent).next_to(note, DOWN, buff=0.45, aligned_edge=LEFT)

        # 纯单行短句 2
        with self.voiceover("答案深藏在求导中，复指数求导会掉出虚数常数 i。") as tracker:
            self.play(Write(f1), run_time=tracker.duration * 0.45)
            self.play(Write(f2), run_time=tracker.duration * 0.45)
            self.wait(tracker.duration * 0.1)

        # 4. 几何动效：位置向量与永远正交的速度向量
        t_tracker = ValueTracker(0.0)

        # 位置向量 z(t) (天蓝色)
        pos_arrow = always_redraw(lambda: Arrow(
            center_pt,
            axes.c2p(np.cos(t_tracker.get_value()), np.sin(t_tracker.get_value())),
            buff=0,
            color=self.theme.primary,
            stroke_width=2.8,
            max_tip_length_to_length_ratio=0.18
        ))

        # 速度向量 v(t) = i * z(t) (橙色，始终切向垂直)
        vel_arrow = always_redraw(lambda: Arrow(
            axes.c2p(np.cos(t_tracker.get_value()), np.sin(t_tracker.get_value())),
            axes.c2p(
                np.cos(t_tracker.get_value()) - 0.75 * np.sin(t_tracker.get_value()),
                np.sin(t_tracker.get_value()) + 0.75 * np.cos(t_tracker.get_value())
            ),
            buff=0,
            color=self.theme.secondary,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.22
        ))

        # 运动轨迹弧线
        arc_path = always_redraw(lambda: Arc(
            radius=unit_len,
            start_angle=0,
            angle=t_tracker.get_value(),
            arc_center=center_pt,
            color=self.theme.primary,
            stroke_width=2.5
        ))

        # 纯单行短句 3
        with self.voiceover("在复平面中，乘 i 的几何含义是逆时针旋转 90 度。") as tracker:
            self.play(FadeIn(note), run_time=tracker.duration * 0.9)

        # 纯单行短句 4
        with self.voiceover("这意味着：动点的速度永远严格垂直于其位置。") as tracker:
            self.play(Write(conclusion_box), run_time=tracker.duration * 0.5)
            self.play(Create(pos_arrow), Create(vel_arrow), run_time=tracker.duration * 0.4)
            self.wait(tracker.duration * 0.1)

        # 5. 运动演进到 t = pi
        target_f = self.make_math(r"z(\pi) = e^{i\pi} = -1", font_size=32).next_to(conclusion_box, DOWN, buff=0.5, aligned_edge=LEFT)
        self.colorize_formula(target_f, {r"e^{i\pi}": self.theme.primary, r"-1": self.theme.accent})

        euler_final = self.make_math(r"e^{i\pi} + 1 = 0", font_size=36).move_to(target_f.get_center())
        self.colorize_formula(euler_final, {r"e^{i\pi}": self.theme.primary, r"1": self.theme.secondary, r"0": self.theme.accent})

        # 纯单行短句 5
        with self.voiceover("当速度垂直于位置且速率为 1 时，轨迹必是圆周。") as tracker:
            self.add(arc_path)
            self.play(
                t_tracker.animate(run_time=tracker.duration * 0.9, rate_func=linear).set_value(np.pi * 0.6)
            )

        # 纯单行短句 6
        with self.voiceover("当时间行进到圆周率派，动点刚好抵达实轴负一。") as tracker:
            self.play(
                t_tracker.animate(run_time=tracker.duration * 0.6, rate_func=linear).set_value(np.pi)
            )
            self.play(Write(target_f), run_time=tracker.duration * 0.4)

        # 纯单行短句 7
        with self.voiceover("将负一移至等号左侧，便诞生了欧拉恒等式。") as tracker:
            self.play(
                TransformMatchingTex(target_f, euler_final),
                run_time=tracker.duration * 0.8
            )
            self.wait(tracker.duration * 0.2)

        self.wait(2.0)
