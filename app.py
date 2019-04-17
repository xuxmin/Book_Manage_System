from flask import (
    Flask,
    flash,
    render_template,
    request,    # local 对象??
    redirect,
    session,    # 类似request
    url_for,
    Blueprint,
    make_response,
)
from config import secret_key
from routes.index import main as index_routes
from routes.warehouse import main as ware_routes
from routes.search import main as search_routes

app = Flask(__name__)

app.secret_key = secret_key


app.register_blueprint(index_routes)
app.register_blueprint(ware_routes, url_prefix="/warehouse")
app.register_blueprint(search_routes, url_prefix="/search")


if __name__ == '__main__':
    config = dict(
        debug=True,     # 注意这个发生错误时会显示在页面上
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
