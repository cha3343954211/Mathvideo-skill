"""
BaseMathScene & MovingCameraMathScene: 高品质数学视频标准与动态摄影机基类
内建一键多主题引擎 (3b1b / Claude Light / Claude Dark) 与电影级运镜工具。
"""
from manim import *
import numpy as np
from contextlib import contextmanager
try:
    from layout_guard import LayoutGuard
except ImportError:
    from templates.layout_guard import LayoutGuard

try:
    from audio_engine import AudioEngine
except ImportError:
    from templates.audio_engine import AudioEngine

try:
    from visual_fx import MinimalistVisualFX, SleekPulse
except ImportError:
    from templates.visual_fx import MinimalistVisualFX, SleekPulse

class VoiceoverTracker:
    """语音上下文追踪器：提供音频实际时长 duration"""
    def __init__(self, duration, audio_path=None):
        self.duration = float(duration)
        self.audio_path = audio_path

# ==========================================
# 1. 统一设计规范系统 (Theme Design Tokens)
# ==========================================
class DesignToken:
    """主题设计属性规范"""
    def __init__(self, name, bg_color, text_main, text_muted, primary, secondary, accent, success, alert, grid_color, is_light=False):
        self.name = name
        self.bg_color = bg_color
        self.text_main = text_main
        self.text_muted = text_muted
        self.primary = primary          # 核心主体 (如集合 A, 主函数)
        self.secondary = secondary      # 辅助对比 (如集合 B, 切线)
        self.accent = accent            # 高光顿悟 (结论聚焦)
        self.success = success          # 守恒/相等
        self.alert = alert              # 悖论/死锁/冲突
        self.grid_color = grid_color    # 坐标系网格线
        self.is_light = is_light        # 是否为浅色纸张模式

# 预设的七款顶级美学主题家族
THEMES = {
    # 1. 经典 3Blue1Brown 科技极客暗黑风
    "3b1b_dark": DesignToken(
        name="3b1b_dark",
        bg_color="#121417",
        text_main="#ECEFF4",
        text_muted="#8892B0",
        primary="#3B82F6",      # 天蓝
        secondary="#F97316",    # 活力橙
        accent="#FBBF24",       # 启迪金黄
        success="#10B981",      # 翡翠绿
        alert="#EF4444",        # 珊瑚红
        grid_color="#2A2E39",
        is_light=False
    ),
    # 2. Claude 经典象牙浅米纸学术风 (Quanta / 剑桥学刊质感)
    "claude_light": DesignToken(
        name="claude_light",
        bg_color="#FBF9F5",     # 象牙米纸底
        text_main="#2B2723",    # 活版沉稳深墨
        text_muted="#756E65",   # 优雅灰褐
        primary="#2D5A7B",      # 墨韵石板蓝
        secondary="#CC5A36",    # Claude 招牌赤陶橙
        accent="#B57622",       # 暖金琥珀
        success="#3D6B48",      # 沉静鼠尾草绿
        alert="#B53826",        # 砖石焦红
        grid_color="#DCD5C9",
        is_light=True
    ),
    # 3. Claude 温暖深炭黑人文风
    "claude_dark": DesignToken(
        name="claude_dark",
        bg_color="#1C1C1A",     # 暖炭黑
        text_main="#EDE8E1",    # 羊皮暖白
        text_muted="#9B9488",   # 陶土灰褐
        primary="#5E81AC",      # 雅致石板蓝
        secondary="#D97757",    # Claude 赤陶橙
        accent="#DE9B52",       # 暖金琥珀
        success="#789D7E",      # 鼠尾草绿
        alert="#C45B4A",        # 珊瑚焦红
        grid_color="#302E2B",
        is_light=False
    ),
    # 4. Nord 冰川冷冽极光风
    "nord": DesignToken(
        name="nord",
        bg_color="#2E3440",     # 北极深暗夜
        text_main="#ECEFF4",    # 冰原雪白
        text_muted="#D8DEE9",   # 极地雾灰
        primary="#88C0D0",      # 极光青蓝 (Frost Cyan)
        secondary="#81A1C1",    # 冰河深蓝
        accent="#EBCB8B",       # 极光金黄
        success="#A3BE8C",      # 针叶林松绿
        alert="#BF616A",        # 极地冷红
        grid_color="#3B4252",
        is_light=False
    ),
    # 5. Chalkboard 经典常春藤大学黑板草绿质感
    "chalkboard": DesignToken(
        name="chalkboard",
        bg_color="#1A2A22",     # 哑光深墨绿黑板
        text_main="#F0F4F1",    # 自然粉笔白
        text_muted="#9BA8A0",   # 粉笔淡灰
        primary="#E8DE82",      # 柠檬粉笔黄
        secondary="#7BDCB5",    # 粉笔湖绿
        accent="#FFA07A",       # 粉笔亮橙粉
        success="#A8E6CF",      # 薄荷粉笔绿
        alert="#FF8B94",        # 粉笔朱红
        grid_color="#283C32",
        is_light=False
    ),
    # 6. Solarized Light 经典学术暖白象牙羊皮纸
    "solarized_light": DesignToken(
        name="solarized_light",
        bg_color="#FDF6E3",     # 暖白羊皮纸
        text_main="#586E75",    # 深铅灰墨
        text_muted="#93A1A1",   # 中铅灰
        primary="#268BD2",      # 清雅天蓝
        secondary="#CB4B16",    # 日出暖橙
        accent="#B58900",       # 学者琥珀金
        success="#859900",      # 橄榄青绿
        alert="#DC322F",        # 绯红
        grid_color="#EEE8D5",
        is_light=True
    ),
    # 7. Cyberpunk Neon 高能赛博微电子风
    "cyberpunk_neon": DesignToken(
        name="cyberpunk_neon",
        bg_color="#0D0B18",     # 极夜黑紫
        text_main="#F8F8F2",    # 纯净日光白
        text_muted="#6272A4",   # 电报灰蓝
        primary="#00F0FF",      # 赛博高亮青
        secondary="#FF2A85",    # 高能霓虹粉
        accent="#FFE600",       # 耀眼电光金
        success="#05FFA1",      # 荧光翡翠
        alert="#FF0055",        # 激光警示红
        grid_color="#1F1A3A",
        is_light=False
    )
}

# 默认全局字体
FONT_CHINESE = "Microsoft YaHei"

# 兼容旧代码引用别名
MathTheme = THEMES["3b1b_dark"]
ClaudeTheme = THEMES["claude_dark"]
ClaudeLightTheme = THEMES["claude_light"]
NordTheme = THEMES["nord"]
ChalkboardTheme = THEMES["chalkboard"]
SolarizedLightTheme = THEMES["solarized_light"]
CyberpunkTheme = THEMES["cyberpunk_neon"]


# ==========================================
# 2. 基础场景基类 (BaseMathScene)
# ==========================================
class BaseMathScene(Scene):
    """静态机位数学动画基类 (支持动态换肤、公式高级辅助与声画毫秒级同步)"""
    DEFAULT_THEME = "3b1b_dark"
    ENABLE_VOICEOVER = False  # 是否开启真人质感 TTS 配音 (由工作流第二步决策)
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        self.caption_mobject = None
        self.title_mobject = None
        self.voiceover_timeline = []  # 记录 [(audio_path, start_time_sec)]
        self.apply_theme(getattr(self, "theme_name", self.DEFAULT_THEME))

    @contextmanager
    def voiceover(self, text, voice=None, buffer_wait=0.2):
        """
        声画同步上下文管理器：
        自动根据台词生成/加载真人质感配音，将动画时长与实际音频物理时长锁死。
        同时自动刷新底部字幕！
        """
        # 自动同步刷新底部字幕
        self.set_caption(text)

        curr_time = self.renderer.time if hasattr(self, "renderer") else 0.0
        selected_voice = voice or getattr(self, "VOICE_NAME", "zh-CN-YunxiNeural")

        if getattr(self, "ENABLE_VOICEOVER", False):
            audio_path, duration = AudioEngine.generate_speech(text, voice=selected_voice)
            self.voiceover_timeline.append((str(audio_path), curr_time))
            tracker = VoiceoverTracker(duration=duration, audio_path=audio_path)
        else:
            # 纯净无声模式：依据中文字符数动态估算舒适的阅读停顿时间 (约每秒3.5字)
            estimated_duration = max(len(text) * 0.22, 2.0)
            tracker = VoiceoverTracker(duration=estimated_duration)

        try:
            yield tracker
        finally:
            if buffer_wait > 0:
                self.wait(buffer_wait)

    def apply_theme(self, theme_key):
        """一键应用主题色调"""
        self.theme = THEMES.get(theme_key, THEMES["3b1b_dark"])
        self.camera.background_color = self.theme.bg_color

    def make_text(self, text, font_size=28, color=None, **kwargs):
        """创建主题字体文本"""
        c = color if color is not None else self.theme.text_main
        return Text(text, font=FONT_CHINESE, font_size=font_size, color=c, **kwargs)

    def make_math(self, tex_string, font_size=36, color=None, **kwargs):
        """创建数学公式 (智能适配深色/浅色背景，杜绝公式隐形)"""
        c = color if color is not None else self.theme.text_main
        return MathTex(tex_string, font_size=font_size, color=c, **kwargs)

    def colorize_formula(self, math_tex, color_map):
        """
        公式智能多项式着色器：
        直接传入子字符串映射字典，例如 {"f(x)": BLUE, "x^2": ORANGE, "\\Delta x": RED}
        自动为公式指定部分精确着色，告别手动切片索引的痛苦！
        """
        for substring, color in color_map.items():
            math_tex.set_color_by_tex(substring, color)
        return math_tex

    def stepwise_tex_transform(self, old_tex, new_tex, run_time=1.2, transform_mismatches=True):
        """
        平滑公式渐变演化：
        自动继承旧公式位置并平滑演进匹配项，消除重叠与错位
        """
        new_tex.move_to(old_tex.get_center())
        self.play(
            TransformMatchingTex(
                old_tex,
                new_tex,
                transform_mismatches=transform_mismatches,
                run_time=run_time
            )
        )
        return new_tex

    def play_show_title(self, title_text, subtitle_text=None, font_size=36):
        """优雅无框留白标题"""
        title = self.make_text(title_text, font_size=font_size, color=self.theme.text_main)
        title.to_edge(UP, buff=0.45)
        
        elements = [title]
        if subtitle_text:
            sub = self.make_text(subtitle_text, font_size=font_size * 0.52, color=self.theme.secondary)
            sub.next_to(title, DOWN, buff=0.15)
            elements.append(sub)
            
        group = VGroup(*elements)
        self.title_mobject = group
        self.play(FadeIn(group, shift=DOWN * 0.25), run_time=0.8)
        return group

    def set_caption(self, text, font_size=20, color=None, max_width=11.2):
        """
        纯粹优雅单行字幕 (Strict Single-Line Elegant Mode)：
        永远保持利落单行，绝不折出笨重两行，动态自适应缩放保证 100% 杜绝出界。
        """
        c = color if color is not None else self.theme.text_muted
        # 移除任何意外传入的换行符，强制保证单行清爽
        single_line_text = text.replace("\n", " ").strip()

        # 根据字数动态微调基础字号 (字数越多，字号越精致小巧)
        char_count = len(single_line_text)
        if char_count > 30:
            actual_font_size = 15.5
        elif char_count > 22:
            actual_font_size = 17.5
        else:
            actual_font_size = font_size

        txt = self.make_text(single_line_text, font_size=actual_font_size, color=c)

        # 绝对安全宽度保底：若仍超宽则等比压缩，杜绝切边
        if txt.get_width() > max_width:
            txt.scale_to_fit_width(max_width)

        txt.to_edge(DOWN, buff=0.38)
        if self.caption_mobject is None:
            self.play(FadeIn(txt, shift=UP * 0.1), run_time=0.3)
        else:
            self.play(ReplacementTransform(self.caption_mobject, txt), run_time=0.3)
        self.caption_mobject = txt
        return txt

    def clear_caption(self):
        """清除底部字幕"""
        if self.caption_mobject:
            self.play(FadeOut(self.caption_mobject), run_time=0.3)
            self.caption_mobject = None

    def focus_on(self, mobject, color=None, scale_factor=1.08):
        """高光聚焦外框动画"""
        c = color if color is not None else self.theme.accent
        box = SurroundingRectangle(mobject, color=c, buff=0.15, stroke_width=2.5)
        self.play(Create(box), run_time=0.5)
        self.play(mobject.animate.scale(scale_factor), run_time=0.3)
        self.play(mobject.animate.scale(1 / scale_factor), run_time=0.3)
        self.wait(0.6)
        self.play(FadeOut(box), run_time=0.4)

    def pause(self, t=1.2):
        self.wait(t)

    def scan_collisions(self, min_buff=0.10, verbose=True):
        """扫描当前场景内的所有元素，检测是否存在空间碰撞与重叠"""
        return LayoutGuard.detect_scene_collisions(self, min_buff=min_buff, verbose=verbose)

    def keep_in_bounds(self, mobject, safe_margin=0.55):
        """确保传入的 Mobject 完全处于屏幕安全视口内，超限自动缩放并拉回"""
        camera_frame = getattr(self, "camera_frame", None)
        return LayoutGuard.keep_in_safe_bounds(mobject, camera_frame=camera_frame, safe_margin=safe_margin)

    def avoid_overlap(self, target_mob, obstacles, direction=DOWN, buff=0.35):
        """智能避让：顺着 direction 方向将 target_mob 推开直至完全脱离所有 obstacles"""
        return LayoutGuard.avoid_overlap(target_mob, obstacles, direction=direction, buff=buff)

    # ---------------- 克制高级视效扩展 (Minimalist Visual FX) ----------------
    def add_ambient_glow(self, target_mobject, tint_color=None, opacity=0.06, buff=0.6):
        """添加苹果级超低透明度漫反射底衬，绝不破坏文字笔画的锐利度"""
        color = tint_color or self.theme.accent
        backing = MinimalistVisualFX.create_ambient_backing(target_mobject, tint_color=color, buff=buff, opacity=opacity)
        self.add(backing, target_mobject)
        return backing

    def add_sleek_horizon(self, target_mobject, accent_color=None, stroke_width=1.8):
        """在目标下方添加极简优雅的细线地平线 (1.8px)"""
        color = accent_color or self.theme.accent
        horizon = MinimalistVisualFX.create_sleek_horizon(target_mobject, accent_color=color, stroke_width=stroke_width)
        self.add(horizon)
        return horizon

    def play_focus_revelation(self, target_mobject, accent_color=None, surround_mobjects_to_dim=None, sink_shift=DOWN * 0.45, run_time=1.8):
        """
        3Blue1Brown 标志性纯粹顿悟时刻：
        视线暗场聚光 (Focus Dimming) + 元素沉降分离 (Sink & Dim) + 极简地平线丝滑生长，
        完全去框去遮挡，纯净通透。
        """
        color = accent_color or self.theme.accent
        return MinimalistVisualFX.play_pure_revelation(
            self,
            target_formula=target_mobject,
            accent_color=color,
            background_mobjects=surround_mobjects_to_dim,
            sink_shift=sink_shift,
            run_time=run_time
        )

    def dim_surroundings(self, background_mobjects, dim_opacity=0.18, run_time=1.0):
        """将全场背景与次要图形平滑暗化，消除视觉干扰"""
        return MinimalistVisualFX.play_focus_dimming(
            self,
            focus_mobjects=[],
            background_mobjects=background_mobjects,
            dim_opacity=dim_opacity,
            run_time=run_time
        )


# 便捷子类定义
class ClaudeScene(BaseMathScene):
    DEFAULT_THEME = "claude_dark"

class ClaudeLightScene(BaseMathScene):
    DEFAULT_THEME = "claude_light"

class NordScene(BaseMathScene):
    DEFAULT_THEME = "nord"

class ChalkboardScene(BaseMathScene):
    DEFAULT_THEME = "chalkboard"


# ==========================================
# 3. 动态电影级运镜基类 (MovingCameraMathScene)
# ==========================================
class MovingCameraMathScene(MovingCameraScene, BaseMathScene):
    """
    电影级动态摄影机数学动画基类
    封装相机平滑推近 (Zoom in)、拉远 (Zoom out)、横移追踪 (Pan) 等运镜能力。
    """
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        BaseMathScene.construct(self)
        self.camera_frame = self.camera.frame
        self.default_frame_width = self.camera_frame.width
        self.default_frame_height = self.camera_frame.height
        self.default_frame_center = np.array([0.0, 0.0, 0.0])

    def camera_zoom_to(self, mobject, scale_factor=0.6, buff=0.8, run_time=1.8, rate_func=smooth):
        """
        电影级推镜 (Zoom In)：平滑将摄影机聚焦到某个局部 Mobject
        scale_factor < 1.0 为推近放大，scale_factor > 1.0 为拉远广角
        """
        target_center = mobject.get_center()
        target_width = max(mobject.width * (1.0 / scale_factor) + buff, 3.5)
        
        self.play(
            self.camera_frame.animate.set_width(target_width).move_to(target_center),
            run_time=run_time,
            rate_func=rate_func
        )

    def camera_pan_to(self, target_position, run_time=1.5, rate_func=smooth):
        """横移镜头 (Pan)：平滑将相机中心平移到指定坐标"""
        self.play(
            self.camera_frame.animate.move_to(target_position),
            run_time=run_time,
            rate_func=rate_func
        )

    def camera_reset(self, run_time=1.6, rate_func=smooth):
        """平滑重置镜头到标准全景视角"""
        self.play(
            self.camera_frame.animate.set_width(self.default_frame_width).move_to(self.default_frame_center),
            run_time=run_time,
            rate_func=rate_func
        )

    def set_caption(self, text, font_size=22, color=None):
        """动态相机感知字幕：无论镜头如何缩放平移，字幕始终智能贴合在当前视口底部！"""
        c = color if color is not None else self.theme.text_muted
        
        # 依据当前相机帧的缩放比例自适应缩放字幕
        frame_scale = self.camera_frame.height / self.default_frame_height
        adapted_size = font_size * frame_scale
        
        txt = self.make_text(text, font_size=adapted_size, color=c)
        txt.move_to(self.camera_frame.get_bottom() + UP * (0.4 * frame_scale))
        
        if self.caption_mobject is None:
            self.play(FadeIn(txt, shift=UP * (0.15 * frame_scale)), run_time=0.4)
        else:
            self.play(ReplacementTransform(self.caption_mobject, txt), run_time=0.4)
        self.caption_mobject = txt
        return txt


# ==========================================
# 4. 沉浸式 3D 立体几何数学场景基类 (ThreeDMathScene)
# ==========================================
class ThreeDMathScene(ThreeDScene, BaseMathScene):
    """
    沉浸式 3D 数学动画基类
    特性：
    1. 纯净 HUD 层设计：标题、字幕、公式卡片通过 add_fixed_in_frame_mobjects 锁定在二维正交视口，
       无论 3D 相机如何俯仰旋转，文字永不倒置变形！
    2. 平滑视角过渡：smooth_camera_orientation(phi, theta, zoom, run_time)
    3. 慢速环绕轨道运镜：start_orbital_flight(rate) / stop_orbital_flight()
    """
    DEFAULT_THEME = "nord"

    def construct(self):
        BaseMathScene.construct(self)

    def play_show_title(self, title_text, subtitle_text=None, font_size=36):
        """HUD 固定正交标题"""
        title = self.make_text(title_text, font_size=font_size, color=self.theme.text_main)
        title.to_edge(UP, buff=0.45)
        
        elements = [title]
        if subtitle_text:
            sub = self.make_text(subtitle_text, font_size=font_size * 0.52, color=self.theme.secondary)
            sub.next_to(title, DOWN, buff=0.15)
            elements.append(sub)
            
        group = VGroup(*elements)
        self.title_mobject = group
        self.add_fixed_in_frame_mobjects(group)
        self.play(FadeIn(group, shift=DOWN * 0.25), run_time=0.8)
        return group

    def set_caption(self, text, font_size=22, color=None):
        """HUD 固定正交字幕：锁定视口底端，绝不随 3D 相机翻转"""
        c = color if color is not None else self.theme.text_muted
        txt = self.make_text(text, font_size=font_size, color=c)
        txt.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(txt)
        if self.caption_mobject is None:
            self.play(FadeIn(txt, shift=UP * 0.15), run_time=0.4)
        else:
            self.play(ReplacementTransform(self.caption_mobject, txt), run_time=0.4)
        self.caption_mobject = txt
        return txt

    def add_hud(self, *mobjects):
        """将任意 Mobject 锁定在 2D 视口平面 (HUD 模式)"""
        self.add_fixed_in_frame_mobjects(*mobjects)

    def smooth_camera_orientation(self, phi=None, theta=None, gamma=None, zoom=None, run_time=2.0, rate_func=smooth):
        """电影级 3D 相机平滑运镜：从当前视角平滑过渡至目标俯仰角与方位角"""
        kwargs = {"run_time": run_time, "rate_func": rate_func}
        if phi is not None:
            kwargs["phi"] = phi
        if theta is not None:
            kwargs["theta"] = theta
        if gamma is not None:
            kwargs["gamma"] = gamma
        if zoom is not None:
            kwargs["zoom"] = zoom
        self.move_camera(**kwargs)

    def start_orbital_flight(self, rate=0.08):
        """开启 3D 空间环绕巡航漫游运镜"""
        self.begin_ambient_camera_rotation(rate=rate)

    def stop_orbital_flight(self):
        """停止环绕漫游"""
        self.stop_ambient_camera_rotation()
