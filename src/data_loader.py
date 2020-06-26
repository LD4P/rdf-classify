"""Extracts serialized RDF and loads into one or more graphs"""

import pandas as pd  # type: ignore
import json
import rdflib  # type: ignore
import requests  # type: ignore
from datetime import datetime
from typing import List, Optional
from zipfile import ZipFile

LDP = rdflib.Namespace("http://www.w3.org/ns/ldp#")


def create_tensor(graph: rdflib.Graph, group: str) -> List:
    rt_query = graph.query(SUBJ_RT)
    listing = []
    for subject, rt in rt_query:
        predicates = graph.predicates(subject=subject)
        data = process_predicates(str(subject), predicates, str(rt), group)
        listing.append(data)
    return listing


def predicate_columns(resource_template_group_url: str) -> List:
    properties: List[str] = ['subject', 'resource_template', 'group']
    ld4p_graph = rdflib.Graph()
    ld4p_result = requests.get(resource_template_group_url)
    ld4p_graph.parse(data=ld4p_result.text, format='turtle')
    for rt_url in ld4p_graph.objects(predicate=LDP.contains):
        rt_result = requests.get(str(rt_url))
        if rt_result.status_code > 300:
            print(f"Failed {rt_url} status {rt_result.status_code}")
            continue
        for row in rt_result.json()["propertyTemplates"]:
            property_url = row.get('propertyURI')
            if property_url not in properties:
                properties.append(property_url)
#     with open("properties.json", "w+") as fo:
#         json.dump(properties, fo, indent=2, sort_keys=True)
    return properties


def process_predicates(subject_key: str,
                       predicates: List,
                       resource_template: Optional[rdflib.URIRef],
                       group: str) -> dict:
    data = {'subject': subject_key, 'group': group}
    if resource_template is not None:
        data['resource_template'] = str(resource_template)
    for predicate in predicates:
        pred_key = str(predicate)
        if pred_key in data:
            data[pred_key] += 1  # type: ignore
        else:
            data[pred_key] = 1  # type: ignore

    return data


def to_dataframe(graphs: List[rdflib.Graph], rt_url: str) -> pd.DataFrame:
    """Function takes a list of RDF graphs and a Trellis URL pointing the resource
    templates location
    
    @param graphs -- List of RDF grpahs
    @param rt_url -- Trellis URL to environment's resource templates"""
    start = datetime.utcnow()
    print(f"Starting convert {len(graphs)} to dataframe at {start}")
    raw_data = []
    predicate_cols = predicate_columns(rt_url)
    for i, row in enumerate(graphs):
        graph = row['graph']
        graph.skolemize(authority=f"https://{graph.identifier}.sinopia.io/")
        if not i % 10:
            print(".", end="")
        if not i % 100:
            print(f"{i}", end="")
        subjects = create_tensor(graph, row['group'])
        raw_data.extend(subjects)
    end = datetime.utcnow()
    df = pd.DataFrame(data=raw_data, columns=predicate_cols).fillna(0)
    print(f"Finished at {end} total time {(end-start).seconds / 60.} minutes for dataframe, size {len(df)}")
    return df


def from_zipfile(zip_filepath: str) -> List:
    """Takes a zip filepath, extracts Sinopia RDF files, loading each JSON-LD
    into a rdflib.ConjunctionGraph, returns a list of these graphs.

    @param zip_filepath -- Path to zip files
    """
    graphs = []
    with ZipFile(zip_filepath) as zip_file:
        for zip_info in zip_file.infolist():
            if zip_info.file_size < 1:
                continue
            group = zip_info.filename.split("/")[1].split("_")[0]
            if group.startswith("ld4p"):
                continue
            with zip_file.open(zip_info) as zip_extract:
                raw_data = zip_extract.read()
                graph = rdflib.ConjunctiveGraph()
                try:
                    graph.parse(data=raw_data, format="json-ld")
                    graphs.append({"group": group, "graph": graph})
                except json.JSONDecodeError:
                    print(f"Failed to parse {zip_info.filename}")
                    continue
    return graphs


SUBJ_RT = """PREFIX sinopia: <http://sinopia.io/vocabulary/>
SELECT ?subj ?resource_template
WHERE { ?subj sinopia:hasResourceTemplate ?resource_template }"""
