"""webServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path

from Server01.views import user, post, comment, views

urlpatterns = [
    path('', views.test_deployment, name='test_deployment'),
    # 用户相关
    path("api/login/", user.login),
    path('api/register/', user.register),
    path('api/index/', user.query_user_index),
    path('api/focus/', user.focusOn),
    path('api/user/focus/', user.get_user_focus),
    path('api/user/unfollow/', user.unfollow),
    path('api/user/update/', user.update_user_info),
    path('api/user/avatar/', user.update_avatar),
    path('api/user/post/', user.query_user_index_post),
    path('api/user/post/control/', user.user_control_index),
    path('api/user/remove/fan/', user.remove_fans),
    # 帖子相关
    path('api/upload/', post.upload_post),
    path('api/upload/info/', post.upload_post_info),
    path('api/post/detail/', post.get_post_detail),
    path('api/post/', post.query_post_index),
    path('api/post/control/', post.control_like_collect),
    path('api/post/delete/', post.post_delete),
    # 评论相关
    path('api/comment/', comment.do_comment),
    path('api/comment/main/', comment.get_comment),
    path('api/comment/reply/', comment.load_reply)
]
