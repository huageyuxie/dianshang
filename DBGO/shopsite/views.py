import uuid
from io import BytesIO

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect


from . import models
from . import utils


# 用户登录
def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'shopsite/user_login.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                login(request, user)
                return render(request, 'shopsite/index.html', {})
            else:
                # if request.POST['login_times'] >= 3:
                    # TODO 登录次数超过三次需要验证码
                request.POST['login_times'] += 1
                return render(request, 'shopsite/login.html', {'msg': '用户名或密码错误'})
        except:
            request.POST['login_times'] += 1
            return render(request, 'shopsite/login.html', {'msg': '用户名或密码错误'})


# 用户退出
def user_logout(request):
    """
    用户退出函数
    :param request:
    :return:
    """
    logout(request)
    return redirect('shopsite/index')


# 注册
def user_register(request):
    """
    用户注册函数
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'shopsite/user_register.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        code = request.POST['code']

        # 判断用户名是否可用
        try:
            User.objects.get(username=username)
            return render(request, 'shopsite/register.html', {"msg": "用户名已存在"})
        except:
            # 判断验证码是否正确
            #TODO
            user = User(nickname=username, password=password)
            user.save()
            normaluser = models.NormalUser(nickname=uuid.uuid1())
            normaluser.save()
            return render(request, 'shopsite/index.html',)


# 验证码
def code(request):
    img, create_code = utils.create_code()
    # 将生成的验证码保存到session中
    request.session['code'] = create_code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')
    return HttpResponse(file.getvalue(), 'image/png')




