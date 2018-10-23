# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-23 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shopsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('good_name', models.CharField(max_length=255, verbose_name='商品名称')),
                ('good_price', models.FloatField(verbose_name='商品单价')),
                ('good_stack', models.IntegerField(verbose_name='商品库存')),
                ('good_count', models.IntegerField(default=0, verbose_name='商品销量')),
                ('good_desc', models.CharField(max_length=255, verbose_name='商品详细介绍')),
                ('status', models.IntegerField(default=1, verbose_name='商品状态')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=255, unique=True, verbose_name='商品种类名称')),
                ('cover', models.ImageField(default='static/images/goods/default/default.jpg', upload_to='static/images/goods', verbose_name='商品类型图片')),
                ('intro', models.CharField(max_length=255, verbose_name='商品类型描述')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='品牌父类')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='good_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType'),
        ),
        migrations.AddField(
            model_name='goods',
            name='shopcart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopsite.ShopCart'),
        ),
    ]