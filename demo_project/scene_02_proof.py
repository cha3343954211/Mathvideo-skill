"""
Scene 02: 核心几何推演 (The Proof & Transformation)
构造边长为 (a+b) 的大正方形，通过对比两组全等直角三角形的拼放，揭示空白面积恒等。
"""
from manim import *
from theme_config import BaseMathScene, MathTheme

class Scene02Proof(BaseMathScene):
    def construct(self):
        super().construct()
        
        # 1. 标题与解说
        self.play_show_title("构造对称：无字之证", "Proof without Words")
        self.set_caption("构造两个完全相同的正方形，边长均为 (a + b)...")
        
        # 尺寸定义
        a, b = 1.8, 1.2
        L = a + b
        
        # 两个大正方形框：左侧 Box 1，右侧 Box 2
        box_left = Square(side_length=L, stroke_color=MathTheme.TEXT_MUTED, stroke_width=2.5)
        box_left.shift(LEFT * 3.3 + DOWN * 0.2)
        
        box_right = Square(side_length=L, stroke_color=MathTheme.TEXT_MUTED, stroke_width=2.5)
        box_right.shift(RIGHT * 3.3 + DOWN * 0.2)
        
        lbl_left = self.make_text("排列一：中央留出 c²", font_size=20, color=MathTheme.TEXT_MUTED).next_to(box_left, UP, buff=0.2)
        lbl_right = self.make_text("排列二：分割出 a² 与 b²", font_size=20, color=MathTheme.TEXT_MUTED).next_to(box_right, UP, buff=0.2)
        
        self.play(
            Create(box_left), Create(box_right),
            FadeIn(lbl_left), FadeIn(lbl_right),
            run_time=1.2
        )
        self.pause(0.8)
        
        # 2. 左边正方形内部：四个角放入 4 个直角三角形，中间留出一个倾斜的 c^2 正方形
        bl_bl = box_left.get_corner(DL)
        p1 = bl_bl + np.array([a, 0, 0])
        p2 = bl_bl + np.array([L, b, 0])
        p3 = bl_bl + np.array([b, L, 0])
        p4 = bl_bl + np.array([0, a, 0])
        
        # 中央空白正方形 (c^2)
        inner_c2 = Polygon(p1, p2, p3, p4, fill_color=MathTheme.YELLOW, fill_opacity=0.45, stroke_color=MathTheme.YELLOW, stroke_width=3)
        txt_c2 = MathTex("c^2", color=MathTheme.TEXT_MAIN, font_size=36).move_to(inner_c2.get_center())
        
        # 4 个蓝色角直角三角形
        t1 = Polygon(bl_bl, p1, p4, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        t2 = Polygon(bl_bl + np.array([L, 0, 0]), p2, p1, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        t3 = Polygon(bl_bl + np.array([L, L, 0]), p3, p2, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        t4 = Polygon(bl_bl + np.array([0, L, 0]), p4, p3, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        left_triangles = VGroup(t1, t2, t3, t4)
        
        self.play(FadeIn(left_triangles), run_time=1.0)
        self.play(DrawBorderThenFill(inner_c2), Write(txt_c2), run_time=1.2)
        self.pause(1.0)
        
        # 3. 右边正方形内部：同样 4 个直角三角形成对拼成两个矩形，留出 a^2 与 b^2
        self.set_caption("在右侧正方形中，将这4个完全一样的三角形重新组合...")
        
        br_bl = box_right.get_corner(DL)
        # a^2 区域在右上角 (边长 a)
        sq_a2 = Square(side_length=a, fill_color=MathTheme.BLUE, fill_opacity=0.45, stroke_color=MathTheme.BLUE, stroke_width=3)
        sq_a2.align_to(box_right, UP).align_to(box_right, RIGHT)
        txt_a2 = MathTex("a^2", color=MathTheme.TEXT_MAIN, font_size=34).move_to(sq_a2.get_center())
        
        # b^2 区域在左下角 (边长 b)
        sq_b2 = Square(side_length=b, fill_color=MathTheme.ORANGE, fill_opacity=0.45, stroke_color=MathTheme.ORANGE, stroke_width=3)
        sq_b2.align_to(box_right, DOWN).align_to(box_right, LEFT)
        txt_b2 = MathTex("b^2", color=MathTheme.TEXT_MAIN, font_size=34).move_to(sq_b2.get_center())
        
        # 两个矩形 (每个各含 2 个三角形)
        rect1 = Rectangle(width=a, height=b, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        rect1.align_to(box_right, UP).align_to(box_right, LEFT)
        
        rect2 = Rectangle(width=b, height=a, fill_color=MathTheme.BLUE, fill_opacity=0.35, stroke_width=1.5)
        rect2.align_to(box_right, DOWN).align_to(box_right, RIGHT)
        
        self.play(FadeIn(rect1), FadeIn(rect2), run_time=1.0)
        self.play(
            DrawBorderThenFill(sq_a2), Write(txt_a2),
            DrawBorderThenFill(sq_b2), Write(txt_b2),
            run_time=1.2
        )
        self.pause(1.5)
        
        # 清除过渡
        self.clear_caption()
        self.play(
            *[FadeOut(m) for m in [
                box_left, box_right, lbl_left, lbl_right,
                left_triangles, inner_c2, txt_c2,
                rect1, rect2, sq_a2, txt_a2, sq_b2, txt_b2,
                self.title_mobject
            ]],
            run_time=0.8
        )
