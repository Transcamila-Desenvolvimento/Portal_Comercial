from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as logout_django
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash



def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuario cadastrado com esse nome')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        
        return HttpResponse('Usuario cadastrado com sucesso!')



def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    # POST
    username = request.POST.get('username')
    senha = request.POST.get('senha')

    user = authenticate(request, username=username, password=senha)

    if user:
        login_django(request, user)
        return redirect('plataforma')  # Redireciona pra view protegida
    else:
        messages.error(request, 'Usuário ou senha inválidos.')
        return redirect('login')  # Redireciona de volta pro login com mensagem


@login_required(login_url="/auth/login/")
def plataforma(request):
    return render(request, 'plataforma.html')


def logout(request):
    logout_django(request)
    return redirect('login')

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt', 
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None, from_email=None, 
             request=None, html_email_template_name=None, extra_email_context=None):
        
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        users = UserModel._default_manager.filter(email__iexact=email)
        
        # Captura o momento exato da solicitação
        request_time = timezone.now()
        
        for user in users:
            context = {
                'email': user.email,
                'domain': domain_override or request.get_host(),
                'site_name': 'Portal Transcamila',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                'request_time': request_time,  # Data/hora exata da solicitação
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, 
                email_template_name, 
                context, 
                from_email,
                user.email, 
                html_email_template_name=html_email_template_name
            )


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Atualiza nome
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # Atualiza senha
        current_pw = request.POST.get('current_password')
        new_pw = request.POST.get('new_password')
        confirm_pw = request.POST.get('confirm_password')
        
        if current_pw and new_pw and confirm_pw:
            if new_pw == confirm_pw:
                if request.user.check_password(current_pw):
                    request.user.set_password(new_pw)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Senha alterada com sucesso!')
                else:
                    messages.error(request, 'Senha atual incorreta!')
            else:
                messages.error(request, 'As senhas não coincidem!')
        
        messages.success(request, 'Perfil atualizado!')
        return redirect('editar_perfil')
    
    return render(request, 'usuarios/editar_perfil.html')

@login_required
def atualizar_foto(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        request.user.profile.profile_picture = request.FILES['profile_picture']
        request.user.profile.save()
        messages.success(request, 'Foto atualizada!')
        return redirect('editar_perfil')
    
    return render(request, 'usuarios/atualizar_foto.html')