from flask import Flask, url_for, request, redirect, make_response, Markup, render_template # 从 flask 包导入 Flask类
# 这个类表示一个Flask程序，实例化这个类，就得到我们的程序实例app
# 传入Flask类构造方法的第一个参数是模块或者包的名称。
# 使用特殊变量 __name__ Python会根据所处的模块来赋予 __name__ 变量相应的值
from urllib.parse import urlparse, urljoin  # URL 安全性处理

app = Flask(__name__, template_folder='../templates')


# 注册路由
# 1、浏览器输入URL请求访问某个资源
# 2、Flask接收用户请求并分析URL
# 3、为这个URL找到对应的处理函数
# 4、执行函数并生成响应，返回给浏览器
# 5、浏览器接收并解析响应，将信息显示在页面中
# 可以为一个视图函数绑定多个URL
@app.route('/')
@app.route('/hello')
def hello_world():  # put application's code here
    name = request.args.get('name', 'Flask')
    # 输入‘http://127.0.0.1:5000/hello?name=Grey’
    # 提取出所要查询的 name ，如果没有？以及之后的数据，则默认显示 ‘Flask’
    # args返回字典键值对，如果直接使用request.args['name'],如果没有对应的名为name的键，则返回错误
    # 所以使用get()方法获取数据，如果没有对应值则返回None；get方法的第二个参数设置默认值
    return '<h2>Hello Flask!<h2>' \
           f'<h2>request name is {Markup.escape(name)}<h2>'  # 这种情况下再去执行下面的那条地址，则只会把name后面的东西原封不动的输出
    # 即利用escape函数对用户传入的数据进行了转义，转义并不能避免所有xss攻击，还需要对用户输入数据进行类型验证（第四章）
    # f'<h2>request name is {name}<h2>'
    # 这种输出的话，如果输入'http://127.0.0.1:5000/hello?name=<script>Ealert('Bingo!');</script>'
    # 则会执行alert，显示bingo的弹窗，也就意味着也可以执行其他JavaScript语句
    # 为防范XSS攻击，对用户输入内容进行HTML转义 使用 Jinja2 提供的 escape 函数对用户传入的数据进行转义


# 为函数附加 app.route()装饰器，并传入URL规则做为参数，使得URL与函数相关联
# 此函数称为视图函数
# 可以为URL中添加变量部分 <变量名>
# @app.route('/greet',defaults = {'name' : 'Programmer'})
# 效果等同于在greet函数上设置默认name参数
# @app.route('/greet')
@app.route('/greet/<name>/<year>')
def Greet(name='Programmer', year='18'):  # ‘/greet’的时候默认为‘Programmer’，‘/greet/xxx’的时候为自定义name
    url_string = url_for('Greet', name=f'{name}', year=f'{year}')
    return f'<h2>动态URL，在URL中使用变量为：{name}! <h2> ' \
           f'<h2>url_for函数的应用：{url_string} <h2>'


@app.route('/goback/<int:year>')
def go_back(year):
    # route中的int与year直接不能用空格
    return f'<p>Welcome to {year - 15} <p>'


@app.route('/colors/<any(blue,white,red):color>')
def three_colors(color):
    return f'<p>The color is {color} Love is patient and kind. Love is not jealous or boastful or proud or rude. <p>'
    # color字段需要使用三个可选值之一才不报错


# 重定向
@app.route('/hi')
def hi():
    # return redirect(url_for('hello_world'))#重定向到HelloWorld的视图函数
    return redirect('http://www.helloflask.com')  # 重定向到指定地址


# 设置cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello_world')))
    response.set_cookie('name', name)
    return response


# HttpExercise
@app.route('/foo')
def foo():
    url_string = url_for('do_something')
    return f'<h1> Foo page </h1> <a href = {url_string} >  Do something </a>'


# 两个函数都指向 dosomething的视图链接
@app.route('/bar')
def bar():
    url_string = url_for('do_something')
    return f'<h1> Bar page </h1> <a href = {url_string} >  Do something </a>'


@app.route('/do_something')
def do_something():
    # do something
    return redirect_back()


def redirect_back(default='hello_world', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            # 检测是否为安全URL
            return redirect(target)
            # 返回上一个页面的地址（此地址存在于 request的args字典的next键的对应值中
            # 或者 referrer字段中（防火墙软件或者浏览器可能会自动清除、修改referrer））
    return redirect(url_for(default, **kwargs))  # 如果没有找到，默认返回hello_world视图函数界面


# 但是 next参数 可以以查询字符串的方式写在URL里，所以任何人都可以发给某个用户一个包含next变量指向任何站点的链接
# ‘http://127.0.0.1:5000/do_something?next=http://helloflask.com’将会返回helloflask网站
#  所以要验证URL的安全性
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    # 通过 host_url 获取程序内主机 URl
    # 接收 target 做目标 URL
    test_url = urlparse(urljoin(request.host_url, target))
    # 连接两个参数的url, 将第二个参数中缺的部分用第一个参数的补齐, 如果第二个有完整的路径，则以第二个为主。
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
    # urlparse 六个字段：其中 scheme 是协议  netloc 是域名服务器  path 相对路径  params是参数，query是查询的条件


# 异步加载长文章示例
from jinja2.utils import generate_lorem_ipsum


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    # 生成两段随机文本（ n 参数指定段落数量，默认为 5 ）
    return '''<h1>A very long post</h1>
              <div class = "body"> %s </div>
              <button id = 'load'> Load More </button>
              <script src = 'https://code.jquery.com/jquery-3.3.1.min.js'></script>
              <script type = 'text/javascript'>
              $(function() {
                $('#load').click(function() {
                   $.ajax({
                    url: '/more', //目标URL
                    type: 'get', //请求方法
                    success: function(data){ //返回2xx响应之后触发回调函数
                       $('.body').append(data); //将返回的响应插入到页面中
                    }
                  })
                })
              })
              </script>
              ''' % post_body


@app.route('/more')
def load_post():
    # 点击 load more 之后，在执行/more的视图函数，返回一段随机文本 插入到 post界面中
    return generate_lorem_ipsum(n=1)


@app.route('/test')
def test():
    return render_template('Blili_test_templates/login8.html')


if __name__ == '__main__':
    app.run(debug=True)
