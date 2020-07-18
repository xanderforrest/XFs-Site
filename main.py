from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from utilities import ContentManager
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

CM = ContentManager()
UPLOAD_FOLDER = os.path.join("uploads", "images")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "Hello"


@app.route('/blog')
def blog():
    posts = CM.get_posts()
    return render_template('blog.html', posts=posts)


@app.route('/blog/<blogid>')
def post(blogid):
    post_data = CM.get_post(blogid)
    return render_template('post.html', post=post_data)


@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('blogbuilder.html')
    elif request.method == 'POST':
        id = CM.add_post(request.form.to_dict())
        if id:
            return redirect(url_for("post", blogid=id))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/uploads/image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("file not in post req")
            return "error"
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return "error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file', filename=filename))
    if request.method == 'GET':
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
