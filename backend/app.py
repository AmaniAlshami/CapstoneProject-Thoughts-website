import os
import sys
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
    setup_db,
    Bolgger,
    Blog,
    Comment,
    db_drop_and_create_all,
    Visitor
)
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
  @TODO uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
  !! Running this funciton will add one
  '''
    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTION')
        return response

    # GET

    # For Heroku
    @app.route('/')
    def test_hello():
        return jsonify({"welcom": "Hello World"})

    # retraive all bloggers
    @app.route('/bloggers', methods=['GET'])
    def get_bloggers():
        bolggers = Bolgger.query.all()
        formatted_bolggers = [bolgger.format() for bolgger in bolggers]

        return jsonify({
            'success': True,
            "bolggers": formatted_bolggers
        })

    # retraive all bloges

    @app.route('/blogs', methods=['GET'])
    def get_blogs():
        blogs = Blog.query.all()
        formatted_blogs = [blog.format() for blog in blogs]
        return jsonify({
            'success': True,
            "blogs": formatted_blogs
        })

    # retraive all bloges for one blogger

    @app.route('/<blogger_id>/blogs', methods=['GET'])
    def get_blogger_blog(blogger_id):
        blogger = Bolgger.query.filter(Bolgger.id == blogger_id).one_or_none()
        if blogger is None:
            abort(404)

        blogs = Blog.query.filter(Blog.Bolgger_id == blogger_id).all()
        formatted_blogs = [blog.format() for blog in blogs]

        return jsonify({
            'success': True,
            "blogs": formatted_blogs
        })

    # retraive one blog content

    @app.route('/blogs/<blog_id>', methods=['GET'])
    def get_one_blog(blog_id):
        blog = Blog.query.filter(Blog.id == blog_id).one_or_none()
        if blog is None:
            abort(404)

        blog = blog.format()

        comments = Comment.query.filter(Comment.Blog_id == blog_id).all()
        formatted_comments = [comment.format() for comment in comments]

        return jsonify({
            'success': True,
            "content": blog['content'],
            "id": blog['id'],
            "title": blog['title'],
            "comments": formatted_comments

        })

        # POST

    @app.route('/<blogger_id>/blogs', methods=['POST'])
    @requires_auth('post:blog')
    def new_blog(jwt, blogger_id):
        body = request.get_json()
        title = body.get('title')
        Content = body.get('content')

        try:
            blog = Blog(title=title, content=Content, Bolgger_id=blogger_id)
            blog.insert()
            formatted_blog = blog.format()

            return jsonify({

                'success': True,
                "blog": formatted_blog
            })

        except BaseException:
            abort(422)

    @app.route('/blogs/<blog_id>', methods=['POST'])
    @requires_auth('post:comment')
    def new_comment(jwt, blog_id):

        body = request.get_json()
        VisitorName = body.get('VisitorName')
        comment = body.get('Comment')

        # Get visitor id based on his/her name
        Visitorid = Visitor.query.with_entities(Visitor.id).filter(
            Visitor.VisitorName == VisitorName).one_or_none()
        if Visitorid is None:
            Visitorid = Bolgger.query.with_entities(Bolgger.id).filter(
                Bolgger.BloggerName == VisitorName).one_or_none()

        try:
            new_comment = Comment(
                comment=comment,
                Blog_id=blog_id,
                Visitor_id=Visitorid[0])
            new_comment.insert()
            formatted_comment = new_comment.format()

            return jsonify({
                'success': True,
                "new_comment": formatted_comment
            })
        except BaseException:
            abort(422)

    # Edit (PATCH)

    @app.route('/<int:blogger_id>/blogs/<blog_id>', methods=['PATCH'])
    @requires_auth('patch:blog')
    def edit_blog(jwt, blogger_id, blog_id):

        # CHECK if the same blogger
        current_bolgger_id = Blog.query.with_entities(
            Blog.Bolgger_id).filter(
            Blog.id == blog_id).all()

        if blogger_id != current_bolgger_id[0][0]:
            abort(405)

        body = request.get_json()
        title = body.get('title', None)
        Content = body.get('content', None)

        try:
            blog = Blog.query.filter(Blog.id == blog_id).one_or_none()
            if blog is None:
                abort(404)
            if title:
                blog.title = title
            if Content:
                blog.content = Content

            blog.update()

            formatted_blog = blog.format()

            return jsonify({
                'success': True,
                "blog": formatted_blog
            })
        except BaseException:
            abort(422)

    # DELETE

    @app.route('/<int:blogger_id>/blogs/<int:blog_id>', methods=['DELETE'])
    @requires_auth('delete:blog')
    def delete_blog_and_its_comments(jwt, blogger_id, blog_id):

        blog = Blog.query.filter(Blog.id == blog_id).one_or_none()
        if blog is None:
            abort(404)

        # CHECK if the same blogger
        current_bolgger_id = Blog.query.with_entities(
            Blog.Bolgger_id).filter(
            Blog.id == blog_id).all()

        if blogger_id != current_bolgger_id[0][0]:
            abort(405)

        try:
            blog = Blog.query.filter(Blog.id == blog_id).one_or_none()
            if blog is None:
                abort(404)
            blog.delete()

            # delete all comments for this blog
            commments = Comment.query.filter(Comment.Blog_id == blog_id).all()
            while commments:
                commments.delete()

            return jsonify({
                'success': True
            })

        except BaseException:
            abort(422)

    # Errorhandlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
