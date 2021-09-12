from datetime import date
from flask import request, jsonify, render_template, redirect, flash, session
from flask_login import login_required
from models import Books, app, db, BookIssueRecord


@login_required
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


@login_required
def get_books():
    all_books = Books.query.all()
    book_list = []
    book_issue_record = get_request_issue_record_by_username(session['username'])
    for book in all_books:
        curr_book = {'book_name': book.book_name, 'author': book.author, 'total_pages': book.total_pages,
                     'genre': book.genre, 'rating': book.rating, 'published_date': book.published_date,
                     'is_available': True if not book.issued_to else False, 'has_requested': True if book.book_name in
                                                                                                     book_issue_record else False}
        book_list.append(curr_book)
    return book_list


@login_required
@app.route('/bookslist', methods=['GET', 'POST'])
def books_list():
    bookslist_data = get_books()
    return render_template('bookslist.html', bookslist_data=bookslist_data)


@login_required
@app.route('/updatebook/<book_name>', methods=['GET', 'POST'])
def update_book(book_name):
    if request.method == "POST":
        new_obj = {
            'author': request.form.get('author'),
            'total_pages': request.form.get('total_pages'),
            'genre': request.form.get('genre'),
            'rating': request.form.get('rating'),
            'published_date': request.form.get('published_date')
        }
        Books.query.filter_by(book_name=book_name).update(new_obj)
        db.session.commit()
        return redirect('http://localhost:5000/home')
    else:
        book_data_from_book_name = Books.query.filter_by(book_name=book_name).first()
        output_book_data_from_book_name = {
            'book_name': book_data_from_book_name.book_name,
            'author': book_data_from_book_name.author,
            'rating': book_data_from_book_name.rating,
            'genre': book_data_from_book_name.genre,
            'published_date': book_data_from_book_name.published_date,
            'total_pages': book_data_from_book_name.total_pages
        }
        return render_template('updatebook.html', book_info=output_book_data_from_book_name)


@login_required
@app.route("/requestissue/<book_name>", methods=['GET', 'POST'])
def request_issue(book_name):
    book_issue_record = BookIssueRecord(book_name, session['username'])
    db.session.add(book_issue_record)
    db.session.commit()
    return redirect('http://localhost:5000/home')


@login_required
def get_request_issue_record_by_username(username):
    book_issue_list = []
    book_issue_records = BookIssueRecord.query.filter_by(requested_by=username, status="INITIATED").all()
    for book_record in book_issue_records:
        if book_record.book_name not in book_issue_list:
            book_issue_list.append(book_record.book_name)
    return book_issue_list


@login_required
@app.route("/requests", methods=['GET', 'POST'])
def pending_requests():
    book_entries_list = []
    pending_book_requests = BookIssueRecord.query.filter_by(status="INITIATED").all()
    for book_entries in pending_book_requests:
        pending_book_requests_records = {
            'book_name': book_entries.book_name,
            'request_date': book_entries.request_date,
            'requested_by': book_entries.requested_by,
            'updated_on': book_entries.updated_on,
            'id': book_entries.id,
            'status': book_entries.status,
            'approved_by': book_entries.approved_by
        }
        book_entries_list.append(pending_book_requests_records)
    return render_template('pendingrequests.html', pending_book_requests=book_entries_list)


@login_required
@app.route('/issuebook/<book_name>', methods=['GET', 'POST'])
def issue_books(book_name):
    approved_book_detail = BookIssueRecord.query.filter_by(book_name=book_name).first()
    issued_book_detail = {
        'issued_to': approved_book_detail.requested_by,
        'issued_date': date.today()
    }
    issued_book_detail_status = {
        'status': 'Approved',
        'approved_by': 'Admin'
    }
    Books.query.filter_by(book_name=book_name).update(issued_book_detail)
    BookIssueRecord.query.filter_by(book_name=book_name).update(issued_book_detail_status)
    db.session.commit()
    return redirect('http://localhost:5000/requests')


@login_required
@app.route('/searchbook', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        book_searched = request.form.get('book_name').lower()
        books_list = Books.query.all()
        if books_list and book_searched:
            sanitized_books_list = []
            for book in books_list:
                if book_searched in book.book_name.lower():
                    sanitized_books_list.append({
                        'book_name': book.book_name,
                        'author': book.author,
                        'rating': book.rating,
                        'genre': book.genre,
                        'published_date': book.published_date,
                        'total_pages': book.total_pages
                    })
            return render_template('home.html', book_list=sanitized_books_list)
        else:
            return render_template('home.html')
    return render_template('home.html')
