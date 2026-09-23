"""
layout_guard.py: 空间排版与包围盒碰撞检测器
为 Manim 数学动画提供工业级 AABB 包围盒相交检测、边界溢出预防与智能避让系统。
彻底告别公式文字相互穿透、遮挡重叠和切边溢出。
"""
from manim import *
import numpy as np
import sys

# 增强 Windows 终端编码健壮性
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class BoundingBox2D:
    """二维轴对齐包围盒 (AABB)"""
    def __init__(self, left, right, bottom, top):
        self.left = float(left)
        self.right = float(right)
        self.bottom = float(bottom)
        self.top = float(top)

    @property
    def width(self):
        return max(0.0, self.right - self.left)

    @property
    def height(self):
        return max(0.0, self.top - self.bottom)

    @property
    def center(self):
        return np.array([(self.left + self.right) / 2.0, (self.bottom + self.top) / 2.0, 0.0])

    def intersects(self, other, buff=0.0):
        """检测两个包围盒在考虑安全边距 buff 的情况下是否相交"""
        return not (
            self.right + buff <= other.left or
            self.left - buff >= other.right or
            self.top + buff <= other.bottom or
            self.bottom - buff >= other.top
        )

    def get_overlap_vector(self, other):
        """计算两个相交包围盒之间的重叠深度向量 (dx, dy)"""
        dx = min(self.right, other.right) - max(self.left, other.left)
        dy = min(self.top, other.top) - max(self.bottom, other.bottom)
        if dx > 0 and dy > 0:
            return dx, dy
        return 0.0, 0.0

    def __repr__(self):
        return f"BBox(x=[{self.left:.2f}, {self.right:.2f}], y=[{self.bottom:.2f}, {self.top:.2f}])"


class LayoutGuard:
    """智能空间排版卫士与冲突雷达"""

    DEFAULT_SCREEN_WIDTH = 14.2222
    DEFAULT_SCREEN_HEIGHT = 8.0

    @staticmethod
    def get_bbox(mobject):
        """获取任意 Mobject 的精确 2D 包围盒"""
        # 兼容空组或不可见点
        if mobject.width == 0 and mobject.height == 0:
            p = mobject.get_center()
            return BoundingBox2D(p[0], p[0], p[1], p[1])
        
        left = mobject.get_left()[0]
        right = mobject.get_right()[0]
        bottom = mobject.get_bottom()[1]
        top = mobject.get_top()[1]
        return BoundingBox2D(left, right, bottom, top)

    @classmethod
    def check_overlap(cls, mob_a, mob_b, min_buff=0.12):
        """检测两个对象是否发生空间重叠或安全间距不足"""
        bbox_a = cls.get_bbox(mob_a)
        bbox_b = cls.get_bbox(mob_b)
        return bbox_a.intersects(bbox_b, buff=-min_buff)

    @classmethod
    def detect_scene_collisions(cls, scene, min_buff=0.10, verbose=True):
        """
        全场景碰撞扫描雷达：
        遍历 scene 当前所有可见前景对象，执行两两空间交叠分析，
        输出详细冲突诊断报告。
        """
        # 过滤掉背景、空组及全屏网格等基础辅助线
        candidates = []
        for mob in scene.mobjects:
            # 过滤不可见或尺寸接近全屏的背景
            if mob.width >= cls.DEFAULT_SCREEN_WIDTH * 0.98 and mob.height >= cls.DEFAULT_SCREEN_HEIGHT * 0.98:
                continue
            if mob.width > 0.05 and mob.height > 0.05:
                candidates.append(mob)

        collisions = []
        n = len(candidates)
        for i in range(n):
            for j in range(i + 1, n):
                mob_a = candidates[i]
                mob_b = candidates[j]
                
                # 若互为父子包含关系（即同一个 Group 的子部件），不视为冲突
                if mob_b in mob_a.submobjects or mob_a in mob_b.submobjects:
                    continue

                bbox_a = cls.get_bbox(mob_a)
                bbox_b = cls.get_bbox(mob_b)

                if bbox_a.intersects(bbox_b, buff=-min_buff):
                    dx, dy = bbox_a.get_overlap_vector(bbox_b)
                    collisions.append({
                        "mob_a": mob_a,
                        "mob_b": mob_b,
                        "overlap_dx": dx,
                        "overlap_dy": dy
                    })

        if verbose and collisions:
            print(f"\n[LayoutGuard WARNING] 场景 '{scene.__class__.__name__}' 检测到 {len(collisions)} 处空间碰撞冲突！")
            for idx, c in enumerate(collisions, 1):
                name_a = c["mob_a"].__class__.__name__
                name_b = c["mob_b"].__class__.__name__
                print(f"  [{idx}] {name_a} 与 {name_b} 重叠侵入 (dx={c['overlap_dx']:.2f}, dy={c['overlap_dy']:.2f})")
        elif verbose:
            print(f"[LayoutGuard OK] 场景 '{scene.__class__.__name__}' 空间健康度良好，未发现任何元素碰撞重叠。")

        return collisions

    @classmethod
    def keep_in_safe_bounds(cls, mobject, camera_frame=None, safe_margin=0.55):
        """
        智能屏幕安全边界守护：
        若对象超出屏幕渲染安全区，自动等比缩放并拉回安全视口内，杜绝任何字符切边或出界。
        """
        if camera_frame is not None:
            max_w = camera_frame.width - safe_margin * 2
            max_h = camera_frame.height - safe_margin * 2
            center = camera_frame.get_center()
        else:
            max_w = cls.DEFAULT_SCREEN_WIDTH - safe_margin * 2
            max_h = cls.DEFAULT_SCREEN_HEIGHT - safe_margin * 2
            center = np.array([0.0, 0.0, 0.0])

        # 1. 超宽/超高自动等比缩放
        if mobject.width > max_w:
            mobject.scale_to_fit_width(max_w)
        if mobject.height > max_h:
            mobject.scale_to_fit_height(max_h)

        # 2. 检查越界并平移拉回
        bbox = cls.get_bbox(mobject)
        left_bound = center[0] - max_w / 2.0
        right_bound = center[0] + max_w / 2.0
        bottom_bound = center[1] - max_h / 2.0
        top_bound = center[1] + max_h / 2.0

        shift_x = 0.0
        shift_y = 0.0

        if bbox.left < left_bound:
            shift_x = left_bound - bbox.left
        elif bbox.right > right_bound:
            shift_x = right_bound - bbox.right

        if bbox.bottom < bottom_bound:
            shift_y = bottom_bound - bbox.bottom
        elif bbox.top > top_bound:
            shift_y = top_bound - bbox.top

        if abs(shift_x) > 1e-4 or abs(shift_y) > 1e-4:
            mobject.shift(np.array([shift_x, shift_y, 0.0]))

        return mobject

    @classmethod
    def avoid_overlap(cls, target_mob, obstacles, direction=DOWN, buff=0.35, max_steps=8):
        """
        自动避让推移器：
        若 target_mob 与已有 obstacles 发生包围盒冲突，
        顺着 direction 方向自动推移，直至完全离开所有障碍物并保持充足留白 buff。
        """
        if not isinstance(obstacles, (list, tuple, VGroup, Group)):
            obstacles = [obstacles]

        for _ in range(max_steps):
            collision = False
            for obs in obstacles:
                if obs is target_mob:
                    continue
                if cls.check_overlap(target_mob, obs, min_buff=0.05):
                    collision = True
                    # 沿着 direction 方向顺延推开
                    target_mob.next_to(obs, direction, buff=buff)
                    break
            if not collision:
                break

        return target_mob
