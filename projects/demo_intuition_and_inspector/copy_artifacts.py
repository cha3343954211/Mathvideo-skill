import shutil
from pathlib import Path

p_src = Path("d:/数学教学/数学视频/mathvideo-skill/projects/demo_intuition_and_inspector")
art_dir = Path("C:/Users/33439/.gemini/antigravity-ide/brain/542bc6eb-606b-41b6-bb23-a8387daff282")

# 1. 复制 MP4
v_src = p_src / "media/videos/scene_01_matrix_shear/480p15/MatrixShearScene.mp4"
v_dst = art_dir / "demo_matrix_shear.mp4"
shutil.copyfile(v_src, v_dst)
print("Copied video:", v_dst.stat().st_size)

# 2. 复制单帧 PNG
img_src = p_src / "media/images/scene_01_matrix_shear/MatrixShearScene_ManimCE_v0.21.0.png"
img_dst = art_dir / "fast_inspect_frame.png"
shutil.copyfile(img_src, img_dst)
print("Copied frame png:", img_dst.stat().st_size)
