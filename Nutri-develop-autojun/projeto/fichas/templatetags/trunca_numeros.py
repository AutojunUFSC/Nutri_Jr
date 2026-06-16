from django import template
register = template.Library()

@register.simple_tag
def truncar(valor):
    decimais = len(str(valor).split('.')[1])
    if decimais >= 5:
        numero_separado = str(valor).split('.')
        return numero_separado[0] + '.' + numero_separado[1][:5]
    else:
        return valor