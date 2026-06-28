"""Initialization for the tasks views package."""

from .task_create import TaskCreateView
from .task_detail import TaskDetailView
from .task_inline_update import TaskInlineUpdateView
from .task_delete import TaskDeleteView
from .task_list import TaskListView

__all__ = [
    "TaskCreateView",
    "TaskDetailView",
    "TaskInlineUpdateView",
    "TaskDeleteView",
    "TaskListView",
]