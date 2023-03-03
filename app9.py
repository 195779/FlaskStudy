from flask import Flask,flash,redirect,\
    render_template,request,url_for
'''Flask 消息闪现'''
app = Flask(__name__)
app.secret_key='123456'

@app.route('/')
def index():
    return render_template('app8.html')

@app.route('/login',methods=['POST','GET'])
def login():
    errormsg = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            errormsg = "Invalid username or password.Please try again!"
        else:
            flash('You are successfully logged in')
            return redirect(url_for('index'))
    # GET 或者 POST 中username与password不全为admin
    return render_template('login8.html',error = errormsg)

if __name__ == '__main__':
    Flask.run(debug=True)
