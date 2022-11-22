from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import bridge.models as model
from django.http import JsonResponse


@csrf_exempt
def showAllCourse(request):
    allCourse = model.course.objects.all()
    data = []
    for obj in allCourse:
        course_id = obj.course_id
        course_name = obj.course_name
        course_intro = obj.course_intro
        course_rate = obj.course_rate
        course_total = obj.course_total
        course_capacity = obj.course_capacity
        data.append({"course_id": course_id, "course_name": course_name, "course_intro": course_intro,
                     "course_rate": course_rate, "course_total": course_total, "course_capacity": course_capacity})
    if len(data) == 0:
        return JsonResponse({"data": [], "message": "没有课程"})
    return JsonResponse({"data": data, "message": "查找到所有课程"})


@csrf_exempt
def searchByName(request):
    course_name = request.POST.get('course_name')
    course = model.course.objects.filter(course_name=course_name)
    data = []
    for obj in course:
        course_id = obj.course_id
        course_name = obj.course_name
        course_intro = obj.course_intro
        course_rate = obj.course_rate
        course_total = obj.course_total
        course_capacity = obj.course_capacity
        data.append({"course_id": course_id, "course_name": course_name, "course_intro": course_intro,
                     "course_rate": course_rate, "course_total": course_total, "course_capacity": course_capacity})
        if len(data) == 0:
            return JsonResponse({"data": None, "message": "无此课程"})
        return JsonResponse({"data": data, "message": "查找成功"})
