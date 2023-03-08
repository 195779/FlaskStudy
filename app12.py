"""
encoding ：UTF-8
sqlalchemy 实例演示
"""
from flask import Flask, request, flash, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
from form11 import ContactForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contacts.db"
secretKey = os.urandom(32)
app.config['SECRET_KEY'] = secretKey

db = SQLAlchemy(app)


# 实现一个数据库实例


class ContactDAO(db.Model):
    # 绑定数据库表
    id = db.Column(db.Integer, primary_key=True)
    # id为主键
    name = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    address = db.Column(db.String(100))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)
    language = db.Column(db.String(5))
    data_created = db.Column(db.DateTime, default=datetime.now)

    # 默认值为本地时间 datetime.now 获取 python 环境自带的本地当前时间

    def __init__(self, name, gender, address, email, age, language, data_created):
        self.name = name
        self.gender = gender
        self.address = address
        self.email = email
        self.age = age
        self.language = language
        self.data_created = data_created


@app.route('/')
def show_all():
    return render_template('show12.html', contacts=ContactDAO.query.all())
    # 查询所有记录并显示


@app.route('/add', methods=['POST', 'GET'])
def do_add():
    form1 = ContactForm()
    if request.method == 'POST':
        if not form1.validate():
            # 未通过输入检查
            flash("All fields are not ready.")
            print("All fields are not ready")
            return render_template("add12.html", form=form1)
            # 继续保持为添加界面，且保留原输入
        else:
            contact = ContactDAO(form1.name.data,
                                 form1.Gender.data,
                                 form1.Address.data,
                                 form1.email.data,
                                 form1.Age.data,
                                 form1.language.data,
                                 datetime.now()
                                 )
            try:
                db.session.add(contact)
                db.session.commit()
                flash("All fields are ready. They are all added")
                print("All fields are ready. They are all added")
                return redirect('/')
                # 添加成功，调回 show_all 视图，查询并显示全部
            except Exception as e:
                flash("There is an issue adding contact into db. {0}".format(e))
                return render_template('add12.html', form=form1)
                # 添加失败，继续保持为添加界面
    if request.method == 'GET':
        return render_template('add12.html', form=form1)
        # 请求打开添加界面


@app.route('/delete/<int:id>')
def do_delete(id):
    to_delete = ContactDAO.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
    except Exception as e:
        flash("There is an issue delete contact into db. {0}".format(e))
    # 无论是否完成删除都返回显示视图
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def do_update(id):
    to_update = ContactDAO.query.get_or_404(id)
    # to_update 获取的一行，字段名均为小写
    form1 = ContactForm()

    if request.method == 'GET':
        form1.id.data = to_update.id
        form1.name.data = to_update.name
        form1.Gender.data = to_update.gender
        form1.Address.data = to_update.address
        form1.Age.data = to_update.age
        form1.language.data = to_update.language
        form1.email.data = to_update.email
        return render_template('update12.html', form=form1)

    elif request.method == 'POST':
        to_update.id = id
        to_update.name = form1.name.data
        to_update.gender = form1.Gender.data
        to_update.address = form1.Address.data
        to_update.email = form1.email.data
        to_update.language = form1.language.data
        # to_update.data_created = datetime.now()
        try:
            #db.session.update(to_update)
            db.session.commit()
            # 返回根目录显示全部
        except Exception as e:
            flash("There is an issue update contact into db. {0}".format(e))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)


