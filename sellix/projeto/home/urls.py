from django.urls import path
from .views import add_funcionario, bloqueio, index, modulos, login_view, cadastro, controle, deletar_usuario, dashboard, politica, add_item


urlpatterns = [
    path('', index, name='introducao'),
    path('login/', login_view, name='login'),
    path('modulos/', modulos, name='modulos'),
    path('cadastro/', cadastro, name='cadastro'),
    path('controle/', controle, name='controle'),
    path('bloqueio/', bloqueio, name='bloqueio'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_funcionario/', add_funcionario, name='add_funcionario'),
    path('add_item/', add_item, name='add_item'),
    path('politica/', politica, name='politica'),
    path('controle/deletar/<int:user_id>/', deletar_usuario, name='deletar_usuario'),

]
