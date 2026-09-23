import sys
from pathlib import Path

SKILL_TEMPLATES = Path(__file__).resolve().parent.parent.parent / "skills" / "manim-video" / "templates"
if str(SKILL_TEMPLATES) not in sys.path:
    sys.path.insert(0, str(SKILL_TEMPLATES))

from base_scene import (
    THEMES,
    FONT_CHINESE,
    BaseMathScene,
    NordScene
)
from layout_guard import LayoutGuard
from math_rigs import OrganicMotion
