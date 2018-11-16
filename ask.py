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
    pprint(response)
    func_rels = []
    for item in response:
        roles = {}
        for key, values in item.items():
            # print(key, values)
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

