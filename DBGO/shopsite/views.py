import uuid
from io import BytesIO

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect


from . import models
from . import utils


# 首页
def index(request):
    """
    用户首页
    :param request:
    :return:
    """
    return render(request, 'shopsite/index.html')


# 用户登录
def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    try:
        request.session['login_times']
    except:
        request.session['login_times'] = 1
    if request.method == 'GET':
        request.session['login_times'] = 1
        return render(request, 'shopsite/user_login.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.session['login_times'] > 3:
            input_code = request.POST['code']
            print(request.session['code'])
            if input_code.upper() == request.session['code'].upper():
                del request.session['code']
            else:
                print('验证码错误')
                return render(request, 'shopsite/user_login.html', {'msg': '验证码错误'})
        try:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['login_times'] = 1
                    return render(request, 'shopsite/index.html', {})
                else:
                    print("账号未激活")
                    return render(request, 'shopsite/user_login.html', {'msg': '账户未激活'})
            else:
                request.session['login_times'] += 1
                return render(request, 'shopsite/user_login.html', {'msg': '用户名或密码错误'})

        except:
            request.session['login_times'] += 1
            return render(request, 'shopsite/user_login.html', {'msg': '用户名或密码错误'})


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
        print("使用了GET方式")
        return render(request, 'shopsite/user_register.html', {})
    if request.method == 'POST':
        print("使用POST方式")
        username = request.POST['username']
        password = request.POST['password']
        code = request.POST['code']

        # 判断验证码是否正确
        if code.upper() != request.session['code'].upper():
            print("验证码错误")
            return render(request, 'shopsite/user_register.html', {'msg': "验证码错误"})
        print("验证码正确")
        del request.session['code']

        # 判断用户名是否可用
        if User.objects.filter(username=username):
            print("用户名已存在")
            return render(request, 'shopsite/user_register.html', {"msg": "用户名已存在"})
        else:
            # 创建用户保存用户
            print("用户名可用")
            user = User.objects.create_user(username=username, password=password)
            normal_user = models.NormalUser(nickname="用户" + str(uuid.uuid1()), user=user)
            user.save()
            normal_user.save()
            print("用户保存成功")
            return render(request, 'shopsite./user_login.html',)


# 验证码
def code(request):
    img, create_code = utils.create_code()
    # 将生成的验证码保存到session中
    request.session['code'] = create_code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')
    return HttpResponse(file.getvalue(), 'image/png')




