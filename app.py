from flask import Flask, jsonify, request, Response
import json

from settings import *
from BookModel import *

# GET /books/{isbn}
@app.route ('/books/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# GET /books
@app.route('/books', methods=['GET'])
def hello_world():
    return jsonify({'books': Book.get_all_books()})

# POST/books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if _valid_book_object(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request.",
            "helpString": "Data passed in similar to this {'name': 'book name', 'price': 7.99, 'isbn', 1234567890}"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), 400, mimetype='application/json')
        return response

# PUT /books/[isbn]
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not _valid_put_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request.",
            "helpString": "Data passed in similar to this {'name': 'book name', 'price': 7.99}"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), 400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

# PATCH request for updating only fields that are passed
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/[isbn]
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response
    invalid_book_object_error_msg = {
        "error": "Invalid book object passed in request."
    }
    response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
    return response


def _valid_put_request_data(book_object):
    if ("name" in book_object and
            "price" in book_object):
        return True
    else:
        return False


def _valid_book_object(book_object):
    if ("name" in book_object and
            "price" in book_object and
            "isbn" in book_object):
        return True
    else:
        return False


app.run(port=5000)
