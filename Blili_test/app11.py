from flask import Flask, render_template, request, flash
from form11 import ContactForm

'''
Flask WTF表单实例演示
'''
import os
secretKey = os.urandom(32)
app = Flask(__name__)
app.secret_key = secretKey


@app.route('/', methods=['GET', 'POST'])
def contact():
    form1 = ContactForm()
    if request.method == 'POST':
        if not form1.validate():
            # 做表单检查未通过
            flash('Exist fields are not ready.')
            print("Exist fields are not ready")
            return render_template('Blili_test/contact11.html', form=form1)
            # 由于此处 form=form1，所以已经填好的值如果不需要修改则不需要重新填写，它不会被删掉
        else:
            flash("All fields are ready.")
            print("All fields are ready")
            return render_template('Blili_test/success11.html')
    elif request.method == 'GET':
        return render_template('Blili_test/contact11.html', form=form1)


if __name__ == '__main__':
    app.run(debug=True)
