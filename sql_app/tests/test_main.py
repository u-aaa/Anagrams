from fastapi.testclient import TestClient
from sql_app.main import app


client = TestClient(app)


def test_get_anagrams():
    response = client.get('/anagrams/read.json')
    assert response.status_code == 200
    assert response.json() == {"anagrams": ["ared", "daer", "dare", "dear"]}


def test_get_anagrams_with_limit():
    response = client.get('/anagrams/read.json?limit=2')
    assert response.status_code == 200
    assert response.json() == {"anagrams": ["ared", "daer"]}


def test_get_anagrams_with_limit_negative():
    response = client.get('/anagrams/read.json?limit=two')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['query', 'limit'],
                                           'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}


def test_get_words_with_most_anagrams():
    response = client.get('/anagrams')
    assert response.status_code == 200
    assert response.json() == [{"anagrams": ["angor", "argon", "goran", "grano", "groan", "nagor", "Orang", "orang",
                                             "organ", "rogan", "Ronga"], "len": 11}, {
                                   "anagrams": ["asteer", "Easter", "easter", "Eastre", "reseat", "saeter", "seater",
                                                "staree", "teaser", "Teresa"], "len": 10}, {
                                   "anagrams": ["Elaps", "lapse", "Lepas", "Pales", "salep", "saple", "sepal", "slape",
                                                "spale", "speal"], "len": 10}, {
                                   "anagrams": ["armet", "mater", "Merat", "metra", "ramet", "tamer", "terma", "trame",
                                                "Trema"], "len": 9}, {
                                   "anagrams": ["caret", "carte", "cater", "crate", "creat", "creta", "react", "recta",
                                                "trace"], "len": 9}]


def test_get_words_with_most_anagrams_with_limit():
    response = client.get('/anagrams?limit=1')
    assert response.status_code == 200
    assert response.json() == [{"anagrams": ["angor", "argon", "goran", "grano", "groan", "nagor", "Orang", "orang",
                                             "organ", "rogan", "Ronga"], "len": 11}]


def test_get_anagrams_by_size():
    response = client.get('/anagrams?size=3&limit=2')
    assert response.status_code == 200
    assert response.json() == [{"anagrams": ["amnion", "Minoan", "nomina"]},
                               {"anagrams": ["bedust", "bestud", "busted"]}]


def test_get_dictionary_stats():
    response = client.get('/dictionary/stats')
    assert response.status_code == 200
    assert response.json() == {"word count": 235886, "minimum length": 1, "maximum length": 24, "median length": 9.0,
                               "average length": 9.57}


def test_add_words():
    response = client.post('/words.json', json={"words": ["cats", "hands"]})
    assert response.status_code == 201
    assert response.json() == None


def test_check_anagrams_positive():
    response = client.post('/anagrams', json={"words": ["astilbe", "astilbe", "bestial", "blastie"]})
    assert response.status_code == 200
    assert response.json() == True


def test_check_anagrams_negative():
    response = client.post('/anagrams', json={"words": ["astilbe", "astilbe", "bells", "blastie"]})
    assert response.status_code == 200
    assert response.json() == False


def test_delete_word():
    response = client.delete('/words/read.json')
    assert response.status_code == 204
    assert response.json() is None


def test_delete_word_with_anagrams():
    response = client.delete('/anagrams/{word}.json')
    assert response.status_code == 204
    assert response.json() is None


def test_delete_all_words():
    response = client.delete('/words.json')
    assert response.status_code == 204
    assert response.json() is None
