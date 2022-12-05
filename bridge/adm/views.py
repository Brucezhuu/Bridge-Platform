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
        adm_id = json_obj['adm_id']
        adm_password = json_obj['adm_password']

        # 检验字段是否为空
        if not adm_id or not adm_password:
            res = {'code': 500, 'prompt': '所有字段必须填写'}
            return JsonResponse(res)

        # 检验学号是否存在：
        try:
            adm = md.adm.objects.get(adm_id=adm_id)
        except:
            res = {'code': 500, 'prompt': '教工号不存在，请先注册'}
            return JsonResponse(res)

        # 检验密码是否正确：
        if adm.adm_password != adm_password:
            res = {'code': 500, 'prompt': '密码不正确，请重新输入'}
            return JsonResponse(res)

        token = myJWT.make_token(adm_id)
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
        Id = json_obj.get('adm_id')
        email = json_obj.get('email')
        password_1 = json_obj.get('adm_password1')
        password_2 = json_obj.get('adm_password2')
        adm_name = json_obj.get('adm_realName')
        if not Id:
            result = {'code': 10101, 'error': 'Please give me Id'}
            return JsonResponse(result)

        if not email:
            result = {'code': 10102, 'error': 'Please give me email'}
            return JsonResponse(result)
        if not adm_name:
            result = {'code': 10106, 'error': 'Please give me email'}
            return JsonResponse(result)

        if not password_1 or not password_2:
            result = {'code': 10103, 'error': 'Please give me password'}
            return JsonResponse(result)

        if password_1 != password_2:
            result = {'code': 10104, 'error': 'The password is not same!'}
            return JsonResponse(result)
        # 检查当前用户名是否可用
        old_user = md.adm.objects.filter(adm_id=Id)
        if old_user:
            result = {'code': 10105, 'error': 'The adm_id is already existed!'}
            return JsonResponse(result)
        # # 密码进行哈希　－　md5
        # p_m = hashlib.md5()
        # p_m.update(password_1.encode())

        # 创建用户
        try:
            md.adm.objects.create(adm_id=Id, adm_password=password_2, email=email,
                                  adm_name=adm_name)
        except Exception as e:
            print(e)
            result = {'code': 10106, 'error': 'The adm_id is already used!'}
            return JsonResponse(result)

        # todo 生成token
        token = myJWT.make_token(Id)
        result = {'code': 200, 'adm_id': Id, 'data': {'token': token}}
        return JsonResponse(result)
    else:
        res = {'code': 210, 'prompt': "请求方式应为POST"}
        return JsonResponse(res)


@csrf_exempt
def modify(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    md.adm.objects.filter(adm_id=adm_id).update(adm_name=info.get('adm_name'),
                                                adm_password=info.get('adm_password'),
                                                depart=info.get('depart'), email=info.get('email'),
                                                phone=info.get('phone'))
    return JsonResponse({'code': 210, 'prompt': "修改成功！"})


@csrf_exempt
def add(request):  # 管理员添加课程
    info = json.loads(request.body)
    # adm_id = info.get('adm_id')
    course = info.get('course')
    course_id = course['course_id']
    course_name = course['course_name']
    exist = md.course.objects.filter(course_id=course_id)
    if exist:
        res = {'code': 1, "prompt": "此课程ID已经存在，请重新设置！"}
        return JsonResponse(res)
    # exist = md.adm_course.objects.filter(course_id=course_id, adm_id=adm_id)
    # if exist:
    #     res = {'code': 2, "prompt": "您已开设了此课程，请勿重复开设！"}
    #     return JsonResponse(res)
    course_capacity = course.course_capacity
    course_intro = course.course_intro
    if not course_id or not course_name or not course_capacity:
        return JsonResponse({"code": 3, 'prompt': "课程ID或课程名称或课程容量字段不得为空！"})
    md.course.objects.create(course_total=0, course_id=course_id, course_name=course_name, course_intro=course_intro,
                             course_capacity=course_capacity)
    # md.adm_course.objects.create(adm_id=adm_id, course_id=course_id)
    return JsonResponse({"code": 0, 'prompt': "开课成功，可以在课程广场查看到此课程"})


@csrf_exempt
def delete(request):  # 教师不再设此课
    info = json.loads(request.body)
    # adm_id = info.get('adm_id')
    course = info.get('course')
    # md.adm_course.objects.filter(adm_id=adm_id, course_id=course['course_id']).delete()
    md.course.objects.filter(course_id=course['course_id']).delete()
    res = {'code': 0, "prompt": "删除课程成功！"}
    return JsonResponse(res)


@csrf_exempt
def getinfo(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    adm = md.adm.objects.filter(adm_id=adm_id).first()
    adm_password = adm.adm_password
    adm_name = adm.adm_name
    depart = adm.depart
    email = adm.email
    phone = adm.phone
    message = adm.message
    res = {"adm_id": adm_id, "adm_password": adm_password, "adm_name": adm_name,
           "depart": depart, "email": email, "phone": phone, "message": message}
    return JsonResponse(res)


@csrf_exempt
def changePasswd(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    old_passwd = info.get('old_password')
    new_passwd1 = info.get('new_password1')
    new_passwd2 = info.get('new_password2')
    adm = md.adm.objects.get(adm_id=adm_id)
    if not adm_id or not old_passwd or not new_passwd2 or not new_passwd1:
        return JsonResponse({'code': 3, 'message': "所有字段必须填写！"})
    if adm.adm_password != old_passwd:
        return JsonResponse({'code': 1, "message": "请输入正确的用户名或密码！"})
    if new_passwd1 != new_passwd2:
        return JsonResponse({'code': 2, 'message': "两次输入的新密码不一致！"})
    # adm.objects.update(adm_password=new_passwd2)
    adm.adm_password = new_passwd2
    return JsonResponse({"code": 0, 'message': "更改密码成功！"})


@csrf_exempt
def addMaterial(request):
    info = json.loads(request.body)
    material = info.get('material')
    material_id = material.material_id
    material_name = material.material_name
    material_intro = material.material_intro
    adm_id = info.get("adm_id")
    course_id = info.get('course_id')
    if not material_id or not material_intro or not material_name:
        return JsonResponse({'code': 3, 'message': "所有字段必须填写！"})
    exist = md.course.objects.filter(course_id=course_id)
    if not exist:
        res = {'code': 1, "prompt": "无此课程ID，请重新设置！"}
        return JsonResponse(res)
    # exist = md.adm_course.objects.filter(course_id=course_id, adm_id=adm_id)
    # if not exist:
    #     res = {'code': 2, "prompt": "无此课程开设记录！"}
    #     return JsonResponse(res)
    exist = md.adm.objects.filter(adm_id=adm_id)
    if not exist:
        res = {'code': 3, "prompt": "无此管理员！"}
        return JsonResponse(res)
    md.material.objects.create(material_id=material_id, material_name=material_name, material_intro=material_intro)
    material_item = md.material.objects.get(material_id=material_id)
    adm_item = md.adm.objects.get(adm_id=adm_id)
    course_item = md.course.objects.get(course_id=course_id)
    # md.adm_material.objects.create(adm_id=adm_id, material_id=material_id)
    md.course_material.objects.create(course_id=course_item, material_id=material_item)
    return JsonResponse({"code": 0, 'prompt': "添加课程资料成功！"})


@csrf_exempt
def newThemePost(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    themePost = info.get('themepost')
    global tp_idx
    tp_id = str(tp_idx + 1)
    tp_idx = tp_idx + 1
    tp_title = themePost.tp_title
    tp_content = themePost.tp_content
    tp_time = datetime.datetime.now()
    tp_isadm = True
    if not tp_title:
        return JsonResponse({"code": 1, 'message': "标题不能为空！"})
    if len(tp_title) > 127:
        return JsonResponse({"code": 2, 'message': "标题内容不能超过127个字符"})
    if len(tp_content) > 512:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过512个字符"})
    md.themepost.objects.create(tp_id=tp_id, tp_title=tp_title, tp_content=tp_content, tp_time=tp_time,
                                tp_isadm=tp_isadm)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    adm_item = md.adm.objects.get(adm_id=adm_id)
    md.adm_tp.objects.create(adm_id=adm_item, tp_id=tp_item)
    postCnt = md.adm.objects.get(adm_id=adm_id).postCnt
    md.adm.objects.filter(adm_id=adm_id).update(postCnt=postCnt + 1)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'tp_id': tp_id})


@csrf_exempt
def deleteThemePost(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    tp_id = info.get('tp_id')
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    adm_item = md.adm.objects.get(adm_id=adm_id)
    md.themepost.objects.filter(tp_id=tp_id).delete()
    md.adm_tp.objects.filter(tp_id=tp_item, adm_id=adm_item).delete()
    return JsonResponse({"code": 0, 'prompt': "主题帖删除成功！"})


@csrf_exempt
def newFollowPost(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    tp_id = info.get('tp_id')
    global fp_idx
    fp_id = str(fp_idx + 1)
    fp_idx = fp_idx + 1
    fp_content = info.get('fp_content')
    fp_time = datetime.datetime.now()
    fp_isadm = False
    adm_item = md.adm.objects.get(adm_id=adm_id)
    if not fp_content:
        return JsonResponse({"code": 1, 'message': "内容不能为空！"})
    if len(fp_content) > 127:
        return JsonResponse({"code": 3, 'message': "帖子内容不能超过127个字符"})
    md.followpost.objects.create(fp_id=fp_id, fp_content=fp_content, fp_time=fp_time,
                                fp_isadm=fp_isadm)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.adm_fp.objects.create(adm_id=adm_item, fp_id=fp_item)
    md.tp_fp.objects.create(tp_id=tp_item, fp_id=fp_item)
    return JsonResponse({"code": 0, 'prompt': "发表成功！", 'fp_id': fp_id})


@csrf_exempt
def deleteFollowPost(request):
    info = json.loads(request.body)
    adm_id = info.get('adm_id')
    tp_id = info.get('tp_id')
    fp_id = info.get('fp_id')
    adm_item = md.adm.objects.get(adm_id=adm_id)
    tp_item = md.themepost.objects.get(tp_id=tp_id)
    fp_item = md.followpost.objects.get(fp_id=fp_id)
    md.followpost.objects.filter(fp_id=fp_id).delete()
    md.adm_fp.objects.filter(fp_id=fp_item, adm_id=adm_item).delete()
    md.tp_fp.objects.filter(fp_id=fp_item, tp_id=tp_item).delete()
    return JsonResponse({"code": 0, 'prompt': "评论删除成功！"})
# if __name__ == '__main__':
