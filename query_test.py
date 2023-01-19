import rdflib

QUERY = 'requests/get_quizitem.rq'




g = rdflib.Graph().parse('data.ttl', format='ttl')

with open(QUERY, mode='r', encoding='utf8') as f:
    q = f.read() 


# FILTER(?chapter_no=6 || ?chapter_no=4)

rst = g.query(q)
for dct in rst:
    print({k:v.toPython() for k,v in dct.asdict().items()})

