from utlis.test_setup import TestSetup
from blogs.models import BlogPost



class TestModel (TestSetup):




    def test_blogs_creatiion_model(self):
        """ testing blogs creation process"""

        user = self.create_test_user()

        post = BlogPost(title = "My life", text = "making a mockery of people is my life", owner = user)
        post.save()

        self.assertEqual(post.get_title(), "My life")
