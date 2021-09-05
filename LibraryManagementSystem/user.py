from flask import request, jsonify
from models import Books, app, db


def search_books():
    book_name_to_be_searched = ""

    return "Search for books"


def request_issue():
    book_name = request.body.get('book_name')
    username = request.body.get('username')
    return "Request for Issue"


def issued_books():
    return "Issue book history"
