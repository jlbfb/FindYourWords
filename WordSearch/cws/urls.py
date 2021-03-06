from django.urls import path, include
from .views import (index,
                    grid,
                    verify,
                    board,
                    print_view,
                    download,
                    delete_board)

app_name = 'cws'

urlpatterns = [
    path('', index, name='index'),
    path('update', index, name='update'),
    path('grid', grid, name='grid'),
    path('board', board, name='board'),
    path('download', download, name='download'),
    path('dboard', delete_board, name='dboard'),
    path('verify', verify, name='verify'),
    path('print_view', print_view, name='print_view')
    ]