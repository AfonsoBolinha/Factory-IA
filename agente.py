"""
agente.py

Diogo Ferreira, 46198
Afonso Martins, 45838
"""
# Imports
import time
import gender_guesser.detector as gender

# Definir os Corredores e as divisões
corredor1 = [(30, 165), (135, 350), "corredor 1"]
corredor2 = [(165, 165), (485, 185), "corredor 2"]
corredor3 = [(30, 380), (500, 435), "corredor 3"]
corredor4 = [(530, 215), (635, 435), "corredor 4"]
divisao5 = [(30, 30), (135, 135), "multiusos"]
divisao6 = [(180, 30), (285, 135), "multiusos"]
divisao7 = [(330, 30), (485, 135), "multiusos"]
divisao8 = [(530, 30), (770, 185), "multiusos"]
divisao9 = [(665, 230), (770, 285), "multiusos"]
divisao10 = [(665, 330), (770, 385), "entrada da fábrica"]
divisao11 = [(530, 465), (770, 570), "multiusos"]
divisao12 = [(330, 465), (485, 570), "multiusos"]
divisao13 = [(180, 465), (285, 570), "multiusos"]
divisao14 = [(30, 465), (135, 570), "multiusos"]
divisao15 = [(160, 230), (485, 335), "multiusos"]

# Definir todas as localizações
all_locations = [corredor1, corredor2, corredor3, corredor4,
                     divisao5, divisao6, divisao7, divisao8,
                     divisao9, divisao10, divisao11, divisao12,
                     divisao13, divisao14, divisao15]

# Definir as zonas
zonas = ["teste", "montagem", "inspeção", "escritório", "empacotamento", "laboratório"]

# Definir as variáveis globais
lastVisited = []
lastZone = []
posicaoGlobal = []
lastTime = time.time()
lastBateria = 100
momentBateria = 100
striped = ""
lastTimeChecked = time.time()


# Saber a localização atual, com base na posição do agente
def get_current_location(position):
    for start, end, nome in all_locations:
        if start[0] <= position[0] <= end[0] and start[1] <= position[1] <= end[1]:
            return nome
    return ""


def pergunta1(objetos):
    if len(objetos) == 1 and time.time() - lastTimeChecked > 1:
        if ("visitante" in objetos[0]) or ("supervisor" in objetos[0]) or ("operário" in objetos[0]):
            if "visitante" in objetos[0]:
                striped = objetos[0].replace("visitante_", "")
            if "operário" in objetos[0]:
                striped = objetos[0].replace("operário_", "")
            if "supervisor" in objetos[0]:
                striped = objetos[0].replace("supervisor_", "")
            if (gender.Detector().get_gender(name=striped, country="portugal") == "male") or (
                    gender.Detector().get_gender(name=striped, country="portugal") == "mostly_male"):
                if len(lastVisited) == 2:
                    if lastVisited[1] != striped:
                        lastVisited.pop(0)
                        lastVisited.append(striped)
                else:
                    lastVisited.append(striped)


def pergunta2(objetos):
    global lastZone, zonas
    if len(objetos) == 1:
        for zona in zonas:
            if zona in objetos[0]:
                if len(lastZone) == 1:
                    lastZone.pop(0)
                    lastZone.append(zona)
                else:
                    lastZone.append(zona)


def pergunta3():
    # 3. Qual o caminho para a zona de empacotamento?
    pass


def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string
    # podem achar o tempo atual usando, p.ex.
    # time.time()

    global momentBateria, striped
    momentBateria = bateria

    global posicaoGlobal
    posicaoGlobal = posicao

    # 1
    # pergunta1(objetos)

    # 2
    pergunta2(objetos)
    if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [corredor1, corredor2, corredor3, corredor4]):
        lastZone.clear()


def resp1():
    # 1. Qual foi a penúltima pessoa do sexo masculino que viste?
    if len(lastVisited) == 2:
        print("A penúltima pessoa foi o " + lastVisited[0] + ".")
    else:
        print("Não há penúltima pessoa.")


def resp2():
    # 2. Em que zona te encontras?
    current_location = get_current_location(posicaoGlobal)

    if current_location:
        if len(lastZone) == 1:
            current_location = lastZone[0]
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao5]):
                divisao5[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao6]):
                divisao6[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao7]):
                divisao7[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao8]):
                divisao8[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao9]):
                divisao9[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao10]):
                divisao10[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao11]):
                divisao11[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao12]):
                divisao12[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao13]):
                divisao13[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao14]):
                divisao14[2] = current_location
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao15]):
                divisao15[2] = current_location

    print(f"Estou na/no {current_location}.")


def resp3():
    # 3. Qual o caminho para a zona de empacotamento?
    empacotamento_division = next((div for div in all_locations if "empacotamento" in div[2]), None)

    if empacotamento_division:
        if get_current_location(posicaoGlobal) == empacotamento_division[2]:
            print("Já cá estou bro.")
        else:
            print("Not there lol.")
    else:
        print("Ainda não sei onde se encontra a zona de empacotamento.")


def resp4():
    pass


def resp5():
    pass


def resp6():
    global lastTime
    global lastBateria

    res = ((time.time() - lastTime) * 100) / (lastBateria - momentBateria)

    lastTime = time.time()
    lastBateria = momentBateria

    print(f"Faltam {round(res, 2)} segundos")

    pass


def resp7():
    pass


def resp8():
    print("0.53")
    pass