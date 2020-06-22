from django.conf.urls import url, include

from myproject.demo1 import views

urlpatterns = [
    url('upload/', views.upload),
    url('show/', views.show)
]
