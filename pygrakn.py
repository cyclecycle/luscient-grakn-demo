import grakn
from pprint import pprint


class Graph():

    def __init__(self, **kwargs):
        pass

    def __enter__(self, uri='localhost:48555', **kwargs):
        self.client = grakn.Grakn(uri=uri)
        self.session = self.client.session(keyspace='cognitive_impairment', **kwargs)
        self.tx = self.session.transaction(grakn.TxType.READ)
        return self

    def execute(self, query):
        answer_iterator = self.tx.query(query)
        data = []
        for concept in answer_iterator.collect_concepts():
            base_type = concept.base_type
            if base_type == 'ATTRIBUTE':
                parsed = self.parse_attribute(concept)
            elif base_type == 'ENTITY':
                parsed = self.parse_entity(concept)
            elif base_type == 'RELATIONSHIP':
                parsed = self.parse_relationship(concept)
            elif base_type == 'ROLE':
                parsed = self.parse_role(concept)
            else:
                print(concept)
                print(dir(concept))
                print()
            data.append(parsed)
            print()
            print()
        return data

    def parse_attribute(self, concept):
        d = {
            'id': concept.id,
            'type': concept.base_type.lower(),
            'label': concept.type().label(),
            'value': concept.value()
        }
        return d

    def parse_attributes(self, attributes):
        for attr in attributes:
            yield parse_attributes(attr)

    def parse_entity(self, concept):
        d = {
            'id': concept.id,
            'type': concept.base_type.lower(),
            'isa': concept.type().label(),
            'attributes': list(self.parse_attributes(concept.attributes()))
        }
        return d

    def parse_relationship(self, concept):
        d = {
            'id': concept.id,
            'type': concept.base_type.lower(),
            'isa': concept.type().label(),
            'roles': list(self.parse_roles(concept.role_players_map()))
        }
        return d

    def parse_roles(self, concept):
        for role in concept:
            yield self.parse_role(role)

    def parse_role(self, concept):
        d = {
            'id': concept.id,
            'label': concept.label(),
        }
        # print(dir(concept))
        players = []
        for player in concept.players():
            players.append({
                'id': player.id,
                'label': player.label()
            })
        d['players'] = players
        return d

    def __exit__(self, type, value, traceback):
        self.tx.close()
