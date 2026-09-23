"""
render_manager.py: Manim 场景批量渲染与视频无损拼接工具
支持快速低清预览 (-ql)、高清全量渲染 (-qh) 以及一键将各幕合成为完整视频。
"""
import os
import sys
import argparse
import subprocess
import glob
from pathlib import Path

# 确保控制台支持 UTF-8
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_manim_cmd():
    """获取可用的 manim 执行命令"""
    # 优先检查 python -m manim
    return [sys.executable, "-m", "manim"]

def get_ffmpeg_cmd():
    """获取 ffmpeg 命令"""
    # 优先检查系统 PATH
    import shutil
    p = shutil.which("ffmpeg")
    if p:
        return p
    # 常见 winget 路径
    winget_glob = glob.glob(r"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\*ffmpeg*\**\bin\ffmpeg.exe", recursive=True)
    if winget_glob:
        return winget_glob[0]
    return "ffmpeg"

def render_scene(script_path, scene_name, quality="l", preview=False):
    """
    渲染指定脚本中的场景
    quality: 'l' (480p), 'm' (720p), 'h' (1080p), 'k' (4K)
    """
    cmd = get_manim_cmd() + ["render", script_path, scene_name, f"-q{quality}"]
    if preview:
        cmd.append("-p")
    
    print(f"\n[🚀 渲染开始] 文件: {script_path} | 场景: {scene_name} | 画质: {quality}")
    print(f"执行命令: {' '.join(cmd)}")
    
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"[❌ 渲染失败] 场景 {scene_name} 退出代码: {res.returncode}")
        return False
    print(f"[✅ 渲染成功] 场景: {scene_name}")
    return True

def stitch_videos(video_list, output_file):
    """使用 ffmpeg concat 模式无损拼接多个 mp4 视频"""
    ffmpeg = get_ffmpeg_cmd()
    temp_list_file = "concat_list.tmp.txt"
    
    with open(temp_list_file, "w", encoding="utf-8") as f:
        for v in video_list:
            abs_path = os.path.abspath(v).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
            
    print(f"\n[🎬 开始拼接视频] 包含 {len(video_list)} 个分幕，目标输出: {output_file}")
    
    concat_cmd = [
        ffmpeg, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_list_file,
        "-c", "copy",
        output_file
    ]
    
    res = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    
    if os.path.exists(temp_list_file):
        os.remove(temp_list_file)
        
    if res.returncode == 0 and os.path.exists(output_file):
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"[🎉 拼接完成] 完整视频已生成: {output_file} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"[❌ 拼接失败] {res.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Manim 视频工程渲染与拼接管线")
    parser.add_argument("--action", choices=["render", "stitch", "pipeline"], default="pipeline",
                        help="执行动作: render(仅渲染), stitch(仅拼接已有视频), pipeline(全流程渲染+拼接)")
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="l",
                        help="渲染画质: l(480p快速预览), m(720p), h(1080p高清交付), k(4k)")
    parser.add_argument("--scenes", nargs="+", help="按顺序指定要处理的脚本与类名，格式：script.py:SceneName")
    parser.add_argument("--output", default="final_math_video.mp4", help="最终拼接导出的视频文件名")
    
    args = parser.parse_args()
    
    if not args.scenes:
        print("[!] 请使用 --scenes 参数指定场景，例如: --scenes scene_01.py:IntroScene scene_02.py:ProofScene")
        return 1
        
    tasks = []
    for item in args.scenes:
        if ":" in item:
            s_file, s_name = item.split(":", 1)
        else:
            s_file, s_name = item, None
        tasks.append((s_file, s_name))
        
    rendered_files = []
    
    # 1. 渲染阶段
    if args.action in ["render", "pipeline"]:
        for s_file, s_name in tasks:
            success = render_scene(s_file, s_name or "", quality=args.quality)
            if not success:
                print(f"[!] 终止流程: {s_file}:{s_name} 渲染未通过")
                return 1

    # 2. 定位生成的视频文件
    # Manim 默认路径结构: media/videos/{script_stem}/{res}/{SceneName}.mp4
    res_dir_map = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
    target_res = res_dir_map.get(args.quality, "480p15")
    
    for s_file, s_name in tasks:
        stem = Path(s_file).stem
        pattern = f"media/videos/{stem}/{target_res}/{s_name}.mp4"
        matched = glob.glob(pattern)
        if matched:
            rendered_files.append(matched[0])
        else:
            # 模糊查找最近修改的 mp4
            candidates = glob.glob(f"media/videos/{stem}/**/{s_name}.mp4", recursive=True)
            if candidates:
                rendered_files.append(candidates[0])
            else:
                print(f"[!] 警告: 未找到渲染后的文件 {pattern}")
                
    # 3. 拼接阶段
    if args.action in ["stitch", "pipeline"]:
        if len(rendered_files) < 1:
            print("[!] 未找到待拼接的视频分幕，无法执行拼接。")
            return 1
        stitch_videos(rendered_files, args.output)
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
