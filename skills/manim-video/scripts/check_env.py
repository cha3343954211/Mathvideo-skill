"""
Manim 视频制作环境自检与诊断脚本
用于检查 Python、Manim、FFmpeg、LaTeX、中文字体等核心依赖。
"""
import sys
import os
import shutil
import subprocess

# 兼容 Windows GBK 控制台编码
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_status(name, passed, message=""):
    symbol = "[√]" if passed else "[×]"
    print(f"{symbol} {name:<16}: {message}")

def check_python():
    v = sys.version_info
    passed = v.major == 3 and v.minor >= 9
    print_status("Python 版本", passed, f"{v.major}.{v.minor}.{v.micro} ({sys.executable})")
    return passed

def check_manim():
    try:
        import manim
        print_status("Manim 模块", True, f"v{manim.__version__}")
        return True
    except ImportError as e:
        print_status("Manim 模块", False, f"未安装或无法导入: {e}")
        return False

def check_command(cmd_name, test_arg="--version"):
    # 优先使用 PATH，如果未在 PATH 则检查 Python Scripts
    cmd_path = shutil.which(cmd_name)
    if not cmd_path:
        # 尝试备选路径 (Windows)
        py_scripts = os.path.join(os.path.dirname(sys.executable), "Scripts")
        candidate = os.path.join(py_scripts, f"{cmd_name}.exe")
        if os.path.exists(candidate):
            cmd_path = candidate

    if not cmd_path:
        print_status(cmd_name, False, "未在系统 PATH 中找到")
        return False, None
    
    try:
        res = subprocess.run([cmd_path, test_arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace", timeout=5)
        first_line = (res.stdout or res.stderr).splitlines()[0] if (res.stdout or res.stderr) else "OK"
        print_status(cmd_name, True, f"{first_line[:50]}... ({cmd_path})")
        return True, cmd_path
    except Exception as e:
        print_status(cmd_name, False, f"调用出错: {e}")
        return False, None

def check_chinese_fonts():
    try:
        import manimpango
        fonts = manimpango.list_fonts()
        candidates = ["Microsoft YaHei", "SimHei", "SimSun", "KaiTi", "PingFang SC", "Noto Sans CJK SC"]
        available = [f for f in candidates if f in fonts]
        if available:
            print_status("中文字体支持", True, f"可用: {', '.join(available[:3])} (推荐首选: {available[0]})")
            return True, available[0]
        else:
            print_status("中文字体支持", False, "未匹配到常见中文字体，请检查系统字体库")
            return False, None
    except Exception as e:
        print_status("中文字体支持", False, f"ManimPango 检测异常: {e}")
        return False, None

def main():
    print("=" * 60)
    print("           Manim 数学视频环境诊断报告")
    print("=" * 60)
    
    py_ok = check_python()
    manim_ok = check_manim()
    ffmpeg_ok, _ = check_command("ffmpeg", "-version")
    latex_ok, _ = check_command("latex", "--version")
    dvisvgm_ok, _ = check_command("dvisvgm", "--version")
    font_ok, pref_font = check_chinese_fonts()
    
    print("=" * 60)
    all_ok = py_ok and manim_ok and ffmpeg_ok and font_ok
    if all_ok:
        print("[OK] 恭喜！核心视频渲染环境配置完整，可直接开始制作数学动画！")
        if not latex_ok or not dvisvgm_ok:
            print("[!] 提示: LaTeX / dvisvgm 暂未就绪，建议普通文本使用 Text() 代替 MathTex()，或补全 LaTeX 路径。")
    else:
        print("[!] 存在必要依赖未就绪，请参考诊断提示进行配置或环境变量追加。")
    print("=" * 60)
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
