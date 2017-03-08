from flask import Flask,json
import os
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>'%self.name
    def to_json(self):
        return {"id": self.id,
                    "name": self.name,
                    "age": self.age}

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Post %r>' % self.title

    def to_json(self):
        return {"id": self.id,
                "title": self.title,
                "text": self.text}
@app.route('/users')
def users():
    users = User.query.all()
    return json.dumps([user.to_json() for user in users])
@app.route('/posts')
def posts():
    posts = Post.query.all()
    return json.dumps([post.to_json() for post in posts])

if __name__=='__main__':
    manager.run()