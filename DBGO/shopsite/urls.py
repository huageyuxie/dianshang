from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.user_register, name='user_register'),

]