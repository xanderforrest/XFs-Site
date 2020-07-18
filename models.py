from main import db
from datetime import datetime


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<BlogPost %r>' % self.heading
