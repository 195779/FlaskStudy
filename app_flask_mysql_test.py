"""
encoding ：UTF-8
flask_mysql_test 实例演示
"""
from flask import Flask, request, flash, redirect, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
from Blili_test.form11 import ContactForm

app = Flask(__name__)
# 设置数据库链接地址
DB_URI = "mysql+pymysql://root:123456@localhost:3306/flask_study"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 是否追踪数据库修改，一般不开启，会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 不需要commit 自动保存, 默认False(防止忘记写commit提交)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

secretKey = os.urandom(32)
app.config['SECRET_KEY'] = secretKey
# 涉及的表单的提交（WTF），为防止CSRF攻击，必须要提供secretKey（否则会报错提醒）

db = SQLAlchemy(app)


class contact(db.Model):
    # Flask中使用mysql作为数据库，在py文件中创建表格（类）的方法比直接在本地mysql中创建表格要方便得多
    # 主要方便直接对table作为对象来执行操作
    id = db.Column(db.Integer, primary_key=True)
    # id为主键
    name = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    address = db.Column(db.String(100))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)
    language = db.Column(db.String(5))
    createDate = db.Column(db.Date(), default=datetime.now)
    updateDate = db.Column(db.Time(), default=datetime.now)
    # Date()  Time()  DateTime()

    def __init__(self, name, gender, address, email, age, language):
        self.name = name
        self.gender = gender
        self.address = address
        self.email = email
        self.age = age
        self.language = language


@app.route('/')
def show_all():
    contacts = contact.query.all()
    if contacts:
        for contact_test in contacts:
            print("createDate_year: "+str(contact_test.createDate.year), "type: " + str(type(contact_test.createDate.year)))
            print("createDate_month："+str(contact_test.createDate.month), "type: " + str(type(contact_test.createDate.month)))
            print("createDate_day: " +str(contact_test.createDate.day), "type: "+str(type(contact_test.createDate.day)))
            print("updateDate_hour: "+str(contact_test.updateDate.hour), "type: "+str(type(contact_test.updateDate.hour)))
            print("updateDate_minute: "+str(contact_test.updateDate.minute), "type: "+str(type(contact_test.updateDate.minute)))
            print("updateDate_minute: "+str(contact_test.updateDate.second), "type: "+str(type(contact_test.updateDate.second)))
        return render_template('app_flask_mysql_test_templates/app_flask_mysql_test_show.html', contacts=contacts)
    else:
        return render_template("app_flask_mysql_test_templates/app_flask_mysql_test_show.html",contacts=None)
    # HTML 中的 add 按钮的 target 属性改为 _self 在默认当前窗口打开链接
    # _blank 在新窗口打开链接
    # _parent 在父窗口打开链接


@app.route('/mysql_add', methods=['POST', 'GET'])
def mysql_add():
    form_mysql_add = ContactForm()
    if request.method == 'POST':
        if not form_mysql_add.validate():
            # 未通过输入检查
            flash("Not all fields are ready !")
            print('Not all fields are ready !')
            return render_template('app_flask_mysql_test_templates/app_flask_mysql_test_add.html', form=form_mysql_add)
            # 继续保持为添加界面，且保留原输入
        else:
            flash('All fields are ready !')
            print("All fields are ready ！")
            contact_Data = contact(
                form_mysql_add.name.data,
                form_mysql_add.Gender.data,
                form_mysql_add.Address.data,
                form_mysql_add.email.data,
                form_mysql_add.Age.data,
                form_mysql_add.language.data
            )
            try:
                db.session.add(contact_Data)
                db.session.commit()
                flash('All fields are posted')
                print('All fields are posted')
                return redirect(url_for('show_all'))
                # 添加成功，调回 show_all 视图，查询并显示全部
            except Exception as e:
                flash("There is an issue adding contact into db. {0}".format(e))
                return render_template('Blili_test_templates/add12.html', form=form_mysql_add)
                # 添加失败，继续保持为添加界面
    if request.method == 'GET':
        return render_template('app_flask_mysql_test_templates/app_flask_mysql_test_add.html', form=form_mysql_add)
        # 请求打开添加页面


@app.route('/delete/<int:id>')
def mysql_delete(id):
    to_delete = contact.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
    except Exception as e:
        flash("There is an issue delete contact into db. {0}".format(e))
    # 无论是否完成删除都返回显示视图
    return redirect(url_for('show_all'))


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def mysql_update(id):
    to_update = contact.query.get_or_404(id)
    form_mysql_update = ContactForm()
    if request.method == 'POST':
        if not form_mysql_update.validate():
            # 未通过输入检查
            flash("Not all fields are ready !")
            print('Not all fields are ready !')
            return render_template('app_flask_mysql_test_templates/app_flask_mysql_test_update.html', form=form_mysql_update)
            # 继续保持为添加界面，且保留原输入
        else:
            to_update.id = id
            to_update.name = form_mysql_update.name.data
            to_update.gender = form_mysql_update.Gender.data
            to_update.address = form_mysql_update.Address.data
            to_update.email = form_mysql_update.email.data
            to_update.age = form_mysql_update.Age.data
            to_update.language = form_mysql_update.language.data
            to_update.updateDate = datetime.now()
            try:
                db.session.commit()
            except Exception as e:
                flash("There is an issue update contact into db. {0}".format(e))

    if request.method == 'GET':
        form_mysql_update.id.data = to_update.id
        form_mysql_update.name.data = to_update.name
        form_mysql_update.Gender.data = to_update.gender
        form_mysql_update.Address.data = to_update.address
        form_mysql_update.Age.data = to_update.age
        form_mysql_update.language.data = to_update.language
        form_mysql_update.email.data = to_update.email
        return render_template('app_flask_mysql_test_templates/app_flask_mysql_test_update.html', form=form_mysql_update)

    return redirect(url_for('show_all'))


if __name__ == '__main__':
    app.run(debug=True)
