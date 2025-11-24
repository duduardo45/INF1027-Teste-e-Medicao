import unittest
from .ExploradorPlataforma import ExploradorPlataforma

class TestMapeamento(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Inicializa o explorador (e o jogo) apenas uma vez para todos os testes.
        Isso economiza tempo pois não abre/fecha o jogo a cada teste.
        """
        print("Inicializando o Explorador e o Jogo...")
        cls.explorador = ExploradorPlataforma(headless=False)

    def test_varredura_plataforma_exemplo(self):
        """
        Testa a varredura de uma plataforma específica e verifica se gerou resultados.
        """
        # --- Configuração do Cenário ---
        nivel = 0
        
        # Plataforma do início do jogo (Nível 0)
        # Formato: (x, y, w, h, slope, slip, support, snow)
        # Nota: Para testes rápidos, reduzi a largura (w) para 5 pixels. 
        # A largura real no jogo é 128.
        # Plataforma real do Nível 0 (Largura 128)
        plataforma = (352, 185, 128, 175, 0, 0, False, False)
        
        # --- Execução ---
        resultados = self.explorador.mapear_plataforma(nivel, plataforma)
        
        # --- Verificações ---
        
        # 1. Deve retornar um dicionário
        self.assertIsInstance(resultados, dict)
        
        # 2. Não deve estar vazio
        self.assertGreater(len(resultados), 0, "O mapeamento não retornou nenhum resultado.")
        
        # 3. Verificação da estrutura dos dados
        # Pega um item qualquer para validar o formato
        chave_exemplo = list(resultados.keys())[0]
        valor_exemplo = resultados[chave_exemplo]
        
        print(f"\nExemplo de dado capturado:")
        print(f"Entrada (X, Carga, Dir): {chave_exemplo}")
        print(f"Saída (Nível, X, Y): {valor_exemplo}")
        
        # Valida se a chave tem 3 elementos (pos_x, carga, direcao)
        self.assertEqual(len(chave_exemplo), 3)
        
        # Valida se o valor tem 3 elementos (nivel, x, y)
        self.assertEqual(len(valor_exemplo), 3)

if __name__ == "__main__":
    unittest.main()