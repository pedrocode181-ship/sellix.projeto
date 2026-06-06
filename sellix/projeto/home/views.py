from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Company, Funcionario, Membership, TableItem, Venda


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
                'error': 'Login inválido, tente novamente'
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

    membership = Membership.objects.filter(user=request.user).first()

    if not membership:
        return redirect('bloqueio')

    company = membership.company

    # ATUALIZA NOME DA EMPRESA (opcional)
    if request.method == "POST":
        new_name = request.POST.get("name")
        if new_name:
            company.name = new_name
            company.save()

    return render(request, "core/dashboard.html", {
        "company": company,
        "items": TableItem.objects.filter(company=company),
        "funcionarios": Funcionario.objects.filter(company=company),
        "vendas": Venda.objects.filter(company=company),
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

        produto = request.POST.get("produto")
        preco = request.POST.get("preco")

        if produto and preco:

            TableItem.objects.create(
                company=company,
                nome=produto,
                preco=preco,
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

        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")

        if nome and cargo:  # 👈 EVITA ERRO
            Funcionario.objects.create(
                company=company,
                nome=nome,
                cargo=cargo
            )

    return redirect('dashboard')

# -----------------------
# VENDAS
# -----------------------

@login_required
def add_venda(request):

    if request.method == "POST":

        membership = Membership.objects.filter(user=request.user).first()

        if not membership:
            return redirect('dashboard')

        company = membership.company

        valor = request.POST.get("valor")
        mes = request.POST.get("mes")

        if valor and mes:
            Venda.objects.create(
                company=company,
                valor=float(valor),
                data=mes
            )

    return redirect("dashboard")


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