from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('gmail', '').strip()
        password = request.POST.get('senha', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # cria session

            if user.is_superuser:
                return redirect('controle')

            return redirect('page2')

        return render(request, 'core/login.html', {
            'error': 'Login inválido',
            'gmail': username,
        })

    return render(request, 'core/login.html')


@login_required
def page2(request):
    return render(request, 'core/page2.html')


def modulos(request):
    return render(request, 'core/modulos.html')


def cadastro(request):
    nome_user = ''
    gmail_user = ''

    if request.method == 'POST':
        gmail_user = request.POST.get('gmail', '').strip()
        nome_user = request.POST.get('nome', '').strip()

        if nome_user and gmail_user:
            numero_desenvolvedor = '5581994317883'
            mensagem = (
                f'Olá, meu nome é {nome_user} e gostaria de saber mais sobre a Sellix '
                'e como é o processo de cadastro.'
            )
            mensagem_codificada = quote(mensagem)
            url_whatsapp = f'https://wa.me/{numero_desenvolvedor}?text={mensagem_codificada}'
            return redirect(url_whatsapp)

        # se faltar algum campo, mostra erro e mantém valores
        return render(request, 'core/cadastro.html', {
            'error': 'Preencha nome e e-mail',
            'nome': nome_user,
            'gmail': gmail_user,
        })

    return render(request, 'core/cadastro.html')


# ==========================
# 🔐 ADMIN (SÓ VOCÊ)
# ==========================


@login_required
def controle(request):
    if not request.user.is_superuser:
        return redirect('page2')

    usuarios = User.objects.all()
    return render(request, 'core/controle.html', {'usuarios': usuarios})


@login_required
def deletar_usuario(request, user_id):
    if not request.user.is_superuser:
        return redirect('page2')

    usuario = get_object_or_404(User, id=user_id)

    # impede deletar você mesmo sem querer
    if usuario == request.user:
        return redirect('controle')

    # aceitar apenas POST para evitar CSRF via link
    if request.method != 'POST':
        return redirect('controle')

    usuario.delete()
    return redirect('controle')