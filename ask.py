import os
import primal_grakn.primal_grakn as grakn
from pprint import pprint
import markdown


CWD = os.path.abspath(os.path.dirname(__file__))
QUERY_DIR = os.path.join(CWD, 'queries')
KEYSPACE = 'bft5'


def valence_to_arrow(valence):
    if valence == 'UP':
        return '&uarr;'
    return '&darr;'


def func_rels_to_table(results):
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


def sort_explanation(flat_explanation):
    # the fact we want to explain appears with the key from the query
    to_explain = [x for x in flat_explanation if 'trig_rel' in x][0]['trig_rel']
    if not to_explain.object.is_inferred():
        return [to_explain]  # Fact is the explanation of itself
    # Get the start point and end point ids
    start_point = to_explain['triggering']['id']
    end_point = to_explain['triggered']['id']
    # Only want keys 'rel' and 'rel2' for our explanation
    flat_explanation = [x for x in flat_explanation if any([k in x for k in {'rel', 'rel2'}])]
    # Go through each relationship until we've found all ids to connect our start point to our end point
    order = []
    id_to_find = start_point
    while id_to_find != end_point:
        for i, item in enumerate(flat_explanation):
            data = list(item.values())[0]
            # Find if our id is the triggering id
            is_next_rel = False
            if data['triggering']['id'] == id_to_find:
                # If it is, then add it to the order
                order.append(i)
                id_to_find = data['triggered']['id']
    # Create ordered list of facts
    results = []
    for i in order:
        results.append(list(flat_explanation[i].values())[0])
    return results


def create_consequences_table(results):
    html = '''<tr>
<td rowspan="2"><b>Consequence</b></td>
<td colspan="2" align="center"><b>Premise</b></td>
</tr>
<tr>
<td align="center"><b>Relationship</b></td>
<td align="center"><b>Source</b></td>
</tr>
'''
    # for item in results:
    for item in results:
        row = '<tr>'
        name = item['triggered']['name']['value']
        arrow = valence_to_arrow(item['triggered']['valence']['value'])
        row += '\n<td rowspan=\"{0}\">{1} {2}</td>'.format(len(item['explanation']), arrow, name)
        row += '\n{0}\n</tr>'
        for i, fact in enumerate(item['explanation']):
            td = '<td>{0} {1} &rarr; {2} {3}</td>\n<td>{4}</td>'
            td = td.format(
                valence_to_arrow(fact['triggering']['valence']['value']),
                fact['triggering']['name']['value'],
                valence_to_arrow(fact['triggered']['valence']['value']),
                fact['triggered']['name']['value'],
                'SOURCE'
            )
            if i == 0:
                row = row.format(td)
                html += row
            else:
                row = '\n<tr>\n{}\n</tr>'.format(td)
                html += row
    html = '<table>\n' + html + '\n</table>'
    print(html)
    return html


with grakn.Graph(keyspace=KEYSPACE) as graph:
    # query_file = os.path.join(QUERY_DIR, 'consequences_of_bft_increase.gql')
    # query_file = os.path.join(QUERY_DIR, 'paths_to_ros.gql')
    # query_file = os.path.join(QUERY_DIR, 'bft_to_cancer.gql')
    query_file = os.path.join(QUERY_DIR, 'bft_to_cancer_with_source.gql')
    concept_maps = graph.execute(query_file, from_file=True)
    pprint(concept_maps)
    raise
    # pprint(concept_maps)
    results = []
    for concept_map in concept_maps:
        # pprint(concept_map)
        # raise
        # pprint(concept_map.flat_explanation)
        sorted_facts = sort_explanation(concept_map.flat_explanation)
        pprint(sorted_facts)
        concept_map['trig_rel']['explanation'] = sorted_facts
        results.append(concept_map['trig_rel'])
    # pprint(results)
    html = create_consequences_table(results)
