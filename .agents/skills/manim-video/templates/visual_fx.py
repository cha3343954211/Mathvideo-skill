"""
Minimalist Visual Shading & Pure Elegance Engine for Manim
==========================================================
追求 3Blue1Brown 与现代顶级学术期刊的纯粹留白克制美学：
1. FocusDimming: 视线暗场聚光（次要元素淡化沉降，彻底避免与公式穿插碰撞）
2. SleekHorizon: 极简纯净下划线 (1.5px 极细微流光，从中心向两侧丝滑展开)
3. PureTypography: 彻底杜绝任何多余的色块框与发光晕染，保持公式矢量笔画极致锐利
"""

import numpy as np
from manim import (
    VGroup, VMobject, Dot, Circle, Line,
    rate_functions, smooth,
    FadeIn, FadeOut, Create, AnimationGroup,
    DOWN, UP, LEFT, RIGHT,
    WHITE, YELLOW, GOLD, BLUE, TEAL, PURPLE
)


class MinimalistVisualFX:
    """极简克制高级视效"""

    @staticmethod
    def create_sleek_horizon(
        target_mobject: VMobject,
        accent_color=GOLD,
        width_ratio: float = 1.05,
        stroke_width: float = 1.6,
        buff: float = 0.22
    ) -> Line:
        """
        极简流光地平线：
        在公式正下方平滑展开一条极细克制的细线 (1.6px)，无多余边框。
        """
        w = target_mobject.get_width() * width_ratio
        center = target_mobject.get_center()
        y = target_mobject.get_bottom()[1] - buff

        start = np.array([center[0] - w / 2, y, 0])
        end = np.array([center[0] + w / 2, y, 0])

        horizon = Line(
            start=start,
            end=end,
            stroke_color=accent_color,
            stroke_width=stroke_width,
            stroke_opacity=0.8
        )
        return horizon

    @staticmethod
    def play_pure_revelation(
        scene,
        target_formula: VMobject,
        accent_color=GOLD,
        background_mobjects=None,
        sink_shift=DOWN * 0.45,
        run_time: float = 1.8
    ):
        """
        3Blue1Brown 标志性纯粹顿悟时刻：
        1. 背景几何与坐标系不仅平滑暗化至 10%，而且轻微向外沉降 (Sink & Dim)，腾出巨大的视觉留白；
        2. 核心公式纯净显现，下方纤细地平线从中心向两侧优雅生长展开；
        3. 彻底杜绝任何生硬矩形底色框，视觉完全通透。
        """
        horizon = MinimalistVisualFX.create_sleek_horizon(
            target_formula,
            accent_color=accent_color,
            width_ratio=1.05,
            stroke_width=1.6,
            buff=0.22
        )

        anims = [
            Create(horizon, run_time=run_time * 0.85, rate_func=smooth),
        ]

        if background_mobjects:
            for mob in background_mobjects:
                if isinstance(mob, VMobject):
                    anims.append(
                        mob.animate(run_time=run_time * 0.8, rate_func=smooth)
                            .set_opacity(0.10)
                            .shift(sink_shift)
                    )

        scene.play(*anims)
        return horizon


class SleekPulse:
    """极简微呼吸动画组件"""
    @staticmethod
    def attach_subtle_breath(line_mobject: Line, min_opacity: float = 0.5, max_opacity: float = 0.9, period: float = 2.4):
        def updater(mob, dt):
            t = getattr(mob, "_breath_t", 0.0) + dt
            setattr(mob, "_breath_t", t)
            phase = (np.sin(t * (2 * np.pi / period)) + 1.0) / 2.0
            mob.set_stroke(opacity=min_opacity + (max_opacity - min_opacity) * phase)
        line_mobject.add_updater(updater)
        return line_mobject

