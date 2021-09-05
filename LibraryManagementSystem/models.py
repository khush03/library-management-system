import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:12345678@localhost/Library'
app.config['SECRET_KEY'] = b'\xed\xd47\x83\xaf\xeb*\xd1\xe1Y\x89e\xfc\xb0E\xb2\xc5\x9d\x1d/\xe8\xbf\xc7\xc9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


class User(db.Model):
    __tablename__ = 'user_data'
    username = db.Column(db.String(50), primary_key=True)
    contact = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, username, contact, email, password, address, role='user'):
        self.username = username
        self.contact = contact
        self.email = email
        self.password = password
        self.address = address
        self.role = role

    def __repr__(self):
        return '<username {}>'.format(self.username)


class BookIssueRecord(db.Model):
    __tablename__ = 'issue_records'
    status = db.Column(db.String(20), primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    request_date = db.Column(db.String(30), nullable=False)
    requested_by = db.Column(db.String(20), nullable=False)
    approved_by = db.Column(db.String(20), nullable=False)
    updated_on = db.Column(db.String(20), nullable=False)

    def __init__(self, status, book_name, request_date, requested_by, approved_by):
        self.status = status
        self.book_name = book_name
        self.request_date = request_date
        self.requested_by = requested_by
        self.approved_by = approved_by
        self.updated_on = datetime.datetime.now()

