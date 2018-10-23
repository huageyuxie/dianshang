from django.conf.urls import url


from . import views
urlpatterns = [
    url(r'add_store/$', views.add_store, name='add_store'),
    url(r'del_store/$', views.del_store, name='del_store'),
    url(r'update_store/$', views.update_store, name='update_store'),
    url(r'open_store/$', views.open_store, name='open_store'),
    url(r'close_store/$', views.close_store, name='close_store'),
    url(r'update_cover/$', views.update_cover, name='cupdate_cover'),
]