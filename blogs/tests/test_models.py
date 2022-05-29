from utlis.test_setup import TestSetup
from blogs.models import BlogPost
from blogs.models import Comments


class TestModel (TestSetup):




    def test_blogs_creatiion_model(self):
        """ testing blogs creation process"""
        username = "testuser"
        user = self.create_test_user(username)
        current_blogs = BlogPost.objects.all().count()
        post = BlogPost(title = "My life", text = "making a mockery of people is my life", owner = user)
        post.save()

        self.assertTrue(BlogPost.objects.all().count() > current_blogs)
        self.assertEqual(post.get_title(), "My life")


    def test_commenst_creation_model(self):
        """ testing comments creation model"""
        username = "commentsuser"
        owner = self.create_test_user(username)
        usernamepost = "postuser"
        post = self.create_test_blog(usernamepost)

        comment = Comments.objects.create(text = "Anycomment text", post = post, owner = owner, active = True)

        comment.save()

        self.assertEqual(comment.text, "Anycomment text")