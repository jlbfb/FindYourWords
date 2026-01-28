from django.shortcuts import render
# from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Find Your Words'
    }
    template = 'index.html'

    return render(request, template, context)
