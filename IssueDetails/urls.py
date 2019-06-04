from django.urls import path

from . import views

app_name = "IssueDetails"

urlpatterns = [
    path('register_user', views.register_user, name='register_user'),
    path('issues', views.read_repo, name='read_repo'),
    path('', views.index, name='index'),
]
