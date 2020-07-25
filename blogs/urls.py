from django.urls import path

from .views import (about,
                    PostlListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostlListView)

app_name = 'blogs'

urlpatterns = [
    path('', PostlListView.as_view(), name='blogs-home'),
    path('about/', about, name='blogs-about'),

    path('post/detail/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/update/<slug:slug>/', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostlListView.as_view(), name='user-posts'),
]