from flask import Flask,render_template,request,flash
from form11 import ContactForm

'''Flask WTF'''

app = Flask(__name__)
app.secret_key='123456'

@app.route('/',methods=['GET','POST'])
def contact():
    form1 = ContactForm()
    if request.method == 'POST':
        if form1.validate() == False:
            flash("All fileds are required.")
            return render_template('contact11.html',form=form1)
        else:
            return render_template('success11.html')
    elif request.method == 'GET':
        return render_template('contact11.html',form=form1)

if __name__ == '__main__':
    app.run(debug=True)
