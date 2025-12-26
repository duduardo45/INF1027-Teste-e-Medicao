import networkx as nx
import matplotlib.pyplot as plt
from AgenteTeste import AgenteTeste


# =======================================================
#   OBJETO PLATAFORMA (não usado diretamente)
# =======================================================
class Plataforma:
    def __init__(self, x, y, w, h, slope, slip, support, snow):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.slope = slope
        self.slip = slip
        self.support = support
        self.snow = snow


# =======================================================
#   TESTADOR PRINCIPAL
# =======================================================
class PlataformaTester:

    def __init__(self, plataforma: Plataforma):
        self.plataforma = plataforma
        self.agente = AgenteTeste()

    # --------------------------------------------------
    #   TESTAR PULOS A PARTIR DE POSIÇÕES
    # --------------------------------------------------
    def testar_combinacoes(self, niveis, posicoes, cargas, direcoes):
        resultados = []

        for nivel in niveis:
            for (x, y) in posicoes:
                for carga in cargas:
                    for direcao in direcoes:

                        self.agente.definir_estado_inicial(nivel, x, y)

                        nivel_f, x_f, y_f = self.agente.executar_teste_pulo(
                            direcao=direcao,
                            frames_carga=carga
                        )

                        resultados.append({
                            "nivel_inicial": nivel,
                            "x_inicial": x,
                            "y_inicial": y,
                            "carga": carga,
                            "direcao": direcao,
                            "nivel_final": nivel_f,
                            "x_final": x_f,
                            "y_final": y_f
                        })

        return resultados

    # --------------------------------------------------------------
    #   MULTI-ITER BFS DE PULOS (com opção de restrição de Y)
    # --------------------------------------------------------------
    def explorar_multiplos_pulos(
        self,
        posicoes_iniciais,
        cargas,
        direcoes,
        niveis=[0],
        max_iter=3,
        tolerancia_y=3,
        usar_restricao_y=True
    ):

        resultados_total = []
        fronteira = posicoes_iniciais[:]  # lista de (x,y)

        for camada in range(max_iter):
            print(f"\n=== CAMADA {camada} ===")

            novos_resultados = []
            nova_fronteira = []

            for (x0, y0) in fronteira:

                resultados = self.testar_combinacoes(
                    niveis=niveis,
                    posicoes=[(x0, y0)],
                    cargas=cargas,
                    direcoes=direcoes
                )

                for r in resultados:
                    y_final = r["y_final"]
                    novos_resultados.append(r)

                    if not usar_restricao_y:
                        nova_fronteira.append((r["x_final"], r["y_final"]))
                    else:
                        if abs(y_final - y0) > tolerancia_y:
                            nova_fronteira.append((r["x_final"], r["y_final"]))

            resultados_total.extend(novos_resultados)
            fronteira = nova_fronteira[:]

        return resultados_total

    # --------------------------------------------------
    #   GERAR O GRAFO
    # --------------------------------------------------
    def gerar_grafo(self, resultados):
        G = nx.MultiDiGraph()

        for dados in resultados:

            x_i = dados.get("x_inicial")
            y_i = dados.get("y_inicial")
            x_f = dados.get("x_final")
            y_f = dados.get("y_final")

            if None in (x_i, y_i, x_f, y_f):
                print("Aviso: posição inválida detectada:", dados)
                continue

            nodo_inicial = (x_i, y_i)
            nodo_final = (x_f, y_f)

            G.add_node(nodo_inicial)
            G.add_node(nodo_final)

            G.add_edge(
                nodo_inicial,
                nodo_final,
                carga=dados["carga"],
                direcao=dados["direcao"],
                dados=dados
            )

        return G

    # --------------------------------------------------
    #   AGRUPAR Ys EM NÍVEIS HORIZONTAIS
    # --------------------------------------------------
    def agrupar_y_em_niveis(self, G, tolerancia_y=5):

        ys = sorted({y for (x, y) in G.nodes()})

        grupos = []
        for y in ys:
            colocado = False
            for grupo in grupos:
                if abs(y - grupo[-1]) <= tolerancia_y:
                    grupo.append(y)
                    colocado = True
                    break
            if not colocado:
                grupos.append([y])

        y_map = {}
        for nivel, grupo in enumerate(grupos):
            for y in grupo:
                y_map[y] = nivel

        return y_map

    # --------------------------------------------------
    #   PLOTAR GRAFO — X real, Y em níveis, arestas curvas
    # --------------------------------------------------
    def plotar_grafo(self, G, espaco_vertical=200, tolerancia_y=5):
            """
            Agora o X é exatamente o X real do jogo.
            Apenas Y é convertida para níveis verticais.
            """

            # 1 — agrupar Y em níveis
            y_map = self.agrupar_y_em_niveis(G, tolerancia_y)

            # 2 — posições reais: X real / Y por nível
            pos = {}
            for (x, y) in G.nodes():
                nivel = y_map[y]
                pos[(x, y)] = (x, nivel * espaco_vertical)

            # 3 — estilos
            cor_por_direcao = {
                "direita": "tab:blue",
                "esquerda": "tab:red",
                "up": "tab:green",
                "down": "tab:purple"
            }

            def calcular_espessura(carga):
                return max(0.5, carga / 20.0)

            plt.figure(figsize=(15, 10))

            # 4 — nós (sem labels)
            nx.draw_networkx_nodes(
                G, pos,
                node_size=200,
                node_color="lightgray",
                edgecolors="black"
            )

            # 5 — arestas
            for (u, v, k, data) in G.edges(keys=True, data=True):

                direcao = data.get("direcao", "")
                carga = data.get("carga", 0)

                cor = cor_por_direcao.get(direcao, "black")
                largura = calcular_espessura(carga)

                # curvatura da aresta
                rad = 0.15 + (k * 0.15)

                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=[(u, v)],
                    width=largura,
                    edge_color=cor,
                    arrowsize=10,
                    connectionstyle=f"arc3,rad={rad}"
                )

            # estilo Jump King
            plt.gca().invert_yaxis()

            # sem eixos
            plt.axis("off")

            plt.title("Grafo — X Real do Jogo / Y Aglutinado por Nível")
            plt.show()


# =======================================================
#   EXEMPLO DE USO
# =======================================================
if __name__ == "__main__":

    plataforma = Plataforma(
        x=0, y=0, w=10, h=1,
        slope=0.0, slip=0.0, support=True, snow=False
    )

    tester = PlataformaTester(plataforma)

    posicoes_iniciais = [(330, 250)]
    cargas = [5, 15, 30, 60]
    direcoes = ["direita", "esquerda"]

    resultados = tester.explorar_multiplos_pulos(
        posicoes_iniciais,
        cargas=cargas,
        direcoes=direcoes,
        niveis=[1],
        max_iter=1,
        tolerancia_y=3,
        usar_restricao_y=False
    )

    grafo = tester.gerar_grafo(resultados)

    tester.plotar_grafo(
        grafo,
        espaco_vertical=250,
        tolerancia_y=5,
    )
