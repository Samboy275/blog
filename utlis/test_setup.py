
from django.test import TestCase
from users.models import User
from faker import Faker
from blogs.models import BlogPost



class TestSetup (TestCase):
    

    def setUp(self):
        print("test starts")
        
        self.faker = Faker()
        self.password = self.faker.paragraph(nb_sentences=5)
        self.email = self.faker.email()
        self.user = {
            "Username" : self.faker.name().split(" ")[0],
            "email" :  self.email,
            "Password1" : self.password,
            "Password2" : self.password
        }

    def create_test_user(self, username):
        
        user = User.objects.create_user(
            username = username, email = "email@email.com"
        )
        user.set_password('password123')
        user.email_verified = True
        user.save()

        return user

    def create_test_blog(self, username):

        user = self.create_test_user(username)

        post = BlogPost.objects.create(owner = user, title = "Test", text = "testing blog creation model")

        post.save()
        return post
    def tearDown(self):
        print("test finished")