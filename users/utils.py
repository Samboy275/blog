from inspect import classify_class_attrs
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six



class TokenGenerator(PasswordResetTokenGenerator):


    def make_hash_value(self, user, timestamp):
        """a function to return a token that expired after a certain time"""
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.email_verified)

generate_token = TokenGenerator()
