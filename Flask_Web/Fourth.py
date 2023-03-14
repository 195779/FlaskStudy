import uuid

from flask import Flask, send_from_directory, render_template, redirect, url_for, request, flash, session, \
    make_response, Markup
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

from Fourth_Forms import LoginForm, UploadForm, MultiUploadForm, \
    RichTextForm, NewPostForm, SignForm, RegisterForm, SignForm2, RegisterForm2
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.secret_key = os.urandom(32)


@app.route('/postSuccess')
def postSuccess():
    return render_template('Flask_Web_templates/Flask_Web_4/postsuccess.html')


@app.route('/index', methods=["POST", "GET"])
@app.route('/basic', methods=["POST", "GET"])
def basic():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        return redirect(url_for('postSuccess'))
    else:
        return render_template('Flask_Web_templates/Flask_Web_4/basic.html', form=form)


@app.route('/bootstrap', methods=["POST", "GET"])
def bootstrap():
    form = LoginForm()
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home %s!' % username)
        # base.html 中 在 block content 之前接收了 flash 的 messages 则会显示在其之前
        return redirect(url_for('postSuccess'))
    else:
        return render_template("Flask_Web_templates/Flask_Web_4/bootstrap.html", form=form)


# app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
# 设置报文大小


app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=["POST", "GET"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success!')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))

    return render_template('Flask_Web_templates/Flask_Web_4/upload.html', form=form)


@app.route('/upload/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('Flask_Web_templates/Flask_Web_4/uploaded.html')


app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/multi_upload', methods=["GET", "POST"])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        # 验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))
        # 检查文件是否存在
        photos = request.files.getlist('photo')
        if not photos[0].filename:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))

        for f in photos:
            # 检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file type')
                return redirect(url_for("multi_upload"))
        flash('Upload success')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    else:
        return render_template('Flask_Web_templates/Flask_Web_4/upload.html', form=form)


from flask_ckeditor import CKEditor

ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400


# 使用内置本地资源


@app.route('/ckeditor', methods=['GET', 'POST'])
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published!')
        return render_template('Flask_Web_templates/Flask_Web_4/post.html', title=title, body=body)
    return render_template('Flask_Web_templates/Flask_Web_4/ckeditor.html', form=form)


@app.route('/two-submits', methods=['POST', "GET"])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        if form.save.data:
            flash("You click the 'Save' button")
        elif form.publish.data:
            flash("You save the 'Publish' button")
            return render_template('Flask_Web_templates/Flask_Web_4/post.html', title=title, body=body)
    return render_template("Flask_Web_templates/Flask_Web_4/2submit.html", form=form)


@app.route('/multi-form', methods=["POST", "GET"])
def multi_form():
    signIn_Form = SignForm()
    register_Form = RegisterForm()

    if signIn_Form.submit1.data and signIn_Form.validate_on_submit():
        username_sign = signIn_Form.username.data
        nameString_sign = "the sign_in username is : %s " % username_sign
        flash(nameString_sign)
    if register_Form.submit2.data and register_Form.validate_on_submit():
        username_register = register_Form.username.data
        nameString_register = "the  register username is : %s " % username_register
        flash(nameString_register)
    return render_template("Flask_Web_templates/Flask_Web_4/2Form.html",
                           register_form=register_Form, signIn_form=signIn_Form)



@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signIn_form = SignForm2()
    register_form = RegisterForm2()

    return render_template('Flask_Web_templates/Flask_Web_4/2form2view.html', signIn_form=signIn_form, register_form=register_form)


@app.route('/handle-signin', methods=["POST"])
def handle_signin():
    signIn_form = SignForm2()
    register_form = RegisterForm2()

    if signIn_form.validate_on_submit():
        username = signIn_form.username.data
        flash('%s, you just submit the SignIn Form.' % username)
        return redirect(url_for('integrate_ckeditor'))
    return render_template('Flask_Web_templates/Flask_Web_4/2form2view.html', signIn_form=signIn_form, register_form=register_form)


@app.route('/handle-register', methods=["POST"])
def handle_register():
    signIn_form = SignForm2()
    register_form = RegisterForm2()

    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        return redirect(url_for('integrate_ckeditor'))
    return render_template('Flask_Web_templates/Flask_Web_4/2form2view.html', signIn_form=signIn_form, register_form=register_form)



if __name__ == '__main__':
    Flask.run(debug=True)
