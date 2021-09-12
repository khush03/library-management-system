from flask import render_template, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

import models
from models import app, db, User
import admin
import forms

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(int(userid))


@app.route('/', methods=['GET'])
def index():
    return render_template("landing.html")


@login_required
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

# ******************************Authorization-handelers Views*************************


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = forms.LoginForm()
    username = form.username.data
    password = form.password.data
    user = models.User.get_by_username(username)
    if user is not None and user.check_password(password):
        login_user(user, form.remember_me.data)
        return render_template('home.html')
    else:
        return render_template('signin.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        contact = form.contact.data
        address = form.address.data
        user_details = User(username=username, email=email, password=generate_password_hash(password),
                            contact=contact, address=address)
        db.session.add(user_details)
        db.session.commit()
        return redirect('http://localhost:5000/signin')
    return render_template("signup.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/unregister/<username>', methods=['GET', 'POST'])
@login_required
def unregister(username):
    User.query.filter_by(username=username).delete()
    db.session.commit()
    return redirect('http://localhost:5000')


# def get_user_list():
#     users_list = []
#     users = User.query.all()
#     for user in users:
#         if user.username not in users_list:
#             users_list.append(user.username)
#         # print(users)
#     print(users_list)
#     return users_list


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
