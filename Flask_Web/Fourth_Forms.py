from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, Length, ValidationError


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
    submit = SubmitField()
