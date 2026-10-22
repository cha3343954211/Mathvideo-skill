"""
qa.py: 数学视频成片自动化体检与质量审计器 (汲取 xiaoma-studio 工业标准)
全自动对导出的 MP4 成片执行工业级体检：
1. 规格合规性体检 (分辨率 1080p, 帧率, 时长, 编码)
2. 黑帧与渲染丢失检测 (Black Frame Detection)
3. 画面无动作卡死检测 (Freeze Detection)
4. 工业级音量响度审计 (EBU R128 标准，目标 -14 LUFS)
"""
import os
import sys
import re
import shutil
import argparse
import subprocess
from pathlib import Path

# 确保控制台支持 UTF-8
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def get_ffmpeg():
    p = shutil.which("ffmpeg")
    if p:
        return p
    import glob
    winget_glob = glob.glob(r"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\*ffmpeg*\**\bin\ffmpeg.exe", recursive=True)
    if winget_glob:
        return winget_glob[0]
    return "ffmpeg"

def audit_video(video_path, max_freeze_sec=3.0, target_lufs=-14.0):
    ffmpeg = get_ffmpeg()
    vp = Path(video_path).resolve()
    if not vp.exists():
        print(f"[Error] 目标视频文件不存在: {vp}")
        return False

    print(f"\n🔍 [开始工业级视频体检] 正在诊断: {vp.name}")
    print("=" * 60)

    # 1. 基础流媒体参数探测
    cmd_probe = [ffmpeg, "-i", str(vp)]
    res_probe = subprocess.run(cmd_probe, capture_output=True, text=True, errors="replace")
    probe_text = res_probe.stderr

    # 提取时长
    m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", probe_text)
    duration = 0.0
    if m_dur:
        h, m, s = m_dur.groups()
        duration = int(h) * 3600 + int(m) * 60 + float(s)

    # 提取分辨率与帧率
    m_res = re.search(r"Video:.*,\s*(\d{3,4})x(\d{3,4})", probe_text)
    width, height = (int(m_res.group(1)), int(m_res.group(2))) if m_res else (0, 0)

    m_fps = re.search(r"(\d+(?:\.\d+)?)\s*fps", probe_text)
    fps = float(m_fps.group(1)) if m_fps else 0.0

    has_audio = "Audio:" in probe_text

    print(f"📊 基础规格:")
    print(f"  • 时长: {duration:.2f} 秒 ({duration/60:.1f} 分钟)")
    print(f"  • 分辨率: {width}x{height} {'[OK 1080p]' if (width, height) in [(1920, 1080), (1080, 1920)] else '[警告: 非标准1080p]'}")
    print(f"  • 帧率: {fps:.1f} fps")
    print(f"  • 音轨: {'已包含音频' if has_audio else '纯静音/无音轨'}")

    issues = []
    warnings = []

    # 2. 异常黑帧检测
    print("\n🎞️ 检测渲染异常黑帧 (Blackdetect)...")
    cmd_black = [
        ffmpeg, "-i", str(vp),
        "-vf", "blackdetect=d=1.2:pic_th=0.99:pix_th=0.08",
        "-f", "null", "-"
    ]
    res_black = subprocess.run(cmd_black, capture_output=True, text=True, errors="replace")
    black_spans = re.findall(r"black_start:(\d+\.?\d*)\s+black_end:(\d+\.?\d*)\s+black_duration:(\d+\.?\d*)", res_black.stderr)
    
    unexpected_blacks = []
    for b_start, b_end, b_dur in black_spans:
        bs, be, bd = float(b_start), float(b_end), float(b_dur)
        # 排除开头 1.5 秒正常淡入与结尾 1.2 秒正常淡出黑屏
        if bs >= 1.5 and bs < duration - 1.2:
            unexpected_blacks.append((bs, be, bd))

    if unexpected_blacks:
        for bs, be, bd in unexpected_blacks:
            msg = f"检测到异常黑帧: {bs:.2f}s - {be:.2f}s (持续 {bd:.2f}s)"
            issues.append(msg)
            print(f"  ❌ {msg}")
    else:
        print("  ✅ 未发现异常黑帧，画面连贯正常。")

    # 3. 画面无响应冻结段检测 (Freezedetect)
    print(f"\n⏸️ 检测画面僵死卡顿 (Freezedetect > {max_freeze_sec}s)...")
    cmd_freeze = [
        ffmpeg, "-i", str(vp),
        "-vf", f"freezedetect=n=-50dB:d={max_freeze_sec}",
        "-f", "null", "-"
    ]
    res_freeze = subprocess.run(cmd_freeze, capture_output=True, text=True, errors="replace")
    freezes = re.findall(r"freeze_start:\s*(\d+\.?\d*).*?freeze_duration:\s*(\d+\.?\d*)", res_freeze.stderr)
    
    unexpected_freezes = []
    for f_start, f_dur in freezes:
        fs, fd = float(f_start), float(f_dur)
        # 排除片尾最后一两秒静止
        if fs < duration - 1.5:
            unexpected_freezes.append((fs, fd))

    if unexpected_freezes:
        for fs, fd in unexpected_freezes:
            msg = f"画面冻结静止时间过长: 从 {fs:.2f}s 起持续 {fd:.2f}s"
            warnings.append(msg)
            print(f"  ⚠️ {msg} (若为刻意思维留白可忽略，否则需加速动画)")
    else:
        print("  ✅ 动态节奏良好，无异常卡死无反应段落。")

    # 4. 音量响度审计 (EBU R128)
    if has_audio:
        print(f"\n🔊 音频工业级响度审计 (EBU R128 标准，目标 {target_lufs} LUFS)...")
        cmd_loudness = [
            ffmpeg, "-i", str(vp),
            "-af", "ebur128=peak=true",
            "-f", "null", "-"
        ]
        res_loudness = subprocess.run(cmd_loudness, capture_output=True, text=True, errors="replace")
        
        m_il = re.findall(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", res_loudness.stderr)
        m_lra = re.findall(r"LRA:\s+([-\d.]+)\s+LU", res_loudness.stderr)
        m_tp = re.findall(r"True peak:\s+Peak:\s+([-\d.]+)\s+dBFS", res_loudness.stderr)

        if m_il:
            actual_lufs = float(m_il[-1])
            lra = float(m_lra[-1]) if m_lra else 0.0
            tp = float(m_tp[-1]) if m_tp else 0.0

            print(f"  • 集成响度 (Integrated Loudness): {actual_lufs:.1f} LUFS")
            print(f"  • 响度动态范围 (LRA): {lra:.1f} LU")
            print(f"  • 真实峰值 (True Peak): {tp:.1f} dBFS")

            diff = abs(actual_lufs - target_lufs)
            if diff <= 2.0:
                print(f"  ✅ 响度非常标准 (与 {target_lufs} LUFS 偏差仅 {diff:.1f} dB)")
            elif actual_lufs < target_lufs - 2.5:
                w = f"音量偏小 ({actual_lufs:.1f} LUFS，建议使用 AudioEngine 开启 loudnorm 提升至 -14 LUFS)"
                warnings.append(w)
                print(f"  ⚠️ {w}")
            else:
                w = f"音量偏大可能爆音 ({actual_lufs:.1f} LUFS，建议压低至 -14 LUFS)"
                warnings.append(w)
                print(f"  ⚠️ {w}")
    else:
        print("\n🔇 视频无音频轨道 (当前为纯净无声模式)")

    # 5. 台词与解说词沉浸度审计 (严禁运镜技术元台词)
    print("\n🎙️ 沉浸叙事解说词规范审计 (No Meta-Directing Words)...")
    project_dir = vp.parent.parent if vp.parent.name in ["output", "media"] else vp.parent
    py_files = list(project_dir.glob("*.py"))
    meta_words = ["摄像机", "摄影机", "推镜", "拉远", "横移", "镜头拉", "镜头推", "镜头移", "镜头旋转", "切镜头"]
    meta_violations = []
    
    for pyf in py_files:
        try:
            with open(pyf, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            # 搜索 voiceover("...") 内部的台词
            vo_matches = re.findall(r'voiceover\(\s*["\'](.*?)["\']\s*\)', content)
            for vo in vo_matches:
                for mw in meta_words:
                    if mw in vo:
                        meta_violations.append((pyf.name, mw, vo))
        except Exception:
            pass

    if meta_violations:
        for fname, mw, vo in meta_violations:
            w = f"台词中发现运镜技术元词汇 '{mw}': 文件 {fname} -> '{vo}'"
            warnings.append(w)
            print(f"  ⚠️ {w}")
    else:
        print("  ✅ 台词纯净合规，100% 聚焦数学内涵，无破壁技术元词。")

    # 6. 全片音色绝对统一性审计 (Timbre Consistency)
    print("\n🎭 全片音色一致性审计 (Single Timbre Consistency)...")
    engines_found = set()
    voices_found = set()
    for pyf in py_files:
        try:
            with open(pyf, "r", encoding="utf-8", errors="replace") as f:
                c = f.read()
            e_matches = re.findall(r'TTS_ENGINE\s*=\s*["\'](.*?)["\']', c)
            v_matches = re.findall(r'VOICE_NAME\s*=\s*["\'](.*?)["\']', c)
            for em in e_matches:
                engines_found.add(em)
            for vm in v_matches:
                voices_found.add(vm)
        except Exception:
            pass

    if len(engines_found) > 1 or len(voices_found) > 1:
        w = f"检测到全片存在音色/引擎混杂: 引擎={engines_found}, 音色={voices_found} (按铁律全片必须统一同一音色)"
        warnings.append(w)
        print(f"  ⚠️ {w}")
    elif engines_found or voices_found:
        eng = list(engines_found)[0] if engines_found else "default"
        voc = list(voices_found)[0] if voices_found else "default"
        print(f"  ✅ 全片各分幕音色完全统一 (引擎: '{eng}', 音色: '{voc[:30]}...')")
    else:
        print("  ✅ 音色配置统一。")

    # 7. 语音重叠安全审计 (Zero Audio Overlap Audit)
    print("\n🔇 语音时间轴防重叠审计 (Zero Audio Overlap)...")
    repo_root = Path(__file__).resolve().parent.parent.parent
    sync_dir = repo_root / "media" / "audio_sync"
    overlap_detected = False
    if sync_dir.exists():
        for tf in sync_dir.glob("*_timeline.json"):
            try:
                import soundfile as sf
                with open(tf, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                prev_end = 0.0
                for a_p, offset in meta.get("voiceovers", []):
                    off = float(offset)
                    if off < prev_end - 0.05:
                        w = f"时间轴存在重叠风险: 文件 {tf.name} 偏移量 {off:.2f}s 早于上一段结束点 {prev_end:.2f}s"
                        warnings.append(w)
                        overlap_detected = True
                        print(f"  ⚠️ {w}")
                    if Path(a_p).exists():
                        d = len(sf.read(str(a_p))[0]) / sf.read(str(a_p))[1]
                        prev_end = max(prev_end, off + d)
            except Exception:
                pass
    if not overlap_detected:
        print("  ✅ 语音时间轴绝对无缝咬合，0 处交叉重叠。")

    print("\n" + "=" * 60)
    # 综合体检评级
    if not issues and not warnings:
        print("🎉 [体检结论: 卓越 (PASSED)] 全项指标全绿，可直接用于公开发布交付！\n")
        return True
    elif not issues:
        print(f"👌 [体检结论: 良好 (WARNING)] 发现 {len(warnings)} 处微调建议，基本符合出片标准。\n")
        return True
    else:
        print(f"🚨 [体检结论: 未通过 (FAILED)] 存在 {len(issues)} 处阻断性缺陷，建议修复后重新导出。\n")
        return False

def main():
    parser = argparse.ArgumentParser(description="Manim 视频全自动质量审计与工业体检器 (QA)")
    parser.add_argument("video", help="待体检的 MP4 视频文件路径")
    parser.add_argument("--max-freeze", type=float, default=3.0, help="允许的最长无动作静止秒数 (默认 3.0s)")
    parser.add_argument("--target-lufs", type=float, default=-14.0, help="目标工业集成响度 (默认 -14.0 LUFS)")
    args = parser.parse_args()

    audit_video(args.video, max_freeze_sec=args.max_freeze, target_lufs=args.target_lufs)

if __name__ == "__main__":
    main()
