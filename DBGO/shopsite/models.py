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
    gender = models.BooleanField(blank=True, verbose_name="用户性别")
    # 用户头像
    header = models.ImageField(upload_to='static/images/headers',
                               default='static/images/headers/default.jpg',
                               verbose_name='用户头像')
    # 联系方式
    phone = models.CharField(max_length=30, blank=True, verbose_name='用户联系方式')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
