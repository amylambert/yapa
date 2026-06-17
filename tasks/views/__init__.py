"""Initialization for the tasks views package."""

from .task_create import TaskCreateView
from .task_detail import TaskDetailView
from .subtask_create import SubTaskCreateView
from .task_inline_update import TaskInlineUpdateView
from .task_delete import TaskDeleteView

__all__ = [
    "TaskCreateView",
    "TaskDetailView",
    "SubTaskCreateView",
    "TaskInlineUpdateView",
    "TaskDeleteView",
]