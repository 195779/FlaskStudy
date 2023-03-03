from flask import Flask, url_for, request,redirect,make_response,Markup # 从 flask 包导入 Flask类
# 这个类表示一个Flask程序，实例化这个类，就得到我们的程序实例app
# 传入Flask类构造方法的第一个参数是模块或者包的名称。
# 使用特殊变量 __name__ Python会根据所处的模块来赋予 __name__ 变量相应的值
from urllib.parse import urlparse,urljoin # URL 安全性处理
app = Flask(__name__)

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
    name = request.args.get('name','Flask') # 输入‘http://127.0.0.1:5000/hello?name=Grey’
    # 提取出所要查询的 name ，如果没有？以及之后的数据，则默认显示 ‘Flask’
    # args返回字典键值对，如果直接使用request.args['name'],如果没有对应的名为name的键，则返回错误
    # 所以使用get()方法获取数据，如果没有对应值则返回None；get方法的第二个参数设置默认值
    return '<h2>Hello Flask!<h2>' \
           f'<h2>request name is {Markup.escape(name)}<h2>' # 这种情况下再去执行下面的那条地址，则只会把name后面的东西原封不动的输出
    # 即利用escape函数对用户传入的数据进行了转义，转义并不能避免所有xss攻击，还需要对用户输入数据进行类型验证（第四章）
    # f'<h2>request name is {name}<h2>'
    # 这种输出的话，如果输入'http://127.0.0.1:5000/hello?name=<script>Ealert('Bingo!');</script>'
    # 则会执行alert，显示bingo的弹窗，也就意味着也可以执行其他JavaScript语句
    # 为防范XSS攻击，对用户输入内容进行HTML转义 使用 Jinja2 提供的 escape 函数对用户传入的数据进行转义
# 为函数附加 app.route()装饰器，并传入URL规则做为参数，使得URL与函数相关联
# 此函数称为视图函数
# 可以为URL中添加变量部分 <变量名>
#@app.route('/greet',defaults = {'name' : 'Programmer'})
# 效果等同于在greet函数上设置默认name参数
#@app.route('/greet')
@app.route('/greet/<name>/<year>')
def Greet(name = 'Programmer',year = '18'): # ‘/greet’的时候默认为‘Programmer’，‘/greet/xxx’的时候为自定义name
    url_string = url_for('Greet', name = f'{name}',year = f'{year}')
    return f'<h2>动态URL，在URL中使用变量为：{name}! <h2> ' \
           f'<h2>url_for函数的应用：{url_string} <h2>'


@app.route('/goback/<int:year>')
def go_back(year):
    ### route中的int与year直接不能用空格
    return f'<p>Welcome to {year-15} <p>'

@app.route('/colors/<any(blue,white,red):color>')
def three_colors(color):
    return f'<p>The color is {color} Love is patient and kind. Love is not jealous or boastful or proud or rude. <p>'
#### color字段需要使用三个可选值之一才不报错

### 重定向
@app.route('/hi')
def hi():
    #return redirect(url_for('hello_world'))#重定向到HelloWorld的视图函数
    return redirect('http://www.helloflask.com') #重定向到指定地址

### 设置cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello_world')))
    response.set_cookie('name',name)
    return response


### HttpExercise
@app.route('/foo')
def foo():
    url_string = url_for('do_something')
    return f'<h1> Foo page </h1> <a href = {url_string} >  Do something </a>'
#两个函数都指向 dosomething的视图链接
@app.route('/bar')
def bar():
    url_string  = url_for('do_something')
    return f'<h1> Bar page </h1> <a href = {url_string} >  Do something </a>'
@app.route('/do_something')
def do_something():
    # do something
    return redirect_back()

def redirect_back(default = 'hello_world' , **kwargs):
    for target in request.args.get('next'),request.referrer :
        if not target:
            continue
        if is_safe_url(target):
            # 检测是否为安全URL
            return redirect(target)
            # 返回上一个页面的地址（此地址存在于 request的args字典的next键的对应值中
            # 或者 referrer字段中（防火墙软件或者浏览器可能会自动清除、修改referrer））
    return redirect(url_for(default,**kwargs)) # 如果没有找到，默认返回hello_world视图函数界面
# 但是 next参数 可以以查询字符串的方式写在URL里，所以任何人都可以发给某个用户一个包含next变量指向任何站点的链接
# ‘http://127.0.0.1:5000/do_something?next=http://helloflask.com’将会返回helloflask网站
#  所以要验证URL的安全性
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    ### 通过 host_url 获取程序内主机 URl
    ### 接收 target 做目标 URL
    test_url = urlparse(urljoin(request.host_url,target))
    # 连接两个参数的url, 将第二个参数中缺的部分用第一个参数的补齐, 如果第二个有完整的路径，则以第二个为主。
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc
    # urlparse 六个字段：其中 scheme 是协议  netloc 是域名服务器  path 相对路径  params是参数，query是查询的条件


### 异步加载长文章示例
from jinja2.utils import generate_lorem_ipsum
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n = 2) ## 生成两段随机文本（ n 参数指定段落数量，默认为 5 ）
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
    return generate_lorem_ipsum(n = 1)


### 第三章 模板
#### 创建模板
from flask import render_template
user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html',user = user,movies = movies)

#### 注册模板上下文处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo = foo) # 等价于 return {'foo' : foo}
#### 当我们调用 render_template()函数渲染任意一个模板的时候，所有使用 app.context_processor 修饰器注册的
#### 模板上下文函数都会被执行，这些函数的返回值会被添加进 模板 中，因此我们可以在模板中直接使用 foo 变量
#### 还可以将其作为方法调用： app.contxt_processor(inject_foo)  # inject_foo 即前面的 inject_foo 函数
#### 另外如果不写函数，而是写 lambda表达式 ，则为 ： app.context_processor(lambda: dict(foo = 'I am foo.'))

#### 全局对象
#### Jinja2 内置模板全局函数
#### range([start,stop[,step]) # 与python的range用法相同
#### lipsum(n=5,html=True,min=20,max=100) ##生成随机文本，共5段，每段包含20-100个单词
#### dict(**items) ## 与python中的dict()用法相同
#### Flask内置模板全局函数
#### url_for()               生成url的函数
#### get_flashed_messages() 获取flash消息函数

#### 自定义全局函数
# 修饰器： app.template_global 直接将函数注册为模板全局函数
@app.template_global
def bar():
    return 'I am bar'
# 将bar函数注册为全局函数
# 同样也可以直接调用，以函数名为参数，或者使用lambda表达式


### 过滤器
#### 修改和过滤变量值的特殊函数，过滤器与变量用一个竖线（管道符号）隔开，需要参数的过滤器可以像函数一样使用括号传递
# {{movies | length}}  获取movies列表的长度
# {{name | title }} 将name变量标题化，相当于调用name.title()
# 转换为大写
# {% filter upper %}
#     This text becomes uppercase.
# {% endfilter %}
# 过滤器可以叠加使用 <h1> Hello,{{ name|default('陌生人')|title }} ! </h1>
#### 自定义过滤器,与注册全局函数相似 @app.template_filter()

#### 测试器 使用 is 链接变量和测试器
#### {% if age is number %}
####     {{ age * 365 }}
#### {% else %}
####     无效的数字
#### {% endif %}
#### 自定义测试器 @app.template_test()
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


if __name__ == '__main__':
    app.run(debug = True)

