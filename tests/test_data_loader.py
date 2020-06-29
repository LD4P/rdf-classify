import rdflib  # type: ignore
import responses  # type: ignore
import unittest
from src import data_loader


class TestExtract(unittest.TestCase):

    def test_from_zipfile(self):
        assert hasattr(data_loader, "from_zipfile")


class TestCreateTensor(unittest.TestCase):

    def test_empty_graph(self):
        empty_graph = rdflib.Graph()
        self.assertEqual(data_loader.create_tensor(empty_graph, 'pcc'), [])


class TestPredicateColumns(unittest.TestCase):

    def setUp(self):
        self.TRELLIS_URI = 'https://trellis.sinopia.io/repository/ld4p'

    @responses.activate
    def test_default_predicate_columns(self):
        responses.add(responses.GET,
                      self.TRELLIS_URI,
                      body="",
                      content_type="text/turtle",
                      status=200)
        properties = data_loader.predicate_columns(
            self.TRELLIS_URI)
        self.assertEqual(len(properties), 3)
        self.assertEqual(properties, ['subject', 'resource_template', 'group'])
