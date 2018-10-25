from django.conf.urls import  url

from . import views


urlpatterns = [
    url(r"^(?P<count>\d+)/(?P<good_id>)/add/$", views.add, name="add"),
    url(r"^list/$", views.list, name="list"),
]