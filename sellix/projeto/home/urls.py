from django.urls import path
from .views import add_funcionario, bloqueio, index, modulos, login_view, cadastro, controle, deletar_usuario, dashboard, politica, add_item, add_venda


urlpatterns = [
    path('', index, name='introducao'),
    path('login/', login_view, name='login'),
    path('modulos/', modulos, name='modulos'),
    path('cadastro/', cadastro, name='cadastro'),
    path('controle/', controle, name='controle'),
    path('bloqueio/', bloqueio, name='bloqueio'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add_funcionario/', add_funcionario, name='add_funcionario'),
    path('dashboard/add_item/', add_item, name='add_item'),
    path('dashboard/politica/', politica, name='politica'),
    path('dashboard/add_venda/', add_venda, name='add_venda'),
    path('controle/deletar/<int:user_id>/', deletar_usuario, name='deletar_usuario'),
 ]