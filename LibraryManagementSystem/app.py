import json
import unicodedata

from flask import jsonify, render_template, request
from models import Books, app, db, User
from admin import get_books
import requests


@app.route('/', methods=['GET'])
def index():
    return render_template("landing.html")


@app.route('/land', methods=['GET'])
def test():
    print("landing")


@app.route('/home', methods=['GET'])
def home():
    bookslist_data = requests.get('http://localhost:5000/bookslist')
    bookslist_data = unicodedata.normalize('NFKD', bookslist_data.text).encode('ascii', 'ignore')
    bookslist_data = json.loads(bookslist_data)
    print("output of get books ", bookslist_data)
    return render_template("home.html", bookslist_data=bookslist_data)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        contact = request.form.get('contact-number')
        address = request.form.get('address')
        user_details = User(username=username, email=email, password=password, contact=contact, address=address)
        user = User.query.filter_by(username=username).all()
        if len(user) == 0:
            db.session.add(user_details)
            db.session.commit()
        return render_template('signin.html')
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_list = User.query.filter_by(username=username, password=password).all()
        if len(user_list) == 0:
            return render_template('signin.html', error="Invalid Username or password!")
        else:
            return render_template('home.html')
    return render_template('signin.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
