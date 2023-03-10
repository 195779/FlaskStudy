from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
import os

'''
Flask 文件上传实例演示
'''
app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = 'uploaddir/'
# 要先在project的目录下创建一个名为uploaddir的文件夹


@app.route('/')
def upload_file():
    return render_template('Blili_test_templates/upload10.html')


@app.route('/uploader', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        f = request.files['file111']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # 保存文件到 组成的路径
        # 文件上传到文件夹uploaddir
        return 'file uploaded successfully'
    elif request.method == 'GET':
        return render_template('Blili_test_templates/upload10.html')


if __name__ == '__main__':
    Flask.run(debug=True)
