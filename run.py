from http.cookiejar import debug

from flask import Flask

from config import settings
from db.database import init_db

app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY

if __name__ == '__main__':
    init_db()
    app.run(port=5466, debug=True)