"""
fast_inspector.py: 毫秒级单帧切片质检器
无需等待全量 MP4 渲染，仅需约 0.5 秒即可抽取渲染单张高清静态帧 PNG，
用于快速检验长公式排版、几何构图、配色对比与元素防重叠。
"""
import os
import sys
import glob
import shutil
import argparse
import subprocess
from pathlib import Path

# 终端编码安全
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def inspect_frame(script_path, scene_name, output_image=None, copy_to_artifact=False):
    """
    单帧快速质检：
    使用 manim -s -ql 仅渲染末帧 PNG
    """
    script = Path(script_path).resolve()
    if not script.exists():
        print(f"[Error] 脚本文件未找到: {script}")
        return None

    cmd = [sys.executable, "-m", "manim", "-s", "-ql", str(script), scene_name]
    print(f"\n[⚡ 快速帧质检] 正在提取 {scene_name} 关键帧...")
    print(f"执行命令: {' '.join(cmd)}")

    res = subprocess.run(cmd, cwd=str(script.parent), capture_output=True, text=True, errors="replace")
    if res.returncode != 0:
        print(f"[Error] 帧提取失败 (code {res.returncode}):\n{res.stderr}")
        return None

    # 寻找生成的 PNG 图片
    media_dir = script.parent / "media" / "images"
    png_pattern = str(media_dir / "**" / f"{scene_name}*.png")
    found_pngs = glob.glob(png_pattern, recursive=True)

    if not found_pngs:
        # 回退检查上层
        found_pngs = glob.glob(str(script.parent / "**" / f"{scene_name}*.png"), recursive=True)

    if not found_pngs:
        print("[Warning] 未能在输出目录找到匹配的 PNG 图像")
        return None

    # 按修改时间找最新的一张
    found_pngs.sort(key=os.path.getmtime, reverse=True)
    latest_png = Path(found_pngs[0])
    size_kb = latest_png.stat().st_size / 1024.0
    print(f"[OK] 关键帧质检图片已生成: {latest_png} ({size_kb:.1f} KB)")

    if output_image:
        target_dest = Path(output_image).resolve()
        target_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(latest_png, target_dest)
        print(f"[OK] 已导出至目标路径: {target_dest}")
        latest_png = target_dest

    return latest_png

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manim 毫秒级单帧切片质检工具")
    parser.add_argument("script", help="场景 Python 脚本文件路径")
    parser.add_argument("scene", help="Scene 类名")
    parser.add_argument("-o", "--output", default=None, help="目标保存图片路径")
    args = parser.parse_args()

    inspect_frame(args.script, args.scene, args.output)
