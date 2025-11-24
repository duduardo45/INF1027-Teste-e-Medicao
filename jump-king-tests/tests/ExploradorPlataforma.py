import sys
import os
import math

# Garante que o Python encontre os módulos na pasta raiz
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .AgenteTeste import AgenteTeste

class ExploradorPlataforma:
    def __init__(self, headless=True):
        """
        Inicializa o AgenteTeste.
        """
        # Configura para modo headless e FPS alto para máxima velocidade
        self.agente = AgenteTeste(headless=headless, fps=10000)
        
        # Ajuste vertical para o Rei ficar exatamente sobre a plataforma.
        self.king_feet_offset = 31 

    def mapear_plataforma(self, nivel_id, plataforma_params):
        """
        Explora saltos a partir de uma plataforma usando amostragem de pontos.

        Args:
            nivel_id (int): O ID do nível onde a plataforma está.
            plataforma_params (tuple): (x, y, w, h, slope, slip, support, snow)
            
        Returns:
            dict: { (pos_x, carga, direcao): (nivel_final, x_final, y_final) }
        """
        # Desempacota os parâmetros
        px, py, pw, ph, slope, slip, support, snow = plataforma_params
        
        start_y = py - self.king_feet_offset
        resultados = {}
        
        # Define os limites
        start_x = int(px)
        end_x = int(px + pw)
        
        # --- Lógica de Amostragem (10 pontos) ---
        # Se a largura for menor que 10, testamos todos os pixels disponíveis.
        # Caso contrário, pegamos 10 pontos distribuídos igualmente.
        num_amostras = 10
        
        if pw < num_amostras:
            pontos_teste = list(range(start_x, end_x + 1))
        else:
            pontos_teste = []
            step = pw / (num_amostras - 1)
            for i in range(num_amostras):
                ponto = int(start_x + (i * step))
                # Garante que não ultrapasse o limite da plataforma
                if ponto > end_x: 
                    ponto = end_x
                pontos_teste.append(ponto)
            
            # Remove duplicatas e ordena (por segurança em arredondamentos)
            pontos_teste = sorted(list(set(pontos_teste)))

        print(f"\n--- Iniciando Mapeamento Otimizado ---")
        print(f"Plataforma: ({px}, {py}) | Largura: {pw}")
        print(f"Pontos de teste selecionados ({len(pontos_teste)}): {pontos_teste}")

        # Loop pelos pontos selecionados
        for pos_x in pontos_teste:
            
            print(f"\n--> Testando Posição X: {pos_x}")
            
            # Loop de Carga: 0 a 35 frames
            for carga in range(36):
                
                for direcao in ['direita', 'esquerda']:
                    
                    # 1. Posiciona
                    self.agente.definir_estado_inicial(nivel_id, float(pos_x), float(start_y))
                    
                    # 2. Pula
                    resultado = self.agente.executar_teste_pulo(direcao, carga)
                    
                    # 3. Notifica (Print solicitado)
                    # Formato: [Carga] Direção -> Resultado Final
                    print(f"   [{carga:02d}f] {direcao[:3].upper()} -> Pousou em {resultado}")
                    
                    # 4. Salva
                    chave = (pos_x, carga, direcao)
                    resultados[chave] = resultado

        print(f"\n--- Mapeamento Concluído ---")
        print(f"Total de testes realizados: {len(resultados)}")
        return resultados