"""blog_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog_api.views import add_face,delete_face,encode_face

urlpatterns = [
    path('admin/', admin.site.urls),
    #增加人脸
    path('add_face/', add_face),
    #删除人脸
    path('delete_face/', delete_face)
    #重新编码
    path('encode_face/', encode_face)
]
