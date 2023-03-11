import uuid

from flask import Flask, send_from_directory, render_template, redirect, url_for, request, flash, session, make_response, Markup
from Fourth_Forms import LoginForm, UploadForm
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


app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
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


if __name__ == '__main__':
    Flask.run(debug=True)
