"""
DIOGO KINDA THIKKK
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
Diogo Ferreira, 46198
Afonso Martins, 45838

"""
import time

nomesM = ["Ricardo", "Paulo", "Adérito", "Rui", "Miguel", "Paulo", "Fábio", "Carlos", "Joaquim"]
lastVisited = []

zonas = ["teste", "montagem", "inspeção", "escritório", "empacotamento", "laboratório"]
lastZone = []


def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string
    # podem achar o tempo atual usando, p.ex.
    # time.time()
    if len(objetos) == 1:
        if (objetos[0][-1]!='a') and (("visitante" in objetos[0]) or ("operário" in objetos[0]) or (("supervisor" in objetos[0]))):
            if len(lastVisited) == 2:
                if lastVisited[1] != objetos[0]:
                    lastVisited.pop(0)
                    lastVisited.append(objetos[0])
            else:
                lastVisited.append(objetos[0])

    if len(objetos) == 1:
        for zona in zonas:
            if zona in objetos[0]:
                if len(lastZone) == 1:
                    lastZone.pop(0)
                    lastZone.append(zona)
                else:
                    lastZone.append(zona)


def resp1():
    if len(lastVisited) == 2:
        print(lastVisited[0])
    else:
        print("Não ha penultima pessoa")


def resp2():
    if len(lastZone) == 1:
        print(lastZone[0])
    else:
        print("nao ha ultima zona")


def resp3():
    pass


def resp4():
    pass


def resp5():
    pass


def resp6():
    pass


def resp7():
    pass


def resp8():
    pass
