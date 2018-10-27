import os
import json
import pygrakn.pygrakn as grakn
from pprint import pprint


CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
PATH = os.path.join(DATA_DIR, 'processed/inf.json')
KEYSPACE = 'colorectal_cancer'


with open(PATH) as f:
    results = json.load(f)


with grakn.Graph(keyspace=KEYSPACE) as graph:
    for result in results:
        # for relationship in result['entity_phrase_relationships']:
        #     component2id = {}
        #     # Insert the phrases from each component of the relationship
        #     for component in {'subj', 'pred', 'obj'}:
        #         phrase_data = relationship[component]
        #         phrase_text = phrase_data['text']
        #         query = 'insert $x isa phrase has text \"{text}\";'.format(text=phrase_text)
        #         response = graph.execute(query)
        #         pprint(response)
        #         phrase_id = response[0]['id']
        #         component2id[component] = phrase_id
        #     # Map the phrases together as entity_phrase_relationship
        #     query = '''
        #         match
        #             $subj id {subj_id};
        #             $pred id {pred_id};
        #             $obj id {obj_id};
        #         insert
        #             (
        #                 subject: $subj,
        #                 predicate: $pred,
        #                 object: $obj
        #             )
        #             isa entity_phrase_relationship;
        #         '''.format(
        #         subj_id=component2id['subj'],
        #         pred_id=component2id['pred'],
        #         obj_id=component2id['obj'],
        #     )
        #     response = graph.execute(query)
        #     pprint(response)
        for directional_assertion in result['directional_assertions']:
            if directional_assertion['level'] == 
            for component in {'antecedent', 'subsequent'}:
                text = directional_assertion[component]['text']
                valence = directional_assertion[component]['valence']
                query = 'insert '
    graph.commit()
