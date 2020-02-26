from rdf_classify import load


class TestLoad:

    def test_uri_to_hash(self):
        uri = "https://sinopia.io/"
        uri_hash = load.uri_to_hash(uri)  # Using default
        print(f"{uri} {uri_hash}")
        # assert uri_hash == [1917, 1900, 1716]

    def test_uri_to_matrix(self):
        uri = "http://a.io/"
        matrix = load.uri_to_matrix(uri)
        assert matrix
