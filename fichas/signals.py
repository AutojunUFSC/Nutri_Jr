from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .calculos import attTabela
from .models import Ficha, Ficha_Ingrediente, Tabela


def _recalculaTabelaDaFicha(ficha):
  try:
    tabela = Tabela.objects.get(pk=ficha.pk)
  except Tabela.DoesNotExist:
    return  # Ficha recém-criada por registrarFichaBase, a Tabela ainda vai ser criada
  itensReceita = Ficha_Ingrediente.objects.filter(ficha=ficha)
  attTabela(tabela, itensReceita, ficha)


# Campos que o próprio attTabela() grava na Ficha (pesoLiquidoPreparacao/numPorcoes).
# Um save com update_fields exatamente igual a esse veio de dentro do attTabela() —
# ignorar evita loop infinito (save da Ficha -> signal -> attTabela -> save da Ficha -> ...).
_CAMPOS_SALVOS_PELO_ATTTABELA = {'pesoLiquidoPreparacao', 'numPorcoes'}


# Garante que a Tabela nunca fique com valores desatualizados em relação à
# Ficha, independente de qual view (ou o admin) alterou o peso da porção.
@receiver(post_save, sender=Ficha)
def recalculaTabelaAoSalvarFicha(sender, instance, update_fields, **kwargs):
  if update_fields is not None and set(update_fields) == _CAMPOS_SALVOS_PELO_ATTTABELA:
    return
  _recalculaTabelaDaFicha(instance)


# Idem para qualquer alteração nos itens da receita (peso, adição, remoção) —
# inclui o caminho de salvarReceita(), que antes não recalculava a Tabela.
@receiver(post_save, sender=Ficha_Ingrediente)
def recalculaTabelaAoSalvarItemReceita(sender, instance, **kwargs):
  _recalculaTabelaDaFicha(instance.ficha)


@receiver(post_delete, sender=Ficha_Ingrediente)
def recalculaTabelaAoRemoverItemReceita(sender, instance, **kwargs):
  _recalculaTabelaDaFicha(instance.ficha)
