import pygrakn.pygrakn as grakn


KEYSPACE = 'test'


with grakn.Graph(keyspace=KEYSPACE) as graph:
    