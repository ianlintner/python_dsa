"""Smoke tests for ML, NLP, and NN modules."""


def test_ml_imports():
    """Test that ML modules can be imported."""
    from interview_workbook.ml.linear_regression import LinearRegressionGD

    # Basic functionality test
    X = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
    y = [1.0, 2.0, 3.0]

    lr = LinearRegressionGD(epochs=10)
    lr.fit(X, y)
    predictions = lr.predict([[4.0, 5.0]])
    assert len(predictions) == 1


def test_nlp_imports():
    """Test that NLP modules can be imported."""
    from interview_workbook.nlp.tfidf import TfidfVectorizer
    from interview_workbook.nlp.tokenization import whitespace_tokenize

    # Basic functionality test
    tokens = whitespace_tokenize("hello world")
    assert tokens == ["hello", "world"]

    # TF-IDF test
    docs = [["hello", "world"], ["world", "test"]]
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(docs)
    assert len(vectors) == 2


def test_nn_imports():
    """Test that NN modules can be imported."""
    from interview_workbook.nn.activations import relu, sigmoid, softmax

    # Basic functionality test
    assert relu(1.0) == 1.0
    assert relu(-1.0) == 0.0

    assert 0.0 < sigmoid(1.0) < 1.0

    probs = softmax([1.0, 2.0, 3.0])
    assert abs(sum(probs) - 1.0) < 1e-6
