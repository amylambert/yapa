"""Initialization context exposing data layer entities for the notes app."""

from .tag import Tag
from .note import Note

__all__ = ["Tag", "Note"]