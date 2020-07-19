from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from utilities import ContentManager
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(__file__) + '/new.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<BlogPost %r>' % self.heading


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    print(BlogPost.query.all())
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/services/websites')
def websites():
    return render_template('services/websites.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/blog')
def blog():
    posts = BlogPost.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/blog/post')
def testroute():
    test_data = {"heading": "Miraculous Flask Website in 5 Steps!", "date": "20th July", "image": "test.png", "content": "<p>CONTENT REEEE</p>"}
    return render_template('blog/post.html', post=test_data)


@app.route('/blog/<blogid>')
def post(blogid):
    post_data = CM.get_post(blogid)
    return render_template('post.html', post=post_data)


@app.route('/admin/new-blog', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('admin/blog-editor.html')
    elif request.method == 'POST':
        data = request.form.to_dict()

        id = CM.add_post(request.form.to_dict())
        if id:
            return redirect(url_for("post", blogid=id))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/upload', methods=['GET', 'POST'])
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
