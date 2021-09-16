import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Bolgger, Blog ,Comment ,Visitor , db_drop_and_create_all




class ThoughtsTestCase(unittest.TestCase):
    """This class represents the Thoughts test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "Thoughts_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /blogs 

    def test_get_blogs(self):
        res = self.client().get('/blogs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['blogs'])
## ?
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # GET '/bloggers' 

    def test_get_bloggers(self):
        res = self.client().get('/bloggers')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
   
    
    # GET '/${blogger_id}/blogs'   

    def test_get_blogs_for_one_blogger(self):

        res = self.client().get('/1/blogs')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['blogs'])


    def test_404_sent_requesting_beyond_valid_blogger(self):

        res = self.client().get('/1000/blogs')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    # GET '/blogs/${blog_id}'   

    def test_get_one_blog(self):

        res = self.client().get('/blogs/1')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)


    
    def test_404_sent_requesting_beyond_valid_blog(self):

        res = self.client().get('/blogs/1000')
        data = json.loads(res.data)  

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    # POST '/${blogger_id}/blogs' - create blog

    def test_create_new_blog(self):
        res = self.client().post('/1/blogs',
        json={'title': 'New testing blog',
        'content': 'This is a new blog'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_405_if_blogs_creation_not_allowed(self):
        res = self.client().post('/blogs', json={'title': 'New testing blog',
        'content': 'This is a new blog'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
 

 ##TODO: add auth check for testing .. 

    '''

    # POST '/blogs/${blog_id}' - new comment

    def test_create_new_comment(self):
        res = self.client().post('/blogs/1',
        json={"VisitorName":'John',"Comment":'this new comment'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       # self.blog_id = data['blogs']['id']
    
    def test_422_if_visitor_name_does_not_exist(self):
        res = self.client().post('/blogs/1',
        json={"VisitorName":'John22',"Comment":'this new comment'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')  



# PATCH  '${blogger_id}/blogs/${blog_id}' 

    def test_edit_blog(self):
        res = self.client().patch('/1/blogs/1',
        json={'title': 'New edit blog',
        'content': 'This is a chaging blog'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_405_if_blogs_edit_not_allowed(self):
        res = self.client().patch('/2/blogs/1',
        json={'title': 'New edit blog',
        'content': 'This is a chaging blog'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')



    # DELETE '${blogger_id}/blogs/${blog_id}' 


    def test_delete_question(self):
        res = self.client().delete('/1/blogs/2')
        data = json.loads(res.data)

        blog = Blog.query.filter(Blog.id == 2).one_or_none()
        formatted_blog = blog.format()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deletedBlog'], formatted_blog)
        self.assertEqual(blog, None)
        

    def test_404_if_blog_does_not_exist(self):
        res = self.client().delete('/1/blogs/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')    
    '''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()