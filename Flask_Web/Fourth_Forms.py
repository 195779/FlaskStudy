from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,TextAreaField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('userName', validators=[DataRequired()], render_kw={'placeholder': 'Your Username'})
    # DataRequired(message=None) 验证数据是否有效
    password = PasswordField('passWord', validators=[DataRequired(), Length(8, 128)])
    # Length(min=-1,max--1,message=None) 验证输入值的长度是否在给定范围内
    remember = BooleanField("Remember me")
    # BooleanField 复选框，值被处理为TRUE或者FALSE
    submit = SubmitField('Log in')
    # SubmitField 提交按钮


# 行内验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField()

    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError("Must be 42")


class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'])])
    # 检测文件类型
    submit = SubmitField()


class MultiUploadForm(FlaskForm):
    photo = FileField('Upload Image', validators={DataRequired()})
    # DataRequired 确保包含文件
    submit = SubmitField()


class RichTextForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')


class SignForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 28)])
    submit1 = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254)])
    password = StringField('Password', validators=[DataRequired(), Length(8,128)])
    submit2 = SubmitField("Register")


class SignForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 28)])
    submit1 = SubmitField('Sign in')

class RegisterForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = StringField('Password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField("Register")
