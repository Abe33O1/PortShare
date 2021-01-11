from django.urls import path
from . import views
from .views import home, PostListView, PostDetailView, PostCreateView, PostUpdateView,PostDeleteView,UserPostListView, tagged

urlpatterns = [
    path('', PostListView.as_view(), name='portfolio-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('tag/<slug:slug>/', tagged, name="tagged"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='portfolio-about'),
]
