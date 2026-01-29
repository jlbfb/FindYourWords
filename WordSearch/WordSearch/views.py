from django.shortcuts import render
# from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Find Your Words',
        'font_style': 'sans_serif',
        'font_name': 'Sans Serif',
    }
    template = 'index.html'

    return render(request, template, context)
