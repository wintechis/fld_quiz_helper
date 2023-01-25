from typing import List, Dict, Any, Set, Union
import os
from flask import session
import rdflib
from .myDataclasses import Chapter, QuizItem, LearningGoal


DATA_PATH = f'{os.path.dirname(__file__)}/data.ttl'

def add_chapters_session():
    if not session.get('chapters'):
        print(DATA_PATH)
        graph = load_graph(DATA_PATH)
        session['chapters'] = get_chapters(graph)


def load_graph(path: str) -> rdflib.Graph:
    return rdflib.Graph().parse(path, format='ttl')


def get_chapters(graph: rdflib.Graph) -> List[Dict[str, Any]]:
    lst = []
    query = get_query('get_chapters.rq')
    rst = graph.query(query)
    for row in  rst:
        lst.append(
                {k:v.toPython() if v else None for k,v in row.asdict().items()}
            )
    return lst

def get_query(path: str):
    path = os.path.join('requests', path)
    with open(path, mode='r', encoding='utf8') as f:
        return f.read() 


def get_item_cls(dct: Union[Dict[str, Any], QuizItem]) -> QuizItem:
    if isinstance(dct, QuizItem): return dct
    return QuizItem(dct['statement'], dct['isTrue'], dct['answer'])

def get_chapter_cls(dct: Union[Dict[str, Any], Chapter]) -> Chapter:
    if isinstance(dct, Chapter): return dct
    return Chapter(label=dct['label'], no=dct['no']) 

def get_items(chapter_nos: Set[str]) -> List[Dict[str, Any]]:
    # load graph
    graph = load_graph(DATA_PATH)

    query = get_query('get_quizitems.rq')
    # add FILTER statement
    chapter_nos = [val for val in chapter_nos if val.isnumeric()]
    if chapter_nos:
        query = replace_placeholder(query, 'chapter_no', chapter_nos)
    rst = graph.query(query)

    lst = []
    for row in rst:
        dct =  {k:v.toPython() if v else None for k,v in row.asdict().items()}
        quiz_item = get_item_cls(dct)
        chapter = get_chapter(graph, dct['chapter_no'])
        lst.append({
            'chapter':chapter,
            'quiz': quiz_item}
            )
    return lst

def get_chapter(graph: rdflib.Graph, chapter_no: int) -> Chapter:
    query = get_query('get_chapters.rq')
    query = replace_placeholder(query, 'no', [str(chapter_no)])
    rst = graph.query(query)
    for row in  rst:
        dct =  {k:v.toPython() if v else None for k,v in row.asdict().items()}
    return get_chapter_cls(dct)

def replace_placeholder(query: str, var: str, values: Set[str]) -> str:
    expr = [f'?{var}={val}' for val in values] 
    return  query.replace('#PLACEHOLDER', f'FILTER({"||".join(expr)})')


def resolve_chapters(input: str) -> set[str]: 
    chapters = set()
    if input:
        lst_input = input.replace(' ', '').replace(';', ',').split(',')
        if isinstance(lst_input, str):
            lst_input = [lst_input]
        for val in lst_input:
            if '-' in val:
                x = list(map(int, val.split('-')))
                lower, upper = min(x), max(x)
                chapters.update(expand_range(lower, upper))
            elif val.isnumeric():
                chapters.add(val)
            continue
    return chapters

def expand_range(lower: int, upper: int) -> set[str]:
    return {str(x) for x in range(lower, upper+1)}