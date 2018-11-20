import os
import json
import primal_grakn as grakn
from pprint import pprint


CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
PATH = os.path.join(DATA_DIR, 'output.json')
KEYSPACE = 'luscient_grakn_demo'


with open(PATH) as f:
    results = json.load(f)


with grakn.Graph(keyspace=KEYSPACE) as graph:
    for result in results:
        for func_rel in result['functional_relationships']['entity_level']:
            concept_ids = {}
            for component in {'antecedent', 'consequent'}:
                named_entity = func_rel[component]['text']
                valence = func_rel[component]['valence']
                # Get or insert the drive-concept
                response = graph.match_or_insert('$driven_concept isa driven-concept has name \"{0}\" has valence \"{1}\";'.format(named_entity, valence))
                ent_id = response[0]['driven_concept']['id']
                concept_ids[component] = ent_id
            # Insert the triggering-relationship
            query = '''
                match
                    $triggering isa driven-concept id {ant_id};
                    $triggered isa driven-concept id {con_id};
                insert
                    $trig_rel
                    (
                        triggering: $triggering,
                        triggered: $triggered
                    )
                    has source-text \"{source_text}\"
                    has source-name \"{source_name}\"
                    has source-id \"{source_id}\"
                    isa triggering-relationship;
            '''.format(
                    ant_id=concept_ids['antecedent'],
                    con_id=concept_ids['consequent'],
                    source_text=result['original_text'],
                    source_name=result['reference']['source'],
                    source_id=result['reference']['id'],
                )
            response = graph.execute(query)

    graph.commit()
