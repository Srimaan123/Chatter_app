import os
from flask import Flask
from auth import auth_bp
from contacts import contacts_bp
from chat import chat_bp

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

app.register_blueprint(auth_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
