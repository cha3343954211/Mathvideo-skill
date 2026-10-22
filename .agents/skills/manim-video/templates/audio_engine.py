"""
audio_engine.py: 声音设计与语音合成引擎
为 Manim 提供零成本、高品质的 edge-tts 神经网络人声合成、精确时长探测与音画混流压制。
支持本地 Hash 缓存、BGM 背景氛围衬底混音与自动音量闪避。
"""
import os
import sys
import re
import json
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
    @classmethod
    def generate_speech_local(cls, text, cache_dir=None, rate=-1, voice="kangkang"):
        """
        纯本地离线语音合成 (Windows 原生 SAPI / OneCore，零网络依赖，毫秒级响应)
        - rate: 语速调节 (-10 ~ 10, 默认 -1 沉稳从容学术播报风格)
        - voice: "kangkang" (沉稳男声) | "huihui" (亲和女声) | 或索引 int
        """
        import win32com.client
        c_dir = Path(cache_dir or cls.CACHE_DIR)
        c_dir.mkdir(parents=True, exist_ok=True)

        voice_tag = str(voice).lower()
        hash_key = hashlib.md5(f"local_sapi_r{rate}_v{voice_tag}_{text}".encode("utf-8")).hexdigest()
        out_file = c_dir / f"{hash_key}.wav"

        if out_file.exists() and out_file.stat().st_size > 0:
            duration = cls.get_audio_duration(out_file)
            return out_file, duration

        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        selected_token = None

        # 优先在 OneCore 高级现代声音中查找 (如微软康康沉稳男声)
        try:
            cat = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
            cat.SetId(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
            tokens = cat.EnumerateTokens()
            for t in tokens:
                desc = t.GetDescription().lower()
                if ("kangkang" in desc or "male" in desc) and "kangkang" in voice_tag:
                    selected_token = t
                    break
                elif "huihui" in desc and "huihui" in voice_tag:
                    selected_token = t
                    break
        except Exception:
            pass

        if selected_token is not None:
            speaker.Voice = selected_token
        elif isinstance(voice, int):
            voices = speaker.GetVoices()
            if voice < voices.Count:
                speaker.Voice = voices.Item(voice)

        speaker.Rate = rate

        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        # 3 = SSFMCreateForWrite
        stream.Open(str(out_file), 3)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()

        duration = cls.get_audio_duration(out_file)
        return out_file, duration

    @classmethod
    def generate_speech_voxcpm(cls, text, cache_dir=None, voice_design=None):
        """
        调用本地 VoxCPM2 离线神经语音大模型 (Intel Arc B580 硬件加速)
        - 采样率 48kHz 超高保真、连续扩散声学生成
        - 默认音色：(四十岁上下的男性，嗓音低沉浑厚，气息沉稳，数学纪录片旁白)
        """
        c_dir = Path(cache_dir or cls.CACHE_DIR)
        c_dir.mkdir(parents=True, exist_ok=True)
        # 针对类似微软云扬播音级音色设计
        if not voice_design or "yunyang" in str(voice_design).lower() or "云扬" in str(voice_design):
            v_design = "(专业新闻纪录片男播音员，三十多岁成熟男性，普通话一级甲等，字正腔圆，嗓音浑厚沉稳大气，富有磁性与共鸣，解说从容，央视大型纪录片解说腔)"
        else:
            v_design = voice_design

        skill_root = Path(__file__).resolve().parent.parent.parent.parent
        ref_candidate = skill_root / "media" / "yunyang_ref.wav"

        ref_tag = "_cloned" if ref_candidate.exists() else ""
        hash_key = hashlib.md5(f"voxcpm_{v_design}_{text}{ref_tag}".encode("utf-8")).hexdigest()
        out_file = c_dir / f"{hash_key}.wav"

        if out_file.exists() and out_file.stat().st_size > 0:
            dur = cls.get_audio_duration(out_file)
            return out_file, dur

        worker_script = Path(__file__).resolve().parent.parent / "scripts" / "voxcpm_batch.py"
        venv_py = r"D:\AIworks\TTS\.venv311\Scripts\python.exe"
        if not Path(venv_py).exists():
            print(f"[AudioEngine] 警告: 未找到本地 VoxCPM 环境 ({venv_py})，降级为 local SAPI")
            return cls.generate_speech_local(text, cache_dir=cache_dir)

        temp_in = c_dir / f"req_{hash_key}.json"
        temp_out = c_dir / f"res_{hash_key}.json"
        with open(temp_in, "w", encoding="utf-8") as f:
            json.dump([{"key": hash_key, "text": text}], f)

        cmd = [
            venv_py, str(worker_script),
            "--json_in", str(temp_in),
            "--json_out", str(temp_out),
            "--out_dir", str(c_dir),
            "--voice_design", v_design
        ]
        if ref_candidate.exists():
            cmd.extend(["--ref_wav", str(ref_candidate.resolve())])

        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        try:
            temp_in.unlink(missing_ok=True)
            if temp_out.exists():
                with open(temp_out, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                temp_out.unlink(missing_ok=True)
                if hash_key in meta:
                    p, d = meta[hash_key]
                    return Path(p), float(d)
        except Exception:
            pass

        dur = cls.get_audio_duration(out_file)
        return out_file, dur

    @classmethod
    def generate_speech(cls, text, voice=None, cache_dir=None, engine="auto"):
        """
        合成语音并返回 (audio_path, duration)
        engine 可选:
          - "voxcpm": 本地 VoxCPM2 离线神经语音大模型 (Intel Arc B580 显卡加速，48kHz 播音级沉稳男声)
          - "auto": 优先尝试 edge-tts 在线高质量，断网时自动无缝降级为本地 VoxCPM / SAPI
          - "local": 纯本地 Windows SAPI / OneCore 离线引擎
          - "edge": 微软神经网络语音合成 (需网络连接)
        """
        if engine == "voxcpm":
            return cls.generate_speech_voxcpm(text, cache_dir=cache_dir, voice_design=voice)
        elif engine == "local":
            return cls.generate_speech_local(text, cache_dir=cache_dir)

        c_dir = Path(cache_dir or cls.CACHE_DIR)
        c_dir.mkdir(parents=True, exist_ok=True)
        selected_voice = voice or cls.DEFAULT_VOICE

        # 依据文本和音色哈希计算文件名
        hash_key = hashlib.md5(f"{selected_voice}_{text}".encode("utf-8")).hexdigest()
        out_file = c_dir / f"{hash_key}.mp3"

        if out_file.exists() and out_file.stat().st_size > 0:
            duration = cls.get_audio_duration(out_file)
            return out_file, duration

        try:
            import edge_tts
            # 执行异步合成
            async def _synth():
                communicate = edge_tts.Communicate(text, selected_voice)
                await communicate.save(str(out_file))

            asyncio.run(_synth())
            duration = cls.get_audio_duration(out_file)
            return out_file, duration
        except Exception as e:
            if engine == "auto":
                print(f"[AudioEngine] Edge-TTS 在线失败 ({e})，自动无缝降级为本地离线 SAPI 引擎...")
                return cls.generate_speech_local(text, cache_dir=cache_dir)
            raise e

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

        # 严格防重叠物理校准：后一段音频必须在前一段朗读完毕之后开始
        sanitized_audio = []
        last_end_time = 0.0
        for a_file, start_t in audio_files_with_offsets:
            a_p = Path(a_file).resolve()
            dur = cls.get_audio_duration(a_p)
            safe_start = max(float(start_t), last_end_time + 0.05)
            sanitized_audio.append((a_p, safe_start))
            last_end_time = safe_start + dur

        # 构建复杂音频过滤图 (filter_complex)
        inputs = ["-i", str(v_path)]
        filter_parts = []
        mix_inputs = len(sanitized_audio)

        for idx, (a_file, start_t) in enumerate(sanitized_audio):
            inputs.extend(["-i", str(Path(a_file).resolve())])
            # adelay 延迟毫秒数
            delay_ms = max(0, int(start_t * 1000))
            filter_parts.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[a{idx+1}]")

        concat_labels = "".join([f"[a{i+1}]" for i in range(mix_inputs)])
        filter_parts.append(f"{concat_labels}amix=inputs={mix_inputs}:normalize=0[voice]")

        # 如果有 BGM
        if bgm_path and Path(bgm_path).exists():
            bgm_idx = mix_inputs + 1
            inputs.extend(["-i", str(Path(bgm_path).resolve())])
            filter_parts.append(f"[{bgm_idx}:a]volume={bgm_volume}[bgm]")
            filter_parts.append(f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[pre_norm]")
            filter_parts.append(f"[pre_norm]loudnorm=I=-14:LRA=11:TP=-1.5[aout]")
            final_map_audio = "[aout]"
        else:
            filter_parts.append(f"[voice]loudnorm=I=-14:LRA=11:TP=-1.5[aout]")
            final_map_audio = "[aout]"

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
    def add_bgm_to_video(cls, video_path, bgm_path, output_path, bgm_volume=0.12, fade_out_sec=2.5, normalize_loudness=True, target_lufs=-14.0):
        """
        为任意已有视频 (纯画面或已有原声) 一键添加背景音乐：
        - 自动循环 BGM 直至视频结束 (-stream_loop -1)
        - 自动将 BGM 音量压低至舒适衬底 (默认 0.12 / 约 -18dB)
        - 视频收尾最后 fade_out_sec 秒自动平滑淡出 (afade)
        - 若视频原先已有声音，自动双轨混合 (amix)，绝不覆盖原音！
        - 支持按工业级 -14 LUFS 响度标准化 (loudnorm)
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

        norm_filter = f",loudnorm=I={target_lufs}:LRA=11:TP=-1.5" if normalize_loudness else ""
        if has_orig_audio:
            # 双轨混合：保留原声 + BGM 混流
            filter_complex = f"{bgm_filter};[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2{norm_filter}[aout]"
            final_map = "[aout]"
        else:
            # 纯画面添加 BGM
            filter_complex = f"{bgm_filter}{norm_filter}[bgm_norm]" if normalize_loudness else bgm_filter
            final_map = "[bgm_norm]" if normalize_loudness else "[bgm]"

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

        print(f"[BGM] 正在为视频混入背景音乐: {b_path.name} (音量={bgm_volume*100:.0f}%, 尾部淡出={fade_out_sec}s, -14LUFS={normalize_loudness})")
        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if res.returncode == 0 and out_p.exists():
            print(f"[OK] 配乐视频合成完毕: {out_p} ({out_p.stat().st_size / (1024*1024):.2f} MB)")
            return True
        else:
            print(f"[Error] 配乐合成失败: {res.stderr}")
            return False


class ACEStepMusic:
    """
    ACE-Step (开源基础音乐模型) 调度与生成器
    - 支持对接官方 acestep.api_server (POST /release_task, POST /query_result, GET /v1/audio)
    - 针对本地离线场景提供即开即用的高品质学术氛围伴奏 (Ambient Piano / Minimal Acoustic)
    - 专为数学纪录片与科普短片优化的提示词预设工程 (Prompt Engineering)
    """

    DEFAULT_API_URL = "http://127.0.0.1:8000"
    DEFAULT_MUSIC_DIR = Path("assets/music")

    # 专为数学动画定制的 ACE-Step 风格提示词模板
    PROMPTS = {
        "academic_piano": "minimalist academic ambient piano, documentary soundtrack, contemplative, elegant, 80 bpm, no vocals, high quality",
        "geometric_ambient": "deep cinematic drone, warm analog synthesizer, crystalline harmonics, science documentary, 90 bpm, no vocals",
        "renaissance_lute": "classical acoustic guitar and chamber strings, elegant golden ratio proportion, baroque aesthetic, no vocals",
        "modern_minimal": "modern neoclassical piano, subtle rhythmic pulse, scientific discovery, wonder, 100 bpm, instrumental"
    }

    @classmethod
    def check_server(cls, api_url=None):
        """探测本地或局域网 ACE-Step API 服务是否就绪"""
        import urllib.request
        url = (api_url or cls.DEFAULT_API_URL).rstrip("/") + "/health"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    @classmethod
    def generate_music_api(cls, prompt, duration=30, output_path=None, api_url=None, timeout=120):
        """
        通过 ACE-Step 官方 REST API 异步生成背景音乐
        """
        import json
        import time
        import urllib.request

        base_url = (api_url or cls.DEFAULT_API_URL).rstrip("/")
        release_url = f"{base_url}/release_task"
        query_url = f"{base_url}/query_result"

        payload = {
            "prompt": prompt,
            "duration": duration,
            "lyrics": "" # 纯器乐无歌词
        }

        req = urllib.request.Request(
            release_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            task_id = data.get("task_id")
            if not task_id:
                raise RuntimeError(f"ACE-Step 提交任务失败: {data}")

        print(f"[ACE-Step] 任务已提交，Task ID: {task_id}，正在等待扩散模型推理...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(3)
            q_req = urllib.request.Request(
                query_url,
                data=json.dumps({"task_id": task_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(q_req, timeout=10) as q_resp:
                q_data = json.loads(q_resp.read().decode("utf-8"))
                status = q_data.get("status")
                if status == 1: # 成功
                    audio_url = q_data.get("audio_url")
                    if not audio_url.startswith("http"):
                        audio_url = f"{base_url}{audio_url}"
                    
                    target_out = Path(output_path or f"media/acestep_{task_id}.wav")
                    target_out.parent.mkdir(parents=True, exist_ok=True)
                    urllib.request.urlretrieve(audio_url, str(target_out))
                    print(f"[ACE-Step] 音乐生成成功并已下载: {target_out}")
                    return target_out
                elif status == 2: # 失败
                    raise RuntimeError(f"ACE-Step 模型生成失败: {q_data.get('message')}")

        raise TimeoutError(f"ACE-Step 生成超时 ({timeout}s)")

    @classmethod
    def get_music(cls, style="academic_piano", target_duration=30, custom_prompt=None, api_url=None):
        """
        获取契合数学视频的背景音乐：
        1. 若 ACE-Step API 在线，优先使用 ACE-Step 实时生成全新乐段；
        2. 若未启动 API，智能使用本地预置的 ACE-Step 纯净和声乐段，确保 100% 离线顺畅运行。
        """
        prompt = custom_prompt or cls.PROMPTS.get(style, cls.PROMPTS["academic_piano"])
        is_server_online = cls.check_server(api_url)

        if is_server_online:
            print(f"[ACE-Step] 检测到本地 ACE-Step 模型服务在线！正在调度生成: {prompt[:40]}...")
            try:
                out_path = Path("media/voiceover_cache") / f"acestep_{style}.wav"
                return cls.generate_music_api(prompt, duration=target_duration, output_path=out_path, api_url=api_url)
            except Exception as e:
                print(f"[ACE-Step] API 生成异常 ({e})，平滑降级为本地离线乐段...")

        # 离线保底方案：使用预置高质感乐段
        fallback_file = cls.DEFAULT_MUSIC_DIR / "acestep_ambient_piano.wav"
        if fallback_file.exists():
            print(f"[ACE-Step] 启用本地 ACE-Step 风格优雅氛围伴奏: {fallback_file.name}")
            return fallback_file
        
        raise FileNotFoundError(f"未找到本地伴奏且 ACE-Step API 未开启: {fallback_file}")

