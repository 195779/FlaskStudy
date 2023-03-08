from flask import Flask,redirect,url_for
'''Flask URL 构建与简单重定向'''

app = Flask(__name__)


@app.route('/admin/')
def hello_admin():
    return 'Hello Admin'


@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))
    # 如果输入的name == admin 则重定向到hello_admin视图
    # 否则，重定向到hello_guest视图，并将user的name赋给guest


if __name__ == '__main__':
    Flask.run(debug=True)