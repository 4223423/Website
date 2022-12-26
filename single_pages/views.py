from django.shortcuts import render
from blog.models import Post


# 함수방식( <-> class)
def landing(request) :
    recent_posts = Post.objects.order_by('-pk')[:3]
    # 끝에서 3개까지만 역순으로 (최신) 포스트 가져오기
    # blog post_list 에 나오는 최신 글 3개를 가져옴.ArithmeticError
    return render(
        request, 
        'single_pages/landing.html',
        {
            'recent_posts' : recent_posts,
        }
        
    )

def about_me(request) :
    return render(
        request,
        'single_pages/about_me.html'
    )

# Create your views here.
