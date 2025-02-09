from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, uid, name, email, role='user'):
        self.uid = uid
        self.name = name
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

class Book:
    def __init__(self, title, author, subject, owner_id, condition='Good', available=True):
        self._id = ObjectId()
        self.title = title
        self.author = author
        self.subject = subject
        self.owner_id = owner_id
        self.condition = condition
        self.available = available

    def to_dict(self):
        return {
            '_id': str(self._id),
            'title': self.title,
            'author': self.author,
            'subject': self.subject,
            'owner_id': self.owner_id,
            'condition': self.condition,
            'available': self.available
        }

class Rental:
    def __init__(self, book_id, renter_id, rental_date=None, return_date=None):
        self._id = ObjectId()
        self.book_id = book_id
        self.renter_id = renter_id
        self.rental_date = rental_date or datetime.utcnow()
        self.return_date = return_date

    def to_dict(self):
        return {
            '_id': str(self._id),
            'book_id': str(self.book_id),
            'renter_id': self.renter_id,
            'rental_date': self.rental_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None
        }
