"""Loads RDF into Pandas and Tensorflow"""

from typing import Any, Dict
import pandas as pd
import numpy as np  # type: ignore
import rdflib  # type: ignore
import tensorflow.keras as keras  # type: ignore
from mypy import List

# Module constants
CLASSES: Dict[Any, Any] = {}
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")
# For now restrictive subset, need to look at the full Unicode
VALID_URL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="  # noqa: E501
# see https://serpstat.com/blog/how-long-should-be-the-page-url-length-for-seo/
MAXLEN = 2048


def uri_to_hash(uri: str, maxlen: int = MAXLEN) -> str:
    uri_hash = keras.preprocessing.text.hashing_trick(uri,
                                                      maxlen,
                                                      hash_function="md5")
    return uri_hash


def uri_to_matrix(uri: str) -> list:
    matrix = []
    for char in uri:
        position = VALID_URL.find(char)
        if position < 0:
            continue  # Ignore for now
        vector = np.zeros(len(VALID_URL))
        vector[position] = 1.0
        matrix.append(vector)
    return matrix


def to_series(graph: rdflib.ConjunctiveGraph):
    for row in graph.query(RT_SUBJECTS):
        subject = str(row[0])
        rt_key = str(row[1])
        if rt_key not in CLASSES:
            CLASSES[rt_key] = {subject: []}
        else:
            CLASSES[rt_key][subject] = []
        for predicate in graph.predicates(subject=row[0]):
            if predicate == SINOPIA.hasResourceTemplate:
                continue
            pred_matrix = uri_to_matrix(str(predicate))
            CLASSES[rt_key][subject].append(pred_matrix)


def subject_to_str(subject):
    if isinstance(subject, rdflib.BNode):
        subject = subject.skolemize(
            authority='https://trellis.stage.sinopia.io/repository/')
    return str(subject)


def to_dataframe(graphs: List[rdflib.Graph]) -> pd.DataFrame:
    raw_data = []
    for i, graph in enumerate(graphs):
        if not i % 10:
            print(".", end="")
        if not i % 100:
            print(f"{i}", end="")
        rt_query = graph.query(RT_SUBJECTS)
        for subj, rt in rt_query:
            subject = {'subject': subject_to_str(subj),
                       'resource_template': str(rt)}
            for predicate in graph.predicates(subject=subj):
                pred_str = str(predicate)
                if pred_str in subject:
                    subject[pred_str] += 1
                else:
                    subject[pred_str] = 1
            raw_data.append(subject)
    return pd.DataFrame(data=raw_data)


def tf_setup(graphs: list):
    # Using the resource template as the key and as Tensorflow classes
    for graph in graphs:
        to_series(graph)


# SPARQL Queries
RT_SUBJECTS = """SELECT ?subj ?resource_template WHERE {
 ?subj <http://sinopia.io/vocabulary/hasResourceTemplate> ?resource_template
}"""
