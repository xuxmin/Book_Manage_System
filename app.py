from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)
from config import secret_key
from routes.index import main as index_routes
from routes.warehouse import main as ware_routes
from routes.search import main as search_routes
from routes.api import main as api_routes
from routes.admin_api import main as admin_api_routes

import config as conf

app = Flask(__name__)

app.secret_key = secret_key


app.register_blueprint(index_routes)
app.register_blueprint(ware_routes, url_prefix="/warehouse")
app.register_blueprint(search_routes, url_prefix="/search")
app.register_blueprint(api_routes, url_prefix="/api")
app.register_blueprint(admin_api_routes, url_prefix="/admin_api")


if __name__ == '__main__':
    config = dict(
        debug=conf.debug,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
