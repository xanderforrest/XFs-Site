from flask import Flask, session, render_template, request, url_for, redirect, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(__file__) + '/new.db'
app.secret_key = b'\x97E\x81-\xb0\xe8M\xee\xdc0\xaf~\x10\xa9j{'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)


BCRYPT_LOG_ROUNDS = 12
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    _password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


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


if __name__ == '__main__':
    app.run(debug=True)
