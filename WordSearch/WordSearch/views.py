from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': 'Find Your Words'
    }
    template = 'index.html'

    
    return render(request, template, context)

# def grids(request, file_name):
#     file_source = fr'/grids/{file_name}'
#     file_text = ''
#     with open(file_source, 'w') as f:
#         for word in f:
#             file_text = file_text + word
#     print(file_text)

#     response = HttpResponse(file_text, content_type='text/plain')
#     response['Content-Disposition'] = f'attachment; filename="{file_name}"'
#     # response.write(p.body)

#     return HttpResponse(response)