from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ #adicionado por goias
from django.db.models.functions import Lower

# Formulário inicial de uma ficha
class FichaFormBase(forms.ModelForm):
  
  # Reescreve propriedades de input de data
  dataCriacao = forms.DateField(
    label='Data de Criação',
    widget=forms.DateInput(format='%d/%m/%Y'),
    input_formats=['%d/%m/%Y', '%d-%m-%Y'],
    help_text='Formato: DD/MM/YYYY ou DD-MM-YYYY'
    )

  class Meta:
    model = Ficha
    fields = ['autor', 'nomeFicha', 'cliente', 'pesoTotal', 'pesoPorcao', 'pesoAnvisa', 'dataCriacao', 'medCaseiraPorcao']
    labels = {'autor': _('Autor:'), 'nomeFicha': _('Nome da receita:'), 'cliente': _('Cliente:'),
              'pesoTotal': _('Peso total:'),'pesoPorcao': _('Peso da porção (Cliente):'),'pesoAnvisa': _('Peso da porção (Anvisa):'),'dataCriacao': _('Data de criação:'),
              'medCaseiraPorcao': _('Medida caseira da porção:')}

  def __init__(self, *args, **kwargs):
    super(FichaFormBase, self).__init__(*args, **kwargs)
    self.fields['autor'].queryset = Membro.objects.all().order_by(Lower('nome'))

# Filtro na lista de fichas
class FichaFiltroForm(forms.Form):
  f_nomeFicha = forms.CharField(label=("Receita"), required=False)
  f_cliente = forms.CharField(label=("Cliente"), required=False)
  f_autor = forms.CharField(label=("Autor"), required=False)

# Formulário para adicionar ingrediente na receita da ficha
class ReceitaForm(forms.ModelForm):
  class Meta:
    model = Ficha_Ingrediente
    fields = ['pesoBruto', 'pesoLiquido', 'medidaCaseira', 'nomeFantasia']
    labels = {'pesoBruto': _('Peso Bruto:'), 
              'pesoLiquido': _('Peso Líquido:'),
              'medidaCaseira': _('Medida Caseira:'), 
              'nomeFantasia': _('Nome Fantasia:')}

# Formulário para adicionar nutrientes extras na tabela nutricional
class NutrienteForm(forms.ModelForm):
  class Meta:
    model = Nutriente
    fields = ['nomeNutri', 'qtde', 'qtde_Arred', 'medida', 'qtde_VD']
    labels = {'nomeNutri': _('Novo Item:'), 'qtde': _('Quantidade Real:'), 
              'qtde_Arred': _('Quantidade Arredondada:'), 'medida': _('Medida:'),
               'qtde_VD': _('Quantidade Valor Diário:')}

# Formulário final de uma ficha
class FormInformacoesComplementares(forms.ModelForm):
  class Meta:
    model = Tabela
    fields = ['informacoesComplementares']
    labels = {'informacoesComplementares': _('Informacões Complementares:')}

# Formulário de ingredientes
class IngredienteForm(forms.ModelForm):
  
  # Reescreve propriedades de input de data
  dataCriacao = forms.DateField(
    label='Data de Criação',
    widget=forms.DateInput(format='%d/%m/%Y'),
    input_formats=['%d/%m/%Y', '%d-%m-%Y'],
    help_text='Formato: DD/MM/YYYY ou DD-MM-YYYY'
    )
  composicao = forms.CharField(
    label='Composição',
    help_text='Formato: leite, açúcar e lactose',
    required=False
    )
  
    
  class Meta:
    model = Ingrediente
    fields = ['autorIng', 'nomeIng', 'composicao', 'origemDosDados', 'qtdeDoIngrediente',
              'addManualmente', 'numRef', 'dataCriacao',
              'proteinas', 'gordTotais','acucaresTotais', 'carboidratos', 'fibras',
              'energiakcal','energiaKJ','calcio', 'ferro', 'magnesio', 'fosforo',
              'potassio', 'sodio', 'zinco', 'cobre', 'manganes',
              'retinol', 'RE', 'vitaminaARAE', 'vitaminaC', 'tiamina',
              'riboflavina', 'niancina', 'piridoxina', 'gordSat', 'gordTrans',
              'gordPoli', 'gordMono', 'colesterol','acucaresadd','omega6','omega3',
              'vitaminaD','vitaminaE','vitaminaK','biotina','acidoFolico','acidoPantotenico',
              'vitaminaB12','cloreto','cromo','fluor','iodo','molibdenio','selenio','colina']
    labels = {'autorIng': _('Autor:'), 'nomeIng': _('Ingrediente:'), 'composicao': _('Composição:'), 
               'origemDosDados': _('Fonte / Marca:'), 'qtdeDoIngrediente': _('Quantidade do ingrediente:'), 
               'dataCriacao': _('Data Criação:'), 'proteinas': _(''), 'gordTotais': _(''),'acucaresTotais': _(''),
                'carboidratos': _(''), 'fibras': _(''), 'energiakcal': _(''), 'energiaKJ': _(''),
               'calcio': _(''), 'ferro': _(''), 'magnesio': _(''), 'fosforo': _(''),
                'potassio': _(''), 'sodio': _(''), 'zinco': _(''), 'cobre': _(''),
                'manganes': _(''), 'retinol': _(''), 'RE': _(''), 'vitaminaARAE': _(''),
                'vitaminaC': _(''), 'tiamina': _(''), 'riboflavina': _(''),
                'niancina': _(''), 'piridoxina': _(''), 'gordSat': _(''),
                'gordTrans': _(''), 'gordPoli': _(''), 'gordMono': _(''),
                'colesterol': _(''), 'acucaresadd': _(''), 'omega6': _(''), 'omega3': _(''),
                'vitaminaD': _(''),'vitaminaE': _(''), 'vitaminaK': _(''),
                'biotina': _(''),'acidoFolico': _(''),'acidoPantotenico': _(''),
                'vitaminaB12': _(''),'cloreto': _(''),'cromo': _(''),'fluor': _(''),
                'iodo': _(''),'molibdenio': _(''),'selenio': _(''),'colina': _('')}

  def __init__(self, *args, **kwargs):
    super(IngredienteForm, self).__init__(*args, **kwargs)
    self.fields['autorIng'].queryset = Membro.objects.all().order_by(Lower('nome'))

# Filtro na lista de ingredientes
class IngredienteFiltroForm(forms.Form):
  f_nomeIng = forms.CharField(label=("Nome"), required=False)
  f_origemDosDados = forms.CharField(label=("Origem"), required=False)
  f_autorIng = forms.CharField(label=("Autor"), required=False)

# Formulário de login
class LoginForm(forms.Form):
  username = forms.CharField(label=("Nome:"), required=True, help_text='Ex: Dino da Nutri')
  password = forms.CharField(label=("Senha:"), required=True, widget=forms.PasswordInput)

# Formulários para cadastros de novos membros
class MembroForm(forms.ModelForm):
  chave = forms.CharField(label=("Chave:"), required=True, widget=forms.PasswordInput)
  senha1 = forms.CharField(label=("Senha:"), required=True, widget=forms.PasswordInput)
  senha2 = forms.CharField(label=("Confirmar senha:"), required=True, widget=forms.PasswordInput)

  class Meta:
    model = Membro
    fields = ['nome', 'semestre', 'email', 'senha1', 'senha2', 'usuario', 'chave']
    labels = {'nome': _('Nome:'), 'semestre': _('Semestre de entrada na Nutri Jr:'), #adicionado por goias
               'email': _('E-mail:'), 'senha1': _('Senha:'), 'senha2':_('Confirmar senha:'), 'chave': _('Chave:')}

# Formulário para alteração de chave de criação de membros
class ChaveForm(forms.ModelForm):
  class Meta:
    model = Chave
    fields  = ['key']
    labels = {'key': _('Nova chave:')}

# Formulário para mudar a senha de um usuário (só o admin tem acesso)
class MudarSenha(forms.Form):
  choices = User.objects.all().order_by(Lower('username'))
  usuario = forms.ModelChoiceField(label=("Membro"), required=True, queryset=choices) # Excluir admin ou algum outro usuário?
  nova_senha = forms.CharField(label=("Nova senha"), required=True, widget=forms.PasswordInput)

# Formulário para apagar um membro transferindo os dados para outro
class ApagarMembro(forms.Form):
  choices = Membro.objects.all().order_by(Lower('nome'))
  membroExcluido = forms.ModelChoiceField(required=True, label=("Excluir membro"), queryset=choices)
  membroDestino = forms.ModelChoiceField(required=True, label=("Transferir autoria para"), queryset=choices, help_text="Isso inclui Fichas e Ingredientes criados por ele")

  def clean(self):
    cleaned_data = super().clean()
    mExcluido = cleaned_data.get("membroExcluido")
    mDestino = cleaned_data.get("membroDestino")

    if mExcluido == mDestino:
      raise forms.ValidationError({'membroDestino': "Os dois membros precisam ser distintos"})
