"""Extracts serialized RDF and loads into one or more graphs"""

import json
import rdflib  # type: ignore
from zipfile import ZipFile


def from_zipfile(zip_filepath: str, exclude: list = [str]) -> list:
    """Takes a zip filepath, extracts Sinopia RDF files, loading each JSON-LD
    into a rdflib.ConjunctionGraph, returns a list of these graphs.

    @param zip_filepath -- Path to zip files
    @param excludes -- Directory of file patterns to match on the zip file.
                       Used to filter out non-RDF payloads.
    """
    graphs = []
    with ZipFile(zip_filepath) as zip_file:
        for zip_info in zip_file.infolist():
            if zip_info.file_size < 1:
                continue
            if zip_info.filename.split("/")[1] in exclude:
                continue
            with zip_file.open(zip_info) as zip_extract:
                graph = rdflib.ConjunctiveGraph()
                raw_rdf = zip_extract.read()
                try:
                    graph.parse(data=raw_rdf, format="json-ld")
                    graphs.append(graph)
                except json.JSONDecodeError:
                    print(f"Failed to parse {zip_info.filename}")
                    continue
    return graphs
