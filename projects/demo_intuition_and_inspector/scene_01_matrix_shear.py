"""
Scene 01: 线性代数的本质与矩阵空间形变 (LinearTransformRig 实战)
展示:
1. 3Blue1Brown 标志性线性代数空间网格形变
2. 基向量 i_hat 与 j_hat 的几何引领
3. 行列式单位面积平行四边形的倾斜与面积守恒直觉 (det = 1)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import BaseMathScene, LinearTransformRig, OrganicMotion

class MatrixShearScene(BaseMathScene):
    def construct(self):
        super().construct()

        # 1. 标题与引入
        self.play_show_title("线性代数之魂：矩阵如何扭曲空间", "LinearTransformRig & Determinant Conservation")
        self.set_caption("矩阵绝不是死板的数字方阵，它本质上是对空间的一场连续拉伸与剪切。")

        # 2. 装配 LinearTransformRig (线性空间网格形变仪)
        rig = LinearTransformRig(
            plane_range=(-5, 5),
            i_color=self.theme.primary,     # 天蓝
            j_color=self.theme.secondary,   # 活力橙
            area_color=self.theme.accent,   # 启迪金
            grid_color=self.theme.grid_color
        )

        # 基向量标签
        i_label = self.make_math(r"\hat{i}", font_size=24, color=self.theme.primary)
        i_label.next_to(rig.i_tracker.get_end(), DOWN, buff=0.15)
        j_label = self.make_math(r"\hat{j}", font_size=24, color=self.theme.secondary)
        j_label.next_to(rig.j_tracker.get_end(), LEFT, buff=0.15)

        self.play(FadeIn(rig), FadeIn(i_label), FadeIn(j_label), run_time=1.5)
        self.pause(0.6)

        # 3. 聚焦行列式单位面积正方形
        self.set_caption("初始状态下，基向量构成的单位正方形面积为 1。")
        self.play(OrganicMotion.pulse_glow(rig.unit_square, color=self.theme.accent, scale=1.08, run_time=0.8))
        self.pause(0.5)

        # 4. 引入剪切矩阵卡片 (HUD 右上角)
        shear_matrix = [[1.0, 1.5], [0.0, 1.0]]
        matrix_tex = self.make_math(
            r"A = \begin{pmatrix} 1 & 1.5 \\ 0 & 1 \end{pmatrix}",
            font_size=28
        )
        self.colorize_formula(matrix_tex, {
            r"1": self.theme.primary,
            r"1.5": self.theme.secondary
        })
        matrix_tex.to_corner(UR, buff=0.8)
        self.play(FadeIn(matrix_tex, shift=LEFT * 0.3), run_time=0.8)
        self.pause(0.5)

        # 5. 执行 3Blue1Brown 标志性矩阵网格空间变换！
        self.set_caption("施加水平剪切变换：整个空间网格倾斜，基向量 i 不动，j 被推向 (1.5, 1)。")
        anim_group, det_val = rig.animate_matrix_transform(shear_matrix, run_time=3.0)

        # 动态跟随更新基向量标签
        self.play(
            anim_group,
            i_label.animate.next_to(np.array([1.0, 0.0, 0.0]), DOWN, buff=0.15),
            j_label.animate.next_to(np.array([1.5, 1.0, 0.0]), UP, buff=0.15),
            run_time=3.0,
            rate_func=smooth
        )
        self.pause(0.5)

        # 6. 行列式面积守恒直觉顿悟
        self.set_caption("虽然正方形被挤压成了倾斜的平行四边形，但底和高完全不变，面积恒为 1！")
        det_tex = self.make_math(r"\det(A) = 1 \times 1 - 1.5 \times 0 = 1", font_size=26, color=self.theme.success)
        det_tex.next_to(matrix_tex, DOWN, buff=0.3, aligned_edge=RIGHT)
        self.play(FadeIn(det_tex, shift=UP * 0.2), run_time=0.8)
        self.play(OrganicMotion.spring_bounce(rig.unit_square, scale_factor=1.06, run_time=0.6))
        self.pause(1.5)

        # 优雅淡出
        self.set_caption("这就是行列式的本质——它是矩阵变换下任何空间图形的面积缩放因子。")
        self.pause(1.2)
        self.play(FadeOut(rig), FadeOut(i_label), FadeOut(j_label), FadeOut(matrix_tex), FadeOut(det_tex), run_time=1.2)
