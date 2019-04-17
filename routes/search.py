from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
)

from routes import current_user
from models.book import Book

from utils import log

main = Blueprint('search', __name__)


@main.route("/")
def index():
    u = current_user()
    print("当前用户:", u)
    if u is None:
        abort(403)
    else:
        books = Book.find_all()
        return render_template('search.html', books=books)


@main.route("/find", methods=['POST'])
def find():
    form = request.form
    print(form)

    return redirect(url_for('.index'))
