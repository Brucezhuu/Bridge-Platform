import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import bridge.models as md
from bridge.tools import myJWT


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == request.POST:
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
            res = {'code': 500, 'prompt': '管理员账号不存在，请先注册'}
            return JsonResponse(res)

        # 检验密码是否正确：
        if adm.adm_password != adm_password:
            res = {'code': 500, 'prompt': '密码不正确，请重新输入'}
            return JsonResponse(res)

        token = myJWT.make_token(adm_id)
        res = {'code': 200, 'prompt': "登录成功！", 'data': {'token': token.decode()}}
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

        Id = json_obj.get('adm_id')
        email = json_obj.get('email')
        password_1 = json_obj.get('adm_password_1')
        password_2 = json_obj.get('adm_password_2')
        if not Id:
            result = {'code': 10101, 'error': 'Please give me username'}
            return JsonResponse(result)
        if not email:
            result = {'code': 10102, 'error': 'Please give me email'}
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
            md.adm.objects.create(adm_id=Id, adm_password=password_2, email=email)
        except Exception as e:
            print(e)
            result = {'code': 10106, 'error': 'The adm_id is already used!'}
            return JsonResponse(result)

        # todo 生成token
        token = myJWT.make_token(Id)
        result = {'code': 200, 'adm_id': Id, 'data': {'token': token.decode()}}
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
                                                phone=info.get('info'))
    return JsonResponse({'code': 210, 'prompt': "修改成功！"})
