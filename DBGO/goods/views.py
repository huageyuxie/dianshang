from django.http import HttpResponse
from django.shortcuts import render,redirect


from . import models
# Create your views here.
# 商品品牌的添加
def add_goods_type(request):
    """
    添加商品的品牌
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'goods/add_goods_type', {'msg': '请在下方完善商品品牌信息'})
    if request.method == "POST":
        goodstype_name = request.POST['goodstype_name']
        goodstype_intro = request.POST['goodstype_intro']
        goodstype_cover = request.FILE.get('goodstype_cover')
        goodstype_parent = request.POST.get('parent', '')
        goods_type = models.GoodsType(type_name=goodstype_name, cover=goodstype_cover, intro=goodstype_intro, parent=goodstype_parent)
        goods_type.save()
        return render(request, 'stores/self_store.html')



# 商品添加
def add_good(request, store_id):
    """
    商品的添加函数
    :param request:
    :return:
    """
    store = models.Store.objects.get(id=store_id)
    if request.method == "GET":
        return render(request, 'goods/add_good.html', {'msg': '添加你想要售卖的商品吧', 'store': store})
    if request.method == "POST":
        good_name = request.POST['good_name']
        good_price = request.POST['good_price']
        good_stack = request.POST['good_stack']
        good_desc = request.POST['good_desc']
        type_name = request.POST['type_name']
        good_type = models.GoodsType.objects.get(type_name=type_name)
        good = models.Goods(good_name=good_name, good_price=good_price, good_stack=good_stack, good_desc=good_desc, good_type=good_type)
        good.store = store
        good.save()
        goods = models.Goods.objects.filter(store=store)
        if goods:
            request.session['goods'] = goods
            return render(request, 'stores/index.html', {'store': store})
        return render(request, 'stores/index.html', {'store': store})


# 商品的修改
def update_good(request, good_id):
    """
    修改商品信息函数
    :param request:
    :return:
    """
    good = models.Goods.objects.get(id=good_id)
    if request.method == "GET":
        return render(request, 'stores/self_store.html', {'good': good})
    if request.method == "POST":
        good_name = request.POST['good_name']
        good_price = request.POST['good_price']
        good_stack = request.POST['good_stack']
        good_desc = request.POST['good_desc']
        good_type = request.POST['good_type']
        good.good_name = good_name
        good.good_price = good_price
        good.good_stack = good_stack
        good.good_desc = good_desc
        good.good_type = good_type
        good.save()
        return render(request, 'stores/index.html')


# 商品的隐藏
def lower_good(request, good_id):
    """
    商品售空，商家删除商品---等于展示的隐藏
    :param request:
    :param good_id:
    :return:
    """
    good = models.Goods.objects.get(id=good_id)
    good.status = 0
    good.save()
    return render(request, 'stores/self_store.html')


# 商品的信息
def good_info(request, good_id):
# def good_info(request):
    """
    展示商品信息
    :param request:
    :return:
    """
    try:
        good = models.Goods.objects.get(id=good_id)
    except:
        return redirect('/shopsite/index/')
    return render(request, 'goods/goods_show.html', {'good': good})
    # return render(request, 'goods/goods_show.html')


# 添加购物车
def shop_good(request, good_id):
    """
    添加商品到购物车
    :param request:
    :return:
    """
    try:
        good = models.Goods.objects.get(id=good_id)
        request.user.normaluser.shopcart.goods = good
        return HttpResponse('success')
    except:
        return render(request, "goods/goods_show.html", {"good": good})



# 商品的删除
def del_good(request, good_id):
    """
    删除商品-彻底删除
    :param request:
    :return:
    """
    good = models.Goods.objects.get(id=good_id)
    good.delete()
    return render(request, 'stores/self_store.html')

