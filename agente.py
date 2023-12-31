"""
agente.py

Diogo Ferreira, 46198
Afonso Martins, 45838
"""
# Imports
import time
import gender_guesser.detector as gender
import networkx as nx

# Definir os Corredores e as divisões
corredor1 = [(30, 165), (135, 350), "corredor1"]
corredor2 = [(165, 165), (485, 185), "corredor2"]
corredor3 = [(30, 380), (500, 435), "corredor3"]
corredor4 = [(530, 215), (635, 435), "corredor4"]
divisao5 = [(30, 30), (135, 135), "multiusos5"]
divisao6 = [(180, 30), (285, 135), "multiusos6"]
divisao7 = [(330, 30), (485, 135), "multiusos7"]
divisao8 = [(530, 30), (770, 185), "multiusos8"]
divisao9 = [(665, 230), (770, 285), "multiusos9"]
divisao10 = [(665, 330), (770, 385), "entrada da fábrica"]
divisao11 = [(530, 465), (770, 570), "multiusos11"]
divisao12 = [(330, 465), (485, 570), "multiusos12"]
divisao13 = [(180, 465), (285, 570), "multiusos13"]
divisao14 = [(30, 465), (135, 570), "multiusos14"]
divisao15 = [(160, 230), (485, 335), "multiusos15"]

# Definir todas as localizações
all_locations = [corredor1, corredor2, corredor3, corredor4,
                     divisao5, divisao6, divisao7, divisao8,
                     divisao9, divisao10, divisao11, divisao12,
                     divisao13, divisao14, divisao15]

# Definir as zonas
zonas = ["teste", "montagem", "inspeção", "escritório", "empacotamento", "laboratório"]


def criar_grafo():
    # Definir as conexões entre as áreas
    conexoes = {
        "corredor1": ["corredor2", "corredor3", divisao5[2]],
        "corredor2": ["corredor1", divisao6[2], divisao7[2]],
        "corredor3": ["corredor4", divisao14[2], divisao13[2], divisao12[2]],
        "corredor4": ["corredor3", divisao11[2], divisao10[2], divisao9[2], divisao8[2]],
        divisao5[2]: ["corredor1"],
        divisao6[2]: ["corredor2"],
        divisao7[2]: ["corredor2"],
        divisao8[2]: ["corredor4"],
        divisao9[2]: ["corredor4"],
        divisao10[2]: ["corredor4"],
        divisao11[2]: ["corredor4"],
        divisao12[2]: ["corredor3"],
        divisao13[2]: ["corredor3"],
        divisao14[2]: ["corredor3"],
        divisao15[2]: ["corredor1"]
    }

    grafo = nx.Graph()
    for key, value in conexoes.items():
        grafo.add_node(key)
        for v in value:
            grafo.add_edge(key, v)
    return grafo

# Definir as variáveis globais
lastVisited = []
lastZone = []
posicaoGlobal = []
lastTime = time.time()
lastBateria = 100
momentBateria = 100
striped = ""
lastTimeChecked = time.time()


# Saber o nome da divisão atual, com base na posição do agente
def get_current_location_name(position):
    for start, end, nome in all_locations:
        if start[0] <= position[0] <= end[0] and start[1] <= position[1] <= end[1]:
            return nome
    return ""


# 1. Qual foi a penúltima pessoa do sexo masculino que viste?
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
                elif len(lastVisited) == 1:
                    if lastVisited[0] != striped:
                        lastVisited.append(striped)
                else:
                    lastVisited.append(striped)


# 2. Em que tipo de zona estás agora?
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


def work(posicao, bateria, objetos):
    # Esta função é invocada em cada ciclo de clock
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

    pergunta1(objetos)

    pergunta2(objetos)
    if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [corredor1, corredor2, corredor3, corredor4]):
        lastZone.clear()


# 1. Qual foi a penúltima pessoa do sexo masculino que viste?
def resp1():
    if len(lastVisited) == 2:
        print("A penúltima pessoa foi o " + lastVisited[0] + ".")
    else:
        print("Não há penúltima pessoa.")


# 2. Em que zona te encontras?
def resp2():
    current_location_name = get_current_location_name(posicaoGlobal)

    if current_location_name:
        if len(lastZone) == 1:
            current_location_name = lastZone[0]
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao5]):
                divisao5[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao6]):
                divisao6[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao7]):
                divisao7[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao8]):
                divisao8[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao9]):
                divisao9[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao10]):
                divisao10[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao11]):
                divisao11[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao12]):
                divisao12[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao13]):
                divisao13[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao14]):
                divisao14[2] = current_location_name
            if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [divisao15]):
                divisao15[2] = current_location_name

    print(f"Estou na/no {current_location_name}.")


# 3. Qual o caminho para a zona de empacotamento?
def resp3():
    # Obter a localização atual do agente
    current_location_name = get_current_location_name(posicaoGlobal)

    # Atualizar o grafo
    graph1 = criar_grafo()

    if not any("empacotamento" in zona for zona in graph1.nodes):
        print("Ainda não conheço a zona de empacotamento.")
        return

    if current_location_name == "empacotamento":
        print("Já estou na zona de empacotamento.")
        return

    if current_location_name:
        # Obter o caminho para a zona de empacotamento
        caminho = nx.shortest_path(graph1, current_location_name, "empacotamento")

        # Imprimir o caminho para a zona de empacotamento
        print(f"O caminho para a zona de empacotamento é: {caminho}")
    else:
        print("Não foi possível determinar a localização atual.")




# 4. Qual a distância até ao laboratório?
def resp4():
    # Obter a localização atual do agente
    current_location_name = get_current_location_name(posicaoGlobal)

    # Atualizar o grafo
    graph2 = criar_grafo()

    if not any("laboratório" in zona for zona in graph2.nodes):
        print("Ainda não conheço o laboratório.")
        return

    if current_location_name == "laboratório":
        print("Já estou no laboratório.")
        return

    if current_location_name:
        # Obter a distância até ao laboratório
        distancia = nx.shortest_path_length(graph2, current_location_name, "laboratório")

        # Imprimir a distância até ao laboratório
        print(f"A distância até ao laboratório é de {distancia} divisões.")
    else:
        print("Não foi possível determinar a localização atual.")


# 5. Quanto tempo achas que demoras a ir de onde estás até ao escritório?
def resp5():
    # Obter a localização atual do agente
    current_location_name = get_current_location_name(posicaoGlobal)

    # Atualizar o grafo
    graph3 = criar_grafo()

    if not any("escritório" in zona for zona in graph3.nodes):
        print("Ainda não conheço o escritório.")
        return

    if current_location_name == "escritório":
        print("Já estou no escritório.")
        return

    if current_location_name:
        # Obter o caminho para o escritório
        caminho = nx.shortest_path(graph3, current_location_name, "escritório")

        # Calcular e imprimir o tempo até ao escritório
        tempo = len(caminho) * 2
        print(f"O tempo até ao escritório é de {tempo} segundos.")
    else:
        print("Não foi possível determinar a localização atual.")


# 6. Quanto tempo achas que falta até ficares sem bateria?
def resp6():
    global lastTime
    global lastBateria

    # Calcular a taxa de descarga
    descarga = ((time.time() - lastTime) * 100) / (lastBateria - momentBateria)

    # Atualizar os valores
    lastTime = time.time()
    lastBateria = momentBateria

    if lastBateria == 0:
        print("Estou sem bateria.")
        return

    # Calcular e imprimir o tempo restante
    tempo_restante = descarga * momentBateria / 100
    print(f"Faltam aproximadamente {round(tempo_restante, 2)} segundos até ficar sem bateria.")


# 7. Qual é a probabilidade da próxima pessoa a encontrares ser um supervisor?
def resp7():
    total_pessoas = len(lastVisited)

    if total_pessoas > 0:
        supervisores = sum(1 for pessoa in lastVisited if "supervisor" in pessoa)
        probabilidade_supervisor = supervisores / total_pessoas
        print(f"A probabilidade da próxima pessoa ser um supervisor é aproximadamente {round(probabilidade_supervisor * 100, 2)}%.")
    else:
        print("Não há pessoas suficientes para calcular a probabilidade.")


# 8. Qual é a probabilidade de encontrar um operário numa zona se estiver lá uma máquina mas não estiver lá um supervisor?
def resp8():
    # Obter a localização atual do agente
    current_location = get_current_location_name(posicaoGlobal)

    if current_location:
        # Verificar se há uma máquina e nenhum supervisor na zona
        maquina_presente = any("máquina" in objetos for objetos in current_location)
        supervisor_presente = any("supervisor" in objetos for objetos in current_location)

        if maquina_presente and not supervisor_presente:
            # Calcular a probabilidade de encontrar um operário
            probabilidade_operario = sum(1 for pessoa in lastVisited if "operário" in pessoa) / len(lastVisited)
            print(f"A probabilidade de encontrar um operário na zona é aproximadamente {round(probabilidade_operario * 100, 2)}%.")
        else:
            print("Não há máquina ou há um supervisor na zona.")
    else:
        print("Não foi possível determinar a localização atual.")