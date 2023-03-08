from flask import Flask, url_for,request,redirect,Markup

'''
Flask 路由 
encoding : UTF-8
'''

app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>This is the index page<h2>"


@app.route('/url_test/<name>')
def url_test_name(name):
    return f'The url_test name is {name}'


@app.route('/url_test/<int:intId>')
def url_test_integer(intId):
    # route中的int与year直接不能用空格
    return f'The url_test integer is {intId}'


@app.route('/url_test/<float:floatId>')
def url_test_float(floatId):
    return 'The url_test float is %.3f' % floatId


@app.route('/colors/<any(blue,white,red):color>')
def three_colors(color):
    return f'<p>The color is {color} ! Love is patient and kind. Love is not jealous or boastful or proud or rude. <p>'
    # color字段需要使用三个可选值之一才不报错


@app.route('/default_body')
@app.route('/default_body/<name>/<year>')
def default_body(name='Programmer', year='18'):
    # ‘/greet’的时候默认为‘Programmer’，‘/greet/xxx’的时候为自定义name
    # year 字段也同理
    url_string = url_for('default_body', name=f'{name}', year=f'{year}')
    return f'<h2>动态URL，在URL中使用变量为：{name} 、 {year} ! <h2> ' \
           f'<h2>url_for函数的应用：{url_string} <h2>'


@app.route('/hello_request')
def hello_request():
    name = request.args.get('name', 'Flask')
    # 输入‘http://127.0.0.1:5000/hello_request?name=Grey’
    # 提取出所要查询的 name ，如果没有？以及之后的数据，则默认显示 ‘Flask’
    # args返回字典键值对，如果直接使用request.args['name'],如果没有对应的名为name的键，则返回错误
    # 所以使用get()方法获取数据，如果没有对应值则返回None；get方法的第二个参数设置默认值
    return '<h2>Hello Flask!<h2>' \
           f'<h2>request name is {Markup.escape(name)}<h2>'  # 这种情况下再去执行下面的那条地址，则只会把name后面的东西原封不动的输出
    # 即利用escape函数对用户传入的数据进行了转义，转义并不能避免所有xss攻击，还需要对用户输入数据进行类型验证（第四章）


@app.route('/hello_requestWrong')
def hello_requestWrong():
    name = request.args.get('name','Flask')
    return f'<h2>request name is {name} <h2>'
    # 如果输入'http://127.0.0.1:5000/hello_requestWrong?name=<script>alert('Bingo!');</script>'
    # 则会执行alert，显示bingo的弹窗，也就意味着也可以执行其他JavaScript语句
    # 为防范XSS攻击，对用户输入内容进行HTML转义 使用 Jinja2 提供的 escape 函数对用户传入的数据进行转义


@app.route('/flask')
def return_flask():
    return "<h2>如果路由的地址最后没有斜杠 ： 则只有输入该完整路由时 才启动<h2>"


@app.route('/python/')
def return_python():
    return '<h2>如果路由的地址最后有斜杠，则无论输入路由地址是否含有最后一个斜杠均可启动<h2>'


if __name__ == '__main__':
    Flask.run(debug=True, threaded=True)
    # 默认host为'127.0.0.1'，仅本机可访问
    # port：端口，默认为5000
    # debug:是否进入debug模式
    # threaded:是否使用线程处理并发请求
