"""
BaseMathScene & MovingCameraMathScene: 高品质数学视频标准与动态摄影机基类
内建一键多主题引擎 (3b1b / Claude Light / Claude Dark) 与电影级运镜工具。
"""
from manim import *
import numpy as np
from pathlib import Path
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
    ),
    # 8. Blueprint 工程蓝图机械制图风 (解析几何/机构联动/空间向量)
    "blueprint": DesignToken(
        name="blueprint",
        bg_color="#0A192F",     # 深海蓝图底
        text_main="#E6F1FF",    # 制图浅银白
        text_muted="#8892B0",   # 蓝图辅助灰
        primary="#64FFDA",      # 激光电光青 (Blueprint Cyan)
        secondary="#FBBF24",    # 标尺琥珀金
        accent="#FF6B6B",       # 关键标注珊瑚红
        success="#34D399",      # 检验通过绿
        alert="#F87171",        # 尺寸公差警报红
        grid_color="#172A45",   # 蓝图精密毫米网格
        is_light=False
    ),
    # 9. Ink Wash 东方水墨古典风 (数学史/算经/古代几何/优雅推导)
    "ink_wash": DesignToken(
        name="ink_wash",
        bg_color="#F4EFE6",     # 仿古生宣纸浅米底
        text_main="#1C1917",    # 沉厚松烟浓墨
        text_muted="#78716C",   # 宿墨淡灰
        primary="#1E3A5F",      # 黛蓝青墨
        secondary="#78350F",    # 赭石熟褐
        accent="#B91C1C",       # 朱砂古印泥红 (核心顿悟点)
        success="#2E5A36",      # 苍竹墨绿
        alert="#991B1B",        # 焦褐朱红
        grid_color="#E2D9CC",   # 浅茶宣纸水印线
        is_light=True
    ),
    # 10. Swiss Modern 瑞士现代主义平面设计风 (集合论/形式公理/概率论)
    "swiss_modern": DesignToken(
        name="swiss_modern",
        bg_color="#F0F2F5",     # 现代工业灰白
        text_main="#0F172A",    # 极致赫尔维提卡黑
        text_muted="#64748B",   # 建筑中性灰
        primary="#002FA7",      # 国际克莱因蓝 (Klein Blue)
        secondary="#FF4500",    # 国际安全橙 (Safety Orange)
        accent="#D97706",       # 现代琥珀
        success="#059669",      # 功能主义翡翠
        alert="#DC2626",        # 国际警示纯红
        grid_color="#D8DEE9",   # 瑞士模数网格
        is_light=True
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
BlueprintTheme = THEMES["blueprint"]
InkWashTheme = THEMES["ink_wash"]
SwissModernTheme = THEMES["swiss_modern"]


# ==========================================
# 2. 基础场景基类 (BaseMathScene)
# ==========================================
class BaseMathScene(Scene):
    """静态机位数学动画基类 (支持动态换肤、公式高级辅助与声画毫秒级同步)"""
    DEFAULT_THEME = "3b1b_dark"
    ENABLE_VOICEOVER = False  # 是否开启真人质感 TTS 配音 (由工作流第二步决策)
    TTS_ENGINE = "auto"       # TTS 引擎模式: "auto" | "local" (离线 SAPI) | "edge"
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        self.caption_mobject = None
        self.title_mobject = None
        self.voiceover_timeline = []  # 记录 [(audio_path, start_time_sec)]
        self.apply_theme(getattr(self, "theme_name", self.DEFAULT_THEME))

    def tear_down(self):
        super().tear_down()
        import json
        scene_name = self.__class__.__name__
        if getattr(self, "voiceover_timeline", None):
            out_dir = Path("media/audio_sync")
            out_dir.mkdir(parents=True, exist_ok=True)
            meta = {
                "scene": scene_name,
                "voiceovers": getattr(self, "voiceover_timeline", [])
            }
            with open(out_dir / f"{scene_name}_timeline.json", "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)

    @contextmanager
    def voiceover(self, text, voice=None, engine=None, buffer_wait=0.2):
        """
        声画同步上下文管理器：
        自动根据台词生成/加载真人质感配音，将动画时长与实际音频物理时长锁死。
        同时自动刷新底部字幕！
        """
        # 沉浸式叙事台词安全守卫 (严格禁止“摄像机/运镜”等元台词泄漏进字幕与音频)
        meta_words = ["摄像机", "摄影机", "推镜", "拉远", "横移", "镜头拉", "镜头推", "镜头移", "镜头旋转", "切镜头"]
        found_meta = [w for w in meta_words if w in text]
        if found_meta:
            import warnings
            warnings.warn(
                f"\n[沉浸叙事防爆警告] 台词中包含了破坏沉浸感的运镜技术术语: {found_meta}！台词内容: '{text}'。\n"
                f"解说词必须是纯粹的人文数学纪录片语言，将运镜作为无形的视听增强！",
                UserWarning
            )

        # 自动同步刷新底部字幕
        self.set_caption(text)

        curr_time = self.renderer.time if hasattr(self, "renderer") else 0.0
        selected_voice = voice or getattr(self, "VOICE_NAME", "zh-CN-YunxiNeural")
        selected_engine = engine or getattr(self, "TTS_ENGINE", "auto")

        if getattr(self, "ENABLE_VOICEOVER", False):
            audio_path, duration = AudioEngine.generate_speech(text, voice=selected_voice, engine=selected_engine)
            self.voiceover_timeline.append((str(audio_path), curr_time))
            tracker = VoiceoverTracker(duration=duration, audio_path=audio_path)
        else:
            # 纯净无声模式：依据中文字符数动态估算舒适的阅读停顿时间 (约每秒3.5字)
            estimated_duration = max(len(text) * 0.22, 2.0)
            tracker = VoiceoverTracker(duration=estimated_duration)

        start_time = self.renderer.time if hasattr(self, "renderer") else 0.0
        try:
            yield tracker
        finally:
            end_time = self.renderer.time if hasattr(self, "renderer") else 0.0
            elapsed = end_time - start_time
            # 严格防重叠：若代码块内动画耗时小于配音物理时长，自动补足剩余时间
            remaining = tracker.duration - elapsed
            if remaining > 0.02:
                self.wait(remaining)
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
        """创建数学公式 (智能适配深色/浅色背景，Unicode 汉字自动防护)"""
        import re
        if re.search(r'[\u4e00-\u9fa5]', tex_string):
            import warnings
            warnings.warn(
                f"\n[LaTeX 编码安全警告] MathTex 中检测到中文字符: '{tex_string}'！\n"
                f"在标准 LaTeX 编译链中这会导致崩溃。请使用 make_text() 创建中文文本，或用 VGroup 组合文字与纯 LaTeX 公式！",
                UserWarning
            )
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

    set_title = play_show_title

    def setup_academic_frame(self, chapter_code="ANALYSIS // CH.01", citation_text=None):
        """
        学术纪录片四角元信息骨架 (Four-Corner Academic Framing):
        左上: 学科分支/章节等宽标签; 右上: 历史原著文献引注;
        将中央 75% 视口纯粹留给数学核心证据与几何推导。
        """
        # 左上角章节代码 (等宽技术质感)
        badge = self.make_text(chapter_code, font_size=15, color=self.theme.primary)
        badge.to_corner(UL, buff=0.42)
        dec_line = Line(LEFT * 0.2, RIGHT * 0.2, color=self.theme.primary, stroke_width=2.0).next_to(badge, LEFT, buff=0.15)
        top_left_grp = VGroup(dec_line, badge)

        frame_elements = [top_left_grp]

        # 右上角学术文献出处引注 (斜体学术范)
        if citation_text:
            cite_txt = self.make_text(citation_text, font_size=14, color=self.theme.text_muted)
            cite_txt.to_corner(UR, buff=0.42)
            frame_elements.append(cite_txt)

        academic_group = VGroup(*frame_elements)
        self.play(FadeIn(academic_group, shift=DOWN * 0.15), run_time=0.6)
        return academic_group

    def play_draw_with_beacon(self, curve, run_time=2.0, beacon_color=None, beacon_radius=0.09):
        """
        曲线头部跟随引导光点 (Leading Focus Beacon):
        曲线按路径长度绘制的同时，其最前沿挂载一个高亮跟随点，视线焦点毫秒级牢牢锚定！
        """
        color = beacon_color or self.theme.accent
        alpha_tracker = ValueTracker(0)

        # 稳健取点函数：兼容 VMobject 单曲线与 VGroup 复合组
        def get_current_point():
            val = max(0.0001, min(0.9999, alpha_tracker.get_value()))
            target = curve
            if isinstance(curve, VGroup):
                submobs = [m for m in curve.submobjects if hasattr(m, "has_no_points") and not m.has_no_points()]
                if not submobs:
                    return curve.get_center()
                # 按照子曲线均分比例定位
                n = len(submobs)
                idx = min(int(val * n), n - 1)
                sub_val = (val * n) - idx
                target = submobs[idx]
                return target.point_from_proportion(max(0.0001, min(0.9999, sub_val)))
            elif hasattr(target, "has_no_points") and not target.has_no_points():
                return target.point_from_proportion(val)
            return curve.get_center()

        # 头部跟随光点 (始终吸附在曲线当前 alpha 位置)
        beacon = always_redraw(
            lambda: Dot(
                point=get_current_point(),
                radius=beacon_radius,
                color=color
            )
        )

        self.add(beacon)
        self.play(
            Create(curve, run_time=run_time, rate_func=linear),
            alpha_tracker.animate(run_time=run_time, rate_func=linear).set_value(1.0)
        )
        # 绘制完成，光点渐隐融入曲线
        self.remove(beacon)
        return curve

    def fade_to_ghost(self, *mobjects, ghost_opacity=0.22, ghost_color=None, run_time=0.6):
        """
        算法迭代的历史幽灵足迹 (Ghost Trails / History Fade):
        将上一轮迭代的切线/构造线平滑退化为暗色低透明度痕迹，
        既清晰保留逼近历史，又决不抢占当前主焦点！
        """
        target_color = ghost_color or self.theme.text_muted
        animations = []
        for mob in mobjects:
            if isinstance(mob, (list, tuple)):
                for sub in mob:
                    animations.append(sub.animate.set_stroke(color=target_color, opacity=ghost_opacity))
            else:
                animations.append(mob.animate.set_stroke(color=target_color, opacity=ghost_opacity))

        if animations:
            self.play(*animations, run_time=run_time)

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

    def read_pause(self, text_or_char_count, min_pause=1.2, max_pause=4.0):
        """
        基于认知心理学公式的人类阅读自适应停顿 (汲取 lemo-opuscar 与 xiaoma-studio)：
        中文阅读节奏模型: (字数 / 4.5 + 1.0) 秒，给观众大脑留足吸收顿悟时间
        """
        if isinstance(text_or_char_count, (int, float)):
            n_chars = float(text_or_char_count)
        else:
            n_chars = float(len(str(text_or_char_count)))
        duration = max(min_pause, min(n_chars / 4.5 + 1.0, max_pause))
        self.wait(duration)
        return duration

    def real_silence(self, duration=1.2):
        """
        顿悟前的真静音留白 (Real Silence Before the Turn)：
        在揭晓关键证明结论、矛盾悖论爆发或 Aha! Moment 前完全静止蓄力，制造心理聚焦。
        """
        self.wait(duration)

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

    def camera_zoom_to(self, target, scale_factor=0.6, buff=0.8, run_time=1.8, rate_func=smooth):
        """
        电影级推镜 (Zoom In)：平滑将摄影机聚焦到某个局部 Mobject 或三维坐标点
        scale_factor < 1.0 为推近放大，scale_factor > 1.0 为拉远广角
        """
        if hasattr(target, "get_center"):
            target_center = target.get_center()
            target_width = max(target.width * (1.0 / scale_factor) + buff, 3.5)
        else:
            target_center = np.array(target, dtype=float)
            target_width = self.default_frame_width * scale_factor
        
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
