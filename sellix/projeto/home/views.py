from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Company, Funcionario, Membership, TableItem


# -----------------------
# PÁGINAS PÚBLICAS
# -----------------------

def index(request):
    return render(request, 'core/index.html')


def modulos(request):
    return render(request, 'core/modulos.html')


def bloqueio(request):
    return render(request, 'core/bloqueio.html')


def politica(request):
    return render(request, 'core/politica.html')


# -----------------------
# LOGIN
# -----------------------

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if not user:
            return render(request, 'core/login.html', {
                'error': 'Login inválido'
            })

        auth_login(request, user)

        if user.is_superuser:
            return redirect('controle')

        return redirect('dashboard')

    return render(request, 'core/login.html')


# -----------------------
# CADASTRO
# -----------------------

def cadastro(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        description = request.POST.get('descriçao')

        if User.objects.filter(username=username).exists():
            return render(request, 'core/cadastro.html', {
                'error': 'Usuário já existe'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        company = Company.objects.create(
            name=username,
            description=description
        )

        Membership.objects.create(
            user=user,
            company=company,
            is_admin=True
        )

        auth_login(request, user)

        return redirect('dashboard')

    return render(request, 'core/cadastro.html')


# -----------------------
# DASHBOARD
# -----------------------

@login_required
def dashboard(request):
    labels = ["Produto A", "Produto B", "Produto C"]
    data = [10, 25, 15]
    membership = Membership.objects.filter(user=request.user).first()

    if not membership:
        return redirect('bloqueio')

    company = membership.company

    return render(request, 'core/dashboard.html', {
        'company': company,
        'items': TableItem.objects.filter(company=company),
        'funcionarios': Funcionario.objects.filter(company=company),
        'labels': labels,
        'data': data
    })

# -----------------------
# PRODUTOS
# -----------------------
@login_required
def add_item(request):

    if request.method == "POST":

        membership = Membership.objects.filter(user=request.user).first()
        if not membership:
            return redirect('dashboard')

        company = membership.company

        TableItem.objects.create(
            company=company,
            nome=request.POST.get("produto"),
            preco=request.POST.get("preco"),
        )

    return redirect('dashboard')
# -----------------------
# FUNCIONÁRIOS
# -----------------------

@login_required
def add_funcionario(request):

    if request.method == "POST":

        membership = Membership.objects.filter(user=request.user).first()
        if not membership:
            return redirect('dashboard')

        company = membership.company

        Funcionario.objects.create(
            company=company,
            nome=request.POST.get("nome"),
            cargo=request.POST.get("cargo")
        )

    return redirect('dashboard')

# -----------------------
# CONTROLE (ADMIN)
# -----------------------

@login_required
def controle(request):

    if not request.user.is_superuser:
        return redirect('dashboard')

    return render(request, 'core/controle.html', {
        'usuarios': User.objects.all()
    })


@login_required
def deletar_usuario(request, user_id):

    if not request.user.is_superuser:
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()

    return redirect('controle')