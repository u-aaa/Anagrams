from sql_app.crud import get_sorted, Anagrams
from sql_app.database import SessionLocal, Dictionary
from sqlalchemy.orm import Session
from typing import Optional

db: Session = SessionLocal()
anagram = Anagrams()


def test_get_sorted():
    a: str = get_sorted('word')
    assert a == 'dorw'


def test_add_words():
    anagram.add_words(words=['camps', 'stats', 'Egyptians'], db=db)
    query: str = "SELECT * from dictionary where word in ('camps', 'stats', 'Egyptians')"
    results: list = db.execute(query).fetchall()
    assert results == [('camps', 'acmps', 5, False), ('Egyptians', 'aeginpsty', 9, True), ('stats', 'asstt', 5, False)]


def test_add_words_negative():
    add_words: bool = anagram.add_words(words=['red camps', 'houses'], db=db)
    assert add_words == False
    query: str = "SELECT * from dictionary where word in ('red camps', 'houses')"
    results: list = db.execute(query).fetchall()
    assert results == []


def test_get_dictionary_stats():
    stats: dict = anagram.get_dictionary_stats(db)
    word_count = len(db.query(Dictionary.word).all())
    assert stats == {'word count': word_count, 'minimum length': 1, 'maximum length': 24, 'median length': 9,
                     'average length': 9.57}


def test_get_anagram_with_noun():
    result: list = anagram.get_anagrams(word='rain', db=db)
    assert result == ["arni", "Iran", "Nair", "rani"]


def test_get_anagram_noun_false():
    result: list = anagram.get_anagrams(word='rain', db=db, noun=False)
    assert result == ["arni","rani"]


def test_get_anagram_with_limit():
    result: list = anagram.get_anagrams(word='rain', db=db, limit=1)
    assert result == ["arni"]


def test_get_max_anagrams():
    result: list = anagram.get_max_anagrams(db=db, limit=2)
    assert result == [{'anagrams': ['angor', 'argon', 'goran', 'grano', 'groan', 'nagor', 'Orang', 'orang', 'organ',
                                    'rogan', 'Ronga'], 'len': 11},
                      {'anagrams': ['asteer', 'Easter', 'easter', 'Eastre', 'reseat', 'saeter', 'seater', 'staree',
                                    'teaser', 'Teresa'], 'len': 10}]


def test_get_max_anagram_without_noun():
    result: list = anagram.get_max_anagrams(db=db, limit=2, noun=False)
    assert result == [{'anagrams': ['caret', 'carte', 'cater', 'crate', 'creat', 'creta', 'react', 'recta', 'trace'],
                       'len': 9},
                      {'anagrams': ['angor', 'argon', 'goran', 'grano', 'groan', 'nagor', 'orang', 'organ', 'rogan'],
                       'len': 9}]


def test_get_anagrams_by_size():
    result: list = anagram.get_anagrams_by_size(size=5, limit = 3, db=db)
    assert result == [{'anagrams': ['arculite', 'Cutleria', 'Lucretia', 'reticula', 'Treculia']},
                      {'anagrams': ['anisometric', 'creationism', 'miscreation', 'ramisection', 'reactionism']},
                      {'anagrams': ['Astilbe', 'astilbe', 'bestial', 'blastie', 'stabile']}]


def test_check_anagrams_positive():
    result: bool = anagram.check_anagrams(['raid', 'arid', 'dari'])
    assert result == True


def test_check_anagrams_negative():
    result: bool = anagram.check_anagrams(['raid', 'arid', 'read'])
    assert result == False


def test_delete_words_and_anagrams():
    anagram.delete_word_and_anagrams(word='raid', db=db)
    result: Optional[Dictionary] = db.query(Dictionary).filter_by(sorted_letters=get_sorted('raid')).all()
    assert result == []


def test_delete_word():
    anagram.delete_word(word='read', db=db)
    result: Optional[Dictionary] = db.query(Dictionary).filter_by(word='read').all()
    assert result == []


def test_delete_all():
    anagram.delete_all(db=db)
    result: Optional[Dictionary] = len(db.query(Dictionary).all())
    assert result == 0
