import datetime
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import bridge.models as md
from bridge.tools import myJWT


# Create your views here.
comment_idx = 0
tp_idx = 0
fp_idx = 0

@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_obj = json.loads(request.body)
        teacher_id = json_obj['teacher_id']
        teacher_password = json_obj['teacher_password']

        # 检验字段是否为空
        if not teacher_id or not teacher_password:
            res = {'code': 500, 'prompt': '所有字段必须填写'}
            return JsonResponse(res)

        # 检验学号是否存在：
        try:
            teacher = md.teacher.objects.get(teacher_id=teacher_id)
        except:
            res = {'code': 500, 'prompt': '教工号不存在，请先注册'}
            return JsonResponse(res)

        # 检验密码是否正确：
        if teacher.teacher_password != teacher_password:
            res = {'code': 500, 'prompt': '密码不正确，请重新输入'}
            return JsonResponse(res)

        token = myJWT.make_token(teacher_id)
        res = {'code': 200, 'prompt': "登录成功！", 'data': {'token': token}}
        # res = {'code': 200, 'prompt': "登录成功！"}
        return JsonResponse(res)
    else:
        res = {'code': 210, 'prompt': "请求方式应为POST"}
        return JsonResponse(res)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 创建资源/ 注册用户
        # 注册用户成功后　签发 token[一天]
        # 用户模块状态码　10100 开始　/ 200为正常返回
        # {'code': 200/101xx, 'data':xxx, 'error':xxx}
        # 响应json字符串 return JsonResponse({})
        json_str = request.body
        if not json_str:
            result = {'code': 10100, 'error': 'Please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        print(json_obj)
        Id = json_obj.get('teacher_id')
        email = json_obj.get('email')
        password_1 = json_obj.get('teacher_password1')
        password_2 = json_obj.get('teacher_password2')
        teacher_name = json_obj.get('teacher_realName')
        if not Id:
            result = {'code': 10101, 'error': 'Please give me Id'}
            return JsonResponse(result)

        if not email:
            result = {'code': 10102, 'error': 'Please give me email'}
            return JsonResponse(result)
        if not teacher_name:
            result = {'code': 10106, 'error': 'Please give me email'}
            return JsonResponse(result)

        if not password_1 or not password_2:
            result = {'code': 10103, 'error': 'Please give me password'}
            return JsonResponse(result)

        if password_1 != password_2:
            result = {'code': 10104, 'error': 'The password is not same!'}
            return JsonResponse(result)
        # 检查当前用户名是否可用
        old_user = md.teacher.objects.filter(teacher_id=Id)
        if old_user:
            result = {'code': 10105, 'error': 'The teacher_id is already existed!'}
            return JsonResponse(result)
        # # 密码进行哈希　－　md5
        # p_m = hashlib.md5()
        # p_m.update(password_1.encode())

        # 创建用户
        try:
            md.teacher.objects.create(teacher_id=Id, teacher_password=password_2, email=email,
                                      teacher_name=teacher_name)
        except Exception as e:
            print(e)
            result = {'code': 10106, 'error': 'The teacher_id is already used!'}
            return JsonResponse(result)

        # todo 生成token
        token = myJWT.make_token(Id)
        result = {'code': 200, 'teacher_id': Id, 'data': {'token': token}}
        return JsonResponse(result)
    else:
        res = {'code': 210, 'prompt': "请求方式应为POST"}
        return JsonResponse(res)


@csrf_exempt
def modify(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    md.teacher.objects.filter(teacher_id=teacher_id).update(teacher_name=info.get('teacher_name'),
                                                            teacher_password=info.get('teacher_password'),
                                                            depart=info.get('depart'), email=info.get('email'),
                                                            phone=info.get('phone'))
    return JsonResponse({'code': 210, 'prompt': "修改成功！"})


@csrf_exempt
def add(request):  # 老师新开一个课程
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    course = info.get('course')
    course_id = course['course_id']
    course_name = course['course_name']
    exist = md.course.objects.filter(course_id=course_id)
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)
    course_item = md.course.objects.get(course_id=course['course_id'])
    if exist:
        res = {'code': 1, "prompt": "此课程ID已经存在，请重新设置！"}
        return JsonResponse(res)
    exist = md.teacher_course.objects.filter(course_id=course_item, teacher_id=teacher_item)
    if exist:
        res = {'code': 2, "prompt": "您已开设了此课程，请勿重复开设！"}
        return JsonResponse(res)
    course_capacity = course.course_capacity
    course_intro = course.course_intro
    if not course_id or not course_name or not course_capacity:
        return JsonResponse({"code": 3, 'prompt': "课程ID或课程名称或课程容量字段不得为空！"})
    md.course.objects.create(course_total=0, course_id=course_id, course_name=course_name, course_intro=course_intro,
                             course_capacity=course_capacity)
    md.teacher_course.objects.create(teacher_id=teacher_item, course_id=course_item)
    return JsonResponse({"code": 0, 'prompt': "开课成功，可以在课程广场查看到此课程"})


@csrf_exempt
def delete(request):  # 教师不再设此课
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    course = info.get('course')
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)
    course_item = md.course.objects.get(course_id=course['course_id'])
    md.teacher_course.objects.filter(teacher_id=teacher_item, course_id=course_item).delete()
    md.course.objects.filter(course_id=course['course_id']).delete()
    res = {'code': 0, "prompt": "删除课程成功！"}
    return JsonResponse(res)


@csrf_exempt
def getinfo(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    teacher = md.teacher.objects.filter(teacher_id=teacher_id).first()
    teacher_password = teacher.teacher_password
    teacher_name = teacher.teacher_name
    depart = teacher.depart
    email = teacher.email
    phone = teacher.phone
    message = teacher.message
    res = {"teacher_id": teacher_id, "teacher_password": teacher_password, "teacher_name": teacher_name,
           "depart": depart, "email": email, "phone": phone, "message": message}
    return JsonResponse(res)


@csrf_exempt
def myCourse(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    courses = md.teacher_course.objects.filter(teacher_id=teacher_id)
    course_ids = []
    for s_c in courses:
        course_ids.append(s_c.course_id.course_id)
    data = []
    for course_id in course_ids:
        obj = md.course.objects.filter(course_id=course_id).first()
        course_name = obj.course_name
        course_intro = obj.course_intro
        course_rate = obj.course_rate
        course_total = obj.course_total
        course_capacity = obj.course_capacity
        data.append({"course_id": course_id, "course_name": course_name, "course_intro": course_intro,
                     "course_rate": course_rate, "course_total": course_total, "course_capacity": course_capacity})

    if len(data) == 0:
        return JsonResponse({'code': 1, "data": [], "message": "没有课程"})
    return JsonResponse({'code': 0, "data": data, "message": "查找到所有课程"})


@csrf_exempt
def changePasswd(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    old_passwd = info.get('old_password')
    new_passwd1 = info.get('new_password1')
    new_passwd2 = info.get('new_password2')
    teacher = md.teacher.objects.get(teacher_id=teacher_id)
    if not teacher_id or not old_passwd or not new_passwd2 or not new_passwd1:
        return JsonResponse({'code': 3, 'message': "所有字段必须填写！"})
    if teacher.teacher_password != old_passwd:
        return JsonResponse({'code': 1, "message": "请输入正确的用户名或密码！"})
    if new_passwd1 != new_passwd2:
        return JsonResponse({'code': 2, 'message': "两次输入的新密码不一致！"})
    # teacher.objects.update(teacher_password=new_passwd2)
    teacher.teacher_password = new_passwd2
    return JsonResponse({"code": 0, 'message': "更改密码成功！"})


@csrf_exempt
def addMaterial(request):
    info = json.loads(request.body)
    material = info.get('material')
    material_id = material.material_id
    material_name = material.material_name
    material_intro = material.material_intro
    teacher_id = info.get("teacher_id")
    course_id = info.get('course_id')
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)
    course_item = md.course.objects.get(course_id=course_id)

    if not material_id or not material_intro or not material_name:
        return JsonResponse({'code': 3, 'message': "所有字段必须填写！"})
    exist = md.course.objects.filter(course_id=course_id)
    if not exist:
        res = {'code': 1, "prompt": "无此课程ID，请重新设置！"}
        return JsonResponse(res)
    exist = md.teacher_course.objects.filter(course_id=course_id, teacher_id=teacher_id)
    if not exist:
        res = {'code': 2, "prompt": "无此课程开设记录！"}
        return JsonResponse(res)
    exist = md.teacher.objects.filter(teacher_id=teacher_id)
    if not exist:
        res = {'code': 3, "prompt": "无此老师！"}
        return JsonResponse(res)
    md.material.objects.create(material_id=material_id, material_name=material_name, material_intro=material_intro)
    material_item = md.material.objects.get(material_id=material_id)
    md.teacher_material.objects.create(teacher_id=teacher_item, material_id=material_item)
    md.course_material.objects.create(course_id=course_item, material_id=material_item)
    return JsonResponse({"code": 0, 'prompt': "添加课程资料成功！"})


@csrf_exempt
def newThemePost(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    themePost = info.get('themepost')
    global tp_idx
    tp_id = str(tp_idx + 1)
    tp_idx = tp_idx + 1
    tp_title = themePost.tp_title
    tp_content = themePost.tp_content
    tp_time = datetime.datetime.now()
    tp_isTeacher = True
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)

    if not tp_title:
        return JsonResponse({"code": 1, 'message': "标题不能为空！"})
    if len(tp_title) > 127:
        return JsonResponse({"code": 2, 'message': "标题内容不能超过127个字符"})
    if len(tp_content) > 512:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过512个字符"})
    md.themepost.objects.create(tp_id=tp_id, tp_title=tp_title, tp_content=tp_content, tp_time=tp_time,
                                tp_isTeacher=tp_isTeacher)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    md.teacher_tp.objects.create(teacher_id=teacher_item, tp_id=tp_item)
    postCnt = md.teacher.objects.get(teacher_id=teacher_id).postCnt
    md.teacher.objects.filter(teacher_id=teacher_id).update(postCnt=postCnt + 1)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'tp_id': tp_id})


@csrf_exempt
def deleteThemePost(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    tp_id = info.get('tp_id')
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    md.themepost.objects.filter(tp_id=tp_id).delete()
    md.teacher_tp.objects.filter(tp_id=tp_item, teacher_id=teacher_item).delete()
    return JsonResponse({"code": 0, 'prompt': "主题帖删除成功！"})


@csrf_exempt
def newFollowPost(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    tp_id = info.get('tp_id')
    global fp_idx
    fp_id = str(fp_idx + 1)
    fp_idx = fp_idx + 1
    fp_content = info.get('fp_content')
    fp_time = datetime.datetime.now()
    fp_isTeacher = True
    teacher_item = md.teacher.objects.get(teacher_id=teacher_id)
    if not fp_content:
        return JsonResponse({"code": 1, 'message': "内容不能为空！"})
    if len(fp_content) > 127:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过127个字符"})
    md.followpost.objects.create(fp_id=fp_id, fp_content=fp_content, fp_time=fp_time,
                                fp_isTeacher=fp_isTeacher)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.teacher_fp.objects.create(teacher_id=teacher_item, fp_id=fp_item)
    md.tp_fp.objects.create(tp_id=tp_item, fp_id=fp_item)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'fp_id': fp_id})


@csrf_exempt
def deleteFollowPost(request):
    info = json.loads(request.body)
    teacher_id = info.get('teacher_id')
    tp_id = info.get('tp_id')
    fp_id = info.get('fp_id')
    teacher_item = md.stu.objects.get(teacher_id=teacher_id)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.followpost.objects.filter(fp_id=fp_id).delete()
    md.teacher_fp.objects.filter(fp_id=fp_item, teacher_id=teacher_item).delete()
    md.tp_fp.objects.filter(fp_id=fp_item, tp_id=tp_item).delete()
    return JsonResponse({"code": 0, 'prompt': "评论删除成功！"})
# if __name__ == '__main__':
