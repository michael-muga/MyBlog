import unittest
from app.models import Blog, User


class BlogTest(unittest.TestCase):
    def setUp(self):
        self.user_id = User(username='vitalis', password='computer', email='vitalis@gmail.com')
        self.new_blog = Blog(blog_title='My Birthday',posted_at='14/3/1998', blog_content='The date I took my first breath', user_id=self.user_id.id)


    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.blog_title, 'My Birthday')
        self.assertEquals(self.new_blog.blog_content, 'The date I took my first breath')
        self.assertEquals(self.new_blog.user_id, self.user_id.id)

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_get_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(self)