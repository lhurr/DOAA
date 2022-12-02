from flask_wtf import FlaskForm
from wtforms.validators import Email,Regexp, EqualTo,InputRequired,Length, NumberRange, ValidationError
from wtforms import SubmitField, PasswordField, FloatField, IntegerField, EmailField,RadioField, IntegerRangeField
from . import INTRAPOLATION

password_validator = [
        InputRequired(),
        Regexp(
            regex='.*[A-Z]+.*', message='Password must contain at least one uppercase letter!'),
        Regexp(
            regex='.*[a-z]+.*', message='Password must contain at least one lowercase letter!'),
        Regexp(regex='.*[0-9]+.*',
               message='Password must contain at least one number!'),
        Regexp(regex='.*[!@#$%^&*]+.*',
               message='Password must contain at least one special character [!@#$%^&*]!'),
        Length(min=8, message='Password must contain at least 8 characters!')

]

class RegisterForm(FlaskForm):
    email = EmailField(label='Email Address', validators=[
                        InputRequired(), Email(message='Invalid email!')], render_kw={"placeholder": "Email"})
    password = PasswordField(label='New Password', validators=password_validator, render_kw={"placeholder": "Password"})

    confirm = PasswordField(label='Confirm Password', validators=[
        InputRequired(),
        EqualTo(fieldname='password', message='Passwords must match')
    ],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField(label='Email Address', validators=[
                        InputRequired(), Email()], render_kw={"placeholder": "you@gmail.com"})
    password = PasswordField(label='Password', validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')



class PredictionForm(FlaskForm):
    age = IntegerField(label='Age', validators=[ InputRequired(), NumberRange(min=INTRAPOLATION['age_min'], max=INTRAPOLATION['age_max'])] , render_kw={"placeholder": "Enter age here"})
    height = FloatField(label='Height (cm)', validators=[ InputRequired(), NumberRange(min=INTRAPOLATION['height_min'], max=INTRAPOLATION['height_max'])] , render_kw={"placeholder": "Enter height here"})
    weight = FloatField(label='Weight (kg)', validators=[ InputRequired(), NumberRange(min=INTRAPOLATION['weight_min'], max=INTRAPOLATION['weight_max'] )], render_kw={"placeholder": "Enter weight here"} )
    diabetes = RadioField('1. Do you have diabetes?', choices=[(1, 'Yes'),(0,'No')], validators=[InputRequired()])
    bloodpressure = RadioField(label='2. Do you have blood pressure problems?',choices=[(1, 'Yes'),(0,'No')], validators=[ InputRequired()], default='No' )
    anytransplant = RadioField(label='3. Have you undergone any major organ transplants?', choices=[(1, 'Yes'),(0,'No')],validators=[ InputRequired()] )
    chronic = RadioField(label='4. Do you suffer from any chronic diseases like asthma?', choices=[(1, 'Yes'),(0,'No')],validators=[ InputRequired()] )
    allergies = RadioField(label='5. Do you have any known allergies?', choices=[(1, 'Yes'),(0,'No')],validators=[ InputRequired()] )
    cancer = RadioField(label='6. Do you have any relatives that have history of cancer?',choices=[(1, 'Yes'),(0,'No')] , validators=[ InputRequired()] )
    surgery = IntegerRangeField(label='7. Number of major surgeries you went through?', validators=[ InputRequired(), NumberRange(min=0, max=3)], default=0 )
    submit = SubmitField('Submit for prediction!')