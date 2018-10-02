from django.urls import path
from . import views

app_name = "gifs"

urlpatterns = [
    path('', views.index, name='index'),
    path('new/<path:gif_url>', views.new_gif, name='new'),
    path('editor/<path:gif_url>', views.gif_editor, name='editor'),
    path('edit_gif_to_category/<path:gif_url>', views.edit_gif_to_category,
         name='edit_gif_to_category'),
    path('add_gif_to_category/<path:gif_url>', views.add_gif_to_category,
         name='add_gif_to_category'),
    path('delete_gif_to_user/<path:gif_url>', views.delete_gif_to_user,
         name='delete_gif_to_user'),
    path('search', views.search, name='search'),
]

handler404 = 'gifs.views.handler404'
handler500 = 'gifs.views.handler500'
