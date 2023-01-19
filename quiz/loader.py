from typing import List, Dict
from dataclasses import dataclass
import json

import re

# # Copied from <https://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates>
# def tex_escape(text):
#     """
#         :param text: a plain text message
#         :return: the message escaped to appear correctly in LaTeX
#     """
#     conv = {
#         '&': r'\&',
#         '%': r'\%',
#         '$': r'\$',
#         '#': r'\#',
#         '_': r'\_',
#         '{': r'\{',
#         '}': r'\}',
#         '~': r'\textasciitilde{}',
#         '^': r'\^{}',
#         '\\': r'\textbackslash{}',
#         '<': r'\textless{}',
#         '>': r'\textgreater{}',
#     }
#     regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
#     return regex.sub(lambda match: conv[match.group()], text)

# CHARS = {
#     '&':  r'\&',
#     '%':  r'\%', 
#     '$':  r'\$', 
#     '#':  r'\#', 
#     '_':  r'\letterunderscore{}', 
#     '{':  r'\letteropenbrace{}', 
#     '}':  r'\letterclosebrace{}',
#     '~':  r'\lettertilde{}', 
#     '^':  r'\letterhat{}', 
#     '\\': r'\letterbackslash{}',
# }

@dataclass
class QuizItem:
    statement: str
    isTrue: bool
    goals: List[str]
    answer: str=''

@dataclass
class Chapter:
    title: str
    no: int

@dataclass
class LearningGoal:
    chapter_no: int
    no: int
    description: str

def add_goals(lst: List[str]) -> List[LearningGoal]:
    l = ()
    for i in lst:
        chapter_no, no = i.replace('G', '').split('.')
        l.append(LearningGoal(chapter_no, no))
    return l


# change dir
with open('quiz/items.json', mode='r', encoding='utf-8') as f:
    DATA : Dict = json.load(f)


for key, value in DATA.items():
    for k, val in value.items():
        if k=='title':
            chapter = Chapter(val, int(key))
        if k.isnumeric():
            value[k] = QuizItem(value[k]['statement'], value[k]['isTrue'], value[k]['goals'])

