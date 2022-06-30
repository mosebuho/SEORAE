from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("all/", views.all, name="all"),
    path("free/", views.free, name="free"),
    path("recipe", views.recipe, name="recipe"),
    path("hoogie/", views.hoogie, name="hoogie"),
    path("question/", views.question, name="question"),
    path("notice/", views.notice, name="notice"),
    path("write/", views.write, name="write"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("detail/<int:pk>/delete/", views.delete, name="delete"),
    path("detail/<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/comment/write/", views.comment_write, name="comment_write"),
    path("<int:pk>/comment/delete/", views.comment_delete, name="comment_delete"),
    path("<int:pk>/comment/update/", views.comment_update, name="comment_update"),
    path("<int:pk>/comment/update_done/", views.comment_update_done, name="comment_update_done"),
    path("like/", views.like, name="like"),
]
