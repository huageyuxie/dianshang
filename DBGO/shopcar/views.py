from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from goods.models import Goods
from . import models


@require_GET
@login_required
def add(request, count, goods_id):
    goods = Goods.objects.get(pk=good_id)
    user = request.user

    try:
        shopCar = models.ShopCart.object.get(user=user, goods=goods)
        shopCar.count += int(count)
        shopCar.allTotal = shopCar.count * goods.price
        shopCar.save()
    except:
        shopCar = models.ShopCart(goods=goods, user=user)
        shopCar.count = int(count)
        shopCar.allTotal = shopCar.count * goods.price
        shopCar.save()

    # return redirect(reversed("shopcar:list"))
    return HttpResponse("添加成功")


def list(request):
    shopcars = models.ShopCar.filter(user=request.user).order_by("-addTime")
    return render(request, "shopcar/list.html", {"shopcars": "shopcars"})
