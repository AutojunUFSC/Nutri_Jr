from django.core.management.base import BaseCommand

from fichas.calculos import attTabela
from fichas.models import Ficha, Ficha_Ingrediente, Tabela


class Command(BaseCommand):
    help = (
        "Recalcula a Tabela nutricional de todas as fichas existentes. "
        "Necessário rodar uma vez ao aplicar a correção que passa a recalcular "
        "a Tabela automaticamente via signals: fichas cadastradas antes dessa "
        "correção podem ter ficado com valores de _Porcao/_Arred/_VD desatualizados "
        "em relação ao peso da porção atual (ex.: Porção mostrada no rótulo não bate "
        "com os valores da tabela)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--pk',
            type=int,
            help='Recalcula apenas a ficha com esse ID, em vez de todas.',
        )

    def handle(self, *args, **options):
        fichas = Ficha.objects.all()
        if options['pk']:
            fichas = fichas.filter(pk=options['pk'])

        total = 0
        ignoradas = 0
        falhas = []
        for ficha in fichas:
            try:
                tabela = Tabela.objects.get(pk=ficha.pk)
            except Tabela.DoesNotExist:
                ignoradas += 1
                continue

            # Não imprime nome/dado da ficha aqui: em bases reais grandes gera muito
            # ruído e algumas fichas têm caracteres que quebram a codificação do
            # console do Windows. E não deixa uma ficha com erro (ex.: dado antigo
            # incompleto) interromper o recálculo das demais.
            try:
                itensReceita = Ficha_Ingrediente.objects.filter(ficha=ficha)
                attTabela(tabela, itensReceita, ficha)
                total += 1
            except Exception as e:
                falhas.append((ficha.pk, str(e)))

        self.stdout.write(self.style.SUCCESS(
            f"Concluído: {total} ficha(s) recalculada(s), {ignoradas} sem Tabela (ignorada(s)), "
            f"{len(falhas)} com erro."
        ))
        for pk, erro in falhas:
            self.stdout.write(self.style.ERROR(f"  Ficha {pk}: {erro}"))
