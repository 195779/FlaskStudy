from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,IntegerField,SubmitField,RadioField,SelectField
from wtforms import validators

class ContactForm(FlaskForm):
    name = StringField('Name of Student',[validators.DataRequired('Please enter your name.')])
    Gender = RadioField('Gender',choices=[('M','Male'),('F','Female')])
    Address = TextAreaField('Address')
    email = StringField('Email',[validators.DataRequired('Please enter your email address.')])
    Age = IntegerField('age')
    language = SelectField('Languages',choices=[('cpp','C++',('py','Python'))])
    submit = SubmitField('Send')
