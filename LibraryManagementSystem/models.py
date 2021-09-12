from datetime import date
import os
from flask import Flask, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:12345678@localhost/Library'
app.config['SECRET_KEY'] = b'\xed\xd47\x83\xaf\xeb*\xd1\xe1Y\x89e\xfc\xb0E\xb2\xc5\x9d\x1d/\xe8\xbf\xc7\xc9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = 'book_data'
    book_name = db.Column(db.String(50), primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    published_date = db.Column(db.String(20), nullable=False)
    issued_date = db.Column(db.String(20))
    issued_to = db.Column(db.String(20))

    def __init__(self, book_name, author, total_pages, genre, rating, published_date, issued_date=None, issued_to=None):
        self.book_name = book_name
        self.author = author
        self.total_pages = total_pages
        self.genre = genre
        self.rating = rating
        self.published_date = published_date
        self.issued_date = issued_date
        self.issued_to = issued_to

    def __repr__(self):
        return '<book_name {}>'.format(self.book_name)


class User(db.Model, UserMixin):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, username, contact, email, password, address):
        self.username = username
        self.contact = contact
        self.email = email
        self.password = password
        self.address = address
        self.role = "user"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<username {}>'.format(self.username)


class BookIssueRecord(db.Model):
    __tablename__ = 'issue_records'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    book_name = db.Column(db.String(50))
    request_date = db.Column(db.String(30))
    requested_by = db.Column(db.String(20))
    approved_by = db.Column(db.String(20))
    updated_on = db.Column(db.String(20))

    def __init__(self, book_name, requested_by):
        self.status = "INITIATED"
        self.book_name = book_name
        self.request_date = date.today()
        self.requested_by = requested_by
        self.approved_by = 'admin'
        self.updated_on = date.today()
