from flask import render_template
from flask import request
from flask import Flask,session,redirect,url_for,request
'''Flask Sessions 会话'''

app = Flask(__name__)
app.secret_key = '123456'
### 加密session，sessionID存在于客户端，Session存在于服务器

@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return '登录用户名是' + user + '<br>' + "<b><a href='/logout'>点击这里注销</a></b>"
    return "您暂时未登录，<br><a href = '/login'> <b>点击这里登录</b></a>"

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        print(request.form['username'])
        # 注意都是中括号括起来的
        return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('app7.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    Flask.run(debug=True)
