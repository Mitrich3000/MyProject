from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [

    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('add/', views.PostCreate.as_view(), name='add'),
    path('update/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.PostDelete.as_view(), name='delete'),
    path('subscribe/<int:pk>/', views.subscribe, name='subscribe'),
    path('readed/<int:id>/', views.readed, name='readed'),
    path('', views.PostListView.as_view(), name='blog'),


]