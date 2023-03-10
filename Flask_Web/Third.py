from flask import Flask,render_template,url_for,redirect,request,make_response
"""
第三章 模板
"""

app = Flask(__name__)


# 创建模板
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
    return render_template('Flask_Web/watchlist.html', user=user, movies=movies)


# 注册模板上下文处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo=foo)  # 等价于 return {'foo' : foo}


# 当我们调用 render_template()函数渲染任意一个模板的时候，所有使用 app.context_processor 修饰器注册的
# 模板上下文函数都会被执行，这些函数的返回值会被添加进 模板 中，因此我们可以在模板中直接使用 foo 变量
# 还可以将其作为方法调用： app.contxt_processor(inject_foo)  # inject_foo 即前面的 inject_foo 函数
# 另外如果不写函数，而是写 lambda表达式 ，则为 ： app.context_processor(lambda: dict(foo = 'I am foo.'))

# 全局对象
# Jinja2 内置模板全局函数
# range([start,stop[,step]) # 与python的range用法相同
# lipsum(n=5,html=True,min=20,max=100)
# 生成随机文本，共5段，每段包含20-100个单词
# dict(**items) ## 与python中的dict()用法相同
# Flask内置模板全局函数
# url_for()               生成url的函数
# get_flashed_messages() 获取flash消息函数

# 自定义全局函数
# 修饰器： app.template_global 直接将函数注册为模板全局函数
@app.template_global
def bar():
    return 'I am bar'


# 将bar函数注册为全局函数
# 同样也可以直接调用，以函数名为参数，或者使用lambda表达式


# 过滤器
# 修改和过滤变量值的特殊函数，过滤器与变量用一个竖线（管道符号）隔开，需要参数的过滤器可以像函数一样使用括号传递
# {{movies | length}}  获取movies列表的长度
# {{name | title }} 将name变量标题化，相当于调用name.title()
# 转换为大写
# {% filter upper %}
#     This text becomes uppercase.
# {% endfilter %}
# 过滤器可以叠加使用 <h1> Hello,{{ name|default('陌生人')|title }} ! </h1>
# 自定义过滤器,与注册全局函数相似 @app.template_filter()

# 测试器 使用 is 链接变量和测试器
# {% if age is number %}
#     {{ age * 365 }}
# {% else %}
#     无效的数字
# {% endif %}
# 自定义测试器 @app.template_test()
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


if __name__ == '__main__':
    Flask.run(debug=True)
