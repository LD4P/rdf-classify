__author__ = "Jeremy Nelson"

from rdf_classify import load


class TestLoad:
    def test_uri_to_hash(self):
        uri = "https://sinopia.io/"
        uri_hash = load.uri_to_hash(uri)  # Using default
        assert uri_hash == [1383, 1531, 1399]

    def test_uri_to_matrix(self):
        uri = "http://a.io/"
        matrix = load.uri_to_matrix(uri)
        assert matrix[0][33] == 1.0
        assert matrix[0][22] == 0.0
        assert matrix[1][45] == 1.0
        assert matrix[2][45] == 1.0
        assert matrix[3][41] == 1.0
        assert matrix[4][66] == 1.0
