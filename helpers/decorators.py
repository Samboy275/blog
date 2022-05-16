from django.contrib.auth.decorators import user_passes_test

# checks if user is logged in
def user_check(user):
    """returns true if user isnt logged in"""
    return not user.is_authenticated

user_logout_required = user_passes_test(user_check, '/', None)


def auth_user_should_not_access(viewFunc):
    
    
    return user_logout_required(viewFunc)