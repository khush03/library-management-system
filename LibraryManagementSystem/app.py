from flask import render_template, request, redirect, session, flash
from flask_login import LoginManager, login_required

from models import Books, app, db, User
import requests
import admin
import forms

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET'])
def index():
    if not session.get("username"):
        return redirect("http://localhost:5000")
    return render_template("landing.html")


@login_required
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")


# ******************************Authorization-handelers Views*************************

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
        session["username"] = request.form.get('username')
        session["password"] = request.form.get('password')
        user_list = User.query.filter_by(username=session["username"], password=session["password"]).all()
        if len(user_list) == 0:
            return render_template('signin.html', error="Invalid Username or password!")
        else:
            return render_template('home.html')
    return render_template('signin.html')


@app.route('/unregister/<username>', methods=['GET', 'POST'])
def unregister(username):
    User.query.filter_by(username=username).delete()
    db.session.commit()
    return redirect('http://localhost:5000')


# ******************************Error-handelers Views*************************

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


# ******************************************************************************


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
