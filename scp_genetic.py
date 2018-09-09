import random
from time import time

def le_arquivo(nomeArquivo):
    dic_subconjuntos = dict()
    subconjuntos = set()
    colunas = set()
    arquivo = open(nomeArquivo)
    for linha in arquivo:
        lin = linha.strip("\n").split()
        if linha.startswith(" "):
            dic_subconjuntos[lin[0]] = [float(lin[1]), set()]
            colunas.add(lin[0])
            for i in range(2, len(lin)):
                subconjuntos.add(lin[i])
                dic_subconjuntos[lin[0]][1].add(lin[i])
    arquivo.close()
    return subconjuntos, colunas, dic_subconjuntos

    
def gera_populacao(subconjuntos, colunas, dic_subconjuntos, tamanho_populacao):
    populacao = list()
    while len(populacao) < tamanho_populacao:
        solucao = set()
        custo = 0
        temp = set(subconjuntos)
        while len(temp) != 0:
            linha = random.sample(temp, 1).pop()
            for i in colunas:
                if linha in dic_subconjuntos[i][1]:
                    solucao.add(i)
                    custo += dic_subconjuntos[i][0]
                    temp.difference_update(dic_subconjuntos[i][1])
        populacao.append([custo, solucao])
    return populacao


def aplica_mutacao(novo_individuo, probabilidade, colunas, dic_subconjuntos):
    columnsDif = set(colunas)
    if (len(columnsDif) != 0):
        col = random.sample(columnsDif,1).pop()
        novo_individuo[0] += dic_subconjuntos[col][0]
        novo_individuo[1].add(col)


def VND(subconjuntos, dic_subconjuntos, solucao, r):
    s = solucao
    k = 1
    while k <= r:
        vizinho = gera_populacao(subconjuntos, s[1], dic_subconjuntos, 1).pop()
        if (vizinho[0] < s[0]):
            s = vizinho
            k = 1
        else:
            k += 1
    return s

def selecionar_individuo(populacao):
    return min([random.sample(populacao, 1).pop() for i in range(3)], key = lambda x: x[0])

def gera_individuo(subconjuntos, pais, dic_subconjuntos):
    p = set(pais[0][1])
    p.update(pais[1][1])
    return gera_populacao(subconjuntos, p, dic_subconjuntos, 1).pop()

def atualiza_populacao(populacao, novo_individuo, extremes):
    populacao.sort(key = lambda indiv: indiv[0])
    populacao[len(populacao) - 1] = novo_individuo
    extremes[0] = populacao[len(populacao) - 2][0]
    extremes[1] = populacao[0][0]


def get_solucao_SCP_genetico(subconjuntos, colunas, dic_subconjuntos):
    tamanho_populacao = 1
    extremes = [i for i in range(2)]
    populacao = gera_populacao(subconjuntos, colunas, dic_subconjuntos, tamanho_populacao)
    
    while int(extremes[0]) != int(extremes[1]):
        pais = [selecionar_individuo(populacao) for i in range(2)]
        novo_individuo = gera_individuo(subconjuntos, pais, dic_subconjuntos)
        probabilidade_mutacao = 0.8
        aplica_mutacao(novo_individuo, probabilidade_mutacao, colunas, dic_subconjuntos)
        novo_individuo = VND(subconjuntos, dic_subconjuntos, novo_individuo, 5)
        atualiza_populacao(populacao, novo_individuo, extremes)
        

    return populacao[0]


# ==================================================================================

subconjuntos, colunas, dic_subconjuntos = le_arquivo("input2.txt")

tempo_exec_inicial = time()
tempo_exec = 0
solucao = get_solucao_SCP_genetico(subconjuntos, colunas, dic_subconjuntos)
tempo_exec = time() - tempo_exec_inicial

print("Solução: ", solucao)
print("Tempo de execução: ", tempo_exec)