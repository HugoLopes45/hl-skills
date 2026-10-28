from flask import Flask

from app.webhooks import bp

app = Flask(__name__)
app.register_blueprint(bp)
