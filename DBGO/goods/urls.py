from django.conf.urls import url
# from django.conf import settings


from . import views
urlpatterns = [
    url(r'add_good/(\d+)/$', views.add_good, name='add_good'),
    url(r'del_good/$', views.del_good, name='del_good'),
    url(r'update_good/$', views.update_good, name='update_good'),
    url(r'lower_good/$', views.lower_good, name='lower_good'),
    url(r'good_info/(\d+)/$', views.good_info, name='good_info'),
    url(r'shop_good/(\d+)/$', views.shop_good, name='shop_good'),
]