from flask import Flask
views = Blueprint('views')
app = Flask(__name__)
@views.route('')
@app.route("/")
def home():
    return "This is the homepage"

if __name__ == '__main__':
    app.run(debug=True,port=8000)
