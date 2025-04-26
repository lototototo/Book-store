from http.cookiejar import debug

from flask import Flask

from config import settings
from db.database import init_db
from routes import main_blueprint, login_manager


app = Flask(import_name=__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = settings.SECRET_KEY
init_db()
app.register_blueprint(blueprint=main_blueprint, url_prefix='/')
if __name__ == '__main__':
    app.run(port=5466, debug=True)