from sqlalchemy.orm import Session
from sql_app.database import Dictionary, Base
from typing import Optional
from statistics import median, mean
from collections.abc import Iterable


def get_sorted(word: str):
    return ''.join(sorted(word.lower()))

def check_is_noun(word: str):
    return True if word[0].isupper() else False


def create_tables(db: Session):
    Base.metadata.create_all(bind=db)
    return None


class Anagrams:
    def create_table(self, db: Session):
        Base.metadata.create_all(bind=db)

    def load_dictionary_table(self, db: Session):
        with open('./dictionary/dictionary.txt', 'r') as f:
            counter: int = 0
            for line in f:
                word: str = line.strip()
                sorted_letters: str = get_sorted(word)
                word_len: int = len(word)
                is_noun = check_is_noun(word)
                db_item: Dictionary = Dictionary(word=word, sorted_letters=sorted_letters, word_len=word_len,
                                                 is_noun=is_noun)
                db.add(db_item)
                counter += 1
                if counter % 100 == 0:
                    db.commit()
            db.commit()

    def add_words(self, words: list, db: Session) -> Optional[str]:
        for word in words:
            single_word: int = len(word.split(' '))
            if single_word == 1:
                check_word: Optional[Dictionary] = db.query(Dictionary).filter_by(word=word, word_len=len(word)).first()
                if check_word is None:
                    db_item: Dictionary = Dictionary(word=word, sorted_letters=get_sorted(word), word_len=len(word),
                                                     is_noun=check_is_noun(word))
                    db.add(db_item)
            else:
                db.rollback()
                return False
        db.commit()
        return True

    def get_dictionary_stats(self, db: Session):
        words_len: list = [value[0] for value in db.query(Dictionary.word_len).all()]
        min_len: int = min(words_len)
        max_len: int = max(words_len)
        avg_len: float = mean(words_len)
        median_len: float = median(words_len)
        return {"word count": len(words_len), "minimum length": min_len, "maximum length": max_len,
                "median length": median_len, "average length": round(avg_len, 2)}

    def get_anagrams(self, word: str, db: Session, limit: Optional[int] = None, noun: bool = True):
        if noun:
            fetch_anagrams: Dictionary = db.query(Dictionary).filter_by(sorted_letters=get_sorted(word),
                                                                        word_len=len(word))
        else:
            fetch_anagrams = db.query(Dictionary).filter_by(sorted_letters=get_sorted(word), word_len=len(word),
                                                            is_noun=noun)
        anagrams: list = [anagram.word for anagram in fetch_anagrams if word.lower() != anagram.word.lower() and
                          anagram.word.lower() != anagram.sorted_letters.lower()]
        if limit is None:
            return anagrams
        if len(anagrams) >= limit:
            return anagrams[:limit]
        return anagrams

    def get_max_anagrams(self, db: Session, limit: int = 5, noun: bool = True):
        if noun:
            query: str = 'SELECT sorted_letters, count(*) FROM public.dictionary  ' \
                         'WHERE word_len > 2 GROUP BY sorted_letters ' \
                         'HAVING count(*) > 1 ' \
                         f'ORDER BY count(*) DESC LIMIT {limit}'
        else:
            query = 'SELECT sorted_letters, count(*) FROM public.dictionary  ' \
                         'WHERE word_len > 2 and is_noun = False GROUP BY sorted_letters ' \
                         'HAVING count(*) > 1 ' \
                         f'ORDER BY count(*) DESC LIMIT {limit}'
        max_sorted: Iterable = db.execute(query)

        return [{'anagrams': self.get_anagrams(word=word[0], db=db, noun=noun), 'len': word[1]}
                for word in max_sorted]

    def get_anagrams_by_size(self, size: int, db: Session, limit: int = 5, noun: bool = True):
        if noun:
            query: str = 'SELECT sorted_letters FROM public.dictionary ' \
                         'WHERE word_len > 1 GROUP BY sorted_letters ' \
                         f'HAVING count(*) = {size} ' \
                         f'ORDER BY count(*) DESC LIMIT {limit}'
        else:
            query = 'SELECT sorted_letters FROM public.dictionary ' \
                    'WHERE word_len > 1 and is_noun = False GROUP BY sorted_letters ' \
                    f'HAVING count(*) = {size} ' \
                    f'ORDER BY count(*) DESC LIMIT {limit}'
        fixed_size: Iterable = db.execute(query)
        return [{'anagrams': self.get_anagrams(word[0], db)} for word in fixed_size]

    def check_anagrams(self, words: list):
        for word in words:
            first = get_sorted(words[0])
            for word in words:
                if first != get_sorted(word):
                    return False
                    break
            return True

    def delete_word_and_anagrams(self, word: str, db: Session):
        db.query(Dictionary).filter_by(sorted_letters=get_sorted(word), word_len=len(word)).delete()
        db.commit()
        return None

    def delete_all(self, db: Session):
        db.query(Dictionary).delete()
        db.commit()
        return None

    def delete_word(self, word: str, db: Session):
        dict_item = db.query(Dictionary).filter_by(word=word, word_len=len(word))
        if dict_item:
            dict_item.delete()
            db.commit()
        return None
