import random
from io import BytesIO

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


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
        try:
            is_remember = request.POST['is_remember']
        except:
            is_remember = ''
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
                    login_user = models.NormalUser.objects.get(user=user)
                    request.session['login_times'] = 1
                    request.session['login_user'] = login_user
                    if is_remember == 'YES':
                        response = redirect('/shopsite/index/')
                        response.set_cookie('login_user', login_user, max_age=1800)
                        return response
                    else:
                        return redirect('/shopsite/index/')
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
    try:
        del request.session['login_user']
    except:
        return redirect('/shopsite/index')


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

        # 判断验证码是否正确
        if code.upper() != request.session['code'].upper():
            return render(request, 'shopsite/user_register.html', {'msg': "验证码错误"})
        del request.session['code']

        # 判断用户名是否可用
        if User.objects.filter(username=username):
            return render(request, 'shopsite/user_register.html', {"msg": "用户名已存在"})
        else:
            # 创建用户保存用户
            user = User.objects.create_user(username=username, password=password)
            normal_user = models.NormalUser(nickname="用户" + random.randint(1000000), user=user)
            user.save()
            normal_user.save()
            return render(request, 'shopsite/index.html',)


# 个人信息展示界面
@require_GET
@login_required(login_url='/shopsite/user_login/')
def user_self(request):
    """
    返回当前用户个人信息界面，可以使用request.session['login_user'].属性查看信息
    :param request:
    :return:
    """
    return render(request, 'shopsite/user_self.html')


#用户修改界面
@login_required(login_url="/shopsite/user_login/")
def update_user_self(request):
    """
    修改用户信息界面
    修改nickname,age,gender
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'shopsite/update_user_self.html')
    if request.method == 'POST':
        nickname = request.POST['nickname']
        age = request.POST['age']
        gender = request.POST['gender']
        new_user = models.NormalUser.objects.get(user=request.user)
        new_user.nickname = nickname
        new_user.age = age
        new_user.gender = gender
        new_user.save()
        return redirect('/shopsite/user_self/')


# 修改个人密码
@login_required(login_url="/shopsite/user_login/")
def update_user_password(request):
    """
    修改个人密码
    :param request:
    :return:
    """
    if request.method == "GET":
        return redirect('/shopsite/update_user_self/')
    if request.method == "POST":
        password = request.POST['password']
        new_password = request.POST['new_password']
        if password == request.user.password:
            user = models.User.objects.get(username=request.user.username)
            user.password = new_password
            return render(request, 'shopsite/user_login.html', {'msg':
                                                                 '修改密码成功，请重新登陆'})
        else:
            return redirect('/shopsite/update_user_self/')


# 修改头像
@login_required(login_url="/shopsite/user_login/")
def update_user_header(request):
    """
    修改头像
    :param request:
    :return:
    """
    user = request.user
    try:
        header = request.FILES.get("avatar")
        header = '/static/images/headers/' + user.username + header
    except:
        header = '/static/images/headers/default.jpg'
    user.normaluser.header = header
    user.save()
    user.normaluser.save()
    return redirect('/shopsite/update_user_self/')



# 验证码
def code(request):
    """
    生成验证码
    :param request:
    :return:
    """
    img, create_code = utils.create_code()
    # 将生成的验证码保存到session中
    request.session['code'] = create_code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')
    return HttpResponse(file.getvalue(), 'image/png')


