"""
make_demo.py: 3Blue1Brown 标志性美学示范工程全自动流水线
1. 1080p 高清渲染 Scene3B1BLagrangeDemo
2. 调度本地 VoxCPM2 离线神经语音合成 (48kHz 超高保真播音级沉稳解说)
3. 声音与画面毫秒级防重叠混流
4. 混入 3b1b 标志性灵动轻快马林巴/钢琴节奏 BGM 并执行 -14 LUFS 响度标准化
5. 生成 12 宫格电影级故事板拼图看板 (Contact Sheet)
6. 工业级全套 QA 健康体检
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# 确保控制台支持 UTF-8
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent.parent
SKILL_TEMPLATES = REPO_ROOT / "skills" / "manim-video" / "templates"
SKILL_SCRIPTS = REPO_ROOT / "skills" / "manim-video" / "scripts"

sys.path.insert(0, str(SKILL_TEMPLATES))
sys.path.insert(0, str(SKILL_SCRIPTS))

from audio_engine import AudioEngine, ACEStepMusic, get_ffmpeg
from contact_sheet import create_contact_sheet
from qa import audit_video

SCENE_NAME = "Scene3B1BLagrangeDemo"
SCENE_FILE = PROJECT_DIR / "scene_3b1b.py"
OUTPUT_DIR = PROJECT_DIR / "output"


def main():
    print("\n" + "=" * 75)
    print("🎬 [3Blue1Brown 标志性视觉美学示范片: 《拉格朗日中值定理：几何与算式共鸣》]")
    print("=" * 75)

    ffmpeg_exe = get_ffmpeg()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = OUTPUT_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    raw_render_dir = OUTPUT_DIR / "raw_renders"
    raw_render_dir.mkdir(parents=True, exist_ok=True)

    # 1. 1080p 高清渲染
    print(f"\n🎥 [步骤 1/4] 渲染 3b1b 场景: {SCENE_NAME} (1080p 30fps)...")
    cmd_render = [
        sys.executable, "-m", "manim", "render",
        "-qh", "--fps", "30",
        str(SCENE_FILE),
        SCENE_NAME,
        "--media_dir", str(raw_render_dir)
    ]
    res_render = subprocess.run(cmd_render, cwd=str(REPO_ROOT), capture_output=True, text=True, errors="replace")
    if res_render.returncode != 0:
        print(f"[Error] 场景渲染失败:\n{res_render.stderr}")
        sys.exit(1)

    glob_mp4 = list((raw_render_dir / "videos").glob(f"**/{SCENE_NAME}.mp4"))
    if not glob_mp4:
        print(f"[Error] 未找到场景 {SCENE_NAME} 的 MP4 输出")
        sys.exit(1)
    raw_video = glob_mp4[0]
    print(f"  ✅ 画面渲染成功: {raw_video.name} ({raw_video.stat().st_size / 1024:.1f} KB)")

    # 2. 读取时间轴并混入 VoxCPM 本地离线配音
    print(f"\n🎙️ [步骤 2/4] 混入 VoxCPM2 48kHz 离线播音解说音频...")
    timeline_file = REPO_ROOT / "media" / "audio_sync" / f"{SCENE_NAME}_timeline.json"
    audio_with_offsets = []
    if timeline_file.exists():
        with open(timeline_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        for a_path, offset in meta.get("voiceovers", []):
            audio_with_offsets.append((a_path, float(offset)))

    voiced_scene = temp_dir / f"{SCENE_NAME}_voiced.mp4"
    AudioEngine.mix_scene_audio(raw_video, audio_with_offsets, voiced_scene)
    print(f"  ✅ 沉稳男声配音混流完成: {voiced_scene.name}")

    # 3. 压制 3b1b 标志性灵动马林巴 / 钢琴节奏 BGM (-14 LUFS 标准化)
    print(f"\n🎵 [步骤 3/4] 压制 3b1b 标志性灵动轻快节奏环境音乐 (-14 LUFS)...")
    # 获取适合 3b1b 风格的马林巴/轻快学术节奏 BGM
    bgm_path = ACEStepMusic.get_music(
        style="3b1b_marimba",
        target_duration=60,
        custom_prompt="Playful marimba and minimalist acoustic piano in the style of 3Blue1Brown, crisp lively mathematical discovery tempo, elegant, rhythmic, subtle cello bassline"
    )

    final_master_video = OUTPUT_DIR / "3b1b_lagrange_demo_1080p.mp4"
    AudioEngine.add_bgm_to_video(
        video_path=voiced_scene,
        bgm_path=bgm_path,
        output_path=final_master_video,
        bgm_volume=0.13,
        fade_out_sec=2.5,
        normalize_loudness=True,
        target_lufs=-14.0
    )
    print(f"  🏆 3b1b 最终母带压制完成: {final_master_video.name} ({final_master_video.stat().st_size / (1024*1024):.2f} MB)")

    # 4. 生成 12 宫格看板与 QA 自动化体检
    print(f"\n🖼️ [步骤 4/4] 生成 12 宫格故事板看板与工业级体检...")
    contact_sheet_png = OUTPUT_DIR / "3b1b_lagrange_demo_contact_sheet.png"
    create_contact_sheet(
        video_path=final_master_video,
        output_image_path=contact_sheet_png,
        num_frames=12,
        grid_cols=4,
        header_title="3BLUE1BROWN VISUAL AESTHETIC DEMO // DYNAMIC GEOMETRY & COLOR SYNCHRONICITY"
    )
    print(f"  ✅ 12 宫格故事板看板已生成: {contact_sheet_png.name}")

    print("\n🩺 [成片健康体检报告 (QA)]:")
    audit_passed = audit_video(final_master_video, max_freeze_sec=3.0, target_lufs=-14.0)
    if audit_passed:
        print("  ✅ 视频全项指标审计通过，符合专业发布标准！")

    print("\n" + "=" * 75)
    print("🎉 [3b1b 纯正风格示范片制作完成!]")
    print(f"  • 母带视频: {final_master_video.resolve()}")
    print(f"  • 12 宫格看板: {contact_sheet_png.resolve()}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
