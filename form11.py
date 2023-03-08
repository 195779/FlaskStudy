from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, RadioField,HiddenField, SelectField
from wtforms import validators
# 其中StringField 为 旧版本的 textField


class ContactForm(FlaskForm):
    # 自定义contactForm类

    id = HiddenField('id')
    # 隐藏控件（用在app12中）
    name = StringField('Name of Student', [validators.InputRequired('Please enter your name.')])
    # 文本控件：其label为“Name of Student” ，做validators输入有效性检查
    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    # 选择性控件：其label为‘Gender’,选项值为M显示为Male 与 值为F显示为Female
    Address = TextAreaField('Address')
    # 大文本的地址控件
    email = StringField('Email', [validators.InputRequired('Please enter your email address.'),
                                  validators.Email('Please enter your email address.')])
    # 邮件控件，做了两个检查。1、必须输入 2、必须输入有效性格式
    Age = IntegerField('age')
    # 整型控件
    language = SelectField('Languages', choices=[('cpp', 'C++'), ('py', 'Python')])
    # 下拉控件
    submit = SubmitField('Send')
    # 提交控件
