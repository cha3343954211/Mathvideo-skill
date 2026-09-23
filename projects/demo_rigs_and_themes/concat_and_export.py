import sys
from pathlib import Path
import shutil

skill_scripts = Path(__file__).resolve().parent.parent.parent / "skills" / "manim-video" / "scripts"
sys.path.insert(0, str(skill_scripts))
from render_manager import stitch_videos

p_root = Path(__file__).resolve().parent
s1 = p_root / "media/videos/scene_01_dynamic_derivative/480p15/DynamicDerivativeScene.mp4"
s2 = p_root / "media/videos/scene_02_riemann_chalkboard/480p15/RiemannChalkboardScene.mp4"

out_mp4 = p_root / "demo_breakthrough_2_6.mp4"
stitch_videos([str(s1), str(s2)], str(out_mp4))

artifact_path = Path("C:/Users/33439/.gemini/antigravity-ide/brain/542bc6eb-606b-41b6-bb23-a8387daff282/demo_breakthrough_2_6.mp4")
shutil.copyfile(out_mp4, artifact_path)
print("SUCCESS: Demo video stitched and copied to artifact! Size:", artifact_path.stat().st_size)
