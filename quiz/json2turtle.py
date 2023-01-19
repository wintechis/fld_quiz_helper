import rdflib
from loader import DATA, QuizItem

NS = rdflib.Namespace("http://example.org/")

def add_quiz_item(g:rdflib.Graph, c: rdflib.BNode, no: str, q: QuizItem) -> None:
    item = rdflib.BNode() # store implementations should store value
    g.add((item, rdflib.RDF.type, NS.QuizItem))
    g.add((item, NS.has_answer, rdflib.Literal(q.answer, datatype=rdflib.XSD.string)))
    g.add((item, NS.has_statement, rdflib.Literal(q.statement, datatype=rdflib.XSD.string)))
    g.add((item, NS.is_True, rdflib.Literal(q.isTrue, datatype=rdflib.XSD.boolean)))
    g.add((item, NS.has_no, rdflib.Literal(k, datatype=rdflib.XSD.int)))

    for goal in q.goals:
        g.add((item, NS.has_goal, rdflib.Literal(goal, datatype=rdflib.XSD.string)))

    g.add((c, NS.has_item, item))



g = rdflib.Graph()


g.namespace_manager.bind("ex", NS)

for key, val in DATA.items():
    chapter = rdflib.BNode() # store implementations should store value
    for k, v in val.items():

        if isinstance(v, QuizItem):
            add_quiz_item(g,  c=chapter, no=k, q=v)
        else:
            g.add((chapter, rdflib.RDFS.label, rdflib.Literal(v)))
            g.add((chapter, NS.has_no , rdflib.Literal(key, datatype=rdflib.XSD.int)))
            g.add((chapter, rdflib.RDF.type, NS.Chapter))


g.serialize(destination='data.ttl', format='ttl')