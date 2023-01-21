from dataclasses import dataclass


@dataclass
class QuizItem:
    statement: str
    isTrue: bool
   # goals: List[str]
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