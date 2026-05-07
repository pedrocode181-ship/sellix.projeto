from django.urls import path, include
from .views import index, modulos, page2, login, cadastro
urlpatterns = [
    path('', index, name='introdução'),
    path('login/', login, name='login'),
    path('page2/', page2, name='page2'),
    path('modulos/', modulos, name='modulos'),
    path('cadastro/', cadastro, name='cadastro')
]