import re

from django import template

register = template.Library()

# Mapa de frações comuns em medida caseira de cozinha (xícara, colher etc.).
# Cada entrada é fracao_decimal: "numerador/denominador".
_MAPA_FRACOES = {
    0.5: "1/2",
    0.25: "1/4",
    0.75: "3/4",
    0.125: "1/8",
    0.375: "3/8",
    0.625: "5/8",
    0.875: "7/8",
    1 / 3: "1/3",
    2 / 3: "2/3",
    1 / 6: "1/6",
    5 / 6: "5/6",
    0.2: "1/5",
    0.4: "2/5",
    0.6: "3/5",
    0.8: "4/5",
}

# Tolerância pequena o bastante pra pegar truncamento de 2 casas decimais
# (ex.: "0.33" digitado como 1/3) sem confundir um decimal comum "solto"
# (ex.: "0.37") com uma oitava parte (0.375) por coincidência.
_TOLERANCIA = 0.004

# \d* (não \d+) pra também capturar decimais sem zero à esquerda, ex.: ".5"
_REGEX_DECIMAL = re.compile(r"(?<![\d.,])(\d*)[.,](\d+)(?![\d.,])")


def _fracao_mais_proxima(parte_decimal):
    for valor, texto in _MAPA_FRACOES.items():
        if abs(parte_decimal - valor) < _TOLERANCIA:
            return texto
    return None


def _substitui_decimal_por_fracao(match):
    parte_inteira_str, parte_decimal_str = match.group(1), match.group(2)
    parte_inteira = int(parte_inteira_str) if parte_inteira_str else 0
    parte_decimal = float(f"0.{parte_decimal_str}")

    fracao = _fracao_mais_proxima(parte_decimal)
    if fracao is None:
        return match.group(0)  # Sem fração conhecida próxima: mantém o número original

    if parte_inteira:
        return f"{parte_inteira} {fracao}"
    return fracao


@register.filter
def fracao(texto):
    # Converte números decimais dentro do texto (ex.: "0.5 xícara") para a
    # notação em fração ("1/2 xícara"), mais natural pra medida caseira no
    # rótulo. Números sem fração conhecida próxima ficam como estavam.
    if not texto:
        return texto
    return _REGEX_DECIMAL.sub(_substitui_decimal_por_fracao, str(texto))
