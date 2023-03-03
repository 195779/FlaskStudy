from flask import Flask, url_for, render_template, request, abort, redirect

'''Flask 重定向和错误'''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('app6.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        # 注意格式为 : request.form['xxx']  获得 name 为 xxx 的提交的 text 类型的数据
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
    elif request.method == "GET":
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return 'logged in successfully'

if __name__ == '__main__':
    Flask.run(debug=True)
