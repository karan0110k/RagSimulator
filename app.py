from flask import Flask, render_template
from routes.upload import upload_bp
from routes.chat import chat_bp

app = Flask(__name__)

app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, port=5001, threaded=False)