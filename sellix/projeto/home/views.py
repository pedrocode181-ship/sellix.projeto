from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def login(request):
    email_user = None
    senha_user = None

    if request.method == 'POST':
        email_user = request.POST.get('email')
        senha_user = request.POST.get('senha')

    if senha_user in ['1234', 'pedro']:
        return redirect('page2')

    return render(request, 'core/login.html')

def page2(request):
    return render(request, 'core/page2.html')

def modulos(request):
    return render(request, 'core/modulos.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')