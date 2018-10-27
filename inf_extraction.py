import requests
import os
import json
from pprint import pprint

CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')

API_URL = 'http://localhost:5000/api'

'''TODO

implement acronym and coref resolution on API side
    run relex on coref resolved, but 
named ent annotation with becas
API handling whole docs
    gives sent idx, chunk idx, token idx of components

'''

def process(text):
    text = str(text)
    print(text)
    r = requests.post(
        API_URL, 
        json={
            'text': text,
            'named_entities': True,
            'detect_valence': True,
            'directional_assertions': True,
        },
    )
    result = r.json()
    # Check for error
    return result


results = []
for fp in os.scandir(os.path.join(DATA_DIR, 'colorectal_cancer')):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
        result = process(content)
        results.append(result)


print(results)
with open(os.path.join(DATA_DIR, 'processed/inf.json'), 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
