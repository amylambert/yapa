"""Initialization context exposing package view controllers."""

from .note_create import NoteCreateView
from .note_inline_update import NoteInlineUpdateView
from .note_detail import NoteDetailView
from .note_delete import NoteDeleteView
from .note_list import NoteListView

__all__ = [
    "NoteCreateView",
    "NoteInlineUpdateView",
    "NoteDetailView",
    "NoteDeleteView",
    "NoteListView",
]