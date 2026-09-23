# 常用数学动画典型模式库 (Design Patterns)

本参考库汇总了数学视频中最具教学穿透力的高频动效代码范式，可直接借鉴与组装。

---

## 模式 1：导数切线与动态极限 (Calculus: Tangent & Secant)

**教学目标**：展示割线随着 $\Delta x \to 0$ 逼近切线的极限过程。

```python
from manim import *

class TangentSecantPattern(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 10, 2], x_length=7, y_length=5)
        curve = axes.plot(lambda x: 0.3 * (x - 1)**2 + 1, color="#3B82F6")
        
        dx = ValueTracker(2.5) # 割线步长
        x0 = 2.0
        
        # 动态割线
        secant = always_redraw(lambda: 
            axes.get_secant_slope_group(
                x=x0,
                graph=curve,
                dx=dx.get_value(),
                dx_line_color="#F97316",
                df_line_color="#EAB308",
                secant_line_color="#10B981",
                secant_line_length=5
            )
        )
        
        self.play(Create(axes), Create(curve))
        self.add(secant)
        self.wait(1)
        # 逼近动画：让 dx 逐渐趋近于 0.001
        self.play(dx.animate.set_value(0.01), run_time=4.0, rate_func=smooth)
        self.wait(1.5)
```

---

## 模式 2：黎曼积分面积逼近 (Calculus: Riemann Sum)

**教学目标**：矩形数量从少到多，展示面积积分逼近。

```python
from manim import *

class RiemannSumPattern(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 6, 1], x_length=7, y_length=4.5)
        curve = axes.plot(lambda x: 0.2 * x**2 + 0.5, color="#3B82F6")
        
        rects_coarse = axes.get_riemann_rectangles(curve, x_range=[0.5, 4.5], dx=1.0, color="#10B981")
        rects_fine = axes.get_riemann_rectangles(curve, x_range=[0.5, 4.5], dx=0.1, color="#10B981")
        
        self.play(Create(axes), Create(curve))
        self.play(Create(rects_coarse), run_time=1.5)
        self.wait(1)
        self.play(ReplacementTransform(rects_coarse, rects_fine), run_time=2.5)
        self.wait(1.5)
```

---

## 模式 3：线性变换与网格形变 (Linear Algebra: Matrix Transform)

**教学目标**：直观展示一个矩阵将二维空间基底拉伸旋转。

```python
from manim import *

class LinearTransformPattern(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        matrix = [[2, 1], [0.5, 1.5]]
        self.apply_matrix(matrix)
        self.wait(1.5)
```

---

## 模式 4：核心结论聚光灯强调 (The Spotlight Pattern)

**教学目标**：在观众看到关键结论时，进行聚焦引导。

```python
def highlight_focus(scene, mobject):
    surround = SurroundingRectangle(mobject, color="#EAB308", buff=0.15, stroke_width=3)
    arrow = Arrow(start=UP * 0.8, end=ORIGIN, color="#EAB308").next_to(surround, UP)
    scene.play(Create(surround), GrowArrow(arrow), run_time=0.8)
    scene.play(Indicate(mobject, color="#EAB308", scale_factor=1.1), run_time=0.8)
    scene.wait(1.0)
    scene.play(FadeOut(surround), FadeOut(arrow), run_time=0.5)
```
