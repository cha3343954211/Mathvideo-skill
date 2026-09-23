"""
Scene 01: 音画毫秒级对齐实战 (Voiceover Context Engine)
展示:
1. with self.voiceover(...) as tracker 上下文管理器
2. 动画运行时间 run_time 与真人质感语音实际物理时长 100% 锁死
3. 自动生成音轨时间轴并压制为真正有声大片
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import NordScene, DynamicTangentRig, OrganicMotion, AudioEngine

class AudioSyncScene(NordScene):
    ENABLE_VOICEOVER = True  # 激活真人质感 TTS 配音
    VOICE_NAME = "zh-CN-YunxiNeural"  # 微软经典沉稳男声云希

    def construct(self):
        super().construct()

        # 1. 标题与引入
        self.play_show_title("微积分之眼：音画对齐与动切线", "AudioSyncEngine & Millisecond Accuracy")

        # 2. 坐标系与函数
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 4, 1],
            x_length=7.5,
            y_length=5.0,
            axis_config={"color": self.theme.grid_color, "stroke_width": 2}
        ).shift(DOWN * 0.4 + LEFT * 1.5)

        func = lambda x: 0.25 * (x**3) - x + 0.5
        graph = axes.plot(func, x_range=[-2.8, 2.8], color=self.theme.primary, stroke_width=3.5)

        # 语句 1：介绍导数本质 (动画时间严格与语音长度同步)
        speech_1 = "欢迎来到微积分探索。导数的几何本质，是切线斜率随曲线上点位置的瞬时演变。"
        with self.voiceover(speech_1) as tracker:
            self.play(Create(axes), Create(graph), run_time=tracker.duration)

        # 3. 装配 DynamicTangentRig
        x_tracker = ValueTracker(-2.2)
        rig = DynamicTangentRig(
            axes=axes,
            func=func,
            tracker=x_tracker,
            tangent_length=3.2,
            tangent_color=self.theme.secondary,
            dot_color=self.theme.accent,
            show_slope_label=True,
            show_projections=True,
            decimal_places=2
        )

        # 语句 2：动切线滑动
        speech_2 = "当我们装配动切线机械装置，切线方向与斜率数值随动点向右连续滑动。"
        with self.voiceover(speech_2) as tracker:
            self.play(FadeIn(rig), run_time=1.0)
            remaining_time = max(tracker.duration - 1.0, 1.0)
            self.play(x_tracker.animate.set_value(-1.1547), run_time=remaining_time, rate_func=smooth)

        # 语句 3：极值点停顿与顿悟
        speech_3 = "在极大值极值点处，切线完全水平，瞬时导数斜率精确降为零。"
        with self.voiceover(speech_3) as tracker:
            bounce_time = min(tracker.duration * 0.4, 0.8)
            wait_time = tracker.duration - bounce_time
            self.play(OrganicMotion.spring_bounce(rig.dot, scale_factor=1.6, run_time=bounce_time))
            if wait_time > 0:
                self.wait(wait_time)

        # 4. 淡出收尾
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(rig), run_time=1.2)

        # 保存语音时间轴以供压制脚本合成
        timeline_file = Path("voiceover_timeline.json")
        timeline_data = [
            {"audio": item[0], "start_time": item[1]}
            for item in self.voiceover_timeline
        ]
        timeline_file.write_text(json.dumps(timeline_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[AudioEngine] 语音时间轴已记录: {len(timeline_data)} 段配音 -> {timeline_file}")
