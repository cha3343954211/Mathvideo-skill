"""
Scene 01: 引子与直觉提问 (The Hook)
提出问题：两条直角边的平方和，为什么永远等于斜边的平方？
"""
from manim import *
from theme_config import BaseMathScene, MathTheme

class Scene01Intro(BaseMathScene):
    def construct(self):
        super().construct()
        
        # 1. 播放标题
        title = self.play_show_title("勾股定理：几何直观证明", "Pythagorean Theorem: Visual Proof")
        self.set_caption("在任意直角三角形中，两直角边与斜边存在永恒的秘密...")
        
        # 2. 构造直角三角形 (a=3, b=2) 居中偏下
        scale = 0.8
        a = 3.0 * scale
        b = 2.0 * scale
        
        p_c = np.array([-1.5, -1.0, 0])      # 直角顶点
        p_a = p_c + np.array([a, 0, 0])     # 直角边 a 的端点
        p_b = p_c + np.array([0, b, 0])     # 直角边 b 的端点
        
        triangle = Polygon(p_c, p_a, p_b, color=MathTheme.BLUE, fill_opacity=0.3, stroke_width=4)
        
        # 直角标记
        right_angle = RightAngle(
            Line(p_c, p_a), Line(p_c, p_b),
            length=0.35, color=MathTheme.TEXT_MUTED
        )
        
        # 边长标注
        label_a = MathTex("a", color=MathTheme.TEXT_MAIN).next_to(Line(p_c, p_a), DOWN, buff=0.15)
        label_b = MathTex("b", color=MathTheme.TEXT_MAIN).next_to(Line(p_c, p_b), LEFT, buff=0.15)
        label_c = MathTex("c", color=MathTheme.TEXT_MAIN).next_to(Line(p_a, p_b).get_center(), UP + RIGHT, buff=0.1)
        
        tri_group = VGroup(triangle, right_angle, label_a, label_b, label_c)
        
        self.play(Create(triangle), Create(right_angle), run_time=1.2)
        self.play(Write(label_a), Write(label_b), Write(label_c), run_time=1.0)
        self.pause(1.0)
        
        # 3. 三条边向外长出正方形 (几何直观)
        self.set_caption("三条边各自向外延伸出正方形，面积分别为 a², b² 和 c²")
        
        # 边 a 对应正方形 (下侧)
        sq_a = Square(side_length=a, fill_color=MathTheme.BLUE, fill_opacity=0.4, stroke_color=MathTheme.BLUE)
        sq_a.next_to(Line(p_c, p_a), DOWN, buff=0)
        txt_a2 = MathTex("a^2", color=MathTheme.TEXT_MAIN).move_to(sq_a.get_center())
        
        # 边 b 对应正方形 (左侧)
        sq_b = Square(side_length=b, fill_color=MathTheme.ORANGE, fill_opacity=0.4, stroke_color=MathTheme.ORANGE)
        sq_b.next_to(Line(p_c, p_b), LEFT, buff=0)
        txt_b2 = MathTex("b^2", color=MathTheme.TEXT_MAIN).move_to(sq_b.get_center())
        
        self.play(
            GrowFromEdge(sq_a, UP), Write(txt_a2),
            GrowFromEdge(sq_b, RIGHT), Write(txt_b2),
            run_time=1.5
        )
        self.pause(1.2)
        
        # 提出核心疑问
        self.set_caption("如何不靠繁琐计算，仅凭一双眼睛就能看清：a² + b² = c²？")
        self.pause(1.5)
        
        # 清场过渡
        self.clear_caption()
        self.play(
            *[FadeOut(mob) for mob in [tri_group, sq_a, txt_a2, sq_b, txt_b2, title]],
            run_time=0.8
        )
