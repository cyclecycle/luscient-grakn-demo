# luscient-grakn-demo

This repo accompanies the article titled "Biomedical Fact Extraction and Reasoning - Knowledge Graphs from Scientific Text".

## Set up

### Requirements

These steps assume you have [Grakn]() running (e.g, with `grakn server start`).

Python requirements are listed in requirements.txt. Install them with:

```bash
pip install -r requirements.txt
```

### Create the graph

Instantiate the schema and rules. This can be done in the bash shell like:

```bash
graql console -k luscient_grakn_demo -f schema.gql
graql console -k luscient_grakn_demo -f rules.gql
```

## Extracting information from text

The 'luscient_api.py' script looks in data/input.json for a list of records, each with data for 'text' and PubMed Central ID ('pmcid').

You can replace these records with your own.

For each record it will attempt to retrieve results from the [API](http://www.luscient.io/artifact).

The results are stored in data/output.json.

## Inserting into Grakn

The 'insert_to_grakn.py' script takes the results in data/output.json and inserts them into the grakn keyspace named 'luscient_grakn_demo'.

## Querying

The 'ask.py' file is set up to run any query that returns triggering-relationships with variable name '$triggering_relationship' (like any of the queries in /queries folder) and create an outcome table like that shown in the article (outcome_table.html).

You can change the code to point to a different .gql query file.

Beyond that, you can explore and query the graph through any of the normal methods of interacting with Grakn.