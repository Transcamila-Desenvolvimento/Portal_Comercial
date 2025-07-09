from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Proposta

@login_required(login_url='/auth/login/')
def gestao_comercial(request):
    if request.method == "GET":
        propostas = Proposta.objects.all()
        return render(request, 'propostas.html', {'propostas': propostas})

@login_required(login_url='/auth/login/')
def incluir_proposta(request):
    return render(request, 'incluir.html')