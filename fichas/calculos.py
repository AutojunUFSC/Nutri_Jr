import math

# Extraído de views.py para poder ser chamado tanto pelas views quanto pelos
# signals (fichas/signals.py), sem import circular.

def round_half_down(n, decimals=0):
    # Arredondada pra baixo quando na metade: Ex: 32,4 -> 32 ; 32,5 -> 32 ; 32,6 -> 33
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier - 0.5) / multiplier

def arredondaNutriente_ANVISA(condicaoParaZero, valor, unidade):
    if condicaoParaZero:
        return 0.0

    if valor is None:
        return 0.0

    unidade = (unidade or '').strip()

    # Regra: kcal/kJ -> inteiro
    if unidade in ('kcal', 'kJ'):
        return round_half_down(valor, 0)

    # Regra: ≥10 -> inteiro
    if valor >= 10:
        return round_half_down(valor, 0)

    # Regra: ≥1 e <10 -> 1 casa
    elif valor >= 1:
        return round_half_down(valor, 1)

    # Regra: <1 -> 1 casa para g, 2 casas para mg/μg
    else: # valor < 1
        if unidade == 'g':
            return round_half_down(valor, 1)
        elif unidade in ('mg', 'μg', 'ug'):
            return round_half_down(valor, 2)
        else:
            return round_half_down(valor, 2)

# Calcula e formata o número de porções (pesoPorcao do cliente / pesoAnvisa, Task 5.3) segundo
# as regras da ANVISA (conferidas contra o commit de referência da Ceanut, ffbc3c5):
# - número exato -> valor inteiro ("10 porções")
# - quebrado e > 3 porções -> TRUNCA pro inteiro (3,6 -> 3), precedido de "Cerca de"
# - quebrado e <= 3 porções -> arredonda pro oitavo mais próximo, em número misto ("1 e 1/2 porções")
# Oitavos (não só quartos) pra não colapsar em "0 porções" quando a porção do cliente é bem
# menor que a porção Anvisa mas ainda maior que zero (ex.: 35/300 = 0,117 -> "1/8 porção").
def calcularNumPorcoes(pesoPorcao, pesoAnvisa):
  if not pesoPorcao or not pesoAnvisa:
    return "0 porções"

  porcoes = pesoPorcao / pesoAnvisa

  def formatoPlural(inteiro):
    return f"{inteiro} {'porção' if inteiro == 1 else 'porções'}"

  if abs(porcoes - round(porcoes)) < 0.001:
    return formatoPlural(round(porcoes))

  if porcoes > 3:
    # Regra Ceanut: quebrado e >3 porções trunca pro inteiro, não arredonda (3,6 -> 3).
    return f"Cerca de {formatoPlural(int(porcoes))}"

  oitavos = round(porcoes * 8)
  inteiro, resto = divmod(oitavos, 8)
  fracoesTexto = {1: "1/8", 2: "1/4", 3: "3/8", 4: "1/2", 5: "5/8", 6: "3/4", 7: "7/8"}
  if resto == 0:
    return formatoPlural(inteiro)
  if inteiro == 0:
    return f"{fracoesTexto[resto]} porção"
  return f"{inteiro} e {fracoesTexto[resto]} porções"

# Função utilizada pelas views (e pelos signals) que atualiza a tabela. Necessario qdo há troca de valores em outras tabelas.
def attTabela(tabela, itensDaReceita, ficha):

  def resetaNutrientes(tabela): # Reseta o valor dos nutrientes e valor energético
    tabela.proteinas = 0
    tabela.gordTotais = 0
    tabela.carboidratos = 0
    tabela.fibras = 0
    tabela.energiakcal = 0
    tabela.energiaKJ = 0
    tabela.calcio = 0
    tabela.ferro = 0
    tabela.magnesio = 0
    tabela.fosforo = 0
    tabela.potassio = 0
    tabela.sodio = 0
    tabela.zinco = 0
    tabela.cobre = 0
    tabela.manganes = 0
    tabela.retinol = 0
    tabela.RE = 0
    tabela.vitaminaARAE = 0
    tabela.vitaminaC = 0
    tabela.tiamina = 0
    tabela.riboflavina = 0
    tabela.niancina = 0
    tabela.piridoxina = 0
    tabela.gordSat = 0
    tabela.gordTrans = 0
    tabela.gordPoli = 0
    tabela.gordMono = 0
    tabela.colesterol = 0
    tabela.acucaresadd = 0
    tabela.omega6 = 0
    tabela.omega3 = 0
    tabela.vitaminaD = 0
    tabela.vitaminaE = 0
    tabela.vitaminaK = 0
    tabela.biotina = 0
    tabela.acidoFolico = 0
    tabela.acidoPantotenico = 0
    tabela.vitaminaB12 = 0
    tabela.cloreto = 0
    tabela.cromo = 0
    tabela.fluor = 0
    tabela.iodo = 0
    tabela.molibdenio = 0
    tabela.selenio = 0
    tabela.colina = 0
    tabela.acucaresTotais = 0
  resetaNutrientes(tabela)

  def adicionaValoresComBaseNaReceita(tabela, itensDaReceita): # Faz a soma do valor energético e nutrientes de todos os itens da receita e coloca na tabela
    for itemReceita in itensDaReceita:
      # `or 0` protege contra item de receita antigo com pesoLiquido nulo (existe em dados reais)
      pesoLiquido = itemReceita.pesoLiquido or 0
      tabela.proteinas += (itemReceita.ingrediente.proteinas_100g / 100) * pesoLiquido
      tabela.gordTotais += (itemReceita.ingrediente.gordTotais_100g / 100) * pesoLiquido
      tabela.carboidratos += (itemReceita.ingrediente.carboidratos_100g / 100) * pesoLiquido
      tabela.fibras += (itemReceita.ingrediente.fibras_100g / 100) * pesoLiquido
      tabela.calcio += (itemReceita.ingrediente.calcio_100g / 100) * pesoLiquido
      tabela.ferro += (itemReceita.ingrediente.ferro_100g / 100) * pesoLiquido
      tabela.magnesio += (itemReceita.ingrediente.magnesio_100g / 100) * pesoLiquido
      tabela.fosforo += (itemReceita.ingrediente.fosforo_100g / 100) * pesoLiquido
      tabela.potassio += (itemReceita.ingrediente.potassio_100g / 100) * pesoLiquido
      tabela.sodio += (itemReceita.ingrediente.sodio_100g / 100) * pesoLiquido
      tabela.zinco += (itemReceita.ingrediente.zinco_100g / 100) * pesoLiquido
      tabela.cobre += (itemReceita.ingrediente.cobre_100g / 100) * pesoLiquido
      tabela.manganes += (itemReceita.ingrediente.manganes_100g / 100) * pesoLiquido
      tabela.retinol += (itemReceita.ingrediente.retinol_100g / 100) * pesoLiquido
      tabela.RE += (itemReceita.ingrediente.RE_100g / 100) * pesoLiquido
      tabela.vitaminaARAE += (itemReceita.ingrediente.vitaminaARAE_100g / 100) * pesoLiquido
      tabela.vitaminaC += (itemReceita.ingrediente.vitaminaC_100g / 100) * pesoLiquido
      tabela.tiamina += (itemReceita.ingrediente.tiamina_100g / 100) * pesoLiquido
      tabela.riboflavina += (itemReceita.ingrediente.riboflavina_100g / 100) * pesoLiquido
      tabela.niancina += (itemReceita.ingrediente.niancina_100g / 100) * pesoLiquido
      tabela.piridoxina += (itemReceita.ingrediente.piridoxina_100g / 100) * pesoLiquido
      tabela.gordSat += (itemReceita.ingrediente.gordSat_100g / 100) * pesoLiquido
      tabela.gordTrans += (itemReceita.ingrediente.gordTrans_100g / 100) * pesoLiquido
      tabela.gordPoli += (itemReceita.ingrediente.gordPoli_100g / 100) * pesoLiquido
      tabela.gordMono += (itemReceita.ingrediente.gordMono_100g / 100) * pesoLiquido
      tabela.colesterol += (itemReceita.ingrediente.colesterol_100g / 100) * pesoLiquido
      tabela.acucaresadd += (itemReceita.ingrediente.acucaresadd_100g / 100) * pesoLiquido
      tabela.omega6 += (itemReceita.ingrediente.omega6_100g / 100) * pesoLiquido
      tabela.omega3 += (itemReceita.ingrediente.omega3_100g / 100) * pesoLiquido
      tabela.vitaminaD += (itemReceita.ingrediente.vitaminaD_100g / 100) * pesoLiquido
      tabela.vitaminaE += (itemReceita.ingrediente.vitaminaE_100g / 100) * pesoLiquido
      tabela.vitaminaK += (itemReceita.ingrediente.vitaminaK_100g / 100) * pesoLiquido
      tabela.biotina += (itemReceita.ingrediente.biotina_100g / 100) * pesoLiquido
      tabela.acidoFolico += (itemReceita.ingrediente.acidoFolico_100g / 100) * pesoLiquido
      tabela.acidoPantotenico += (itemReceita.ingrediente.acidoPantotenico_100g / 100) * pesoLiquido
      tabela.vitaminaB12 += (itemReceita.ingrediente.vitaminaB12_100g / 100) * pesoLiquido
      tabela.cloreto += (itemReceita.ingrediente.cloreto_100g / 100) * pesoLiquido
      tabela.cromo += (itemReceita.ingrediente.cromo_100g / 100) * pesoLiquido
      tabela.fluor += (itemReceita.ingrediente.fluor_100g / 100) * pesoLiquido
      tabela.iodo += (itemReceita.ingrediente.iodo_100g / 100) * pesoLiquido
      tabela.molibdenio += (itemReceita.ingrediente.molibdenio_100g / 100) * pesoLiquido
      tabela.selenio += (itemReceita.ingrediente.selenio_100g / 100) * pesoLiquido
      tabela.colina += (itemReceita.ingrediente.colina_100g / 100) * pesoLiquido
      tabela.acucaresTotais += (itemReceita.ingrediente.acucaresTotais_100g / 100) * pesoLiquido

    tabela.save()
  adicionaValoresComBaseNaReceita(tabela, itensDaReceita)

  def calculaEnergiaAtwater(tabela): # Calcula o valor energético a partir dos macronutrientes da receita (Proteínas*4 + Carboidratos*4 + Gorduras*9)
    tabela.energiakcal = (tabela.proteinas * 4) + (tabela.carboidratos * 4) + (tabela.gordTotais * 9)
    tabela.energiaKJ = tabela.energiakcal * 4.184
    tabela.save()
  calculaEnergiaAtwater(tabela)

  def somaPesoLiquidoDaReceita(itensDaReceita): # Faz a soma do Peso liquido da receita
    soma = 0
    for itemReceita in itensDaReceita:
      soma += itemReceita.pesoLiquido or 0
    return soma
  somaPesoLiquido = somaPesoLiquidoDaReceita(itensDaReceita)

  def atualizaNutriente_100g(tabela, ficha): # Atualiza o nutriente_100g, valor dinâmico que muda quando a receita muda
    peso = ficha.pesoTotal
    if peso and peso > 0:
      tabela.proteinas_100g = (tabela.proteinas * 100) / peso
      tabela.gordTotais_100g = (tabela.gordTotais * 100) / peso
      tabela.carboidratos_100g = (tabela.carboidratos * 100) / peso
      tabela.fibras_100g = (tabela.fibras * 100) / peso
      tabela.energiakcal_100g = (tabela.energiakcal * 100) / peso
      tabela.energiaKJ_100g = (tabela.energiaKJ * 100) / peso
      tabela.calcio_100g = (tabela.calcio * 100) / peso
      tabela.ferro_100g = (tabela.ferro * 100) / peso
      tabela.magnesio_100g = (tabela.magnesio * 100) / peso
      tabela.fosforo_100g = (tabela.fosforo * 100) / peso
      tabela.potassio_100g = (tabela.potassio * 100) / peso
      tabela.sodio_100g = (tabela.sodio * 100) / peso
      tabela.zinco_100g = (tabela.zinco * 100) / peso
      tabela.cobre_100g = (tabela.cobre * 100) / peso
      tabela.manganes_100g = (tabela.manganes * 100) / peso
      tabela.retinol_100g = (tabela.retinol * 100) / peso
      tabela.RE_100g = (tabela.RE * 100) / peso
      tabela.vitaminaARAE_100g = (tabela.vitaminaARAE * 100) / peso
      tabela.vitaminaC_100g = (tabela.vitaminaC * 100) / peso
      tabela.tiamina_100g = (tabela.tiamina * 100) / peso
      tabela.riboflavina_100g = (tabela.riboflavina * 100) / peso
      tabela.niancina_100g = (tabela.niancina * 100) / peso
      tabela.piridoxina_100g = (tabela.piridoxina * 100) / peso
      tabela.gordSat_100g = (tabela.gordSat * 100) / peso
      tabela.gordTrans_100g = (tabela.gordTrans * 100) / peso
      tabela.gordPoli_100g = (tabela.gordPoli * 100) / peso
      tabela.gordMono_100g = (tabela.gordMono * 100) / peso
      tabela.colesterol_100g = (tabela.colesterol * 100) / peso
      tabela.acucaresadd_100g = (tabela.acucaresadd * 100) / peso
      tabela.omega6_100g = (tabela.omega6 * 100) / peso
      tabela.omega3_100g = (tabela.omega3 * 100) / peso
      tabela.vitaminaD_100g = (tabela.vitaminaD * 100) / peso
      tabela.vitaminaE_100g = (tabela.vitaminaE * 100) / peso
      tabela.vitaminaK_100g = (tabela.vitaminaK * 100) / peso
      tabela.biotina_100g = (tabela.biotina * 100) / peso
      tabela.acidoFolico_100g = (tabela.acidoFolico * 100) / peso
      tabela.acidoPantotenico_100g = (tabela.acidoPantotenico * 100) / peso
      tabela.vitaminaB12_100g = (tabela.vitaminaB12 * 100) / peso
      tabela.cloreto_100g = (tabela.cloreto * 100) / peso
      tabela.cromo_100g = (tabela.cromo * 100) / peso
      tabela.fluor_100g = (tabela.fluor * 100) / peso
      tabela.iodo_100g = (tabela.iodo * 100) / peso
      tabela.molibdenio_100g = (tabela.molibdenio * 100) / peso
      tabela.selenio_100g = (tabela.selenio * 100) / peso
      tabela.colina_100g = (tabela.colina * 100) / peso
      tabela.acucaresTotais_100g = (tabela.acucaresTotais * 100) / peso
    else:
      tabela.proteinas_100g = 0
      tabela.gordTotais_100g = 0
      tabela.carboidratos_100g = 0
      tabela.fibras_100g = 0
      tabela.energiakcal_100g = 0
      tabela.energiaKJ_100g = 0
      tabela.calcio_100g = 0
      tabela.ferro_100g = 0
      tabela.magnesio_100g = 0
      tabela.fosforo_100g = 0
      tabela.potassio_100g = 0
      tabela.sodio_100g = 0
      tabela.zinco_100g = 0
      tabela.cobre_100g = 0
      tabela.manganes_100g = 0
      tabela.retinol_100g = 0
      tabela.RE_100g = 0
      tabela.vitaminaARAE_100g = 0
      tabela.vitaminaC_100g = 0
      tabela.tiamina_100g = 0
      tabela.riboflavina_100g = 0
      tabela.niancina_100g = 0
      tabela.piridoxina_100g = 0
      tabela.gordSat_100g = 0
      tabela.gordTrans_100g = 0
      tabela.gordPoli_100g = 0
      tabela.gordMono_100g = 0
      tabela.colesterol_100g = 0
      tabela.acucaresadd_100g = 0
      tabela.omega6_100g = 0
      tabela.omega3_100g = 0
      tabela.vitaminaD_100g = 0
      tabela.vitaminaE_100g = 0
      tabela.vitaminaK_100g = 0
      tabela.biotina_100g = 0
      tabela.acidoFolico_100g = 0
      tabela.acidoPantotenico_100g = 0
      tabela.vitaminaB12_100g = 0
      tabela.cloreto_100g = 0
      tabela.cromo_100g = 0
      tabela.fluor_100g = 0
      tabela.iodo_100g = 0
      tabela.molibdenio_100g = 0
      tabela.selenio_100g = 0
      tabela.colina_100g = 0
      tabela.acucaresTotais_100g = 0

    tabela.save()
  atualizaNutriente_100g(tabela, ficha)

  def atualizaNutriente_Porcao(tabela, ficha): # Atualiza o nutriente_Porcao, valor dinâmico que muda quando o nutriente_100g muda
    # `or 0` protege contra ficha com pesoAnvisa e pesoPorcao nulos/zerados (existe em
    # dados reais antigos, ex.: fichas sem nenhum peso de porção preenchido) - sem isso
    # peso_por_porção vira None e quebra a conta abaixo.
    peso_por_porção = ficha.pesoAnvisa or ficha.pesoPorcao or 0
    tabela.proteinas_Porcao = (tabela.proteinas_100g / 100) * peso_por_porção
    tabela.gordTotais_Porcao = (tabela.gordTotais_100g / 100) * peso_por_porção
    tabela.carboidratos_Porcao = (tabela.carboidratos_100g / 100) * peso_por_porção
    tabela.fibras_Porcao = (tabela.fibras_100g / 100) * peso_por_porção
    tabela.energiakcal_Porcao = (tabela.energiakcal_100g / 100) * peso_por_porção
    tabela.energiaKJ_Porcao = (tabela.energiaKJ_100g / 100) * peso_por_porção
    tabela.calcio_Porcao = (tabela.calcio_100g / 100) * peso_por_porção
    tabela.ferro_Porcao = (tabela.ferro_100g / 100) * peso_por_porção
    tabela.magnesio_Porcao = (tabela.magnesio_100g / 100) * peso_por_porção
    tabela.fosforo_Porcao = (tabela.fosforo_100g / 100) * peso_por_porção
    tabela.potassio_Porcao = (tabela.potassio_100g / 100) * peso_por_porção
    tabela.sodio_Porcao = (tabela.sodio_100g / 100) * peso_por_porção
    tabela.zinco_Porcao = (tabela.zinco_100g / 100) * peso_por_porção
    tabela.cobre_Porcao = (tabela.cobre_100g / 100) * peso_por_porção
    tabela.manganes_Porcao = (tabela.manganes_100g / 100) * peso_por_porção
    tabela.retinol_Porcao = (tabela.retinol_100g / 100) * peso_por_porção
    tabela.RE_Porcao = (tabela.RE_100g / 100) * peso_por_porção
    tabela.vitaminaARAE_Porcao = (tabela.vitaminaARAE_100g / 100) * peso_por_porção
    tabela.vitaminaC_Porcao = (tabela.vitaminaC_100g / 100) * peso_por_porção
    tabela.tiamina_Porcao = (tabela.tiamina_100g / 100) * peso_por_porção
    tabela.riboflavina_Porcao = (tabela.riboflavina_100g / 100) * peso_por_porção
    tabela.niancina_Porcao = (tabela.niancina_100g / 100) * peso_por_porção
    tabela.piridoxina_Porcao = (tabela.piridoxina_100g / 100) * peso_por_porção
    tabela.gordSat_Porcao = (tabela.gordSat_100g / 100) * peso_por_porção
    tabela.gordTrans_Porcao = (tabela.gordTrans_100g / 100) * peso_por_porção
    tabela.gordPoli_Porcao = (tabela.gordPoli_100g / 100) * peso_por_porção
    tabela.gordMono_Porcao = (tabela.gordMono_100g / 100) * peso_por_porção
    tabela.colesterol_Porcao = (tabela.colesterol_100g / 100) * peso_por_porção
    tabela.acucaresadd_Porcao = (tabela.acucaresadd_100g / 100) * peso_por_porção
    tabela.omega6_Porcao = (tabela.omega6_100g / 100) * peso_por_porção
    tabela.omega3_Porcao = (tabela.omega3_100g / 100) * peso_por_porção
    tabela.vitaminaD_Porcao = (tabela.vitaminaD_100g / 100) * peso_por_porção
    tabela.vitaminaE_Porcao = (tabela.vitaminaE_100g / 100) * peso_por_porção
    tabela.vitaminaK_Porcao = (tabela.vitaminaK_100g / 100) * peso_por_porção
    tabela.biotina_Porcao = (tabela.biotina_100g / 100) * peso_por_porção
    tabela.acidoFolico_Porcao = (tabela.acidoFolico_100g / 100) * peso_por_porção
    tabela.acidoPantotenico_Porcao = (tabela.acidoPantotenico_100g / 100) * peso_por_porção
    tabela.vitaminaB12_Porcao = (tabela.vitaminaB12_100g / 100) * peso_por_porção
    tabela.cloreto_Porcao = (tabela.cloreto_100g / 100) * peso_por_porção
    tabela.cromo_Porcao = (tabela.cromo_100g / 100) * peso_por_porção
    tabela.fluor_Porcao = (tabela.fluor_100g / 100) * peso_por_porção
    tabela.iodo_Porcao = (tabela.iodo_100g / 100) * peso_por_porção
    tabela.molibdenio_Porcao = (tabela.molibdenio_100g / 100) * peso_por_porção
    tabela.selenio_Porcao = (tabela.selenio_100g / 100) * peso_por_porção
    tabela.colina_Porcao = (tabela.colina_100g / 100) * peso_por_porção
    tabela.acucaresTotais_Porcao = (tabela.acucaresTotais_100g / 100) * peso_por_porção

    tabela.save()
  atualizaNutriente_Porcao(tabela, ficha)

  def atualizaNutriente_Arred(tabela): # Atualiza o nutriente_Arred dinâmico (arredonda a quantidade por porção)
    # Helper to apply ANVISA rounding to both portion (Arred) and 100g columns
    def arredonda_e_salva(nome_campo, cond_zero_porcao, cond_zero_100g):
      val_porcao = getattr(tabela, f"{nome_campo}_Porcao")
      val_100g = getattr(tabela, f"{nome_campo}_100g")
      unidade = getattr(tabela, f"{nome_campo}_unidadeMd")

      setattr(tabela, f"{nome_campo}_Arred", arredondaNutriente_ANVISA(cond_zero_porcao, val_porcao, unidade))
      setattr(tabela, f"{nome_campo}_100g", arredondaNutriente_ANVISA(cond_zero_100g, val_100g, unidade))

    arredonda_e_salva("proteinas", tabela.proteinas_Porcao <= 0.5, tabela.proteinas_100g <= 0.5)
    arredonda_e_salva("gordTotais",
                      tabela.gordTotais_Porcao <= 0.5 and tabela.gordSat_Porcao <= 0.5 and tabela.gordTrans_Porcao <= 0.5 and tabela.gordMono_Porcao == 0 and tabela.gordPoli == 0,
                      tabela.gordTotais_100g <= 0.5 and tabela.gordSat_100g <= 0.5 and tabela.gordTrans_100g <= 0.5 and tabela.gordMono_100g == 0 and tabela.gordPoli_100g == 0)
    arredonda_e_salva("carboidratos", tabela.carboidratos_Porcao <= 0.5, tabela.carboidratos_100g <= 0.5)
    arredonda_e_salva("fibras", tabela.fibras_Porcao <= 0.5, tabela.fibras_100g <= 0.5)
    arredonda_e_salva("energiakcal", tabela.energiakcal_Porcao <= 4, tabela.energiakcal_100g <= 4)
    arredonda_e_salva("energiaKJ", tabela.energiaKJ_Porcao <= 17, tabela.energiaKJ_100g <= 17)
    arredonda_e_salva("calcio", False, False)
    arredonda_e_salva("ferro", False, False)
    arredonda_e_salva("magnesio", False, False)
    arredonda_e_salva("fosforo", False, False)
    arredonda_e_salva("potassio", False, False)
    arredonda_e_salva("sodio", tabela.sodio_Porcao <= 5, tabela.sodio_100g <= 5)
    arredonda_e_salva("zinco", False, False)
    arredonda_e_salva("cobre", False, False)
    arredonda_e_salva("manganes", False, False)
    arredonda_e_salva("retinol", False, False)
    arredonda_e_salva("RE", False, False)
    arredonda_e_salva("vitaminaARAE", False, False)
    arredonda_e_salva("vitaminaC", False, False)
    arredonda_e_salva("tiamina", False, False)
    arredonda_e_salva("riboflavina", False, False)
    arredonda_e_salva("niancina", False, False)
    arredonda_e_salva("piridoxina", False, False)
    arredonda_e_salva("gordSat", tabela.gordSat_Porcao <= 0.2, tabela.gordSat_100g <= 0.2)
    arredonda_e_salva("gordTrans", tabela.gordTrans_Porcao <= 0.2, tabela.gordTrans_100g <= 0.2)
    arredonda_e_salva("gordPoli", False, False)
    arredonda_e_salva("gordMono", False, False)
    arredonda_e_salva("colesterol", False, False)
    arredonda_e_salva("acucaresadd", False, False)
    arredonda_e_salva("omega6", False, False)
    arredonda_e_salva("omega3", False, False)
    arredonda_e_salva("vitaminaD", False, False)
    arredonda_e_salva("vitaminaE", False, False)
    arredonda_e_salva("vitaminaK", False, False)
    arredonda_e_salva("biotina", False, False)
    arredonda_e_salva("acidoFolico", False, False)
    arredonda_e_salva("acidoPantotenico", False, False)
    arredonda_e_salva("vitaminaB12", False, False)
    arredonda_e_salva("cloreto", False, False)
    arredonda_e_salva("cromo", False, False)
    arredonda_e_salva("fluor", False, False)
    arredonda_e_salva("iodo", False, False)
    arredonda_e_salva("molibdenio", False, False)
    arredonda_e_salva("selenio", False, False)
    arredonda_e_salva("colina", False, False)
    arredonda_e_salva("acucaresTotais", False, False)

    tabela.save()
  atualizaNutriente_Arred(tabela)

  # Atualiza outros valores dinâmicos
  ficha.pesoLiquidoPreparacao = somaPesoLiquido
  if ficha.pesoPorcao and ficha.pesoAnvisa:
    ficha.numPorcoes = int(ficha.pesoPorcao / ficha.pesoAnvisa)
  else:
    ficha.numPorcoes = 0
  # update_fields identifica esse save como interno pro signal em signals.py, que
  # evita recalcular a Tabela de novo (senão vira loop: save -> signal -> attTabela -> save -> ...)
  ficha.save(update_fields=['pesoLiquidoPreparacao', 'numPorcoes'])

  def atualizaValorDiario(tabela): # Atualiza % de Valor Diário com (%VD) de Referência para uma dieta de 2000kcal
    def calculaPorCentagemValorDiarioNutriente(valor, referencia):
      return round((100 * valor) / referencia)
    tabela.proteinas_VD = calculaPorCentagemValorDiarioNutriente(tabela.proteinas_Arred, 50) # Referência 50 g
    tabela.gordTotais_VD = calculaPorCentagemValorDiarioNutriente(tabela.gordTotais_Arred, 65) # Referência 65 g
    tabela.carboidratos_VD = calculaPorCentagemValorDiarioNutriente(tabela.carboidratos_Arred, 300) # Referência 300 g
    tabela.fibras_VD = calculaPorCentagemValorDiarioNutriente(tabela.fibras_Arred, 25) # Referência 25 g
    tabela.energiakcal_VD = calculaPorCentagemValorDiarioNutriente(tabela.energiakcal_Arred, 2000) # Referência 2000 kcal
    tabela.energiaKJ_VD = calculaPorCentagemValorDiarioNutriente(tabela.energiaKJ_Arred, 8400) # Referência 8400 kJ
    tabela.calcio_VD = calculaPorCentagemValorDiarioNutriente(tabela.calcio_Arred, 1000) # Referência 1000 mg
    tabela.ferro_VD = calculaPorCentagemValorDiarioNutriente(tabela.ferro_Arred, 14) # Referência 14 mg
    tabela.magnesio_VD = calculaPorCentagemValorDiarioNutriente(tabela.magnesio_Arred, 420) # Referência 420 mg
    tabela.fosforo_VD = calculaPorCentagemValorDiarioNutriente(tabela.fosforo_Arred, 700) # Referência 700 mg
    tabela.potassio_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.sodio_VD = calculaPorCentagemValorDiarioNutriente(tabela.sodio_Arred, 2000) # Referência 2000 mg
    tabela.zinco_VD = calculaPorCentagemValorDiarioNutriente(tabela.zinco_Arred, 11) # Referência 11 mg
    tabela.cobre_VD = calculaPorCentagemValorDiarioNutriente(tabela.cobre_Arred, 0.9) # Referência 900 ug
    tabela.manganes_VD = calculaPorCentagemValorDiarioNutriente(tabela.manganes_Arred, 3) # Referência 3 mg
    tabela.retinol_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.RE_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.vitaminaARAE_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.vitaminaC_VD = calculaPorCentagemValorDiarioNutriente(tabela.vitaminaC_Arred, 100) # Referência 100 mg
    tabela.tiamina_VD = calculaPorCentagemValorDiarioNutriente(tabela.tiamina_Arred, 1.2) # Referência 1.2 mg
    tabela.riboflavina_VD = calculaPorCentagemValorDiarioNutriente(tabela.riboflavina_Arred, 1.2) # Referência 1.2 mg
    tabela.niancina_VD = calculaPorCentagemValorDiarioNutriente(tabela.niancina_Arred, 15) # Referência 15 mg
    tabela.piridoxina_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.gordSat_VD = calculaPorCentagemValorDiarioNutriente(tabela.gordSat_Arred, 20) # Referência 20 g
    tabela.gordTrans_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.gordPoli_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.gordMono_VD = calculaPorCentagemValorDiarioNutriente(0, 1)
    tabela.colesterol_VD = calculaPorCentagemValorDiarioNutriente(tabela.colesterol_Arred, 300) # Referência 300 mg
    tabela.acucaresadd_VD = calculaPorCentagemValorDiarioNutriente(tabela.acucaresadd_Arred, 50) # Referência 50 g
    tabela.omega6_VD = calculaPorCentagemValorDiarioNutriente(tabela.omega6_Arred, 18) # Referência 18 mg
    tabela.omega3_VD = calculaPorCentagemValorDiarioNutriente(tabela.omega3_Arred, 4000) # Referência 4000 mg
    tabela.vitaminaD_VD = calculaPorCentagemValorDiarioNutriente(tabela.vitaminaD_Arred, 15) # Referência 15 µg
    tabela.vitaminaE_VD = calculaPorCentagemValorDiarioNutriente(tabela.vitaminaE_Arred, 15) # Referência 15 µg
    tabela.vitaminaK_VD = calculaPorCentagemValorDiarioNutriente(tabela.vitaminaK_Arred, 120) # Referência 120 µg
    tabela.biotina_VD = calculaPorCentagemValorDiarioNutriente(tabela.biotina_Arred, 30) # Referência 30 µg
    tabela.acidoFolico_VD = calculaPorCentagemValorDiarioNutriente(tabela.acidoFolico_Arred, 400) # Referência 400 µg
    tabela.acidoPantotenico_VD = calculaPorCentagemValorDiarioNutriente(tabela.acidoPantotenico_Arred, 5) # Referência 5 mg
    tabela.vitaminaB12_VD = calculaPorCentagemValorDiarioNutriente(tabela.vitaminaB12_Arred, 2.4) # Referência 2.4 µg
    tabela.cloreto_VD = calculaPorCentagemValorDiarioNutriente(tabela.cloreto_Arred, 2300) # Referência 2300 mg
    tabela.cromo_VD = calculaPorCentagemValorDiarioNutriente(tabela.cromo_Arred, 35) # Referência 35 µg
    tabela.fluor_VD = calculaPorCentagemValorDiarioNutriente(tabela.fluor_Arred, 4) # Referência 4 mg
    tabela.iodo_VD = calculaPorCentagemValorDiarioNutriente(tabela.iodo_Arred, 150) # Referência 150 µg
    tabela.molibdenio_VD = calculaPorCentagemValorDiarioNutriente(tabela.molibdenio_Arred, 45) # Referência 45 µg
    tabela.selenio_VD = calculaPorCentagemValorDiarioNutriente(tabela.selenio_Arred, 11) # Referência 11 mg
    tabela.colina_VD = calculaPorCentagemValorDiarioNutriente(tabela.colina_Arred, 550) # Referência 550 mg

    tabela.save()
  atualizaValorDiario(tabela)
