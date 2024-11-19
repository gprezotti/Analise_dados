import numpy as np
import csv
from datetime import datetime

# Abre o arquivo e lê os dados com csv.reader
with open('vendas.csv', mode='r', encoding='utf-8') as arquivo:
    leitor_csv = csv.reader(arquivo)
    cabecalho = next(leitor_csv)
    dados = np.array(list(leitor_csv))  # Transforma os dados lidos em um array do NumPy

# Converte colunas numéricas do array
dados[:, 3] = dados[:, 3].astype(float)  # Quantidade
dados[:, 4] = dados[:, 4].astype(float)  # Preço
dados[:, 5] = dados[:, 5].astype(float)  # Valor total

# Extrai colunas específicas em arrays separados para facilitar a manipulação
datas = np.array([datetime.strptime(data, "%Y-%m-%d") for data in dados[:, 0]])  # Datas como objetos datetime
regioes = dados[:, 1]
produtos = dados[:, 2]
quantidades = dados[:, 3].astype(float)
valores_totais = dados[:, 5].astype(float)
dias_semana = np.array([data.weekday() for data in datas])  # Dias da semana como inteiros

# Calcula métricas gerais
media_valor_total = np.mean(valores_totais)
mediana_valor_total = np.median(valores_totais)
desvio_padrao_valor_total = np.std(valores_totais)

# Calcula a quantidade total de vendas por produto
produtos_unicos, indices = np.unique(produtos, return_inverse=True)
vendas_por_produto = np.zeros(len(produtos_unicos))
np.add.at(vendas_por_produto, indices, quantidades)

# Calcula o valor total de vendas por produto
valor_total_por_produto = np.zeros(len(produtos_unicos))
np.add.at(valor_total_por_produto, indices, valores_totais)

# Calcula vendas por região
regioes_unicas, indices_regioes = np.unique(regioes, return_inverse=True)
vendas_por_regiao = np.zeros(len(regioes_unicas))
np.add.at(vendas_por_regiao, indices_regioes, valores_totais)

# Calcula a venda média por dia da semana
vendas_por_dia = np.zeros(7)
np.add.at(vendas_por_dia, dias_semana, valores_totais)
contagem_dias = np.bincount(dias_semana)
media_vendas_por_dia = vendas_por_dia / contagem_dias

# Calcula variação diária de vendas
dias_ordenados = np.unique(dias_semana)
vendas_ordenadas = vendas_por_dia[dias_ordenados]
variacoes_vendas = np.diff(np.append(vendas_ordenadas, vendas_ordenadas[0]))  # Adiciona o primeiro dia para fechar o ciclo

# Dicionário para transformar índice do dia em texto
dias_semana_texto = {
    0: "Segunda-Feira",
    1: "Terça-Feira",
    2: "Quarta-Feira",
    3: "Quinta-Feira",
    4: "Sexta-Feira",
    5: "Sábado",
    6: "Domingo",
}

print("\n### ANÁLISE ESTATÍSTICA ###")
print(f"Média do valor total: {media_valor_total:.2f}")
print(f"Mediana do valor total: {mediana_valor_total:.2f}")
print(f"Desvio padrão do valor total: {desvio_padrao_valor_total:.2f}")

# Printa o produto com a maior quantidade vendida
produto_mais_vendido = produtos_unicos[np.argmax(vendas_por_produto)]
quantidade_mais_vendida = np.max(vendas_por_produto)
print(f"\nO produto '{produto_mais_vendido}' foi vendido {quantidade_mais_vendida:.0f} vezes, sendo o mais vendido.")

# Printa o produto com o maior valor total de vendas
produto_maior_valor = produtos_unicos[np.argmax(valor_total_por_produto)]
valor_maior_venda = np.max(valor_total_por_produto)
print(f"O produto '{produto_maior_valor}' rendeu um total de R${valor_maior_venda:.2f}, sendo o produto com o maior valor total de vendas.")

# Printa o valor toral vendido por região
for i, regiao in enumerate(regioes_unicas):
    print(f"A região {regiao} teve um total de R${vendas_por_regiao[i]:.0f}.")

# Printa a média de vendas por dia da semana
for dia, media in enumerate(media_vendas_por_dia):
    print(f"{dias_semana_texto[dia]}: R${media:.2f}")

print("\n\n### ANÁLISE TEMPORAL ###")
# Printa o dia da semana com o maior número de vendas
dia_mais_vendas = np.argmax(vendas_por_dia)
print(f"\n{dias_semana_texto[dia_mais_vendas]} foi o dia da semana com o maior número de vendas.")

# Printa a variação diária no valor total de vendas
print("\n### VARIAÇÃO DIÁRIA NO VALOR TOTAL DAS VENDAS ###")
for i in range(len(dias_ordenados)):
    dia_atual = dias_ordenados[i]
    dia_seguinte = dias_ordenados[(i + 1) % len(dias_ordenados)]
    variacao = variacoes_vendas[i]
    print(f"De {dias_semana_texto[dia_atual]} para {dias_semana_texto[dia_seguinte]}: R${variacao:.2f}")