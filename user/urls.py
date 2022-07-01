from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "user"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("findmyid/", views.findmyid, name="findmyid"),
    path("findmyid_done/", views.findmyid_done, name="findmyid_done"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("myboard/<int:pk>/", views.myboard, name="myboard"),
    path("mycomment/<int:pk>/", views.mycomment, name="mycomment"),
    path("mylikeboard/<int:pk>/", views.mylikeboard, name="mylikeboard"),
    path("mypwchange/<int:pk>/", views.mypwchange, name="mypwchange"),
    path("user_quit/<int:pk>/", views.user_quit, name="user_quit"),
    path("profile/<int:pk>/update/", views.name_edit, name="name_edit"),
    path("profile/<int:pk>/update_done/", views.name_edit_done, name="name_edit_done"),
]
