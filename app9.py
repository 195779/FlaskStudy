from flask import Flask,flash,redirect,\
    render_template,request,url_for
'''Flask 消息闪现'''
import os
secretKey = os.urandom(32)
app = Flask(__name__)
app.secret_key = secretKey


@app.route('/')
def index():
    return render_template('app8.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    errorMessage = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            errorMessage = "username或password 不为 'admin' "
            print(errorMessage)
        else:
            flash("用户名与密码都为 'admin' ,登录成功 You are successfully logged in")
            return redirect(url_for('index'))

    return render_template('login8.html', error=errorMessage)
    # GET 或者 POST 中username与password不全为admin的时候，返回login8.html,给error变量赋值errorMessage


if __name__ == '__main__':
    Flask.run(debug=True)
