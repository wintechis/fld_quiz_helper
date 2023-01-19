from typing import Set, List
from dataclasses import dataclass
import random
from loader import DATA, QuizItem
from py2LaTeX import create_LaTeX


@dataclass
class Settings:
    no_items: int
    chapters: set
    max_per_chapter: int


class DoesNotComputeExeption(Exception):
    pass


def expand_range(lower: int, upper: int) -> set[int]:
    return {x for x in range(lower, upper+1)}

def get_chapters(input: str) -> set[int]:
    chapters = set()
    lst_input = input.replace(' ', '').replace(';', ',').split(',')
    for val in lst_input:
        if '-' in val:
            lower, upper = min(val.split('-')), max(val.split('-'))
            chapters.update(expand_range(int(lower), int(upper)))
        elif val.isnumeric():
            chapters.add(int(val))
        continue

    return chapters


def select_items(s: Settings) -> List[QuizItem]:
    if len(s.chapters) * s.max_per_chapter < s.no_items:
        raise DoesNotComputeExeption
    
    # keep only existing chapters' keys
    d_set = set(map(int, DATA.keys()))
    d = {str(val):0 for val in d_set.intersection(s.chapters)}

    # get random distribution
    keys = tuple(d.keys())
    for i in range(s.no_items):
        while True:
            k = random.choice(keys)
            if d[k] < s.max_per_chapter: break
        d[k] += 1 

    # retrieve random QuizItems
    lst = []
    for k, v in d.items():
        keys = tuple(key for key in DATA[k].keys() if key.isnumeric())
        for i in range(v):
            while True:
                k2 = random.choice(keys)
                q = DATA[k][k2]    
                if not q in lst:
                    lst.append(q)
                    break
    return lst

if __name__ == '__main__':
    c = get_chapters('1-10')
    s = Settings(10, c , 2)
    print(create_LaTeX(select_items(s)))



