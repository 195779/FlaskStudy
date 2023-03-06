
from flask import Flask,render_template,request
from werkzeug.wrappers.response import Response
'''
Flask 将表单数据发送到模板
表单结构定义在HTML中
'''
app = Flask(__name__)


@app.route('/')
def student():
    return render_template('app5.html')


@app.route('/result',methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        rst = request.form
        # 取得表单数据
        return render_template('result5.html', result=rst)


if __name__ == '__main__':
    Flask.run(debug=True)