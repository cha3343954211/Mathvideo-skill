import shutil
from pathlib import Path

src = Path("d:/数学教学/数学视频/mathvideo-skill/projects/demo_3d_saddle/media/videos/scene_01_saddle_surface/480p15/SaddlePoint3DScene.mp4")
dst = Path("C:/Users/33439/.gemini/antigravity-ide/brain/542bc6eb-606b-41b6-bb23-a8387daff282/demo_3d_saddle.mp4")

shutil.copyfile(src, dst)
print("SUCCESS: 3D Demo video copied! Size:", dst.stat().st_size)
