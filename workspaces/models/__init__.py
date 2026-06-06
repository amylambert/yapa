"""Needed to make models package work properly"""

from .task import Task
from .workspace import Workspace

# Explictly declare exported classes
__all__ = ["Workspace", "Task"]