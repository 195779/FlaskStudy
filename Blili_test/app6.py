from flask import Flask, url_for, render_template, request, abort, redirect

'''
Flask 重定向和错误
（表单的定义依然位于HTML中）
'''

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    return render_template('Blili_test_templates/app6.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # 如果 post 提交时数据
        # 注意格式为 : request.form['xxx']  获得 name 为 xxx 的提交的 text 类型的数据
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
            # 返回401，放弃
    elif request.method == "GET":
        # 如果为 GET 请求，转入index视图
        return redirect(url_for('index'))


@app.route('/success')
def success():
    return 'logged in successfully'


if __name__ == '__main__':
    Flask.run(debug=True)
