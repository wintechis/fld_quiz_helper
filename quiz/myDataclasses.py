from dataclasses import dataclass, field
from typing import List

@dataclass
class QuizItem:
    statement: str
    isTrue: bool
    goals: List[str] = field(default_factory=list)
    answer: str=''

@dataclass
class Chapter:
    label: str
    no: int

@dataclass
class LearningGoal:
    chapter_no: int
    no: int
    description: str

@dataclass
class Settings:
    no_items: int
    chapters: set
    max_per_chapter: int
    ordered: bool