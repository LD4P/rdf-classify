from rdf_classify import data_loader


class TestExtract:
    def test_from_zipfile(self):
        assert hasattr(data_loader, "from_zipfile")
