from django.shortcuts import render


# 함수방식( <-> class)
def landing(request) :
    return render(
        request, 
        'single_pages/landing.html'
    )
def about_me(request) :
    return render(
        request,
        'single_pages/about_me.html'
    )

# Create your views here.
