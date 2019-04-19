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
    g,
)
import json
from models.user import User
from models.card import Card
from models.borrow import Borrow
from models.book import Book
from routes import current_user

from utils import log

main = Blueprint('api', __name__)


@main.route("/borrow", methods=["POST"])
def borrow():
    u = current_user()
    if u is None or u.card_id is None:
        abort(403)
    else:
        # 获取post上来的json数据
        title = json.loads(request.get_data())
        log("用户({})尝试借阅书籍({}):".format(u.username, title))
        if Borrow.borrow_book(title, u) == 1:
            book = Book.find_one(title=title)
            return jsonify({"stock": book.stock})
        else:
            return jsonify({"stock": '-1'})


@main.route("/return", methods=["POST"])
def return_book():
    u = current_user()
    if u is None:
        abort(403)
    else:
        # 获取post上来的json数据
        title = json.loads(request.get_data())
        log("用户({})尝试归还书籍({}):".format(u.username, title))

        if Borrow.return_book(title, u) == 1:
            return jsonify({"deleted": 1})
        else:
            return jsonify({"deleted": 0})


@main.route("/borrowed_books", methods=["POST"])
def borrowed_books():
    u = current_user()
    books = u.borrowed_books()
    bs = []
    for b in books:
        bs.append(b.title)
    return jsonify(bs)
