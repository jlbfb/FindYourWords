from django.shortcuts import render

def index(request):
    context = {
        'title': 'Find Your Words'
    }
    template = 'index.html'

    
    return render(request, template, context)