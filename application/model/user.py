from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
from flask import flash, abort
import datetime,re
from .. import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)

    @validates('email')
    def valid_email(self, key, email):
        assert bool(re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email)), "Email is invalid"
        return email

    @validates('password')
    def valid_password(self, key, password):
        assert password is not None, 'Password cannot be None'
        assert password != '', 'Password cannot be empty'
        return password

    @validates("created_time")
    def valid_createdtime(self, key, created_time):
        assert type(created_time) is datetime.datetime, "Not datetype object"
        return created_time


def add_new_user(new_user):
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except IntegrityError:
        db.session.rollback()
        flash('User with same email already exists',"danger")
        abort(400)
    except Exception as err:
        db.session.rollback()
        flash(err, 'danger')
        abort(500)