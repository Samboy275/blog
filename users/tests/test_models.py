
from utlis.test_setup import TestSetup


class TestModel (TestSetup):



    def test_user_creation(self):
        """ test if user creation works"""

        user = self.create_test_user()
        
        user.save()

        self.assertEqual("username", user.username)