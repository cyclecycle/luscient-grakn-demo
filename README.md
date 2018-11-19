# luscient-grakn-demo

This repo accompanies the article released [here]().

## Set up

### Requirements

These steps assume you have [Grakn]() running (e.g, with `grakn server start`).

Python requirements are listed in requirements.txt. Install them like:

```bash
pip install -r requirements.txt
```

### Create the graph

Instantiate the schema and rules. This can be done in the bash shell like:

```bash
graql console -k luscient-grakn-demo -f schema.gql
graql console -k luscient-grakn-demo -f rules.gql
```

## Extracting information from text

The 'luscient_api.py' script looks in data/input.json for a list of records, each with data for 'text' and PubMed Central ID ('pmcid').

For each record it will attempt to retrieve results from the [API](http://www.luscient.io/artifact).

The results are stored in data/output.json.

## Inserting into Grakn

The 'insert_to_grakn.py' script takes the results in data/output.json and inserts them into the grakn keyspace named 'luscient-grakn-demo'.

## Querying

The 'ask.py' file is set up to run any query that returns of triggering-relationships with variable name ($triggering_relationship) and create an outcome table (outcome_table.html).

Beyond that, you can explore and query the graph through any of the normal methods of interacting with Grakn.