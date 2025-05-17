from django.urls import path

from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("signup/",views.signup,name='signup'),
    path("signin/",views.signin,name='signin'),
    path("logout/",views.logout,name='logout'),
    path("settings/",views.settings,name='settings'),
    path("follow",views.follow,name='follow'),
    path("upload/",views.upload,name="upload"),
    path("search",views.search,name='search'),
    path("like/",views.like_post,name='like'),
    path("profile/<str:id>",views.profile,name='profile'),
    path("delete/<uuid:id>",views.delete_,name="del")

]