from django.shortcuts import render

def home_view(request):
    context = {
        'title': 'Home Page',
        'message': 'Hello World from Django SSR!',
    }
    return render(request, 'pages/home.html', context)
