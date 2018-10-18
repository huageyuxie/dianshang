from django.shortcuts import render


#用户登录
def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'shopsite/login.html', {})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']



#用户退出
def user_loginout(request):
    """
    用户退出函数
    :param request:
    :return:
    """
    pass


#注册
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
        confirm_pwd = request.POST['confirm_pwd']
        code = request.POST['code']




