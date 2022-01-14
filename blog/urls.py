from django.urls import path

from . import views

app_name = 'blog'   # 视图函数命名空间
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),   # 文章详情页
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),    # 同一分类下的文章
]
