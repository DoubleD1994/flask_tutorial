from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]

# GET /books/{isbn}
@app.route ('/books/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

# GET /books
@app.route('/books', methods=['GET'])
def hello_world():
    return jsonify({'books': books})

# POST/books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if _valid_book_object(request_data):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        current_isbn = book['isbn']
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

# PATCH request for updating only fields that are passed
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        updated_book["name"] = request_data['name']
    if "price" in request_data:
        updated_book["price"] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/[isbn]
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
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
