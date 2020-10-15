"""Extracts serialized RDF and loads into one or more graphs"""

import pandas as pd  # type: ignore
import json
import rdflib  # type: ignore
import requests  # type: ignore
from datetime import datetime
from typing import Dict, List, Optional
from zipfile import ZipFile

LDP = rdflib.Namespace("http://www.w3.org/ns/ldp#")
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")


def create_tensor(graph: rdflib.Graph, group: str) -> List:
    rt_query = graph.query(SUBJ_RT)
    listing = []
    for subject, rt in rt_query:
        predicates = graph.predicates(subject=subject)
        data = process_predicates(str(subject), predicates, str(rt), group)
        listing.append(data)
    return listing


def predicate_columns(resource_template_group_url: str) -> List:
    properties: List[str] = ["subject", "resource_template", "group"]
    ld4p_graph = rdflib.Graph()
    ld4p_result = requests.get(resource_template_group_url)
    ld4p_graph.parse(data=ld4p_result.text, format="turtle")
    for rt_url in ld4p_graph.objects(predicate=LDP.contains):
        rt_result = requests.get(str(rt_url))
        if rt_result.status_code > 300:
            print(f"Failed {rt_url} status {rt_result.status_code}")
            continue
        for row in rt_result.json()["propertyTemplates"]:
            property_url = row.get("propertyURI")
            if property_url not in properties:
                properties.append(property_url)
    return properties


def process_predicates(
    subject_key: str,
    predicates: List,
    resource_template: Optional[rdflib.URIRef],
    group: str,
) -> dict:
    data = {"subject": subject_key, "group": group}
    if resource_template is not None:
        data["resource_template"] = str(resource_template)
    for predicate in predicates:
        pred_key = str(predicate)
        if pred_key in data:
            data[pred_key] += 1  # type: ignore
        else:
            data[pred_key] = 1  # type: ignore

    return data


def to_dataframe(graphs: List[dict], rt_url: str) -> pd.DataFrame:
    """Function takes a list of RDF graphs and a Trellis URL pointing the resource
    templates location

    @param graphs -- List of dictionaries with graph and group keys
    @param rt_url -- Trellis URL to environment's resource templates"""
    start = datetime.utcnow()
    print(f"Starting convert {len(graphs)} to dataframe at {start}")
    raw_data = []
    predicate_cols = predicate_columns(rt_url)
    for i, row in enumerate(graphs):
        graph = row["graph"]
        if not i % 10:
            print(".", end="")
        if not i % 100:
            print(f"{i}", end="")
        subjects = create_tensor(graph, row["group"])
        raw_data.extend(subjects)
    end = datetime.utcnow()
    df = pd.DataFrame(data=raw_data, columns=predicate_cols)
    df = df.fillna(0).sample(frac=1).reset_index(drop=True)
    print(
        f"""
    Finished at {end} time {(end-start).seconds / 60.} minutes for dataframe,
    size {len(df)}"""
    )
    return df


def from_api(api_url: str) -> Dict:
    """Takes the new Sinopia API endpoint URI, extracts each resource and
    template, and returns a dictionary with two lists, a resources and a
    templates, and the total number of resources harvested from the api.

    @param api_url -- URI to Sinopia API endpoint
    """

    def add_resource(resource):
        output["total"] += 1
        graph = rdflib.Graph()
        graph.namespace_manager.bind("sinopia", SINOPIA)
        jsonld = json.dumps(resource.pop("data")).encode()
        graph.parse(data=jsonld, format="json-ld")
        payload = {"graph": graph, "meta": resource}
        if "sinopia:template:resource" in resource.get("templateId"):
            output["templates"].append(payload)
        else:
            output["resources"].append(payload)

    output = {"resources": [], "templates": [], "total": 0}
    start = datetime.utcnow()
    print(f"Started harvest of resources at {start} for {api_url}")
    initial = requests.get(f"{api_url}/resource")
    print("0", end="")
    for row in initial.json().get("data"):
        add_resource(row)
    next_link = initial.json().get("links").get("next")
    while 1:
        result = requests.get(next_link)
        if result.status_code > 300:
            break
        payload = result.json()
        new_next = payload.get("links").get("next")
        if new_next == next_link or new_next is None:
            break
        for row in payload.get("data"):
            add_resource(row)
        next_link = new_next
        print(".", end="")
        if not output["total"] % 250:
            print(f"{output['total']}", end="")
    end = datetime.utcnow()
    print(f"\nFinished at {end}, total time {(end-start).seconds / 60.}")
    return output


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
                    authority = f"https://{graph.identifier}.sinopia.io/"
                    graph.skolemize(authority=authority)
                    graphs.append({"group": group, "graph": graph})
                except json.JSONDecodeError:
                    print(f"Failed to parse {zip_info.filename}")
                    continue
    return graphs


SUBJ_RT = """PREFIX sinopia: <http://sinopia.io/vocabulary/>
SELECT ?subj ?resource_template
WHERE { ?subj sinopia:hasResourceTemplate ?resource_template }"""
