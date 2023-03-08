from flask import Flask, make_response, request,redirect,url_for

'''Flask Cookies 演示实验'''

app = Flask(__name__)


@app.route('/hello_cookies')
def hello_cookies():
    return '<h3>this is the test of hello_cookies ! <h3>'


@app.route('/set_cookies')
def set_cookie():
    resp = make_response(redirect(url_for('hello_cookies')))
    resp.set_cookie('aaa_key', 'aaa_value', max_age=3600)
    # 设置key、value、cookie被保存的最长时间为3600秒
    return resp
    # 当make_response('success') 时 页面会显示 'success'
    # 当make_response(redirect(url_for('hello_cookies'))) 时会跳转到hello_cookies 的视图
    # cookies的内容与'success'时保持一致


@app.route('/get_cookies')
def get_cookie():
    cookie_1 = request.cookies.get('aaa_key')
    return cookie_1
    # 返回显示 'aaa_value'

@app.route('/delete_cookies')
def del_cookie():
    resp = make_response('del_success')
    resp.delete_cookie('aaa_key')
    return resp
    # 返回显示 'del_success'


if __name__ == '__main__':
    Flask.run(debug=True)
