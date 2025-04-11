from hindi_stopwords import filter_stopwords

def test_remove_stopwords():
    assert filter_stopwords("मैं और तुम") == "मैं तुम"
