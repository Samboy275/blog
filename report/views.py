from .models import Report
from users.models import User
from blogs.models import Comments, BlogPost
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ReportForm
# Create your views here.

def check_reported_item(type, id):
    """checking if reported item exists"""
    item = None

    if type == 'c':
        item = Comments.objects.filter(id = id)
    elif type == 'p':
        item = BlogPost.objects.filter(id = id)

    return item

  
def report_view(request):
    """view to handle reports"""
    if request.method == "POST":
        report_type = request.POST.get("type")
        reported_id = request.POST.get("reported_id")
        reporter_id = request.POST.get("user_id")
        text = request.POST.get("text")

        # checking for valid type
        if report_type not in ['c', 'p']:
            return JsonResponse({
                'message': "your reports isnt valid"
            })
        
        if check_reported_item(report_type, reported_id) == None:
            return JsonResponse({
                'message' : 'something went bad'
            })
        reporter = User.objects.filter(id = reporter_id)[0]

        if reporter == None:
            return JsonResponse({
                'message': 'something went wrong'
            })

        report = Report(text=text, reporter=reporter, report_type=report_type)

        # TODO : need to fix the model so it can store a refrence to the reported item

        print(report_type, reported_id)

        return JsonResponse({
            'message': "your report was submitted successfully awaiting admin review"
        })
    elif request.method == "GET":
        print("is this the request?")
        form = ReportForm()
        context = {
            "form" : form
        }

        template = render_to_string("report.html", context)

        return JsonResponse({"form" : template})