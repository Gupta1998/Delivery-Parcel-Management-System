from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    status = db.Column(db.Enum('received', 'in_transit', 'delivered'), default='received')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'))
    status = db.Column(db.Enum('received', 'in_transit', 'delivered'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
