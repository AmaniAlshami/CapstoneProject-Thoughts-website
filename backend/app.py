import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Bolgger, Blog ,Comment


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

 

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response

  ##TODO: create apis endpoints

  # GET 

  @app.route('/bloggers',methods=['GET'])
  def get_bloggers():
    pass

  @app.route('/blogs',methods=['GET'])
  def get_blogs():
    pass

  @app.route('/<blogger_id>/blogs',methods=['GET'])
  def get_blogger_blog():
    pass

  @app.route('/blog_id',methods=['GET'])
  def get_blogs():
    pass

  @app.route('/<blog_id>/comments',methods=['GET'])
  def get_comments():
    pass

  # POST 

  @app.route('/<blogger_id>/blog',methods=['POST'])
  def new_blog():
    pass 

  @app.route('/<blog_id>/comments',methods=['POST'])
  def new_comment():
    pass 


  # Edit (PATCH)

  @app.route('/<blogger_id>/<blog_id>',methods=['PATCH'])
  def edit_blog():
    pass 

  @app.route('/<blog_id>/<comment_id>',methods=['PATCH'])
  def edit_comment():
    pass 


 # DELETE 

  @app.route('/<blogger_id>/<blog_id>',methods=['DELETE'])
  def delete_blog():
    pass 

  @app.route('/<blog_id>/<comment_id>',methods=['DELETE'])
  def delete_comment():
    pass 




  return app

APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)