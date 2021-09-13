import os
from sqlalchemy import Column, String, Integer, relationship , ForeignKey
from flask_sqlalchemy import SQLAlchemy


DB_HOST = os.getenv('DB_HOST', 'localhost:5432')  
DB_USER = os.getenv('DB_USER', '')  
DB_PASSWORD = os.getenv('DB_PASSWORD', '')  
DB_NAME = os.getenv('DB_NAME', 'thoughts')  
DB_PATH = 'postgres://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



class Bolgger(db.Model):
    __tablename__ = "Bolgger"

    id = db.Column(Integer, primary_key=True)
    BlogerName = Column(String(80), nullable=False)
    Blog = relationship("Post", backref="Bolgger")
    children = relationship("Comment", backref="Bolgger")

class Blog(db.Model):
    __tablename__ = "Blog"

    id = db.Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    Blog = Column(String(500), nullable=False)
    Bolgger_id = Column(Integer, ForeignKey('Bolgger.id'))
    Comment = relationship("Comment", backref="Blog")

  

class Comment(db.Model):

    __tablename__ = "Comment"

    id = db.Column(Integer, primary_key=True)
    comment = Column(String(200), nullable=False)
    Bolgger_id = Column(Integer, ForeignKey('Bolger.id'))
    Blog_id = Column(Integer, ForeignKey('Blog.id'))


##TODO:format data 