from rdf_classify import extract


class TestExtract:

    def test_from_zipfile(self):
        assert hasattr(extract, 'from_zipfile')
