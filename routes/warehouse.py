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

main = Blueprint('warehouse', __name__)


@main.route("/")
def index():
    u = current_user()
    log("当前用户:", u)
    if u.role == 1:
        return render_template("warehouse.html")
    else:
        abort(403)


@main.route("/add", methods=['POST'])
def add():
    form = request.form
    book = Book()
    book.from_form(form)
    if Book.has_book(book.title) is False:
        log("save to database")
        book.save()
    return redirect(url_for('.index'))
