from typing import List
import random
from .py2LaTeX import create_LaTeX
from .myDataclasses import Settings, QuizItem
from .etc import get_items, resolve_chapters


class DoesNotComputeExeption(Exception):
    def __init__(self, no_items: int, len_chapters: int, max_per_chapter: int):
        self.message = f'"# Items" must be greater than "Chapters" times "Max per chapter": {no_items} > {len_chapters} x {max_per_chapter}'

class TooFewItemsException(Exception):
    def __init__(self, target: int, available: int):
         self.message = f'Only {available} Quizitems are available, but {target} Quizitems were requested. Please refine your selection!'


def select_items(s: Settings) -> List[QuizItem]:
    if len(s.chapters) * s.max_per_chapter < s.no_items:
        raise DoesNotComputeExeption(s.no_items, len(s.chapters), s.max_per_chapter)
    
    items = get_items(s.chapters)

    item_per_chapter = {}
    for i in range(s.no_items):
        if not len(items): 
            raise TooFewItemsException(s.no_items, i)
        while True:
            item = random.choice(items)
            k = item['chapter'].no
            if k not in item_per_chapter.keys():
                item_per_chapter[k] = []       
            if len(item_per_chapter[k]) < s.max_per_chapter: break
        item_per_chapter[k].append([item['quiz'], int(k)])
        items.remove(item)

    lst_flat = []
    for x in item_per_chapter.values():
        lst_flat.extend(x)

    if s.ordered:
        lst_flat.sort(key = lambda x:x[1])

    # isolate Quizitems
    lst, _ = zip(*lst_flat)
     
    return lst


def generate_LaTeX(s: Settings) -> str:
    items = select_items(s)
    return create_LaTeX(items)

if __name__ == '__main__':
    c = resolve_chapters('1-10')
    s = Settings(10, c , 2, True)
    print(generate_LaTeX(s))



