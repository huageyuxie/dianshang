from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class NormalUser(models.Model):
    # 用户ID
    id = models.AutoField(primary_key=True)
    # 用户昵称
    nickname = models.CharField(max_length=255, unique=True, verbose_name="用户昵称")
    # 用户年龄
    age = models.IntegerField(default=0, verbose_name="用户年龄")
    # 用户性别
    gender = models.CharField(max_length=5, blank=True, null=True, verbose_name="用户性别")
    # 用户头像
    header = models.ImageField(upload_to='static/images/headers',
                               default='/static/images/headers/default.jpg',
                               verbose_name='用户头像')
    # 联系方式
    phone = models.CharField(max_length=30, blank=True, verbose_name='用户联系方式')

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    # 收货人姓名
    recv_name = models.CharField(max_length=255, verbose_name='收货人')
    # 收货人联系方式
    recv_phone = models.IntegerField(verbose_name="收货人联系方式")
    # 国家
    native = models.CharField(max_length=50, verbose_name="国家")
    # 省份
    provice = models.CharField(max_length=50, verbose_name="省份")
    # 市区
    city = models.CharField(max_length=50, verbose_name="市区")
    # 县区
    country = models.CharField(max_length=50, verbose_name="县区")
    # 街道
    street = models.CharField(max_length=255, verbose_name="街道")
    # 详细介绍
    desc = models.CharField(max_length=255, verbose_name="详细描述")
    # 是否是默认地址
    status = models.BooleanField(default=False, verbose_name="是否默认地址")

    # 属于谁的地址
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, verbose_name="地址所属用户")