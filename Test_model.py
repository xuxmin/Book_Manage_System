import json
from models.user import User
from models.card import Card
from models.borrow import Borrow
from models.book import Book
from routes import current_user
from models.apiError import APIValueError

from utils import log

if __name__ == "__main__":
    records = []
    record = {}
    bs = Borrow.find_all()
    for b in bs:
        book = Book.find_one(id=b.book_id)
        usr = User.find_one(card_id=b.card_id)
        record['usr'] = usr.username
        record['book'] = book.title
        record['bt'] = b.borrow_date
        record['deleted'] = b.deleted
        records.append(record)
    print(records)
