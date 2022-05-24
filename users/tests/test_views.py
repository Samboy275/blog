

from utlis.test_setup import TestSetup
from django.urls import  reverse
from django.contrib.messages import get_messages



class Test_Views(TestSetup):


    def test_register_response(self):
        """Method to test the response of teh register page"""

        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
    
    def test_login_response(self):
        """Method to test the response of the login page"""

        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")



    def test_user_registeration_process(self):
        """Method to test the user registeration process"""

        response = self.client.post(reverse("users:register"), self.user)
        self.assertEqual(response.status_code, 302)

    def test_user_login_successfully(self):
        """ test if a user can login successfully"""
        username = 'loginuser'
        user = self.create_test_user(username)

        response = self.client.post(reverse("users:login"), {
            "Username" : user.username,
            "Password" : "password123"
        })

        self.assertEqual(response.status_code, 302)


        storage = get_messages(response.wsgi_request)

        self.assertIn(f"Welcome {user.username}", list(map(lambda x: x.message, storage)))

    def test_username_taken_registeration_process(self):
        """Method to test the user registeration process"""
        self.client.post(reverse("users:register"), self.user)
        response = self.client.post(reverse("users:register"), self.user)
        self.assertEqual(response.status_code, 409)

        storage = get_messages(response.wsgi_request)

        self.assertIn("Username already exists", 
                        list(map(lambda x: x.message, storage)))
    
    def test_email_taken_registeration_process(self):
        """Method to test the user registeration process"""
        self.user2 = {
            "Username" : "username",
            "email" :  self.email,
            "Password1" : "password",
            "Password2" : "password"
        }
        self.client.post(reverse("users:register"), self.user)
        response = self.client.post(reverse("users:register"), self.user2)
        self.assertEqual(response.status_code, 409)