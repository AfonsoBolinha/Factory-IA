"""
agente.py

Diogo Ferreira, 46198
Afonso Martins, 45838
"""
# Imports
import time
import gender_guesser.detector as gender
import heapq

# Definir os Corredores e as divisões
corredor1 = [(30, 165), (135, 350), "corredor 1"]
corredor2 = [(165, 165), (485, 185), "corredor 2"]
corredor3 = [(30, 380), (500, 435), "corredor 3"]
corredor4 = [(530, 215), (635, 435), "corredor 4"]
divisao5 = [(30, 30), (135, 135), "multiusos 5"]
divisao6 = [(180, 30), (285, 135), "multiusos 6"]
divisao7 = [(330, 30), (485, 135), "multiusos 7"]
divisao8 = [(530, 30), (770, 185), "multiusos 8"]
divisao9 = [(665, 230), (770, 285), "multiusos 9"]
divisao10 = [(665, 330), (770, 385), "entrada da fábrica"]
divisao11 = [(530, 465), (770, 570), "multiusos 11"]
divisao12 = [(330, 465), (485, 570), "multiusos 12"]
divisao13 = [(180, 465), (285, 570), "multiusos 13"]
divisao14 = [(30, 465), (135, 570), "multiusos 14"]
divisao15 = [(160, 230), (485, 335), "multiusos 15"]

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


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def build_graph(locations):
    graph = {}

    for start, end, _ in locations:
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []

        graph[start].append((end, 1))
        graph[end].append((start, 1))

    return graph


def find_path(graph, start, goal, locations):
    frontier = []
    heapq.heappush(frontier, (0, start))

    came_from = {}
    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = 0

    goal_location = locations[goal]

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        current_location_index = None
        for i, (start, end, nome) in enumerate(locations):
            if start[0] == current[0] and start[1] == current[1] and end[0] == current[0] and end[1] == current[1]:
                current_location_index = i
                break

        if current_location_index is None:
            continue

        current_location = locations[current_location_index]

        if current_location not in graph:
            continue

        for next, cost in graph[current_location]:
            new_cost = cost_so_far[current] + cost

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal_location[0], next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    if goal not in came_from:
        return None

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path


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
    pergunta1(objetos)

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
    empacotamento_location = "empacotamento"
    current_location = get_current_location(posicaoGlobal)

    if empacotamento_location not in [nome for _, _, nome in all_locations]:
        print("Ainda não sei onde se encontra a zona de empacotamento.")
        return

    if current_location:
        if current_location != empacotamento_location:
            graph = build_graph(all_locations)

            # Encontrar os índices de current_location e empacotamento_location
            current_index = [i for i, (_, _, nome) in enumerate(all_locations) if nome == current_location]
            goal_index = [i for i, (_, _, nome) in enumerate(all_locations) if nome == empacotamento_location]

            print(f"Current Index: {current_index}")
            print(f"Goal Index: {goal_index}")

            if current_index and goal_index:
                # Use o primeiro elemento das listas, já que deve haver apenas uma correspondência
                current_index = current_index[0]
                goal_index = goal_index[0]

                print(f"Current Index: {current_index}")
                print(f"Goal Index: {goal_index}")

                # Adicionar o argumento locations à chamada da função
                path = find_path(graph, current_location, goal_index, all_locations)

                if path:
                    print(f"Caminho para a zona de empacotamento: {path}")
                else:
                    print("Não foi possível encontrar um caminho para a zona de empacotamento.")
            else:
                print("Erro ao obter os índices das localizações.")
        else:
            print("Já estou na zona de empacotamento.")
    else:
        print("Não consigo determinar a localização atual.")



def resp4():
    pass


def resp5():
    pass


def resp6():
    # 6. Quanto tempo achas que falta até ficares sem bateria?
    global lastTime
    global lastBateria

    # Calcular a taxa de descarga
    descarga = ((time.time() - lastTime) * 100) / (lastBateria - momentBateria)

    # Atualizar os valores
    lastTime = time.time()
    lastBateria = momentBateria

    # Calcular e imprimir o tempo restante
    tempo_restante = descarga * momentBateria / 100
    print(f"Faltam aproximadamente {round(tempo_restante, 2)} segundos até ficar sem bateria.")


def resp7():
    # 7. Qual é a probabilidade da próxima pessoa a encontrares ser um supervisor?
    total_pessoas = len(lastVisited)

    if total_pessoas > 0:
        supervisores = sum(1 for pessoa in lastVisited if "supervisor" in pessoa)
        probabilidade_supervisor = supervisores / total_pessoas
        print(f"A probabilidade da próxima pessoa ser um supervisor é aproximadamente {round(probabilidade_supervisor * 100, 2)}%.")
    else:
        print("Não há pessoas suficientes para calcular a probabilidade.")



def resp8():
    # 8. Qual é a probabilidade de encontrar um operário numa zona se estiver lá uma máquina mas não estiver lá um supervisor?
    # Obter a localização atual do agente
    current_location = get_current_location(posicaoGlobal)

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