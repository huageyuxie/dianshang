from django.conf.urls import url


from . import views
urlpatterns = [
    url(r'add_good/$', views.add_good, name='add_good'),
    url(r'del_good/$', views.del_good, name='del_good'),
    url(r'update_good/$', views.update_good, name='update_good'),
    url(r'lower_good/$', views.lower_good, name='lower_good'),
]