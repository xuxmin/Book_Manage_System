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
    log("当前用户:", u)
    books = Book.find_all()
    if u is None:
        card_id = "None"
    else:
        card_id = u.card_id
    return render_template('index.html', user=u, books=books, card_id=card_id)


@main.route("/register", methods=['GET'])
def register():
    return render_template("register.html")


@main.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@main.route("/logout", methods=['get'])
def log_out():
    session.pop("user_id")
    return redirect(url_for(".index"))


@main.route("/profile", methods=['GET'])
def profile():
    u = current_user()
    if u is None:
        return abort(403)
    else:
        return render_template("profile.html", user=u)


@main.route("/apply", methods=['POST'])
def apply_card():
    u = current_user()
    if u is None:
        return abort(403)
    form = request.form
    Card.apply_card(u, form)
    return redirect(url_for(".index"))

@main.route("/info", methods=['POST'])
def info():
    return render_template("info.html")


@main.route("/admin", methods=['GET'])
def admin():
    u = current_user()
    if u is None or u.role != 1:
        abort(403)
    else:
        return render_template("admin.html", user=u)
