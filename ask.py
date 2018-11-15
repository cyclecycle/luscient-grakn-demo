import os
import pygrakn.pygrakn as grakn
from pprint import pprint
import markdown


CWD = os.path.abspath(os.path.dirname(__file__))
QUERY_DIR = os.path.join(CWD, 'queries')
KEYSPACE = 'bft4'


def func_rels_to_table(results):
    def valence_to_arrow(valence):
        if valence == 'UP':
            return '&uarr;'
        return '&darr;'
    md = '| Antecedent | Consequent |\n|---|---|'
    for item in results:
        md += '\n| {0} {1}| {2} {3} |'.format(
            valence_to_arrow(item['antecedent']['valence']),
            item['antecedent']['text'],
            valence_to_arrow(item['consequent']['valence']),
            item['consequent']['text'],
        )
    html = markdown.markdown(md, extensions=['markdown.extensions.tables'])
    return html


with grakn.Graph(keyspace=KEYSPACE) as graph:
    # query_file = os.path.join(QUERY_DIR, 'consequences_of_bft_increase.gql')
    # query_file = os.path.join(QUERY_DIR, 'paths_to_ros.gql')
    query_file = os.path.join(QUERY_DIR, 'bft_to_cancer.gql')
    response = graph.execute(query_file, from_file=True)
    func_rels = []
    for item in response:
        roles = {}
        for key, values in item.items():
            explanation = values['explanation']
            for answer in explanation.get_answers():
                nested_explanation = answer.explanation()
                print(nested_explanation.query_pattern())
                print()
                print()
                nested_answers = nested_explanation.get_answers()
                if nested_answers:
                    for answer in nested_answers:
                        for k1, v2 in answer.map().items():
                            # print(k1, v2)
                            v2 = graph.parse_concept(v2)
                            if v2['type'] == 'triggering-relationship':
                                pprint(v2)
                            # pprint(v2)
                        # print(answer.map())
                        print()
                        print()
                map_ = answer.map()
                # pprint(map_)
                # for k, v in map_.items():
                    # print(k, v)
                    # if k == 'trig_rel':
                    #     print(v.is_inferred())
                    #     print(dir(v))
                        # pprint(graph.parse_concept(v))
                # print()
                # if 'func_rel' in map_:
                #     rel = map_['func_rel']
                #     ant = map_['ant']
                #     parsed = graph.parse_concept(ant)
                #     pprint(parsed)
            raise
                    # print(v1)
                    # print(dir(v1))
                    # if 'func_rel' in v1:
                    #     print(v1)
                # print(answer.explanation().get_answers())
            # print(explanation.query_pattern())
            # for concept_map in explanation:
            #     print(dir(concept_map))
                # print(dir(answer))
                # print(answer.query_pattern())
                # print(concept_map.map())
                # print(concept_map.explanation().get_answers())
            raise
            for drive_change in values['relates']:
                role = drive_change['role']['label']
                ent_name = drive_change['player']['relates'][0]['player']['attributes'][0]['value']
                valence = drive_change['player']['attributes'][0]['value']
                roles[role] = {'text': ent_name, 'valence': valence}
        func_rels.append(roles)
    # pprint(func_rels)
    html = func_rels_to_table(func_rels)
    with open('results.html', 'w', encoding='utf-8') as file:
        file.write(html)


# def create_consequences_table(results):
#     html = '''
#         <table>
#             <th>
#                 <td>Consequence</td>
#                 <td>Premise</td>
#             </th>
#             <tr>
#                 <td></td>
#                 <td>
#                     <
#                 </td>
#             </tr>
#         </table>
#     '''
#     for item in results:

