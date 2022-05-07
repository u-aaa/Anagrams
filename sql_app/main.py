from fastapi import FastAPI, status, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from sql_app.database import get_db
from sqlalchemy.orm import Session
from sql_app.crud import Anagrams

app = FastAPI()
anagram = Anagrams()


class Words(BaseModel):
    words: list

@app.get('/')
def welcome():
    return 'Welcome to the anagram interface'


@app.get('/dictionary/stats')
def get_dictionary_stats(db: Session = Depends(get_db)):
    return anagram.get_dictionary_stats(db)


@app.get('/anagrams')
def get_list_of_anagrams(size: Optional[int] = None, limit: Optional[int] = 5, noun: bool = True, db: Session = Depends(get_db)):
    '''
    Returns words with the most anagrams if size is not passed.
    Has an optional query param that indicates the maximum number of results to return
    :return: json
    '''
    if size:
        return anagram.get_anagrams_by_size(size=size, limit=limit, noun=noun, db=db)
    return anagram.get_max_anagrams(limit=limit, noun=noun, db=db)


@app.get('/anagrams/{word}.json')
def get_anagrams(word: str, limit: Optional[int] = None, noun: bool = True, db: Session = Depends(get_db)):
    '''
    Returns a JSON array of English-language words that are anagrams of the word passed
    Has an optional query param that indicates the maximum number of results to return
    :return: json
    '''
    if word:
        anagram_list: list = anagram.get_anagrams(word=word, db=db, limit=limit, noun=noun)
        return {'anagrams': anagram_list}

@app.post('/anagrams')
def check_anagrams(words: Words):
    if words.words:
        check = anagram.check_anagrams(words.words)
        return check


@app.post('/words.json', status_code=status.HTTP_201_CREATED)
def add_words(word_list: Words, db: Session = Depends(get_db)):
    '''
    Takes a JSON array of English-language words and adds them to the dictionary.
    :return: None
    '''
    if word_list.words:
        add_words = anagram.add_words(word_list.words, db)
        if add_words is False:
            raise HTTPException(status_code=400, detail="Cannot add phrase to dictionary")
    return None


@app.delete('/words.json', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_words(db: Session = Depends(get_db)):
    '''
    Deletes all words from the dictionary
    :return:
    '''
    return anagram.delete_all(db)


@app.delete('/words/{word}.json', status_code=status.HTTP_204_NO_CONTENT)
def delete_word(word: str, db: Session = Depends(get_db)):
    '''
    Deletes a word from the dictionary
    :return:
    '''
    if word:
        anagram.delete_word(word=word, db=db)
    return None


@app.delete('/anagrams/{word}.json', status_code=status.HTTP_204_NO_CONTENT)
def delete_word_with_anagrams(word: str, db: Session = Depends(get_db)):
    if word:
        anagram.delete_word_and_anagrams(word=word, db=db)
    return None
