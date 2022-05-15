from django.shortcuts import render




# 404 error handler

def page_not_found(request, exception):

    return render(request, "page_not_found.html") 



def server_error(request):

    return render(request, "server-error.html") 