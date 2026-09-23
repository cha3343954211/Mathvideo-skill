import sys
import json
import shutil
from pathlib import Path

# 引入技能库
SKILL_TEMPLATES = Path(__file__).resolve().parent.parent.parent / "skills" / "manim-video" / "templates"
if str(SKILL_TEMPLATES) not in sys.path:
    sys.path.insert(0, str(SKILL_TEMPLATES))
from audio_engine import AudioEngine

p_root = Path(__file__).resolve().parent
v_raw = p_root / "media/videos/scene_01_voiceover_demo/480p15/AudioSyncScene.mp4"
timeline_file = p_root / "voiceover_timeline.json"
out_video = p_root / "demo_audio_sync_final.mp4"

if not timeline_file.exists():
    print(f"[Error] 未找到时间轴文件: {timeline_file}")
    sys.exit(1)

timeline_data = json.loads(timeline_file.read_text(encoding="utf-8"))
audio_tracks = [(item["audio"], item["start_time"]) for item in timeline_data]

print(f"[Mixer] 准备合成 {len(audio_tracks)} 段配音至视频: {v_raw}")
success = AudioEngine.mix_scene_audio(
    video_path=str(v_raw),
    audio_files_with_offsets=audio_tracks,
    output_path=str(out_video)
)

if success and out_video.exists():
    print(f"[SUCCESS] 有声成片已生成: {out_video} ({out_video.stat().st_size / 1024.0:.1f} KB)")
    # 拷贝到工件目录
    art_path = Path("C:/Users/33439/.gemini/antigravity-ide/brain/542bc6eb-606b-41b6-bb23-a8387daff282/demo_audio_sync.mp4")
    shutil.copyfile(out_video, art_path)
    print(f"[SUCCESS] 已同步至工件: {art_path}")
else:
    print("[Error] 混音压制失败！")
    sys.exit(1)
