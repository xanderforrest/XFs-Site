from flask import Flask, session, render_template, request, url_for, redirect, send_from_directory, flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
import os
from main import app, allowed_file
from models import BlogPost, User
from config import app, db, UPLOAD_FOLDER


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


@app.route('/admin')
def admin():
    return render_template('admin.html')


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
        user = User.query.filter_by(email=request.form["email"]).first_or_404()
        if user.is_correct_password(request.form["password"]):
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/uploads')
@login_required
def uploads():
    pics = os.listdir('uploads/')
    return render_template('admin/uploads.html', pics=pics)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
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
