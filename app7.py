from flask import Flask,make_response,request
'''Flask Cookies'''

app = Flask(__name__)

@app.route('/set_cookies')
def set_cookie():
    resp = make_response('success')
    resp.set_cookie('aaa_key','aaa_value',max_age = 3600)
    return resp

@app.route('/get_cookies')
def get_cookie():
    cookie_1 = request.cookies.get('aaa_key')
    return cookie_1

@app.route('/delete_cookies')
def del_cookie():
    resp = make_response('del_success')
    resp.delete_cookie('aaa_key')
    return resp

if __name__ == '__main__':
    Flask.run(debug=True)
