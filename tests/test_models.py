from rdf_classify import model


class TestModel:
    def test_fastforward(self):
        basic_model = model.compile_feedforward(10)
        print(basic_model)
        assert 1
