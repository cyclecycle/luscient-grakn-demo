import pygrakn
from pprint import pprint

'''
directory of useful attributes of grakn objects

    all:
        id
        type().label()

    entity:
        attributes
        relationships
        roles
        type

    attribute:
        type().label()
        value()

    relationship:
        role_players_map
'''

with pygrakn.Graph(keyspace='cognitive_impairment') as graph:
    data = graph.execute('match $x isa relationship; limit 5; get;')
    pprint(data)