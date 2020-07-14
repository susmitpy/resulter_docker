from django.shortcuts import render

from management.models import Division

from django.http import JsonResponse

from django.conf import settings
import os

def home(req):
    return render(req,"public/home.html")

# DB CHECK PASS
def fy_result(req):
    if req.method == 'POST':
        division = req.POST.get("division")
        roll = req.POST.get("roll")
        result_relative_fp = './student_results/{}/roll_{}.html/'.format(division,str(roll))
        return JsonResponse({"filePath":result_relative_fp}, status=200)

    a = Division.objects.all()
    divisions = [i.get("name") for i in a.all().values()]
    return render(req, 'public/fy_result_selector.html', {'divisions': divisions})
