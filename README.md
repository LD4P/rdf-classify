![Python package](https://github.com/LD4P/rdf-classify/workflows/Python%20package/badge.svg)

# Sinopia RDF Classification
Source code and data repository for a [FastAI][FASTAI] project that builds
various models for classifying the Sinopia resource template from an incoming RDF graph
of an entity. A 2020 [presentation](https://ld4p.github.io/classify-rdf-2020/) for
LDP conference goes into more detail.

The **problem** this project attempts to solve is to replace the manually classification that
is now required in Sinopia when importing third-party RDF from sources such as the Library of
Congress [Works][LOC_WORKS] and [Instances][LOC_INSTANCES], [Wikidata][WIKIDATA], or
the Sinopia cohort's converted Share-VDE MARC-to-BIBFRAME RDF. This fine-grained
classification of incoming RDF by Sinopia's existing resource templates.

Open source under the [Apache 2 license](https://www.apache.org/licenses/LICENSE-2.0.txt).
Models and data are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/.
Any rights in individual contents of the database are licensed under the Database
Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

## Older Tensorflow code and documentation
The first iteration of this project attempted to use [TensorFlow][TF]. This
work is availabled in the [`with-tensoflow`](https://github.com/LD4P/rdf-classify/tree/with-tensorflow) branch.


[LOC_INSTANCES]: http://id.loc.gov/ontologies/bibframe.html#c_Instance/
[LOC_WORKS]: http://id.loc.gov/ontologies/bibframe.html#c_Work
[SINOPIA]: https://sinopia.io/
[SINOPIA_DEV]: https://development.sinopia.io/
[SINOPIA_STAGE]: https://stage.sinopia.io/
[WIKIDATA]: https://wikidata.org/

[FASTAI]: https://fastai.io/
[TF]: https://www.tensorflow.org/
