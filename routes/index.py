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

from utils import log

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    if u is None:
        return render_template('index_login.html', user="游客")
    else:
        if u.has_card():
            return render_template('index_user.html', user=u, card="已拥有借书证")
        else:
            return render_template('index_user.html', user=u, card="未拥有借书证")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('.index'))


@main.route("/logout", methods=['get'])
def log_out():
    session.pop("user_id")
    return redirect(url_for(".index"))

@main.route("/apply", methods=['POST'])
def apply_card():
    u = current_user()
    if u is None:
        return abort(403)
    form = request.form
    Card.apply_card(u, form)
    return redirect(url_for(".index"))


@main.route("/api/borrow", methods=["POST"])
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


@main.route("/api/return", methods=["POST"])
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

@main.route("/api/borrowed_books", methods=["POST"])
def borrowed_books():
    u = current_user()
    books = u.borrowed_books()
    bs = []
    for b in books:
        bs.append(b.title)
    return jsonify(bs)
