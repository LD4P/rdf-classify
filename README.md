![Python package](https://github.com/LD4P/rdf-classify/workflows/Python%20package/badge.svg)

# Sinopia RDF Classification
Source code and data repository for a [Tensorflow][TF] project that builds
various models for classifying the Sinopia resource template from an incoming RDF graph
of an entity.

The **problem** this project attempts to solve is to replace the manually classification that
is now required in Sinopia when importing third-party RDF from sources such as the Library of
Congress [Works][LOC_WORKS] and [Instances][LOC_INSTANCES], [Wikidata][WIKIDATA], or
the Sinopia cohort's converted Share-VDE MARC-to-BIBFRAME RDF.

Open source under the [Apache 2 license](https://www.apache.org/licenses/LICENSE-2.0.txt).
Models and data are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/.
Any rights in individual contents of the database are licensed under the Database
Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

## Training and Validation Data
Catalogers using Sinopia's linked-data editor in a [development][SINOPIA_DEV],
[stage][SINOPIA_STAGE], or in [production][SINOPIA] environments construct RDF
entities based on rules specified in one or more resource templates.

## Keras Models

## Predicting RDF's Resource Template with TensorFlow

[LOC_INSTANCES]: http://id.loc.gov/ontologies/bibframe.html#c_Instance/
[LOC_WORKS]: http://id.loc.gov/ontologies/bibframe.html#c_Work
[SINOPIA]: https://sinopia.io/
[SINOPIA_DEV]: https://development.sinopia.io/
[SINOPIA_STAGE]: https://stage.sinopia.io/
[WIKIDATA]: https://wikidata.org/

[TF]: https://www.tensorflow.org/
