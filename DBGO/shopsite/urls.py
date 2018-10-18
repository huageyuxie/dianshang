from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_loginout/$',views.user_loginout,name='user_loginout'),
    url(r'^register/$',views.register,name='register'),

]