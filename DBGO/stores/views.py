import os

from django.shortcuts import render, redirect

# Create your views here.
# 开店
from DBGO import settings
from . import models


def add_store(request):
    """
    创建店铺
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'store/add_store1.html', {'msg': '请填写以下数据'})
    if request.method == "POST":
        name = request.POST['name']
        intro = request.POST['intro']
        user = request.user.normaluser
        store = models.Store(name=name, intro=intro, user=user)
        cover = request.FILES.get('cover', False)
        if cover:
            store.cover = cover
        store.save()
        return render(request, 'store/index.html', {'store': store})


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
        return render(request, 'store/update_html')
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
        return render(request, 'store/index.html', {'msg': "店铺信息修改成功", 'store': store})


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
    return render(request, 'store/index.html', {'msg': '店铺开始营业了', 'store': store})


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
    return render(request, 'store/index.html', {'msg': '店铺暂时歇业了', 'store': store})


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
    os.remove(settings.MEDIA_ROOT + old_cover)
    return render(request, 'store/index.html', {'store': store})