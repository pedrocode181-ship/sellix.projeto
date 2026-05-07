from django.urls import path, include
from .views import index, page2
urlpatterns = [
    path('', index, name='login'),
    path('page2/', page2, name='page2'),
]