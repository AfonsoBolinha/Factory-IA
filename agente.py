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

# Corredores
divisao1 = [(30,165),(135,350)]
divisao2 = [(165,165),(485,185)]
divisao3 = [(30,380),(500,435)]
divisao4 = [(530,215),(635,435)]

# Divisões
divisao5 = [(30,30),(135,135)]
divisao6 = [(530,230),(635,435)]
divisao7 = [(530,230),(635,435)]
divisao8 = [(530,230),(635,435)]
divisao9 = [(530,230),(635,435)]
divisao10 = [(665,330),(770,385)]
divisao11 = [(530,230),(635,435)]
divisao12 = [(530,230),(635,435)]
divisao13 = [(530,230),(635,435)]
divisao14 = [(530,230),(635,435)]

lastVisited = []

zonas = ["teste", "montagem", "inspeção", "escritório", "empacotamento", "laboratório"]
lastZone = []

posicaoGlobal = []

def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string
    # podem achar o tempo atual usando, p.ex.
    # time.time()

    global posicaoGlobal
    posicaoGlobal = posicao

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
                if len(lastZone)==1:
                    lastZone.pop(0)
                    lastZone.append(zona)
                else:
                    lastZone.append(zona)

def resp1():
    if len(lastVisited)==2:
        print("A penúltima pessoa foi o " + lastVisited[0] + ".")
    else:
        print("Não há penúltima pessoa.")


def resp2():
    if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end in [divisao1, divisao2, divisao3, divisao4]):
        print("Estou no corredor.")
    elif any(start[0] <= posicaoGlobal[0] <= end[0] for start, end in [divisao10]):
        print("Estou na entrada da fábrica.")
    else:
        if lastZone:
            print("Estou na/no " + lastZone[0] + ".")
        else:
            print("Não há última zona.")
            print(posicaoGlobal)


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
