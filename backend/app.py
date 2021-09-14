import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Bolgger, Blog ,Comment , db_drop_and_create_all ,Visitor 


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  @TODO uncomment the following line to initialize the datbase
  !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
  !! Running this funciton will add one
  '''
  #db_drop_and_create_all()


  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response

  ##TODO: create apis endpoints

  ##########################
          ## GET ##
  ##########################
  

  # test 

  @app.route('/',methods=['GET'])
  def test_hello():
    return jsonify({
          'success': True,
          "message": "Hello"
     })
  
# retraive all bloggers 
  @app.route('/bloggers',methods=['GET'])
  def get_bloggers():

    bolggers = Bolgger.query.all()
    formatted_bolggers =[bolgger.format() for bolgger in bolggers]
    
    return jsonify({
          'success': True,
          "bolggers": formatted_bolggers
     })
  

 # retraive all bloges  
  @app.route('/blogs',methods=['GET'])
  def get_blogs():

    blogs = Blog.query.all()
    formatted_blogs =[blog.format() for blog in blogs]
    
    return jsonify({
          'success': True,
          "blogs": formatted_blogs
     })


   
 # retraive all bloges for one blogger 
  @app.route('/<blogger_id>/blogs',methods=['GET'])
  def get_blogger_blog(blogger_id):
      blogs = Blog.query.filter(Blog.Bolgger_id == blogger_id).all()
      formatted_blogs =[blog.format() for blog in blogs]
    
      return jsonify({
            'success': True,
            "blogs": formatted_blogs
      })



 # retraive spisefic blog content 
  @app.route('/blogs/<blog_id>',methods=['GET'])
  def get_one_blog(blog_id):
      blog = Blog.query.filter(Blog.id == blog_id).all()
      blog = blog[0].format()
      return jsonify({
            'success': True,
            "content": blog['content'],
            "id": blog['id'] ,
            "title": blog['title']
      })
    
 # retraive all comments for blog 
  @app.route('/<blog_id>/comments',methods=['GET'])
  def get_comments(blog_id):

      comments = Comment.query.filter(Comment.Blog_id == blog_id).all()
      formatted_comments =[comment.format() for comment in comments]
    
      return jsonify({
            'success': True,
            "comments": formatted_comments
      })


 


  ##########################
          ## POST ##
  ##########################

  @app.route('/<blogger_id>/blogs',methods=['POST'])
  def new_blog(blogger_id):

    body = request.get_json()
    title = body.get('title',None)
    Content = body.get('content',None)

    try: 

        blog = Blog(title = title, content = Content, Bolgger_id = blogger_id)
        blog.insert()
        formatted_blog = blog.format()

        return jsonify({
    
           'success': True,
            "blog": formatted_blog
        })

    except:
        abort(422) 



    
  @app.route('/<blog_id>/comments',methods=['POST'])
  def new_comment(blog_id):
    
    body = request.get_json()
    VisitorName = body.get('VisitorName',None)
    comment = body.get('Comment',None)

    ## Get visitor id based on his/her name 
    Visitorid = Visitor.query.with_entities(Visitor.id).filter(Visitor.VisitorName == VisitorName).all()
   
    try: 
        new_comment = Comment(comment = comment, Blog_id = blog_id , Visitor_id =Visitorid[0][0] )
        new_comment.insert()
        formatted_comment = new_comment.format()
        
        return jsonify({
           'success': True,
            "new_comment": formatted_comment
        })
    except:
        abort(422) 

 

    
  ##########################
      ## Edit (PATCH) ##
  ##########################

  @app.route('/<int:blogger_id>/blogs/<blog_id>',methods=['PATCH'])
  def edit_blog(blogger_id,blog_id):
     
    # CHECK if the same blogger 
    current_bolgger_id = Blog.query.with_entities(Blog.Bolgger_id).filter(Blog.id == blog_id).all()
  
    if blogger_id != current_bolgger_id[0][0] :
      abort(405)
    
    body = request.get_json()
    title = body.get('title',None)
    Content = body.get('content',None)

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

    except:
        abort(422) 

  #@app.route('/blogs/<blog_id>/<comment_id>',methods=['PATCH'])
  #def edit_comment():
    #pass 


 
  ##########################
       ## DELETE ##
  ##########################

  @app.route('/<int:blogger_id>/blogs/<blog_id>',methods=['DELETE'])
  def delete_blog_and_its_comments(blogger_id,blog_id):

    # CHECK if the same blogger 
    current_bolgger_id = Blog.query.with_entities(Blog.Bolgger_id).filter(Blog.id == blog_id).all()
    print("******")
    print(current_bolgger_id)
    print(blogger_id)
    print(blog_id)
    print("******")
    if blogger_id != current_bolgger_id[0][0] :
      abort(405)

    try:  
      blog = Blog.query.filter(Blog.id == blog_id).one_or_none()
      if blog is None:
          abort(404)
      blog.delete()

      formatted_blog = blog.format()

      ## delete all comments for this blog 
      commments = Comment.query.filter(Comment.Blog_id == blog_id).all()
      while commments:
        commments.delete()



      return jsonify({
          'success': True,
          "deleteBlog": formatted_blog
      })

    except:
        abort(422) 



  @app.route('/<blog_id>/<comment_id>',methods=['DELETE'])
  def delete_comment():
    pass 






 ##########################
    ## Errorhandler ##
 ##########################

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
  return app

APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)