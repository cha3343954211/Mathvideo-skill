import shutil
from pathlib import Path

src = Path("d:/数学教学/数学视频/mathvideo-skill/projects/demo_layout_guard/media/videos/scene_01_safe_layout/480p15/SafeLayoutScene.mp4")
dst = Path("C:/Users/33439/.gemini/antigravity-ide/brain/542bc6eb-606b-41b6-bb23-a8387daff282/demo_layout_guard.mp4")

shutil.copyfile(src, dst)
print("SUCCESS: LayoutGuard Demo video copied! Size:", dst.stat().st_size)
