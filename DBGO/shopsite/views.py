import os
import random
from io import BytesIO
import uuid

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from DBGO import settings
from shopsite.utils import phone_code
from . import models
from . import utils
from dysms_python import demo_sms_send


# 首页
def index(request):
    """
    用户首页
    :param request:
    :return:
    """
    return render(request, 'shopsite/user_login.html')


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
        try:
            # 手机验证码
            phone = request.POST['login_phone']
            my_code = request.POST['phone_code']
            if my_code == request.session['phone_code']:
                del request.session['phone_code']
                if not models.NormalUser.objects.fliter(phone=phone):
                    user = User.objects.create_user(username=phone, password="")
                    normaluser = models.NormalUser(phone=phone, status=2, nickname="用户" + str(random.randint(0, 1000000)), user=user)
                    shopcart = models.ShopCart()
                    user.is_active = 1
                    user.save()
                    shopcart.save()
                    normaluser.save()
                    login(request, user)
                    return render(request, 'shopsite/user_self.html', {'msg': '您是使用手机验证码快速登陆的，请尽快完善您的密码和个人资料'})
                else:
                    user = models.NormalUser.objects.get(phone=phone).user
                    login(request, user)
                    return render(request, 'shopsite/index.html',)
            else:
                return render(request, 'shopsite/user_login.html', {'msg': '手机验证码错误'})
        except:
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
            normal_user = models.NormalUser(nickname="用户" + str(random.randint(0, 1000000)), user=user)
            shopcart = models.ShopCart(user=normal_user)
            normal_user.shopcart = shopcart
            user.save()
            normal_user.save()
            return render(request, 'shopsite/user_login.html',)


# 个人信息展示界面
@require_GET
@login_required(login_url='/shopsite/user_login/')
def user_self(request):
    """
    返回当前用户个人信息界面，可以使用request.session['login_user'].属性查看信息
    :param request:
    :return:
    """
    user = models.NormalUser.objects.get(user=request.user)
    date = str(user.birthday)[:10]
    print("date:" + date)
    try:
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
    except:
        year = month = day = ''
    print("year:" + year)
    print("month:" + month)
    print("day:" + day)
    return render(request, 'shopsite/user_self.html', {'year': year, 'month': month, 'day': day})


# 用户修改界面
@login_required(login_url="/shopsite/user_login/")
def update_user_self(request):
    """
    修改用户信息界面
    修改nickname,age,gender
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'shopsite/user_self.html')
    if request.method == 'POST':
        new_user = models.NormalUser.objects.get(user=request.user)
        if request.user.normaluser.status == 2:
            username = request.POST.get('username', False)
            if username:
                new_user.username = username
        nickname = request.POST['nickname']
        age = request.POST['age']
        gender = request.POST['gender']
        birthday = request.POST['YYYY'] + '-' + request.POST['MM'] + '-' + request.POST['DD']
        email = request.POST['email']
        phone = request.POST['phone']
        new_user.nickname = nickname
        new_user.age = age
        new_user.gender = gender
        new_user.birthday = birthday
        new_user.email = email
        new_user.phone = phone
        print("修改")
        new_user.save()
        print("修改成功")
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
        return redirect('/shopsite/user_self/')
    if request.method == "POST":
        password = request.POST['password']
        new_password = request.POST['new_password']
        try:
            if authenticate(username=request.user.username, password=password):
                print("密码正确")
                user = models.User.objects.get(username=request.user.username)
                user.set_password(new_password)
                user.save()
                return render(request, 'shopsite/user_login.html', {'msg': '修改密码成功，请重新登陆'})
            else:
                print("密码错误1")
                return redirect('/shopsite/user_self/')
        except:
            print("密码错误2")
            return redirect('/shopsite/user_self/')


# 修改头像
@login_required(login_url="/shopsite/user_login/")
def update_user_header(request):
    """
    修改头像
    :param request:
    :return:
    """
    user = request.user
    avatar2 = str(user.normaluser.header)
    header = request.FILES.get("avatar", False)
    if header:
        user.normaluser.header = header
    user.save()
    user.normaluser.save()
    if avatar2[-11:] != 'default.jpg':
        try:
            os.remove(avatar2)
        except Exception as e:
            print(e)
    return redirect('/shopsite/user_self/')



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


def send_msg(request, phone):
    p_code = phone_code(phone)
    request.session['phone_code'] = p_code
    return HttpResponse(p_code)



def goods_car(request):
    """
    购物车界面
    :param request:
    :return:
    """
    shopcarts = models.ShopCart.objects.filter(user=request.user)
    return render(request,'shopsite/goods_car.html', {'shopcarts': shopcarts})


def cancel_buy(request, shopcart_id):
    """
    删除购物车的商品
    :param request:
    :return:
    """
    shopcart = models.ShopCart.objects.get(id=shopcart_id)
    good = models.Goods.objects.get(shopcart=shopcart)
    good.good_stack += shopcart.count
    good.good_count -= shopcart.count
    good.save()
    shopcart.delete()
    return redirect('/shopsite/goods_car/')


    return render(request,'shopsite/goods_car.html')


# 添加地址
def add_address(request):
    if request.method == "GET":
        return render(request, "shopsite/add_address.html")
    else:
        recv_name = request.POST["recv_name"]
        recv_tel = request.POST["recv_tel"]
        province = request.POST["province"]
        city = request.POST["city"]
        area = request.POST["area"]
        street = request.POST["street"]
        desc = request.POST["desc"]

        try:
            # 地址设为默认
            request.POST["is_default"]
            addresses = models.Address.objects.filter(user=request.user)
            for address in addresses:
                address.is_default = False
                address.save()
            address = models.Address(recv_name=recv_name, recv_tel=recv_tel, province=province, \
                           city=city, area=area, street=street, desc=desc, user=request.user, \
                           is_default=True)
            address.save()
        except:
            address = models.Address(recv_name=recv_name, recv_tel=recv_tel, province=province, \
                                     city=city, area=area, street=street, desc=desc, user=request.user, \
                                     is_default=False)
            address.save()

        return redirect(reverse("shopsite/address_list"))


def address_list(request):
    addresses = models.Address.objects.filter(user=request.user)
    return render(request, "shopsite/list_address.html", {"addresses": addresses})
