from django.urls import reverse
from utlis.test_setup import TestSetup
from blogs.models import BlogPost



class TestView (TestSetup):




    def test_post_creation_view(self):

        user = self.create_test_user()

        self.client.post(reverse("users:login"), {
            "Username" : user.username,
            "Password" : "password123"
        })

        posts = BlogPost.objects.all().count()

        self.assertEqual(posts, 0)
        response = self.client.post(reverse("blogs:new_post"), {
            "owner" : user,
            "title" : "Testing blogs",
            "text" : "testing blog body and content"
        })

        current_posts = BlogPost.objects.all().count()
        print(current_posts)
        self.assertEqual(current_posts, 1)

        self.assertEqual(response.status_code, 302)