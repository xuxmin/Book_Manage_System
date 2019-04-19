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


@main.route("/index", methods=['GET'])
def index2():
    u = current_user()
    log("当前用户:", u)
    if u is None:
        abort(403)
    else:
        books = Book.find_all()
        return render_template('index.html', user=u, books=books, card_id=u.card_id)


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
