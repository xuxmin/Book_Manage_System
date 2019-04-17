from flask import (
    render_template,
    request,    # local 对象??
    redirect,
    session,    # 类似request
    url_for,
    Blueprint,
    make_response,
    abort,
)

from models.user import User
from models.card import Card
from routes import current_user

from utils import log

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    if u is None:
        return render_template('index_login.html', username="游客")
    else:
        if u.has_card():
            return render_template('index_user.html', username=u, card="已拥有借书证")
        else:
            return render_template('index_user.html', username=u, card="未拥有借书证")


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


# @main.route("/api/borrow", methods=['POST'])
# def borrow():
    