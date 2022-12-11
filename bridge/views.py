import json

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
        return JsonResponse({"data": [], "message": "没有课程", 'code': 1})
    return JsonResponse({"data": data, "message": "查找到所有课程", 'code': 0})


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
            return JsonResponse({"code": 1, "data": None, "message": "无此课程"})
        return JsonResponse({"code": 0, "data": data, "message": "查找成功"})


@csrf_exempt
def showCourseComment(request):
    info = json.loads(request.body)
    course_id = info.get('course_id')
    course_item = model.course.objects.get(course_id=course_id)
    course_comments = model.course_comment.objects.filter(course_id=course_item)
    data = []
    comment_ids = []
    for obj in course_comments:
        comment_id = obj.comment_id.comment_id
        comment_ids.append(comment_id)

    for comment_id in comment_ids:
        comment = model.comment.objects.get(comment_id=comment_id)
        stu_item = model.stu_comment.objects.get(comment_id=comment)
        stu_id = stu_item.stu_id.stu_id
        stu = model.stu.objects.get(stu_id=stu_id)
        stu_name = stu.stu_name
        data.append({"stu_id": stu.stu_id, "stu_name": stu_name, "comment_id": comment_id,
                     "comment_content": comment.comment_content,
                     "comment_time": comment.comment_time})
    if len(data) == 0:
        return JsonResponse({"code": 1, "data": None, "message": "此课程暂无任何评价"})
    return JsonResponse({"code": 0, "data": data, "message": "找到所有评价！"})


@csrf_exempt
def showAllTp(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    if not stu_id:
        return JsonResponse({'code': 2, 'message': '学生id为空，请先登陆'})
    stu = model.stu.objects.get(stu_id=stu_id)
    if not stu:
        return JsonResponse({'code': 3, 'message': '无此学生，请先注册'})
    postCnt = stu.postCnt
    allTp = model.themepost.objects.all()
    data = []
    for obj in allTp:
        tp_id = obj.tp_id
        tp_title = obj.tp_title
        tp_content = obj.tp_content
        tp_time = obj.tp_time
        tp_isTeacher = obj.tp_isTeacher
        data.append({"tp_id": tp_id, "tp_title": tp_title, "tp_content": tp_content, "tp_time": tp_time,
                     "tp_isTeacher": tp_isTeacher})
    if len(data) == 0:
        return JsonResponse({"data": [], "message": "没有任何主题帖", 'code': 1, 'postCnt': postCnt})
    return JsonResponse({"data": data, "message": "查找到所有主题帖", 'code': 0, 'postCnt': postCnt})


@csrf_exempt
def showAllFp(request):
    info = json.loads(request.body)
    tp_id = info.get('tp_id')
    tp_item = model.themepost.objects.get(tp_id=tp_id)
    tp_fps = model.tp_fp.objects.filter(tp_id=tp_item)
    fp_ids = []
    data = []
    for obj in tp_fps:
        fp_ids.append(obj.fp_id.fp_id)
    for fp_id in fp_ids:
        fp = model.followpost.objects.get(fp_id=fp_id)
        stu_id = model.stu_fp.objects.get(fp_id=fp_id).stu_id
        stu_name = model.stu.objects.get(stu_id=stu_id).stu_name
        fp_content = fp.fp_content
        fp_time = fp.fp_time
        fp_isTeacher = fp.fp_isTeacher
        data.append({"stu_id": stu_id, "stu_name": stu_name, "fp_content": fp_content, "fp_time": fp_time,
                     "fp_isTeacher": fp_isTeacher})
    if len(data) == 0:
        return JsonResponse({"code": 1, "data": None, "message": "此主题帖暂无任何跟帖"})
    return JsonResponse({"code": 0, "data": data, "message": "找到所有跟帖！"})


@csrf_exempt
def searchTp(request):
    info = json.loads(request.body)
    tp_title = info.get("tp_title")
    tp = model.themepost.objects.filter(tp_title=tp_title)
    data = []
    for obj in tp:
        tp_id = obj.tp_id
        tp_title = obj.tp_title
        tp_content = obj.tp_content
        tp_time = obj.tp_time
        tp_isTeacher = obj.tp_isTeacher
        data.append({"tp_id": tp_id, "tp_title": tp_title, "tp_content": tp_content, "tp_time": tp_time,
                     "tp_isTeacher": tp_isTeacher})
    if len(data) == 0:
        return JsonResponse({"data": [], "message": "没有找到任何主题帖", 'code': 1})
    return JsonResponse({"data": data, "message": "查找到所有主题帖", 'code': 0})


@csrf_exempt
def showCourseMaterial(request):
    info = json.loads(request.body)
    course_id = info.get('course_id')
    course_materials = model.course_material.objects.filter(course_id=course_id)
    material_ids = []
    for obj in course_materials:
        material_ids.append(obj.material_id.material_id)
    data = []
    for material_id in material_ids:
        material = model.material.objects.get(material_id=material_id)
        data.append({"material_id": material_id, 'material_name': material.material_name,
                     "material_intro": material.material_intro})
    if len(data) == 0:
        return JsonResponse({'data': None, 'code': 1, 'message': "该课程暂无任何课程资料！"})
    return JsonResponse({'data': data, 'code': 0, 'message': '查找到该课程所有资料！'})
