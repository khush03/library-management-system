from flask import request, jsonify, render_template
from models import Books, app, db


@app.route('/addbook', methods=['GET', 'POST'])
def add_books():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        author = request.form.get('author')
        total_pages = request.form.get('total_pages')
        genre = request.form.get('genre')
        rating = request.form.get('rating')
        published_date = request.form.get('published_date')
        book_details = Books(book_name=book_name, author=author, total_pages=total_pages, genre=genre, rating=rating,
                             published_date=published_date)
        books = Books.query.filter_by(book_name=book_name).all()
        if len(books) == 0:
            db.session.add(book_details)
            db.session.commit()
    return render_template('addbook.html')


@app.route('/bookslist', methods=['GET'])
def get_books():
    all_books = Books.query.all()
    book_list = []
    for book in all_books:
        curr_book = {}
        curr_book['book_name'] = book.book_name
        curr_book['author'] = book.author
        curr_book['total_pages'] = book.total_pages
        curr_book['genre'] = book.genre
        curr_book['rating'] = book.rating
        curr_book['published_date'] = book.published_date
        book_list.append(curr_book)
    return jsonify(book_list)


@app.route('/updatebook/<book_name>', methods=['GET', 'POST'])
def update_book():
    return render_template('updatebook.html')


@app.route('/issuebook', methods=['GET', 'POST'])
def issue_books():
    return "Issue a book"
