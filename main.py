from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(__file__) + '/new.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), unique=False, nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)
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
    #  TODO ADD PAGES IF GOING TO LIMIT BLOG POSTS PER PAGE
    posts = BlogPost.query.limit(9).all()
    return render_template('blog.html', posts=posts)


@app.route('/blog/<posturl>')
def post(posturl):
    post_data = BlogPost.query.filter_by(url=posturl).first()
    return render_template('blog/post.html', post=post_data)


@app.route('/admin/new-blog', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('admin/blog-editor.html')
    elif request.method == 'POST':
        post_data = BlogPost(heading=request.form["heading"], url=request.form["heading"].lower().replace(" ", "-"),
                             description=request.form["description"], content=request.form["content"],
                             image=request.form["image"])

        db.session.add(post_data)
        db.session.commit()

        return redirect(url_for("post", posturl=post_data.url))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        print(request.form["email"])
        print(request.form["password"])
        return redirect(url_for("home"))


@app.route('/uploads')
def uploads():
    pics = os.listdir('uploads/')
    return render_template('admin/uploads.html', pics=pics)


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
        return render_template('admin/upload.html')


if __name__ == '__main__':
    app.run(debug=True)
