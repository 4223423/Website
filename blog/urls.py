from django.urls import path 
from . import views 

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
#   path('<int:pk>/', views.single_post_page),  # blog/1  , single_post_page-로 가겠다   
#   path('', views.index),  
    path('',views.PostList.as_view()),
   # post_list.html 
    
]