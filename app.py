from flask import Flask, url_for, request,redirect,make_response # 从 flask 包导入 Flask类
# 这个类表示一个Flask程序，实例化这个类，就得到我们的程序实例app
# 传入Flask类构造方法的第一个参数是模块或者包的名称。
# 使用特殊变量 __name__ Python会根据所处的模块来赋予 __name__ 变量相应的值
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
           f'<h2>request name is {name}<h2>'
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

if __name__ == '__main__':
    app.run(debug = True)
