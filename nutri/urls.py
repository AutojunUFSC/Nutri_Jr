"""Colocar URL:

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from fichas import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  # Geral:
  path('admin/', admin.site.urls),
  path('', include('django.contrib.auth.urls')),  # São várias URLS de autenticação de usuário

  # Autenticação:
  path('', views.loginUser, name='loginUser'),
  path('loginUser', views.loginUser, name='loginUser'),
  path('logoutUser', views.logoutUser, name='logoutUser'),

  # Membros:
  path('registrarMembro', views.registrarMembro, name='registrarMembro'),
  path('listaMembros', views.listaMembros, name='listaMembros'),
  path('mudaChave', views.mudaChave, name='mudaChave'),
  path('trocaSenha', views.trocaSenha, name='trocaSenha'),
  path('deletaMembro', views.deletaMembro, name='deletaMembro'),

  # Fichas:
  path('listaFichas', views.listaFichas, name='listaFichas'),  # Lista as fichas
  path('registrarFicha1', views.registrarFichaBase, name='registrarFicha1'),  # Criar nova ficha
  path('registrarFicha1/<int:pk>', views.editarFichaBase, name='editarFicha1'),  # Editar 1ª página de uma ficha
  path('registrarFicha2/<int:pk>', views.editarFichaReceita, name='editarFicha2'),  # Editar 2ª página de uma ficha
  path('registrarFicha3/<int:pk>', views.editarFichaTabela, name='editarFicha3'),  # Editar 3ª página de uma ficha
  path('fichaX/<int:pk>', views.fichaX, name='fichaX'),  # Visualiza uma ficha
  path('deletarFicha/<int:pk>', views.deletarFicha, name='deletarFicha'),  # Deleta uma ficha
  path('atualizarFinalizada/<int:pk>', views.atualizarFinalizada, name='atualizarFinalizada'),  # atualiza se a ficha está finalizada ou não

  # Receitas (Model Ficha_Ingrediente):
  path('deletarItemReceita/<int:pk>/<int:id>/', views.deletarItemReceita, name="deletarItemReceita"),
  path('editarItemReceita/<int:pk>/<int:id>/', views.editarItemReceita, name="editarItemReceita"),
  path('salvarReceita', views.salvarReceita, name="salvarReceita"),

  # Nutrientes:
  path('deletarNutrienteExtra/<int:pk>', views.deletarNutrienteExtra, name="deletarNutrienteExtra"),
  path('atualizarMostrar/<int:pk>/<str:item>/', views.atualizarMostrar, name="atualizarMostrar"),

  # Ingredientes:
  path('listaIngredientes', views.listaIngredientes, name='listaIngredientes'),
  path('registrarIngrediente', views.registrarIngrediente, name='registrarIngrediente'),
  path('editarIngrediente/<int:pk>', views.editarIngrediente, name='editarIngrediente'),
  path('deletarIngrediente/<int:pk>', views.deletarIngrediente, name='deletarIngrediente'),
  path('upload', views.upload, name='upload'),  # Página de upload de ingredientes da TACO

  # Outros:
  path('ajuda', views.ajuda, name='ajuda'),  # Página de ajuda
]


