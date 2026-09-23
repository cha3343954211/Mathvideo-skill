# Manim 最佳工程实践规范 (Best Practices)

## 一、对象管理与生命周期

1. **组合优于单体 (Embrace VGroup)**
   - 将逻辑相关的对象打包装入 `VGroup`，统一进行位移、缩放与淡入淡出：
     ```python
     formula_box = VGroup(rect, formula, label)
     self.play(FadeIn(formula_box, shift=UP))
     ```
2. **显式销毁 (Clean Up Explicitly)**
   - 每个逻辑段落结束时，务必将不再使用的临时辅助线、箭头、中间公式移出屏幕：
     ```python
     self.play(*[FadeOut(mob) for mob in [arrow, label_old]], run_time=0.5)
     ```

---

## 二、坐标系与函数绘制

1. **始终使用 `Axes` 或 `NumberPlane` 的内置方法映射坐标**
   - 严禁用裸坐标放置点：
     ```python
     # 错误做法：绝对世界坐标
     dot = Dot(point=[2, 3, 0])
     
     # 正确做法：使用坐标系自带的 c2p (coords_to_point)
     axes = Axes(x_range=[-2, 5], y_range=[-1, 8])
     dot = Dot(axes.c2p(2, 3), color=MathTheme.ORANGE)
     ```
2. **动态切线与割线标准模式**
   - 使用 `ValueTracker` 动态驱动切点 $x$ 的演化：
     ```python
     t = ValueTracker(1.0)
     dot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), f(t.get_value())), color=YELLOW))
     tangent = always_redraw(lambda: axes.get_tangent_line(axes.c2p(t.get_value(), f(t.get_value())), f))
     self.play(t.animate.set_value(3.5), run_time=3.0, rate_func=smooth)
     ```

---

## 三、公式演化与推导规范

1. **拆解复杂 LaTeX 字符串**
   - 避免将一整行公式写成一个字符串，按符号单元切分，以便做局部的 `TransformMatchingTex` 或变色：
     ```python
     eq1 = MathTex("a^2", "+", "b^2", "=", "c^2")
     eq1[0].set_color(MathTheme.BLUE)
     eq1[2].set_color(MathTheme.GREEN)
     eq1[4].set_color(MathTheme.YELLOW)
     ```
2. **符号对齐推导**
   - 多行公式推导时，使用 `align_to` 保持等号对齐：
     ```python
     step2.next_to(step1, DOWN, buff=0.3)
     step2.align_to(step1[3], LEFT) # 对齐等号
     ```

---

## 四、渲染效能优化

1. **调试阶段强制使用 `-ql`**
   - 480p 15fps 渲染只需数秒，调试排版与动画逻辑完毕后再使用 `-qh`。
2. **单帧渲染验证排版 `-s`**
   - 只想看最终定格画面排版是否出界或重叠时，直接运行：
     ```bash
     python -m manim render -s scene.py MyScene
     ```
   - 会立即在最后一帧生成高清 PNG 图片，极其高效。
