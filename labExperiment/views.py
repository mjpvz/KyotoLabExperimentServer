from django.http import HttpResponse

def test(request):
    return HttpResponse('So far so good!!')
