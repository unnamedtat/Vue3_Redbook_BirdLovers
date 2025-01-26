from django.http import HttpResponse

def test_deployment(request):
    return HttpResponse("这里是后端地址")