import os

from django.shortcuts import render, redirect

# Create your views here.
# 开店
from goods.models import Goods
from . import models


# 首页
def index(request, store_id):
    """
    店铺首页展示
    :param request:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    goods = Goods.objects.filter(store=store)
    request.session['goods'] = goods
    request.session['store'] = store
    return render(request, 'stores/index.html')



def add_store(request):
    """
    创建店铺
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'stores/add_store1.html', {'msg': '请填写以下数据'})
    if request.method == "POST":
        name = request.POST['name']
        intro = request.POST['intro']
        user = request.user.normaluser
        store = models.Store(name=name, intro=intro, user=user)
        cover = request.FILES.get('cover', False)
        if cover:
            store.cover = cover
        store.save()
        return render(request, 'stores/index.html', {'store': store})


# 删除店铺
def del_store(request, store_id):
    """
    删除店铺
    :param request:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    store.status = 0
    store.save()
    return redirect('/shopsite/index/')


# 修改店铺
def update_store(request, store_id):
    """
    修改店铺的信息
    :param request:
    :param store_id:
    :return:
    """
    if request.method == 'GET':
        store = models.Store.objects.get(id=store_id)
        return render(request, 'stores/update_store.html', {'store': store})
    if request.method == "POST":
        name = request.POST['name']
        intro = request.POST['intro']
        user = request.user.normaluser
        store = models.Store.objects.get(id=store_id)
        store.name = name
        store.intro = intro
        store.user = user
        cover = request.FILES.get('cover', False)
        if cover:
            store.cover = cover
        store.save()
        return render(request, 'stores/index.html', {'msg': "店铺信息修改成功", 'store': store})


# 店铺营业
def open_store(request, store_id):
    """
    店铺开始营业
    :param request:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    store.status = 1
    store.save()
    return render(request, 'stores/index.html', {'msg': '店铺开始营业了', 'store': store})


# 店铺歇业
def close_store(request, store_id):
    """
    店铺展示歇业
    :param request:
    :param store_id:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    store.status = 2
    store.save()
    return render(request, 'stores/index.html', {'msg': '店铺暂时歇业了', 'store': store})


# 更换店铺封面
def update_cover(request, store_id):
    """
    更换店铺封面
    :param request:
    :param store_id:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    old_cover = str(store.cover)
    cover = request.FILES.get("cover", False)
    if cover:
        store.cover = cover
    store.save()
    if old_cover[-11:] != 'default.jpg':
        try:
            os.remove(old_cover)
        except Exception as e:
            print(e)
    return render(request, 'stores/index.html', {'store': store})

