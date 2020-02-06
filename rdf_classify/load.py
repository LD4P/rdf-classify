"""Loads RDF into Tensorflow Datasets for training and validation using Pandas"""

import datetime
import rdflib
import pandas as pd
import tensorflow as tf

# Module constants
CLASSES = {}
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")

def to_series(graph):
  for row in graph.query(RT_SUBJECTS):
   subject = str(row[0])
   rt_key = str(row[1])
   if not rt_key in CLASSES:
     CLASSES[rt_key] = { subject: [] }
   else:
     CLASSES[rt_key][subject] = []
   for predicate in graph.predicates(subject=row[0]):
     if predicate == SINOPIA.hasResourceTemplate:
       continue
     pred_key = str(predicate)
     CLASSES[rt_key][subject].append(pred_key)
    

def tf_setup(graphs):
  # Using the resource template as the key and as Tensorflow classes
  for graph in graphs:
    to_series(graph)


# SPARQL Queries
RT_SUBJECTS = """SELECT ?subj ?resource_template WHERE {
 ?subj <http://sinopia.io/vocabulary/hasResourceTemplate> ?resource_template
}"""
