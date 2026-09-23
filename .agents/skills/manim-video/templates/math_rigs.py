"""
math_rigs.py: 高阶数学交互装置与灵动物理动力学组件库
为 3Blue1Brown 级数学视频提供模块化、即插即用的动态机械结构与物理反馈。
"""
from manim import *
import numpy as np


# =========================================================================
# 1. 灵动物理动力学与呼吸微动画 (Organic Motion & Physics Curves)
# =========================================================================
class OrganicMotion:
    """灵动自然运动辅助类：告别生硬线性补间，赋予数学对象物理质感"""

    @staticmethod
    def spring_bounce(mobject, scale_factor=1.15, run_time=0.6):
        """阻尼弹簧回弹冲激：模拟带弹性的受力膨胀与阻尼复原"""
        return Succession(
            mobject.animate(run_time=run_time * 0.4, rate_func=rush_into).scale(scale_factor),
            mobject.animate(run_time=run_time * 0.35, rate_func=smooth).scale(0.95 / scale_factor),
            mobject.animate(run_time=run_time * 0.25, rate_func=smooth).scale(1.0 / 0.95)
        )

    @staticmethod
    def pulse_glow(mobject, color=YELLOW, scale=1.08, run_time=0.8):
        """高光脉冲呼吸：突出关键几何对象或符号"""
        orig_color = mobject.get_color()
        return Succession(
            mobject.animate(run_time=run_time * 0.5).scale(scale).set_color(color),
            mobject.animate(run_time=run_time * 0.5).scale(1.0 / scale).set_color(orig_color)
        )

    @staticmethod
    def wiggle_alert(mobject, run_time=0.8, n_wiggles=4, rotation_angle=0.08):
        """困惑/警告小幅度摆动 (常用于展示反例、矛盾或疑问)"""
        return Wiggle(
            mobject,
            scale_value=1.1,
            rotation_angle=rotation_angle,
            n_wiggles=n_wiggles,
            run_time=run_time
        )


# =========================================================================
# 2. 动切线与导数追踪仪 (Dynamic Tangent & Derivative Rig)
# =========================================================================
class DynamicTangentRig(VGroup):
    """
    函数动切线与导数全自动追踪装置：
    只需改变 value_tracker (x 的值)，切点、切线、斜率数值标签和导数指示全自动无缝重绘！
    """
    def __init__(
        self,
        axes,
        func,
        tracker,
        tangent_length=3.0,
        tangent_color=ORANGE,
        dot_color=YELLOW,
        show_slope_label=True,
        show_projections=True,
        decimal_places=2,
        dx_sample=0.001,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes = axes
        self.func = func
        self.tracker = tracker
        self.tangent_length = tangent_length
        self.tangent_color = tangent_color
        self.dot_color = dot_color
        self.show_slope_label = show_slope_label
        self.show_projections = show_projections
        self.decimal_places = decimal_places
        self.dx_sample = dx_sample

        # 1. 动点 (Dot)
        self.dot = always_redraw(lambda: Dot(
            point=self.axes.c2p(self.tracker.get_value(), self.func(self.tracker.get_value())),
            color=self.dot_color,
            radius=0.075
        ))
        self.add(self.dot)

        # 2. 自动切线 (Tangent Line)
        def get_tangent_line():
            x = self.tracker.get_value()
            p0 = self.axes.c2p(x, self.func(x))
            # 数值微分估算斜率
            df = (self.func(x + self.dx_sample) - self.func(x - self.dx_sample)) / (2 * self.dx_sample)
            
            # 在图表空间计算导数方向向量
            p_right = self.axes.c2p(x + 0.5, self.func(x) + df * 0.5)
            tangent_dir = normalize(p_right - p0)
            
            line = Line(
                p0 - tangent_dir * (self.tangent_length / 2),
                p0 + tangent_dir * (self.tangent_length / 2),
                color=self.tangent_color,
                stroke_width=2.5
            )
            return line

        self.tangent_line = always_redraw(get_tangent_line)
        self.add(self.tangent_line)

        # 3. 虚线正交投影 (Projection Lines)
        if self.show_projections:
            def get_v_line():
                x = self.tracker.get_value()
                y = self.func(x)
                p_curve = self.axes.c2p(x, y)
                p_axis = self.axes.c2p(x, 0)
                return DashedLine(p_axis, p_curve, stroke_width=1.5, color=GREY_B, dash_length=0.08)

            self.v_projection = always_redraw(get_v_line)
            self.add(self.v_projection)

        # 4. 实时斜率动态标签 (Slope Indicator: k = f'(x))
        if self.show_slope_label:
            def get_slope_group():
                x = self.tracker.get_value()
                y = self.func(x)
                slope = (self.func(x + self.dx_sample) - self.func(x - self.dx_sample)) / (2 * self.dx_sample)
                p_dot = self.axes.c2p(x, y)

                label_tex = MathTex(
                    f"k = {slope:.{self.decimal_places}f}",
                    font_size=22,
                    color=self.tangent_color
                )
                # 放在点上方稍作位移，防止与坐标轴或线段穿透
                label_tex.next_to(p_dot, UR, buff=0.15)
                return label_tex

            self.slope_group = always_redraw(get_slope_group)
            self.add(self.slope_group)


# =========================================================================
# 3. 黎曼和矩形逼近器 (Dynamic Riemann Sum Rig)
# =========================================================================
class DynamicRiemannRig(VGroup):
    """
    微积分黎曼和极限逼近装置：
    通过控制 n_tracker (分割矩形数 n) 从 4 到 60 平滑递增，
    生动直观演示离散矩形逼近连续曲边梯形面积的过程。
    """
    def __init__(
        self,
        axes,
        func,
        x_range,
        n_tracker,
        color_scheme=(BLUE, GREEN),
        fill_opacity=0.6,
        stroke_width=1.0,
        show_area_label=True,
        input_sample_type="left",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes = axes
        self.func = func
        self.x_min, self.x_max = x_range
        self.n_tracker = n_tracker
        self.color_scheme = color_scheme
        self.fill_opacity = fill_opacity
        self.stroke_width = stroke_width
        self.show_area_label = show_area_label
        self.input_sample_type = input_sample_type

        # 动态重绘的矩形条集合
        def get_rectangles():
            n = max(int(np.round(self.n_tracker.get_value())), 1)
            rects = self.axes.get_riemann_rectangles(
                self.axes.plot(self.func, x_range=[self.x_min, self.x_max]),
                x_range=[self.x_min, self.x_max],
                dx=(self.x_max - self.x_min) / n,
                color=self.color_scheme,
                fill_opacity=self.fill_opacity,
                stroke_width=self.stroke_width,
                input_sample_type=self.input_sample_type
            )
            return rects

        self.rectangles = always_redraw(get_rectangles)
        self.add(self.rectangles)

        # 动态面积与分割数指示器
        if self.show_area_label:
            def get_status_label():
                n = max(int(np.round(self.n_tracker.get_value())), 1)
                dx = (self.x_max - self.x_min) / n
                # 计算黎曼和
                xs = np.linspace(self.x_min, self.x_max - dx, n)
                approx_area = sum(self.func(x) * dx for x in xs)

                n_tex = MathTex(f"n = {n}", font_size=24, color=WHITE)
                area_tex = MathTex(f"S \\approx {approx_area:.3f}", font_size=24, color=YELLOW)
                group = VGroup(n_tex, area_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
                # 放在坐标系右上角安全区
                group.to_corner(UR, buff=0.8)
                return group

            self.status_label = always_redraw(get_status_label)
            self.add(self.status_label)


# =========================================================================
# 4. 数轴动态游标仪 (Number Line Dynamic Cursor Rig)
# =========================================================================
class NumberLineCursorRig(VGroup):
    """
    一维数轴动态数值探针与高亮游标：
    支持标尺数轴、实时游标浮动标签以及当前区间高亮跟踪。
    """
    def __init__(
        self,
        number_line,
        tracker,
        label_prefix="x = ",
        cursor_color=YELLOW,
        label_color=None,
        decimal_places=2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.number_line = number_line
        self.tracker = tracker
        self.label_prefix = label_prefix
        self.cursor_color = cursor_color
        self.label_color = label_color or cursor_color
        self.decimal_places = decimal_places

        # 游标三角/圆点指示
        def get_cursor():
            val = self.tracker.get_value()
            pt = self.number_line.n2p(val)
            dot = Dot(pt, color=self.cursor_color, radius=0.08)
            arrow = Triangle(color=self.cursor_color, fill_opacity=1.0).scale(0.1)
            arrow.next_to(dot, UP, buff=0.06)
            return VGroup(dot, arrow)

        self.cursor = always_redraw(get_cursor)
        self.add(self.cursor)

        # 浮动动态数值标签
        def get_label():
            val = self.tracker.get_value()
            pt = self.number_line.n2p(val)
            tex = MathTex(
                f"{self.label_prefix}{val:.{self.decimal_places}f}",
                font_size=24,
                color=self.label_color
            )
            tex.next_to(pt, UP, buff=0.35)
            return tex

        self.label = always_redraw(get_label)
        self.add(self.label)


# =========================================================================
# 5. 沉浸式 3D 空间几何组件 (3D Space Rigs)
# =========================================================================
class GradientSurface(Surface):
    """
    高度深度渐变着色 3D 曲面：
    依据 z 坐标在曲面上的分布，通过色盘插值渲染立体渐变光泽
    """
    def __init__(
        self,
        func,
        u_range=(-2, 2),
        v_range=(-2, 2),
        resolution=(32, 32),
        color_gradient=(BLUE_E, TEAL, YELLOW),
        opacity=0.85,
        checkerboard_colors=False,
        **kwargs
    ):
        def param_func(u, v):
            return np.array([u, v, func(u, v)])

        super().__init__(
            param_func,
            u_range=u_range,
            v_range=v_range,
            resolution=resolution,
            checkerboard_colors=checkerboard_colors,
            fill_opacity=opacity,
            **kwargs
        )
        self.set_color_by_gradient(*color_gradient)


class Dynamic3DCursorRig(VGroup):
    """
    曲面 3D 动点追踪装置：
    空间动点在曲面上随 (u_tracker, v_tracker) 移动，
    自动绘制至 xy 平面的虚线正交投影。
    """
    def __init__(
        self,
        axes,
        func,
        u_tracker,
        v_tracker,
        dot_color=YELLOW,
        line_color=GREY_B,
        radius=0.08,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes = axes
        self.func = func
        self.u_tracker = u_tracker
        self.v_tracker = v_tracker
        self.dot_color = dot_color
        self.line_color = line_color
        self.radius = radius

        # 1. 空间曲面动点
        def get_dot():
            u = self.u_tracker.get_value()
            v = self.v_tracker.get_value()
            w = self.func(u, v)
            return Sphere(radius=self.radius, resolution=(12, 12), color=self.dot_color).move_to(self.axes.c2p(u, v, w))

        self.dot = always_redraw(get_dot)
        self.add(self.dot)

        # 2. 垂线至 xy 平面
        def get_v_line():
            u = self.u_tracker.get_value()
            v = self.v_tracker.get_value()
            w = self.func(u, v)
            p_surface = self.axes.c2p(u, v, w)
            p_plane = self.axes.c2p(u, v, 0)
            return DashedLine(p_plane, p_surface, color=self.line_color, stroke_width=2.0)

        self.v_line = always_redraw(get_v_line)
        self.add(self.v_line)

        # 3. xy 平面垂足点
        def get_foot():
            u = self.u_tracker.get_value()
            v = self.v_tracker.get_value()
            return Dot(self.axes.c2p(u, v, 0), color=self.line_color, radius=0.04)

        self.foot = always_redraw(get_foot)
        self.add(self.foot)


# =========================================================================
# 6. 经典高阶数学直觉组件库 (Advanced Intuition Rigs)
# =========================================================================
class LinearTransformRig(VGroup):
    """
    3Blue1Brown 标志性线性代数空间网格形变仪：
    展现“矩阵的本质是对空间的线性变换”。
    自动管理：
    - 二维仿射坐标网格线
    - 基向量 i_hat (1,0) 与 j_hat (0,1)
    - 行列式单位面积平行四边形 (实时反映面积缩放因子与手性翻转)
    """
    def __init__(
        self,
        plane_range=(-5, 5),
        i_color="#3B82F6",  # 天蓝
        j_color="#F97316",  # 活力赤橙
        area_color="#FBBF24", # 启迪金黄
        grid_color="#2A2E39",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.i_color = i_color
        self.j_color = j_color
        self.area_color = area_color
        self.grid_color = grid_color

        # 1. 仿射网格平面
        self.plane = NumberPlane(
            x_range=[plane_range[0], plane_range[1], 1],
            y_range=[plane_range[0], plane_range[1], 1],
            background_line_style={"stroke_color": grid_color, "stroke_width": 1.2},
            axis_config={"stroke_color": GREY_C, "stroke_width": 2.0}
        )
        self.add(self.plane)

        # 2. 追踪基向量终点坐标的追踪器 (初始为单位基向量)
        self.i_tracker = Vector(RIGHT, color=i_color, stroke_width=4.0)
        self.j_tracker = Vector(UP, color=j_color, stroke_width=4.0)

        # 3. 动态单位面积平行四边形 (行列式 det(A) 直观视觉)
        def get_det_square():
            p0 = self.plane.c2p(0, 0)
            pi = self.plane.c2p(1, 0)
            pj = self.plane.c2p(0, 1)
            p_diag = self.plane.c2p(1, 1)
            poly = Polygon(p0, pi, p_diag, pj, stroke_color=self.area_color, stroke_width=2.5)
            poly.set_fill(self.area_color, opacity=0.35)
            return poly

        self.unit_square = get_det_square()
        self.add(self.unit_square)
        self.add(self.i_tracker)
        self.add(self.j_tracker)

    def animate_matrix_transform(self, matrix, run_time=2.5, rate_func=smooth):
        """
        核心动画：平滑施加二维矩阵变换 [[a, b], [c, d]]
        同时驱动网格形变、基向量重定位以及行列式面积四边形变形！
        """
        np_matrix = np.array(matrix)
        # 计算行列式值
        det_val = np.linalg.det(np_matrix)

        # 将基向量和平面一同应用仿射变换
        anim_group = AnimationGroup(
            ApplyMatrix(np_matrix, self.plane, run_time=run_time, rate_func=rate_func),
            ApplyMatrix(np_matrix, self.unit_square, run_time=run_time, rate_func=rate_func),
            ApplyMatrix(np_matrix, self.i_tracker, run_time=run_time, rate_func=rate_func),
            ApplyMatrix(np_matrix, self.j_tracker, run_time=run_time, rate_func=rate_func),
        )
        return anim_group, det_val


class FourierCirclesRig(VGroup):
    """
    傅里叶级数周转轮与频域拟合装置：
    串联多组不同半径与角速度的旋转连杆相量，在末端绘制合成参数曲线。
    """
    def __init__(
        self,
        radii=(1.5, 0.8, 0.4),
        frequencies=(1, -2, 3),
        time_tracker=None,
        center=ORIGIN,
        colors=(BLUE, TEAL, YELLOW),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.radii = radii
        self.frequencies = frequencies
        self.time_tracker = time_tracker or ValueTracker(0.0)
        self.center_pt = center
        self.colors = colors

        def get_circles_and_vectors():
            group = VGroup()
            curr_center = self.center_pt
            t = self.time_tracker.get_value()

            for r, freq, col in zip(self.radii, self.frequencies, self.colors):
                circle = Circle(radius=r, color=col, stroke_width=1.5, stroke_opacity=0.4).move_to(curr_center)
                angle = freq * t * TAU
                target_pt = curr_center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
                vector = Arrow(curr_center, target_pt, buff=0, color=col, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
                group.add(circle, vector)
                curr_center = target_pt

            # 末端指示小点
            end_dot = Dot(curr_center, color=YELLOW, radius=0.06)
            group.add(end_dot)
            return group

        self.rig = always_redraw(get_circles_and_vectors)
        self.add(self.rig)

    def get_end_point(self):
        """获取当前最末端连杆的坐标"""
        t = self.time_tracker.get_value()
        curr_center = self.center_pt
        for r, freq in zip(self.radii, self.frequencies):
            angle = freq * t * TAU
            curr_center = curr_center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
        return curr_center
