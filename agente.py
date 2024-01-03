"""
agente.py

Diogo Ferreira, 46198
Afonso Martins, 45838
"""
# Importar as bibliotecas necessárias
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


# Definir as variáveis globais
lastVisited = []
lastZone = []
posicaoGlobal = []
nomes_genero = []
lastTime = time.time()
lastChargeTime = time.time()
striped = ""
lastBateria = 100
momentBateria = 100
total_pessoas_lista = []
total_pessoas = 0
supervisores_encontrados = 0
operarios_encontrados = 0
total_maquinas_lista = []
total_maquinas = 0


# Função para saber o nome da divisão atual, com base na posição do agente
def get_current_location_name(position):
    for start, end, nome in all_locations:
        if start[0] <= position[0] <= end[0] and start[1] <= position[1] <= end[1]:
            return nome
    return ""


# Função para criar/atualizar o grafo e as suas conexões
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

    # Criar o grafo
    grafo = nx.Graph()
    for key, value in conexoes.items():
        grafo.add_node(key)
        for v in value:
            grafo.add_edge(key, v)
    return grafo


# Função para atualizar o momento da última carga da bateria
def update_last_charge_time():
    global lastChargeTime
    lastChargeTime = time.time()


# Função para guardar a penúltima pessoa do sexo masculino que o agente viu
def pergunta1(objetos):
    global striped
    if len(objetos) == 1:
        if ("visitante" in objetos[0]) or ("supervisor" in objetos[0]) or ("operário" in objetos[0]):
            if "visitante" in objetos[0]:
                striped = objetos[0].replace("visitante_", "")
            if "operário" in objetos[0]:
                striped = objetos[0].replace("operário_", "")
            if "supervisor" in objetos[0]:
                striped = objetos[0].replace("supervisor_", "")
            if (striped, "female") in nomes_genero or (striped, "mostly_female") in nomes_genero:
                return
            if (striped, "unknown") in nomes_genero:
                return
            if (striped, "male") in nomes_genero or (striped, "mostly_male") in nomes_genero:
                if len(lastVisited) == 2:
                    if lastVisited[1] != striped:
                        lastVisited.pop(0)
                        lastVisited.append(striped)
                elif len(lastVisited) == 1:
                    if lastVisited[0] != striped:
                        lastVisited.append(striped)
                else:
                    lastVisited.append(striped)
                return
            else:
                what_gender = gender.Detector().get_gender(name=striped, country="portugal")
                nomes_genero.append((striped, what_gender))


# Função para guardar a última zona onde o agente esteve
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


# Função para guardar o número de pessoas diferentes que o agente viu
def pergunta7(objetos):
    global total_pessoas_lista, total_pessoas, supervisores_encontrados, operarios_encontrados
    temp1 = 0
    temp2 = 0
    if len(objetos) == 1:
        if objetos[0] not in total_pessoas_lista and (objetos[0].startswith(("supervisor", "operário", "visitante"))):
            total_pessoas_lista.append(objetos[0])

    for i in total_pessoas_lista:
        if "supervisor" in i:
            temp1 += 1

    for i in total_pessoas_lista:
        if "operário" in i:
            temp2 += 1

    supervisores_encontrados = temp1
    operarios_encontrados = temp2
    total_pessoas = len(total_pessoas_lista)


# Função para guardar o número de máquinas que o agente viu
def pergunta8(objetos):
    global total_maquinas_lista, total_maquinas
    if len(objetos) == 1:
        if objetos[0] not in total_maquinas_lista and (objetos[0].startswith("máquina")):
            total_maquinas_lista.append(objetos[0])

    total_maquinas = len(total_maquinas_lista)


# Função principal
def work(posicao, bateria, objetos):
    # Esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string
    # podem achar o tempo atual usando, p.ex.
    # time.time()

    # Variáveis globais, para serem usadas em outras funções
    global posicaoGlobal, momentBateria, striped

    # Atualizar as variáveis globais
    momentBateria = bateria
    posicaoGlobal = posicao

    # Chamar as funções para as respetivas perguntas
    pergunta1(objetos)
    pergunta2(objetos)
    pergunta7(objetos)
    pergunta8(objetos)

    # Limpar a última zona se o agente sair dela, ou seja, quando vai para um corredor (para a pergunta 2)
    if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [corredor1, corredor2, corredor3, corredor4]):
        lastZone.clear()

    # Atualizar o momento da última carga da bateria
    if momentBateria == 100:
        update_last_charge_time()


# 1. Qual foi a penúltima pessoa do sexo masculino que viste?
def resp1():
    if len(lastVisited) == 2:
        print("A penúltima pessoa foi o " + lastVisited[0] + ".")
    else:
        print("Não há penúltima pessoa.")


# 2. Em que zona te encontras?
def resp2():
    # Obter a localização atual do agente
    current_location_name = get_current_location_name(posicaoGlobal)

    if current_location_name:
        if len(lastZone) == 1:
            current_location_name = lastZone[0]
            for i in range(0, len(all_locations)):
                if any(start[0] <= posicaoGlobal[0] <= end[0] and start[1] <= posicaoGlobal[1] <= end[1] for start, end, nome in [all_locations[i]]):
                    all_locations[i][2] = current_location_name

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

        # Calcular o tempo até ao escritório (2 segundos por divisão, aproximadamente)
        tempo = len(caminho) * 2
        print(f"O tempo até ao escritório é de aproximadamente {(tempo - 3)} segundos.")
    else:
        print("Não foi possível determinar a localização atual.")


# 6. Quanto tempo achas que falta até ficares sem bateria?
def resp6():
    global lastChargeTime, momentBateria

    # Tempo de vida da bateria em segundos
    tempo_vida_bateria = 3 * 60 + 30

    # Calcular o tempo restante até ficar sem bateria
    tempo_passado_desde_ultima_carga = time.time() - lastChargeTime
    tempo_restante_bateria = tempo_vida_bateria - tempo_passado_desde_ultima_carga

    if momentBateria == 0:
        print("A bateria acabou.")
    else:
        print(f"Tempo restante de bateria: {tempo_restante_bateria:.2f} segundos")
        # Se a bateria estiver prestes a acabar, sugerir carregar novamente
        if tempo_restante_bateria < 30:
            print("Devia ir carregar a bateria em breve.")


# 7. Qual é a probabilidade da próxima pessoa a encontrares ser um supervisor?
def resp7():
    global total_pessoas, supervisores_encontrados

    if total_pessoas > 0:
        probabilidade_supervisor = supervisores_encontrados / total_pessoas
        print(f"A probabilidade da próxima pessoa ser um supervisor é aproximadamente {round(probabilidade_supervisor * 100, 2)}%.")
    else:
        print("Não há pessoas suficientes para calcular a probabilidade.")


# 8. Qual é a probabilidade de encontrar um operário numa zona se estiver lá uma máquina mas não estiver lá um supervisor?
def resp8():
    global total_maquinas, total_pessoas, supervisores_encontrados, operarios_encontrados

    if total_maquinas > 0 and total_pessoas > 0:
        probabilidade_operario = operarios_encontrados / total_pessoas
        probabilidade_supervisor = supervisores_encontrados / total_pessoas
        probabilidade_maquina = total_maquinas / total_pessoas

        probabilidade = probabilidade_operario * (1 - probabilidade_supervisor) * probabilidade_maquina
        print(f"A probabilidade de encontrar um operário numa zona se estiver lá uma máquina mas não estiver lá um supervisor é aproximadamente {round(probabilidade * 100, 2)}%.")
    elif total_maquinas > 0 and total_pessoas == 0:
        print("Não há pessoas suficientes para calcular a probabilidade.")
    elif total_maquinas == 0:
        print("Não há máquinas suficientes para calcular a probabilidade.")