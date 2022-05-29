from django.urls import reverse
from utlis.test_setup import TestSetup
from blogs.models import BlogPost, Comments



class TestView (TestSetup):


    def test_home_page_view(self):
        """show home page test"""
        response = self.client.get(reverse("blogs:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_user_blog_view_page(self):
        """shows user blogs page"""
        usernmae = "postuser"
        post = self.create_test_blog(usernmae)
        response = self.client.get(reverse("blogs:my_post",args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog.html")

    def test_post_creation_view(self):

        username = "postuser"
        user = self.create_test_user(username)

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
        self.assertEqual(current_posts, (posts + 1))

        self.assertEqual(response.status_code, 302)

    def test_user_posts_view(self):

        username = "postsviewuser"
        user = self.create_test_user(username)
        self.client.post(reverse("users:login"), {
            'username' : user.username,
            'password' : 'password123'
        })

        response = self.client.get(reverse("blogs:my_blogs"))

        self.assertEqual(response.status_code, 302)

    def test_comment_view_viwe(self):
        """testing resoonse of post_view"""

        commentuser = self.create_test_user("commentuser")
        self.client.post(reverse("users:login"), {
            "Username" : commentuser.username,
            "Password" : "password123"
        })
        username = "postviewgeneral"

        post = self.create_test_blog(username)

        comments = Comments.objects.all().count()
        response = self.client.post(reverse("blogs:my_post", args=[post.id]), {
            'owner' : commentuser,
            'post' : post,
            'text' : "comment text"
        })
        currnet_comments = Comments.objects.all().count()

        self.assertEqual(currnet_comments, (comments + 1))

        self.assertEqual(response.status_code, 200)


    def test_delete_post_view_page(self):

        user = "deleteuserview"
        post = self.create_test_blog(user)

        self.client.post(reverse("users:login"), {
            "Username" : user,
            "Password" : "password123"
        })

        response = self.client.get(reverse("blogs:delete_post", args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_post.html")


    def test_delete_post_action(self):

        user = "deleteuser"
        post = self.create_test_blog(user)

        current_posts = BlogPost.objects.all().count()
        self.client.post(reverse("users:login"),{
            'Username' : user,
            'Password' : 'password123'
        })
        response = self.client.post(reverse("blogs:delete_post", args=[post.id]))

        posts_after = BlogPost.objects.all().count()
        self.assertEqual(current_posts, (posts_after + 1))

        self.assertEqual(response.status_code, 302)
