# class 방식

# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView) :  # 아래 index부분과 같음.
    model = Post  # model 우리가 정한 함수  
    ordering = '-pk'
    
   # template_name = 'blog/index.html'  # 이렇게도 가능
    
class PostDetail(DetailView):
    model = Post
    

    
# 함수방식 
# from django.shortcuts import render
# from .models import Post 


# def index(request):  
#     posts = Post.objects.all().order_by('-pk') 
    
#     return render (
#         request, 
#         'blog/index.html',
#         {
#             'posts':posts,
#         }
#     )

# def single_post_page(request, pk) : 
#     post = Post.objects.get(pk=pk)  
    
#     return render(
#         request,
#         'blog/single_post_page.html', 
#         {
#              'post' : post,    
#         }
#     )
    
# # Create your views here.
