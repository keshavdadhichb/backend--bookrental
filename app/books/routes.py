from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.models import Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(**data)
    result = books_bp.app.db.be.books.insert_one(new_book.to_dict())
    return jsonify({'message': 'Book created', 'id': str(result.inserted_id)}), 201

@books_bp.route('/books', methods=['GET'])
def get_books():
    books = list(books_bp.app.db.be.books.find())
    return jsonify([Book(**book).to_dict() for book in books]), 200

@books_bp.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = books_bp.app.db.be.books.find_one({'_id': ObjectId(book_id)})
    if book:
        return jsonify(Book(**book).to_dict()), 200
    return jsonify({'error': 'Book not found'}), 404

@books_bp.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    result = books_bp.app.db.be.books.update_one({'_id': ObjectId(book_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Book updated'}), 200
    return jsonify({'error': 'Book not found'}), 404

@books_bp.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_bp.app.db.be.books.delete_one({'_id': ObjectId(book_id)})
    if result.deleted_count:
        return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'error': 'Book not found'}), 404
