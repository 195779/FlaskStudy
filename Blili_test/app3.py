from flask import Flask,render_template

'''
Flask 静态文件
'''

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('app3.html')


if __name__ == '__main__':
    app.run(debug=True)