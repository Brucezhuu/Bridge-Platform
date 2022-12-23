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
        stu_id = json_obj['stu_id']
        stu_password = json_obj['stu_password']

        # 检验字段是否为空
        if not stu_id or not stu_password:
            res = {'code': 500, 'prompt': '所有字段必须填写'}
            return JsonResponse(res)

        # 检验学号是否存在：
        try:
            stu = md.stu.objects.get(stu_id=stu_id)
        except:
            res = {'code': 500, 'prompt': '学号不存在，请先注册'}
            return JsonResponse(res)

        # 检验密码是否正确：
        if stu.stu_password != stu_password:
            res = {'code': 500, 'prompt': '密码不正确，请重新输入'}
            return JsonResponse(res)

        token = myJWT.make_token(stu_id)
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
        Id = json_obj.get('stu_id')
        email = json_obj.get('email')
        password_1 = json_obj.get('stu_password1')
        password_2 = json_obj.get('stu_password2')
        stu_name = json_obj.get('stu_realName')
        if not Id:
            result = {'code': 10101, 'error': 'Please give me Id'}
            return JsonResponse(result)

        if not email:
            result = {'code': 10102, 'error': 'Please give me email'}
            return JsonResponse(result)
        if not stu_name:
            result = {'code': 10106, 'error': 'Please give me email'}
            return JsonResponse(result)

        if not password_1 or not password_2:
            result = {'code': 10103, 'error': 'Please give me password'}
            return JsonResponse(result)

        if password_1 != password_2:
            result = {'code': 10104, 'error': 'The password is not same!'}
            return JsonResponse(result)
        # 检查当前用户名是否可用
        old_user = md.stu.objects.filter(stu_id=Id)
        if old_user:
            result = {'code': 10105, 'error': 'The stu_id is already existed!'}
            return JsonResponse(result)
        # # 密码进行哈希　－　md5
        # p_m = hashlib.md5()
        # p_m.update(password_1.encode())

        # 创建用户
        try:
            md.stu.objects.create(stu_id=Id, stu_password=password_2, email=email, stu_name=stu_name)
        except Exception as e:
            print(e)
            result = {'code': 10106, 'error': 'The stu_id is already used!'}
            return JsonResponse(result)

        # todo 生成token
        token = myJWT.make_token(Id)
        result = {'code': 200, 'stu_id': Id, 'data': {'token': token}}
        return JsonResponse(result)
    else:
        res = {'code': 210, 'prompt': "请求方式应为POST"}
        return JsonResponse(res)


@csrf_exempt
def modify(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    md.stu.objects.filter(stu_id=stu_id).update(stu_name=info.get('stu_name'), stu_password=info.get('stu_password'),
                                                depart=info.get('depart'), email=info.get('email'),
                                                phone=info.get('phone'))
    return JsonResponse({'code': 210, 'prompt': "修改成功！"})


@csrf_exempt
def add(request):
    info = json.loads(request.body)
    stu_id = info.get('username')
    course = info.get('data')
    course_id = course['course_id']
    exist = md.stu_course.objects.filter(stu_id=stu_id, course_id=course_id)
    if exist:
        res = {'code': 1, "prompt": "已存在此选课记录！"}
        return JsonResponse(res)
    course = md.course.objects.filter(course_id=course_id).first()
    course_capacity = course.course_capacity
    course_total = course.course_total
    if course_total < course_capacity:
        stu = md.stu.objects.get(stu_id=stu_id)
        course = md.course.objects.get(course_id=course_id)
        md.stu_course.objects.create(stu_id=stu, course_id=course)
        course_total = course_total + 1
        md.course.objects.filter(course_id=course_id).update(course_total=course_total)
        res = {'code': 0, "prompt": "选课成功！"}
        return JsonResponse(res)
    else:
        res = {'code': 2, "prompt": "课程容量已满，不能再选此课程！"}
        return JsonResponse(res)


@csrf_exempt
def delete(request):
    info = json.loads(request.body)
    stu_id = info.get('username')
    course = info.get('course')
    stu_item = md.stu.objects.filter(stu_id=stu_id).first()
    course_item = md.course.objects.filter(course_id=course['course_id']).first()
    md.stu_course.objects.filter(stu_id=stu_item, course_id=course_item).delete()
    course_total = md.course.objects.filter(course_id=course['course_id']).first().course_total - 1
    md.course.objects.filter(course_id=course['course_id']).update(course_total=course_total)
    res = {'code': 0, "prompt": "退课成功！"}
    return JsonResponse(res)


@csrf_exempt
def getinfo(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    stu = md.stu.objects.filter(stu_id=stu_id).first()
    stu_password = stu.stu_password
    stu_name = stu.stu_name
    depart = stu.depart
    email = stu.email
    phone = stu.phone
    message = stu.message
    postCnt = stu.postCnt
    res = {"stu_id": stu_id, "stu_password": stu_password, "stu_name": stu_name,
           "depart": depart, "email": email, "phone": phone, "message": message, "postCnt": postCnt}
    return JsonResponse(res)


@csrf_exempt
def myCourse(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    # stu_id = "21"
    stu_item = md.stu.objects.get(stu_id=stu_id)
    courses = md.stu_course.objects.filter(stu_id=stu_item)
    course_ids = []
    for s_c in courses:
        course_ids.append(s_c.course_id.course_id)
    data = []
    for course_id in course_ids:
        obj = md.course.objects.get(course_id=course_id)
        course_name = obj.course_name
        course_intro = obj.course_intro
        course_rate = obj.course_rate
        course_total = obj.course_total
        course_capacity = obj.course_capacity
        teacher_item = md.teacher_course.objects.get(course_id=course_id)
        teacher_name = teacher_item.teacher_id.teacher_name
        data.append({"teacher_name": teacher_name, "course_id": course_id, "course_name": course_name,
                     "course_intro": course_intro,
                     "course_rate": course_rate, "course_total": course_total, "course_capacity": course_capacity})

    if len(data) == 0:
        return JsonResponse({'code': 1, "data": [], "message": "没有课程"})
    return JsonResponse({'code': 0, "data": data, "message": "查找到所有课程"})


@csrf_exempt
def changePasswd(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    old_passwd = info.get('old_password')
    new_passwd1 = info.get('new_password1')
    new_passwd2 = info.get('new_password2')
    if not stu_id or not old_passwd or not new_passwd2 or not new_passwd1:
        return JsonResponse({'code': 3, 'message': "所有字段必须填写！"})
    stu = md.stu.objects.get(stu_id=stu_id)
    if stu.stu_password != old_passwd:
        return JsonResponse({'code': 1, "message": "请输入正确的用户名或密码！"})
    if new_passwd1 != new_passwd2:
        return JsonResponse({'code': 2, 'message': "两次输入的新密码不一致！"})
    # stu.objects.update(stu_password=new_passwd2)
    stu.stu_password = new_passwd2
    return JsonResponse({"code": 0, 'message': "更改密码成功！"})


@csrf_exempt
def rateCourse(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    course_id = info.get('course_id')
    score = info.get('score')
    course = md.course.objects.get(course_id=course_id)
    course.course_rate = course.rate + score / course.course_total
    return JsonResponse({"code": 0, 'message': "评分成功！"})


@csrf_exempt
def makeComment(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    course_id = info.get('course_id')
    comment_content = info.get('comment_content')
    comment_time = datetime.datetime.now()
    course_rate = info.get("course_rate")
    global comment_idx
    comment_id = str(comment_idx + 1)
    comment_idx = 1 + comment_idx
    if not comment_content:
        return JsonResponse({"code": 1, 'message': "评价内容不能为空"})
    if len(comment_content) > 255:
        return JsonResponse({"code": 2, 'message': "评价内容不能超过255个字符"})
    md.comment.objects.create(comment_id=comment_id, comment_content=comment_content, comment_time=comment_time)
    stu_item = md.stu.objects.get(stu_id=stu_id)
    comment_item = md.comment.objects.get(comment_id=comment_id)
    course_item = md.course.objects.get(course_id=course_id)
    course_sum = course_item.course_sum
    course_cntComment = course_item.course_cntComment
    # course_item.objects.update(course_sum=course_sum+course_rate, course_cntComment=course_cntComment+1)
    # course_item.objects.update(course_rate=course_sum/course_cntComment)
    md.comment.objects.filter(course_id=course_id).update(course_sum=course_sum + course_rate,
                                                          course_cntComment=course_cntComment + 1)
    course_sum = course_item.course_sum
    course_cntComment = course_item.course_cntComment
    md.comment.objects.filter(course_id=course_id).update(course_rate=float(course_sum) / float(course_cntComment))
    md.stu_comment.objects.create(stu_id=stu_item, comment_id=comment_item)
    md.course_comment.objects.create(course_id=course_item, comment_id=comment_item)
    return JsonResponse({"code": 0, 'prompt': "评论成功！", 'comment_id': comment_id})


@csrf_exempt
def delComment(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    course_id = info.get('course_id')
    comment_id = info.get('comment_id')
    stu_item = md.stu.objects.get(stu_id=stu_id)
    comment_item = md.comment.objects.get(comment_id=comment_id)
    course_item = md.course.objects.get(course_id=course_id)
    md.comment.objects.filter(comment_id=comment_id).delete()
    md.stu_comment.objects.filter(stu_id=stu_item, comment_id=comment_item).delete()
    md.course_comment.objects.filter(course_id=course_item, comment_id=comment_item).delete()
    return JsonResponse({"code": 0, 'prompt': "评论删除成功！"})


@csrf_exempt
def newThemePost(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    themePost = info.get('themepost')
    global tp_idx
    tp_id = str(tp_idx + 1)
    tp_idx = tp_idx + 1
    tp_title = themePost.get('tp_title')
    tp_content = themePost.get("tp_content")
    tp_time = datetime.datetime.now()
    tp_isTeacher = False
    stu_item = md.stu.objects.get(stu_id=stu_id)
    if not tp_title:
        return JsonResponse({"code": 1, 'message': "标题不能为空！"})
    if len(tp_title) > 127:
        return JsonResponse({"code": 2, 'message': "标题内容不能超过127个字符"})
    if len(tp_content) > 512:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过512个字符"})
    md.themepost.objects.create(tp_id=tp_id, tp_title=tp_title, tp_content=tp_content, tp_time=tp_time,
                                tp_isTeacher=tp_isTeacher)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    md.stu_tp.objects.create(stu_id=stu_item, tp_id=tp_item)
    postCnt = md.stu.objects.get(stu_id=stu_id).postCnt
    md.stu.objects.filter(stu_id=stu_id).update(postCnt=postCnt + 1)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'tp_id': tp_id})


@csrf_exempt
def deleteThemePost(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    tp_id = info.get('tp_id')
    stu_item = md.stu.objects.get(stu_id=stu_id)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    md.themepost.objects.filter(tp_id=tp_id).delete()
    md.stu_tp.objects.filter(tp_id=tp_item, stu_id=stu_item).delete()
    return JsonResponse({"code": 0, 'prompt': "主题帖删除成功！"})


@csrf_exempt
def newFollowPost(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    tp_id = info.get('tp_id')
    global fp_idx
    fp_id = str(fp_idx + 1)
    fp_idx = fp_idx + 1
    fp_content = info.get('fp_content')
    fp_time = datetime.datetime.now()
    fp_isTeacher = False
    stu_item = md.stu.objects.get(stu_id=stu_id)
    if not fp_content:
        return JsonResponse({"code": 1, 'message': "内容不能为空！"})
    if len(fp_content) > 127:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过127个字符"})
    md.followpost.objects.create(fp_id=fp_id, fp_content=fp_content, fp_time=fp_time,
                                 fp_isTeacher=fp_isTeacher)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.stu_fp.objects.create(stu_id=stu_item, fp_id=fp_item)
    md.tp_fp.objects.create(tp_id=tp_item, fp_id=fp_item)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'fp_id': fp_id})


@csrf_exempt
def deleteFollowPost(request):
    info = json.loads(request.body)
    stu_id = info.get('stu_id')
    tp_id = info.get('tp_id')
    fp_id = info.get('fp_id')
    stu_item = md.stu.objects.get(stu_id=stu_id)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.followpost.objects.filter(fp_id=fp_id).delete()
    md.stu_fp.objects.filter(fp_id=fp_item, stu_id=stu_item).delete()
    md.tp_fp.objects.filter(fp_id=fp_item, tp_id=tp_item).delete()
    return JsonResponse({"code": 0, 'prompt': "评论删除成功！"})
# if __name__ == '__main__':
#     print(datetime.datetime.now())
