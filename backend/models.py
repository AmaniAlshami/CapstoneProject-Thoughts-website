import os
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'thoughts')
DB_PATH = 'postgres://{}:{}@{}/{}'.format(DB_USER,
                                          DB_PASSWORD, DB_HOST, DB_NAME)

# to setup heroko DB
# DATABASE_URL = os.environ['DATABASE_URL'] insted of DB_PATH

db = SQLAlchemy()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    blogger = Bolgger(
        BloggerName="Amani"
    )
    blog = Blog(
        title="First",
        content=" Hello this is first blog ",
        Bolgger_id=1
    )
    visitor = Visitor(
        VisitorName='John'
    )

    blogger.insert()
    blog.insert()
    visitor.insert()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


class Bolgger(db.Model):
    __tablename__ = "Bolgger"

    id = db.Column(Integer, primary_key=True)
    BloggerName = Column(String(80), nullable=False)
    Blog = db.relationship("Blog", backref="Bolgger")

    def format(self):
        return {
            'id': self.id,
            'BloggerName': self.BloggerName
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            blogger = Bolgger(BloggerName=blogger_name)
            blogger.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            blogger = Bolgger.query.filter(Bolgger.id == id).one_or_none()
            blogger.title = 'Black Coffee'
            blogger.update()
    '''

    def update(self):
        db.session.commit()


class Blog(db.Model):
    __tablename__ = "Blog"

    id = db.Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    content = Column(String(500), nullable=False)
    Bolgger_id = Column(Integer, ForeignKey('Bolgger.id'))
    Comment = db.relationship("Comment", backref="Blog")

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'Bolgger_id': self.Bolgger_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Visitor(db.Model):
    __tablename__ = "Visitor"

    id = db.Column(Integer, primary_key=True)
    VisitorName = Column(String(80), nullable=False)
    Comment = db.relationship("Comment", backref="Visitor")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Comment(db.Model):

    __tablename__ = "Comment"

    id = db.Column(Integer, primary_key=True)
    comment = Column(String(200), nullable=False)
    Visitor_id = Column(Integer, ForeignKey('Visitor.id'))
    Blog_id = Column(Integer, ForeignKey('Blog.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'Visitor_id': self.Visitor_id,
            'Blog_id': self.Blog_id
        }
