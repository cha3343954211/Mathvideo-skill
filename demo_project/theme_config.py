"""
样板工程：主题与基类配置
"""
import sys
import os

# 将父级 skills 目录加入 Python 搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "manim-video", "templates")))
from base_scene import BaseMathScene, MathTheme
