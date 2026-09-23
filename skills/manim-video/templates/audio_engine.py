"""
audio_engine.py: 声音设计与语音合成引擎
为 Manim 提供零成本、高品质的 edge-tts 神经网络人声合成、精确时长探测与音画混流压制。
支持本地 Hash 缓存、BGM 背景氛围衬底混音与自动音量闪避。
"""
import os
import sys
import re
import hashlib
import asyncio
import subprocess
from pathlib import Path

# 确保控制台支持 UTF-8
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 寻找 ffmpeg 路径
def get_ffmpeg():
    import shutil
    import glob
    p = shutil.which("ffmpeg")
    if p:
        return p
    winget_glob = glob.glob(r"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\*ffmpeg*\**\bin\ffmpeg.exe", recursive=True)
    if winget_glob:
        return winget_glob[0]
    return "ffmpeg"


class AudioEngine:
    """语音合成与音频处理引擎"""

    DEFAULT_VOICE = "zh-CN-YunxiNeural"  # 微软经典沉稳知性男声 (推荐)
    FEMALE_VOICE = "zh-CN-XiaoxiaoNeural" # 微软知性亲切女声
    CACHE_DIR = Path("media/voiceover_cache")

    @classmethod
    def get_audio_duration(cls, audio_path):
        """使用 ffmpeg 探测音频精确时长 (秒)"""
        ffmpeg_exe = get_ffmpeg()
        cmd = [ffmpeg_exe, "-i", str(audio_path)]
        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
        if match:
            hours, mins, secs = match.groups()
            return int(hours) * 3600 + int(mins) * 60 + float(secs)
        return 2.5  # 兜底默认值

    @classmethod
    def generate_speech(cls, text, voice=None, cache_dir=None):
        """
        合成语音并返回 (audio_path, duration)
        自动基于文本内容与音色的 MD5 做本地文件缓存
        """
        import edge_tts

        selected_voice = voice or cls.DEFAULT_VOICE
        c_dir = Path(cache_dir or cls.CACHE_DIR)
        c_dir.mkdir(parents=True, exist_ok=True)

        # 依据文本和音色哈希计算文件名
        hash_key = hashlib.md5(f"{selected_voice}_{text}".encode("utf-8")).hexdigest()
        out_file = c_dir / f"{hash_key}.mp3"

        if out_file.exists() and out_file.stat().st_size > 0:
            duration = cls.get_audio_duration(out_file)
            return out_file, duration

        # 执行异步合成
        async def _synth():
            communicate = edge_tts.Communicate(text, selected_voice)
            await communicate.save(str(out_file))

        asyncio.run(_synth())
        duration = cls.get_audio_duration(out_file)
        return out_file, duration

    @classmethod
    def mix_scene_audio(cls, video_path, audio_files_with_offsets, output_path, bgm_path=None, bgm_volume=0.12):
        """
        将分段配音频道、背景音乐与视频 MP4 合成为最终有声视频
        audio_files_with_offsets: [(audio_path, start_time_sec), ...]
        """
        ffmpeg_exe = get_ffmpeg()
        v_path = Path(video_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not audio_files_with_offsets:
            # 纯视频复制
            import shutil
            shutil.copyfile(v_path, out_p)
            return True

        # 构建复杂音频过滤图 (filter_complex)
        inputs = ["-i", str(v_path)]
        filter_parts = []
        mix_inputs = len(audio_files_with_offsets)

        for idx, (a_file, start_t) in enumerate(audio_files_with_offsets):
            inputs.extend(["-i", str(Path(a_file).resolve())])
            # adelay 延迟毫秒数
            delay_ms = int(start_t * 1000)
            filter_parts.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[a{idx+1}]")

        concat_labels = "".join([f"[a{i+1}]" for i in range(mix_inputs)])
        filter_parts.append(f"{concat_labels}amix=inputs={mix_inputs}:normalize=0[voice]")

        # 如果有 BGM
        if bgm_path and Path(bgm_path).exists():
            bgm_idx = mix_inputs + 1
            inputs.extend(["-i", str(Path(bgm_path).resolve())])
            filter_parts.append(f"[{bgm_idx}:a]volume={bgm_volume}[bgm]")
            filter_parts.append(f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]")
            final_map_audio = "[aout]"
        else:
            final_map_audio = "[voice]"

        filter_complex_str = ";".join(filter_parts)

        cmd = [
            ffmpeg_exe, "-y",
            *inputs,
            "-filter_complex", filter_complex_str,
            "-map", "0:v",
            "-map", final_map_audio,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            str(out_p)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if res.returncode != 0:
            print(f"[Error] 音视频混流合成失败: {res.stderr}")
            return False
        return True

    @classmethod
    def add_bgm_to_video(cls, video_path, bgm_path, output_path, bgm_volume=0.12, fade_out_sec=2.5):
        """
        为任意已有视频 (纯画面或已有原声) 一键添加背景音乐：
        - 自动循环 BGM 直至视频结束 (-stream_loop -1)
        - 自动将 BGM 音量压低至舒适衬底 (默认 0.12 / 约 -18dB)
        - 视频收尾最后 fade_out_sec 秒自动平滑淡出 (afade)
        - 若视频原先已有声音，自动双轨混合 (amix)，绝不覆盖原音！
        """
        ffmpeg_exe = get_ffmpeg()
        v_path = Path(video_path).resolve()
        b_path = Path(bgm_path).resolve()
        out_p = Path(output_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)

        if not v_path.exists() or not b_path.exists():
            print(f"[Error] 视频或 BGM 文件不存在: {v_path} / {b_path}")
            return False

        # 探测视频真实时长
        cmd_probe = [ffmpeg_exe, "-i", str(v_path)]
        res_probe = subprocess.run(cmd_probe, capture_output=True, text=True, errors="replace")
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res_probe.stderr)
        v_duration = 10.0
        if match:
            h, m, s = match.groups()
            v_duration = int(h) * 3600 + int(m) * 60 + float(s)

        # 检查原视频是否自带音轨
        has_orig_audio = "Audio:" in res_probe.stderr
        fade_start = max(0.0, v_duration - fade_out_sec)

        # BGM 过滤器：音量微调 + 结尾平滑淡出
        bgm_filter = f"[1:a]volume={bgm_volume},afade=t=out:st={fade_start:.2f}:d={fade_out_sec:.2f}[bgm]"

        if has_orig_audio:
            # 双轨混合：保留原声 + BGM 混流
            filter_complex = f"{bgm_filter};[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
            final_map = "[aout]"
        else:
            # 纯画面添加 BGM
            filter_complex = bgm_filter
            final_map = "[bgm]"

        cmd = [
            ffmpeg_exe, "-y",
            "-i", str(v_path),
            "-stream_loop", "-1",
            "-i", str(b_path),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", final_map,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out_p)
        ]

        print(f"[BGM] 正在为视频混入背景音乐: {b_path.name} (音量={bgm_volume*100:.0f}%, 尾部淡出={fade_out_sec}s)")
        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if res.returncode == 0 and out_p.exists():
            print(f"[OK] 配乐视频合成完毕: {out_p} ({out_p.stat().st_size / (1024*1024):.2f} MB)")
            return True
        else:
            print(f"[Error] 配乐合成失败: {res.stderr}")
            return False
