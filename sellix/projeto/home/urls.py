from django.urls import path, include
from .views import index, page2, login
urlpatterns = [
    path('', index, name='introdução'),
    path('login/', login, name='login'),
    path('page2/', page2, name='page2'),
]