from django.contrib import admin
from fichas.models import Membro, Ficha, Ingrediente, Tabela, Nutriente, Ficha_Ingrediente, Chave

# Models que quero registrar, para aparecerem na página de admin
admin.site.register(Ficha)
admin.site.register(Ingrediente)
admin.site.register(Tabela)
admin.site.register(Nutriente)
admin.site.register(Membro)
admin.site.register(Ficha_Ingrediente)
admin.site.register(Chave)