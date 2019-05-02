from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    jsonify,
)
import json
from models.user import User
from models.card import Card
from models.borrow import Borrow
from models.book import Book
from routes import current_user
from models.apiError import APIValueError

from utils import log

main = Blueprint('admin_api', __name__)


@main.route("/record", methods=["GET"])
def borrow():
    u = current_user()
    if u is None or u.role != 1:
        return jsonify({'code': '403', 'msg': 'access deny'})
    else:
        # 返回借书记录
        records = []
        bs = Borrow.find_all()
        for b in bs:
            record = {}
            book = Book.find_one(id=b.book_id)
            usr = User.find_one(card_id=b.card_id)
            record['usr'] = usr.username
            record['book'] = book.title
            record['bt'] = b.borrow_date
            record['deleted'] = b.deleted
            records.append(record)
        return jsonify(records)
