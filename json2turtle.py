import rdflib
from quiz.myDataclasses import QuizItem,Chapter,LearningGoal
from typing import Dict, Any
import json
import argparse
import os

NS = rdflib.Namespace("http://example.org/")
TARGET = 'data.ttl'

def add_quiz_item(g:rdflib.Graph, c: rdflib.BNode, no: str, q: QuizItem) -> None:
    item = rdflib.BNode() # store implementations should store value
    g.add((item, rdflib.RDF.type, NS.QuizItem))
    g.add((item, NS.has_answer, rdflib.Literal(q.answer, datatype=rdflib.XSD.string)))
    g.add((item, NS.has_statement, rdflib.Literal(q.statement, datatype=rdflib.XSD.string)))
    g.add((item, NS.is_True, rdflib.Literal(q.isTrue, datatype=rdflib.XSD.boolean)))
    g.add((item, NS.has_no, rdflib.Literal(no, datatype=rdflib.XSD.int)))

    for goal in q.goals:
        g.add((item, NS.has_goal, rdflib.Literal(goal, datatype=rdflib.XSD.string)))

    g.add((c, NS.has_item, item))


def dct2graph(data: Dict[str, Any]) -> rdflib.Graph():
    g = rdflib.Graph()
    g.namespace_manager.bind("ex", NS)

    for key, val in data.items():
        chapter = rdflib.BNode()
        for k, v in val.items():

            if isinstance(v, QuizItem):
                add_quiz_item(g,  c=chapter, no=k, q=v)
            else:
                g.add((chapter, rdflib.RDFS.label, rdflib.Literal(v)))
                g.add((chapter, NS.has_no , rdflib.Literal(key, datatype=rdflib.XSD.int)))
                g.add((chapter, rdflib.RDF.type, NS.Chapter))
    return g


def graph2turtle(g: rdflib.Graph ,target: str) -> None:
    g.serialize(destination=target, format='ttl')


def dct2cls(data: Dict[str, Any]) -> None:
    for key, value in data.items():
        for k, val in value.items():
            if k=='title':
                value[k] = Chapter(val, int(key))
            if k.isnumeric():
                value[k] = QuizItem(value[k]['statement'], value[k]['isTrue'], value[k]['goals'])

def load_json() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description ='Convert Json')
    parser.add_argument('file', help='Name of the json file')  
    args = parser.parse_args()
    file_name = os.path.splitext(args.file)[0] + '.json'

    with open(file_name, mode='r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    data = load_json()
    dct2cls(data)
    g = dct2graph(data)
    graph2turtle(g, TARGET)
