"""Initialization for the tasks views package."""

from .task_create import TaskCreateView
from .task_detail import TaskDetailView
from .subtask_create import SubTaskCreateView
from .task_update import TaskInlineUpdateView

__all__ = [
    "TaskCreateView",
    "TaskDetailView",
    "SubTaskCreateView",
    "TaskInlineUpdateView",
]