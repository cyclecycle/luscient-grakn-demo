import os
import json
import pygrakn.pygrakn as grakn
from pprint import pprint


CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
PATH = os.path.join(DATA_DIR, 'output.json')
KEYSPACE = 'test'


with open(PATH) as f:
    results = json.load(f)


with grakn.Graph(keyspace=KEYSPACE) as graph:
    for result in results:
        for func_rels in result['functional_relationships']['entity_level']:
            # First insert the drive_change event for each side of the functional relationship
            drive_change_ids = {}
            for component in {'antecedent', 'consequent'}:
                named_entity = func_rels[component]['text']
                valence = func_rels[component]['valence']
                # Get the named_entity if it already exists
                response = graph.match_or_insert('$named_entity isa named_entity has name \"{}\"'.format(named_entity))
                ent_id = response[0]['id']
                # Match or insert the drive_change event
                query = '''
                    match
                        $drive_change
                            (changed: $named_entity)
                            isa drive_change
                            has valence \"{valence}\";
                        $named_entity id {ent_id};
                    get $drive_change;
                '''.format(ent_id=ent_id, valence=valence)
                response = graph.execute(query)
                if not response:
                    query = '''
                        match
                            $named_entity isa named_entity id {ent_id};
                        insert
                            $drive_change
                                (changed: $named_entity)
                                isa drive_change
                                has valence \"{valence}\";
                    '''.format(ent_id=ent_id, valence=valence)
                    response = graph.execute(query)
                for item in response:
                    if item['type'] == 'drive_change':
                        drive_change_ids[component] = item['id']
            # Insert the functional relatinship
            query = '''
                match
                    $antecedent isa drive_change id {ant_id};
                    $consequent isa drive_change id {con_id};
                insert
                    $func_rel
                    (
                        antecedent: $antecedent,
                        consequent: $consequent
                    )
                    isa functional_relationship;
            '''.format(
                    ant_id=drive_change_ids['antecedent'],
                    con_id=drive_change_ids['consequent'],
                )
            response = graph.execute(query)
            pprint(response)

    graph.commit()
