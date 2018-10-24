import pygrakn.pygrakn as grakn
import requests
from pprint import pprint


with grakn.Graph(keyspace='cognitive_impairment') as graph:
    # data = graph.execute('match $x; limit 10; get;')
    # data = graph.execute('insert $x isa sentence has text \"hi there\";')
    # graph.commit()
    data = graph.execute('match $x isa sentence has text \"hi there\"; get;')
    # data = graph.execute('match $x isa sentence has text \"hi there\"; delete $x;')
    # graph.commit()

    pprint(data)


# read in text data from file
# sent to luscient api
# put results in graph
