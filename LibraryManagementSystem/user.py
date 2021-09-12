from flask import request, jsonify, render_template
from models import Books, app, db


# @app.route('/searchbook', methods=['GET', 'POST'])
# def search_books():
#     return render_template('searchbook.html')


def issued_books():
    return "Issue book history"
