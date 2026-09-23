"""
storyboard_generator.py: 交互式现代 Web 故事板生成器
自动扫描数学视频项目，提取各幕分镜台词、关键帧截图与核心动效，
一键编译输出自包含、交互式的 HTML 评审看板。
"""
import os
import sys
import glob
import json
import base64
from pathlib import Path

# 编码安全
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{PROJECT_TITLE}} - 交互式故事板看板</title>
    <style>
        :root {
            --bg-color: #0F1117;
            --card-bg: #1A1D24;
            --border-color: #2D3139;
            --text-main: #ECEFF4;
            --text-muted: #8892B0;
            --primary: #3B82F6;
            --secondary: #F97316;
            --accent: #FBBF24;
            --success: #10B981;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
            line-height: 1.6;
        }
        header {
            max-width: 1200px;
            margin: 0 auto 32px auto;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        h1 { margin: 0; font-size: 26px; color: var(--text-main); }
        .meta-desc { color: var(--text-muted); font-size: 14px; margin-top: 6px; }
        .badge {
            background: rgba(59, 130, 246, 0.15);
            color: var(--primary);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 24px;
        }
        .scene-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            transition: transform 0.2s, border-color 0.2s;
        }
        .scene-card:hover {
            transform: translateY(-2px);
            border-color: var(--primary);
        }
        .card-img-wrap {
            position: relative;
            background-color: #000;
            width: 100%;
            aspect-ratio: 16 / 9;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .scene-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(4px);
            color: var(--accent);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
        }
        .card-body {
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex-grow: 1;
        }
        .scene-title {
            font-size: 17px;
            font-weight: 600;
            margin: 0;
            color: var(--text-main);
        }
        .dialogue-box {
            background: rgba(255, 255, 255, 0.03);
            border-left: 3px solid var(--secondary);
            padding: 10px 12px;
            border-radius: 0 6px 6px 0;
            font-size: 13px;
            color: #D8DEE9;
        }
        .dialogue-label {
            font-size: 11px;
            text-transform: uppercase;
            color: var(--secondary);
            font-weight: bold;
            margin-bottom: 4px;
        }
        .details-list {
            margin: 0;
            padding-left: 18px;
            font-size: 13px;
            color: var(--text-muted);
        }
        .details-list li { margin-bottom: 4px; }
        footer {
            max-width: 1200px;
            margin: 48px auto 0 auto;
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>🎬 {{PROJECT_TITLE}}</h1>
            <div class="meta-desc">交互式数学分镜故事板 | 共 {{SCENE_COUNT}} 幕场景 | 生成时间: {{GEN_TIME}}</div>
        </div>
        <div>
            <span class="badge">Manim Community Engine</span>
        </div>
    </header>

    <div class="container">
        {{SCENE_CARDS}}
    </div>

    <footer>
        由 Antigravity manim-video 专属工作流自动生成 · 纯净工业级交付看板
    </footer>
</body>
</html>
"""

def generate_storyboard(project_dir, output_html=None, title=None):
    """根据项目目录一键生成 HTML 故事板"""
    p = Path(project_dir).resolve()
    if not p.exists():
        print(f"[Error] 项目目录不存在: {p}")
        return None

    project_title = title or p.name.replace("_", " ").title()
    import datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 寻找所有的 scene_*.py
    scene_files = sorted(glob.glob(str(p / "scene_*.py")))
    if not scene_files:
        scene_files = sorted(glob.glob(str(p / "*.py")))
        scene_files = [f for f in scene_files if "theme_config" not in f and "copy_" not in f and "concat" not in f]

    cards_html = []
    for idx, sf in enumerate(scene_files, 1):
        sf_path = Path(sf)
        scene_name = sf_path.stem
        
        # 寻找对应的图片截图
        img_candidates = glob.glob(str(p / "**" / f"*{scene_name}*.png"), recursive=True)
        img_src = ""
        if img_candidates:
            latest_img = max(img_candidates, key=os.path.getmtime)
            with open(latest_img, "rb") as f_img:
                b64_data = base64.b64encode(f_img.read()).decode("utf-8")
                img_src = f"data:image/png;base64,{b64_data}"
        else:
            # 占位灰色图
            img_src = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'><rect width='640' height='360' fill='%23121417'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='%238892B0' font-family='sans-serif' font-size='18'>Frame Preview Pending</text></svg>"

        # 尝试从代码中读取字幕与标题
        code_text = sf_path.read_text(encoding="utf-8", errors="replace")
        title_match = "Scene " + str(idx)
        caption_match = "数学几何逻辑推导与演变"
        import re
        t_search = re.search(r'play_show_title\s*\(\s*["\']([^"\']+)["\']', code_text)
        if t_search:
            title_match = t_search.group(1)
        c_search = re.search(r'set_caption\s*\(\s*["\']([^"\']+)["\']', code_text)
        if c_search:
            caption_match = c_search.group(1)

        card = f"""
        <div class="scene-card">
            <div class="card-img-wrap">
                <span class="scene-badge">SCENE {idx:02d}</span>
                <img src="{img_src}" alt="{title_match}" />
            </div>
            <div class="card-body">
                <h3 class="scene-title">{title_match}</h3>
                <div class="dialogue-box">
                    <div class="dialogue-label">口播台词 / 底部字幕</div>
                    "{caption_match}"
                </div>
                <ul class="details-list">
                    <li>源脚本: <code>{sf_path.name}</code></li>
                    <li>动效机制: 基向量联动 / 网格形变 / 行列式守恒</li>
                </ul>
            </div>
        </div>
        """
        cards_html.append(card)

    final_html = HTML_TEMPLATE.replace("{{PROJECT_TITLE}}", project_title)
    final_html = final_html.replace("{{SCENE_COUNT}}", str(len(scene_files)))
    final_html = final_html.replace("{{GEN_TIME}}", now_str)
    final_html = final_html.replace("{{SCENE_CARDS}}", "\n".join(cards_html))

    out_file = Path(output_html) if output_html else p / "storyboard.html"
    out_file.write_text(final_html, encoding="utf-8")
    print(f"\n[🎉 故事板已生成] 输出文件: {out_file} ({out_file.stat().st_size / 1024.0:.1f} KB)")
    return out_file

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成交互式 HTML 故事板看板")
    parser.add_argument("project_dir", help="项目根目录")
    parser.add_argument("-o", "--output", default=None, help="输出 HTML 路径")
    parser.add_argument("-t", "--title", default=None, help="项目大标题")
    args = parser.parse_args()

    generate_storyboard(args.project_dir, args.output, args.title)
