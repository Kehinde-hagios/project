from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog_home'),
    path('user/<str:username>', ProfileView.as_view(), name='blog_user'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog_post'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
