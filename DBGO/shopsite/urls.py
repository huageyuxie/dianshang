from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^user_register/$', views.user_register, name='user_register'),
    url(r'^user_self', views.user_self, name='user_self'),
    url(r'^(\d+)/update_user_self', views.update_user_self, name='update_user_self'),



    url(r'^code/$', views.code, name='code'),
    url(r'^$', views.index)
]
