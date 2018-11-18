import os
import json
import primal_grakn.primal_grakn as grakn
from pprint import pprint


CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
PATH = os.path.join(DATA_DIR, 'output.json')
KEYSPACE = 'bft5'


with open(PATH) as f:
    results = json.load(f)


with grakn.Graph(keyspace=KEYSPACE) as graph:
    for result in results:
        # Insert the source
        query = '''
            insert
                $source isa source
                    has text \"{text}\",
                    has source_name \"{source_name}\",
                    has source_id \"{source_id}\";
        '''.format(
                text=result['original_text'],
                source_name=result['reference']['source'],
                source_id=result['reference']['id'],
            )
        response = graph.execute(query)
        source_id = [x for x in response if 'source' in x][0]['source']['id']

        for func_rel in result['functional_relationships']['entity_level']:
            concept_ids = {}
            for component in {'antecedent', 'consequent'}:
                named_entity = func_rel[component]['text']
                valence = func_rel[component]['valence']
                # Get the named_entity if it already exists
                response = graph.match_or_insert('$driven_concept isa driven-concept has name \"{0}\" has valence \"{1}\";'.format(named_entity, valence))
                ent_id = response[0]['driven_concept']['id']
                concept_ids[component] = ent_id
            # Insert the functional relationship
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
                    isa triggering-relationship;
            '''.format(
                    ant_id=concept_ids['antecedent'],
                    con_id=concept_ids['consequent'],
                )
            response = graph.execute(query)
            trig_rel_id = [x for x in response if 'trig_rel' in x][0]['trig_rel']['id']
            # Insert the derivation relationship
            query = '''
                match
                    $derived isa triggering-relationship id {0};
                    $source isa source id {1};
                insert
                    $derivation
                        (
                            derived: $derived,
                            reference: $source
                        )
                    isa derivation;
            '''.format(
                    trig_rel_id,
                    source_id,
                )
            response = graph.execute(query)

    graph.commit()
