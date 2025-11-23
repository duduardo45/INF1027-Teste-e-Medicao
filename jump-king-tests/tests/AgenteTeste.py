import os
import pygame
from .game_tester import GameTester

class AgenteTeste:
    def __init__(self):
        """
        Initialize the test agent using GameTester.
        """
        self.tester = GameTester(headless=False, fps=60)

    def definir_estado_inicial(self, nivel, x, y):
        """
        Set the initial state of the game using GameTester.
        Input: Nível (int), X (float), Y (float)
        """
        self.tester.setup(level=nivel, player_x=x, player_y=y)

    def executar_teste_pulo(self, direcao, frames_carga):
        """
        Execute a controlled jump.
        Input: 
            - direcao: 'direita' ou 'esquerda'
            - frames_carga: quantos frames (ticks) segurar o botão de pulo
        Output:
            - (nivel_final, x_final, y_final)
        """
        # Mapeamento baseado no get_action_dict do King.py
        if direcao == 'direita':
            cmd_carga = 2  # Direita + Espaço
            cmd_solta = 0  # Direita (sem espaço)
        else:
            cmd_carga = 3  # Esquerda + Espaço
            cmd_solta = 1  # Esquerda (sem espaço)

        # 1. Fase de Carga (Segurar botão)
        self.tester.step(frames=frames_carga, action=cmd_carga)

        # 2. Fase de Voo (Soltar botão e esperar pousar)
        # Rodamos frames até o rei parar de cair e parar de se mover
        limite_espera = 600 # Segurança para não travar se cair no infinito

        while limite_espera > 0:
            self.tester.step(frames=1, action=cmd_solta)
            king = self.tester.game.king

            # Critério de parada: Não está caindo, não está pulando e velocidade é zero
            if not king.isFalling and not king.isJump and king.speed == 0 and king.isLanded == False:
                break

            limite_espera -= 1

        return (self.tester.get_current_level(), *self.tester.get_player_position())

    def verificar_determinismo(self, nivel, x, y, direcao, carga, repeticoes=3):
        """
        Roda o MESMO teste várias vezes para ver se o resultado muda.
        """
        resultados = []
        print(f"\n--- Testando Determinismo: Carga {carga} p/ {direcao} ---")

        for i in range(repeticoes):
            self.definir_estado_inicial(nivel, x, y)
            resultado = self.executar_teste_pulo(direcao, carga)
            resultados.append(resultado)
            print(f"Teste {i+1}: Posição Final {resultado}")

        # Verifica se todos os resultados são idênticos
        eh_deterministico = all(r == resultados[0] for r in resultados)

        if eh_deterministico:
            print("Resultado: DETERMINÍSTICO")
        else:
            print("Resultado: NÃO DETERMINÍSTICO")

        return eh_deterministico

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    agente = AgenteTeste()

    # Exemplo: Testar pulo para direita com força média (15 frames)
    # Posição inicial arbitrária (ajuste conforme o level design)
    start_lvl = 0
    start_x = 230
    start_y = 298

    # Teste 1: Pulo fraco (5 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'direita', 5)

    # Teste 2: Pulo médio (15 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'direita', 15)

    # Teste 3: Pulo máximo (30 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'direita', 30)

    # Teste 4: Pulo fraco Esquerda(5 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'esquerda', 5)

    # Teste 5: Pulo médio Esquerda(15 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'esquerda', 15)

    # Teste 6: Pulo máximo Esquerda(30 frames)
    agente.verificar_determinismo(start_lvl, start_x, start_y, 'esquerda', 30)
