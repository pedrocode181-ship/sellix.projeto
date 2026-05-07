from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    email_user = None
    senha_user = None

    if request.method == 'POST':
        email_user = request.POST.get('email')
        senha_user = request.POST.get('senha')

    if senha_user in ['1234', 'pedro']:
        return redirect('page2')

    return render(request, 'core/index.html')

def page2(request):
    return render(request, 'core/page2.html')