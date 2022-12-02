from sqlalchemy.orm import validates
from flask import flash, abort
import datetime
from .. import db, INTRAPOLATION

class PredictionHistory(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    diabetes = db.Column(db.Boolean, nullable=False)
    bloodpressure = db.Column(db.Boolean, nullable=False)
    anytransplant = db.Column(db.Boolean, nullable=False)
    chronic = db.Column(db.Boolean, nullable=False)
    allergy = db.Column(db.Boolean, nullable=False)
    cancer = db.Column(db.Boolean, nullable=False)
    surgery = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.Float, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)

    @validates('user_ID')
    def valid_userid(self,key, user_ID):
        assert user_ID is not None, 'UserID is none'
        assert isinstance(user_ID, int), 'UserID should be integer'
        return user_ID

    @validates('age')
    def valid_age(self,key,age):
        assert isinstance(age, int), 'Age should be integer'
        assert INTRAPOLATION['age_min'] <= age <= INTRAPOLATION['age_max'], 'Age outside valid range'
        return age

    @validates('height')
    def valid_height(self,key,height):
        assert type(height) in {float, int}, 'height should be integer'
        assert INTRAPOLATION['height_min'] <= height <= INTRAPOLATION['height_max'], 'height outside valid range'
        return height

    @validates('weight')
    def valid_weight(self,key,weight):
        assert type(weight) in {float, int}, 'weight should be integer'
        assert INTRAPOLATION['weight_min'] <= weight <= INTRAPOLATION['weight_max'], 'weight outside valid range'
        return weight

    @validates('diabetes')
    def valid_diabetes(self,key,diabetes):
        assert diabetes in {0,1}, 'diabetes should be 0 or 1'
        return diabetes


    @validates('bloodpressure')
    def valid_bloodpressure(self,key,bloodpressure):
        assert bloodpressure in {0,1}, 'bloodpressure should be 0 or 1'

        return bloodpressure


    @validates('anytransplant')
    def valid_anytransplant(self,key,anytransplant):
        assert anytransplant in {0,1}, 'anytransplant should be 0 or 1'
        return anytransplant

    @validates('chronic')
    def valid_chronic(self,key,chronic):
        assert chronic in {0,1}, 'chronic should be 0 or 1'
        return chronic

    @validates('allergy')
    def valid_allergy(self,key,allergy):
        assert allergy in {0,1}, 'allergy should be 0 or 1'
        return allergy

    @validates('cancer')
    def valid_cancer(self,key,cancer):
        
        assert cancer in {0,1}, 'Cancer should be 0 or 1'
        return cancer


    @validates('surgery')
    def valid_surgery(self,key,surgery):
        assert type(surgery) in {int}, 'Surgeries is in wrong format'
        assert 0 <= surgery <=3, 'Surgery must be between 0 and 3'
        return surgery
    @validates('bmi')
    def valid_bmi(self,key,bmi):
        assert type(bmi) in {float, int}, 'BMI is in wrong format'
        assert bmi >0, 'BMI cant be -ve'
        return bmi

    @validates('prediction')
    def valid_prediction(self,key,prediction):
        assert type(prediction) in {float, int}, 'Prediction is in wrong format'
        assert INTRAPOLATION['price_min'] <= prediction <= INTRAPOLATION['price_max'], 'Invalid output range'
        return prediction

    @validates("created_time")
    def valid_createdtime(self, key, created_time):
        assert type(created_time) is datetime.datetime, "Not datetype object"
        return created_time


def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        abort(500)

def delete_entry(entry):
    try:
        db.session.delete(entry)
        db.session.commit()
        return entry.id
    except Exception:
        db.session.rollback()
        abort(500)