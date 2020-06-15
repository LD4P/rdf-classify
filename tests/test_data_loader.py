import rdflib
import unittest
from unittest import mock
from src import data_loader


class TestExtract(unittest.TestCase):

    def test_from_zipfile(self):
        assert hasattr(data_loader, "from_zipfile")


class TestCreateTensor(unittest.TestCase):

    def test_empty_graph(self):
        empty_graph = rdflib.Graph()
        self.assertEqual(data_loader.create_tensor(empty_graph), [])



def mocked_ld4p_get(url):

    def text():
        return

    if url.startswith('https://trellis.sinopia.io/repository/ld4p'):
        return

class TestPredicateColumns(unittest.TestCase):

    @mock.patch('data_loader.predicate_columns.requests.get', side_effect=mocked_ld4p_get)
    def test_predicate_columns(self):
        properties = data_loader.predicate_columns('https://trellis.sinopia.io/repository/ld4p')
        self.assertEqual(len(properties), 5)
