import requests
import os
import json
from pprint import pprint

CWD = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(CWD, 'data')
INFILE = os.path.join(DATA_DIR, 'input.json')
OUTFILE = os.path.join(DATA_DIR, 'output.json')
API_URL = 'http://www.luscient.io/api'


def process(text):
    print(text)
    r = requests.post(API_URL, json={'text': text})
    if not r.status_code == 400:
        result = r.json()
        return result
    print('Something went wrong. API returned:\n\n{}'.format(r.text))
    return None


results = []
with open(INFILE, 'rb') as f:
    input_ = json.load(f)
    for item in input_:
        response = process(item['text'])
        if response:
            response['reference'] = {
                'source': 'PMC',
                'id': item['pmcid']
            }
            results.append(response)


with open(OUTFILE, 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
