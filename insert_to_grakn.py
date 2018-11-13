import os
import json
import pygrakn.pygrakn as grakn
from pprint import pprint


CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
PATH = os.path.join(DATA_DIR, 'output.json')
KEYSPACE = 'bft'


with open(PATH) as f:
    results = json.load(f)


with grakn.Graph(keyspace=KEYSPACE) as graph:
    for result in results:
        for relationship in result['entity_phrase_relationships']:
            component2id = {}
            # Insert the phrases from each component of the relationship
            for component in {'subj', 'pred', 'obj'}:
                phrase_data = relationship[component]
                phrase_text = phrase_data['text']
                query = '$x isa phrase has text \"{text}\";'.format(text=phrase_text)
                response = graph.match_or_insert(query)
                phrase_id = response[0]['id']
                component2id[component] = phrase_id
            # Map the phrases together as entity_phrase_relationship
            query = '''
                match
                    $subj id {subj_id};
                    $pred id {pred_id};
                    $obj id {obj_id};
                insert
                    $epr
                        (
                            subject: $subj,
                            predicate: $pred,
                            object: $obj
                        )
                    isa entity_phrase_relationship;
                '''.format(
                subj_id=component2id['subj'],
                pred_id=component2id['pred'],
                obj_id=component2id['obj'],
            )
            response = graph.execute(query)
        #     pprint(response)
    for result in results:
        for func_rels in result['functional_relationships']['entity_level']:
            # First insert the drive_change event for each side of the dynamic association
            drive_change_ids = {}
            for component in {'antecedent', 'consequent'}:
                ent_name = func_rels[component]['text']
                valence = func_rels[component]['valence']
                # Get the ent if it already exists
                response = graph.match_or_insert('$ent isa named_entity has name \"{}\"'.format(
                    ent_name))
                ent_id = response[0]['id']
                # Match or insert the drive_change event
                query = '''
                    match
                        $drive_change
                            (changed: $named_ent)
                            isa drive_change
                            has valence \"{valence}\";
                        $named_ent id {ent_id};
                    get $drive_change;
                '''.format(ent_id=ent_id, valence=valence)
                response = graph.execute(query)
                if not response:
                    query = '''
                        match
                            $named_ent isa named_entity id {ent_id};
                        insert
                            $drive_change
                                (changed: $named_ent)
                                isa drive_change
                                has valence \"{valence}\";
                    '''.format(ent_id=ent_id, valence=valence)
                    response = graph.execute(query)
                for item in response:
                    if item['type'] == 'drive_change':
                        drive_change_ids[component] = item['id']
                # Create the opposite drive change is doesn't exist. This is for use in the converse inference rules
                if valence == 'UP':
                    valence_conv = 'DOWN'
                elif valence == 'DOWN':
                    valence_conv = 'UP'
                query = '''
                    match
                        $drive_change
                            (changed: $named_ent)
                            isa drive_change
                            has valence \"{valence}\";
                        $named_ent id {ent_id};
                    get $drive_change;
                '''.format(ent_id=ent_id, valence=valence_conv)
                response = graph.execute(query)
                if not response:
                    query = '''
                        match
                            $named_ent isa named_entity id {ent_id};
                        insert
                            $drive_change
                                (changed: $named_ent)
                                isa drive_change
                                has valence \"{valence}\";
                    '''.format(ent_id=ent_id, valence=valence_conv)
                    response = graph.execute(query)
                # pprint(response)
            # Create the dynamic association
            query = '''
                match
                    $antecedent isa drive_change id {ant_id};
                    $consequent isa drive_change id {con_id};
                insert
                    $dynamic_association
                    (
                        antecedent: $antecedent,
                        consequent: $consequent
                    )
                    isa drive_change_relationship;
            '''.format(
                    ant_id=drive_change_ids['antecedent'],
                    con_id=drive_change_ids['consequent'],
                )
            response = graph.execute(query)
            pprint(response)
    # For each ent, create the opposite drive change, for use in converse inference

    graph.commit()
