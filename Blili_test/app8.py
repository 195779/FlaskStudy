from flask import render_template
from flask import request
from flask import Flask,session,redirect,url_for,request
'''Flask Sessions 会话'''

import os

app = Flask(__name__)
secretKey = os.urandom(32)
app.secret_key = secretKey
# 生成随机数加密session，sessionID存在于客户端，Session存在于服务器


@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return '登录用户名是' + user + '<br>' + "<b><a href='/logout'>点击这里注销</a></b>"
        # 如果session中已经存在该username，则执行点击注销将执行logout视图，从session中删除username，然后转回index视图
    return "您暂时未登录，<br><a href = '/login'> <b>点击这里登录</b></a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 提交username：将username写入session中，返回index视图
        session['username'] = request.form['username']
        print(request.form['username'])
        # 注意都是中括号括起来的
        return redirect(url_for('index'))

    elif request.method == 'GET':
        # 请求服务：返回app7.html
        return render_template('Blili_test/app7.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    Flask.run(debug=True)
