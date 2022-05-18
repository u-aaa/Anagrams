import sys

sys.path.append('./')
from sql_app.crud import Anagrams
from sql_app.database import SessionLocal


db = SessionLocal()

def main(db):
    anagram = Anagrams()
    anagram.create_table(db=db)
    anagram.load_dictionary_table(db=db)


if __name__ == '__main__':
    main(db)
