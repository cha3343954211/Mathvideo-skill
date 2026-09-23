import sys
from pathlib import Path

# 将 skill 模版库加入 Python 搜索路径
SKILL_TEMPLATES = Path(__file__).resolve().parent.parent.parent / "skills" / "manim-video" / "templates"
if str(SKILL_TEMPLATES) not in sys.path:
    sys.path.insert(0, str(SKILL_TEMPLATES))

from base_scene import (
    THEMES,
    FONT_CHINESE,
    BaseMathScene,
    MovingCameraMathScene,
    NordScene,
    ChalkboardScene,
    ClaudeLightScene
)
from math_rigs import (
    DynamicTangentRig,
    DynamicRiemannRig,
    NumberLineCursorRig,
    OrganicMotion
)
