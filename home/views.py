from django.shortcuts import render, redirect
from urllib.parse import quote

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def login(request):
    email_user = None
    senha_user = None

    if request.method == 'POST':
        email_user = request.POST.get('email')
        senha_user = request.POST.get('senha')

    if senha_user and senha_user in ['1234', 'pedro']:
        return redirect('page2')

    return render(request, 'core/login.html')

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
            numero_desenvolvedor = 5581994317883
            mensagem = f'Olá, meu nome é {nome_user} e gostaria de saber mais sobre a Sellix e como é o processo de cadastro.'
            mensagem_codificada = quote(mensagem)
            url_whatsapp = f'https://wa.me/{numero_desenvolvedor}?text={mensagem_codificada}'
            return redirect(url_whatsapp)

    return render(request, 'core/cadastro.html')
