"""
contact_sheet.py: 拼图看板自检工具 (汲取 xiaoma-studio 核心精髓)
在全片导出或审核前，将整段视频或多个分幕均匀抽取 9 / 12 / 16 张切片，
自动拼贴为一张高分辨率故事板拼图 (Contact Sheet)，
让模型和人类一眼检视全片的色彩统一性、视觉重心演变、文字层级与防重叠。
"""
import os
import sys
import math
import shutil
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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

def get_video_duration(video_path):
    import re
    ffmpeg = get_ffmpeg()
    cmd = [ffmpeg, "-i", str(video_path)]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 10.0

def extract_frames_from_video(video_path, num_frames=9, temp_dir=None):
    """从单个视频中均匀抽取 num_frames 张静帧"""
    ffmpeg = get_ffmpeg()
    duration = get_video_duration(video_path)
    t_dir = Path(temp_dir or "media/contact_temp")
    t_dir.mkdir(parents=True, exist_ok=True)

    extracted_frames = []
    # 避免截在绝对 0.0s（可能有黑帧），稍微内缩
    start_offset = min(0.3, duration * 0.05)
    end_offset = max(duration - 0.3, duration * 0.95)

    if num_frames == 1:
        timestamps = [duration / 2.0]
    else:
        step = (end_offset - start_offset) / (num_frames - 1)
        timestamps = [start_offset + i * step for i in range(num_frames)]

    base_name = Path(video_path).stem
    for idx, ts in enumerate(timestamps):
        out_frame = t_dir / f"{base_name}_frame_{idx:02d}.png"
        cmd = [
            ffmpeg, "-y",
            "-ss", f"{ts:.3f}",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(out_frame)
        ]
        subprocess.run(cmd, capture_output=True, errors="replace")
        if out_frame.exists() and out_frame.stat().st_size > 0:
            extracted_frames.append((out_frame, ts, f"{base_name}"))

    return extracted_frames

def extract_frames_from_multi_videos(video_paths, frames_per_video=3, temp_dir=None):
    """从多个分幕视频中按顺序各自抽取切片"""
    all_frames = []
    for vp in video_paths:
        frames = extract_frames_from_video(vp, num_frames=frames_per_video, temp_dir=temp_dir)
        all_frames.extend(frames)
    return all_frames

def create_contact_sheet(frame_data_or_video=None, output_path="out/contact_sheet.png", cols=3, sheet_title="Math Video Storyboard Contact Sheet", num_frames=12, video_path=None, grid_cols=None, output_image_path=None, **kwargs):
    """
    全能看板生成器：既支持直接传入 [(img_path, ts, label), ...] 帧数据，
    也支持直接传入视频文件路径自动抽帧拼贴！
    """
    actual_video = video_path or (frame_data_or_video if isinstance(frame_data_or_video, (str, Path)) else None)
    actual_output = output_image_path or output_path
    actual_cols = grid_cols or cols

    if actual_video is not None:
        frame_data = extract_frames_from_video(actual_video, num_frames=num_frames)
    else:
        frame_data = frame_data_or_video

    if not frame_data:
        print("[Error] 没有可供拼贴的关键帧数据")
        return None

    output_path = actual_output
    cols = actual_cols

    total_frames = len(frame_data)
    cols = min(cols, total_frames)
    rows = math.ceil(total_frames / cols)

    # 规范单格缩放尺寸 (以 16:9 计算，单格宽 540，高 304)
    cell_w, cell_h = 540, 304
    margin = 16
    header_h = 68

    sheet_w = cols * cell_w + (cols + 1) * margin
    sheet_h = rows * cell_h + (rows + 1) * margin + header_h

    # 现代高级暗灰背景
    bg_color = (18, 20, 23)
    card_bg = (28, 31, 38)
    text_color = (236, 239, 244)
    accent_color = (59, 130, 246)
    badge_bg = (0, 0, 0, 180)

    canvas = Image.new("RGBA", (sheet_w, sheet_h), bg_color)
    draw = ImageDraw.Draw(canvas)

    # 绘制顶部标题栏
    title_text = f"🎬 {sheet_title} | Total Frames: {total_frames} ({cols}x{rows})"
    draw.text((margin, 20), title_text, fill=text_color)
    subtitle = "Review: 1.Visual Consistency  2.Information Hierarchy  3.No Overlaps  4.Color Contrast"
    draw.text((margin, 44), subtitle, fill=(136, 146, 176))

    # 装饰线
    draw.line([(margin, header_h - 4), (sheet_w - margin, header_h - 4)], fill=(45, 52, 64), width=1)

    # 逐格填充贴图
    for idx, (img_path, ts, label) in enumerate(frame_data):
        c = idx % cols
        r = idx // cols
        x = margin + c * (cell_w + margin)
        y = header_h + margin + r * (cell_h + margin)

        try:
            with Image.open(img_path) as im:
                thumb = im.convert("RGBA").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                canvas.paste(thumb, (x, y))
        except Exception as e:
            # 占位底色
            draw.rectangle([x, y, x + cell_w, y + cell_h], fill=card_bg)

        # 绘制底部信息条 (半透明遮罩)
        bar_h = 28
        bar_overlay = Image.new("RGBA", (cell_w, bar_h), (10, 12, 15, 210))
        canvas.paste(bar_overlay, (x, y + cell_h - bar_h), bar_overlay)

        # 时间戳与标签文字
        mins = int(ts // 60)
        secs = ts % 60
        time_str = f"[{mins:02d}:{secs:04.1f}]"
        info_str = f"{time_str} {label}"
        draw.text((x + 8, y + cell_h - bar_h + 6), info_str, fill=(220, 225, 235))

        # 单元格边框
        draw.rectangle([x, y, x + cell_w, y + cell_h], outline=(55, 65, 81), width=1)

    out_p = Path(output_path).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(str(out_p), quality=95)
    print(f"\n[OK] 故事板拼图看板已生成: {out_p} ({out_p.stat().st_size / 1024:.1f} KB)")
    return out_p

def main():
    parser = argparse.ArgumentParser(description="Manim 故事板拼图看板生成器 (Contact Sheet)")
    parser.add_argument("--videos", nargs="+", help="一个或多个 MP4 视频文件路径")
    parser.add_argument("--video", default=None, help="单个 MP4 视频文件路径")
    parser.add_argument("-n", "--num-frames", type=int, default=9, help="抽取总帧数 (默认 9 帧，九宫格)")
    parser.add_argument("--cols", type=int, default=3, help="拼图列数 (默认 3)")
    parser.add_argument("-o", "--output", default="out/contact_sheet.png", help="输出拼图保存路径")
    parser.add_argument("--title", default="Math Video Contact Sheet", help="看板主标题")
    args = parser.parse_args()

    v_list = []
    if args.videos:
        v_list.extend(args.videos)
    if args.video:
        v_list.append(args.video)

    if not v_list:
        print("[Error] 请通过 --video 或 --videos 指定输入的 MP4 视频文件")
        sys.exit(1)

    temp_cache = Path("media/contact_temp")
    if len(v_list) == 1:
        frames = extract_frames_from_video(v_list[0], num_frames=args.num_frames, temp_dir=temp_cache)
    else:
        per_video = max(1, args.num_frames // len(v_list))
        frames = extract_frames_from_multi_videos(v_list, frames_per_video=per_video, temp_dir=temp_cache)

    create_contact_sheet(frames, output_path=args.output, cols=args.cols, sheet_title=args.title)

if __name__ == "__main__":
    main()
