import unittest
from .AgenteTeste import AgenteTeste

class TestAgenteTeste(unittest.TestCase):

    def setUp(self):
        """
        Set up the test agent for each test case.
        """
        self.agente = AgenteTeste()
        self.start_lvl = 0
        self.start_x = 230
        self.start_y = 298

    def test_pulo_direita(self):
        """
        Test a jump to the right with medium force (15 frames).
        """
        resultado = self.agente.verificar_determinismo(
            self.start_lvl, self.start_x, self.start_y, 'direita', 15
        )
        self.assertTrue(resultado, "O teste de pulo para a direita não foi determinístico.")

    def test_pulo_esquerda(self):
        """
        Test a jump to the left with medium force (15 frames).
        """
        resultado = self.agente.verificar_determinismo(
            self.start_lvl, self.start_x, self.start_y, 'esquerda', 15
        )
        self.assertTrue(resultado, "O teste de pulo para a esquerda não foi determinístico.")

    def test_pulo_fraco_direita(self):
        """
        Test a weak jump to the right (5 frames).
        """
        resultado = self.agente.verificar_determinismo(
            self.start_lvl, self.start_x, self.start_y, 'direita', 5
        )
        self.assertTrue(resultado, "O teste de pulo fraco para a direita não foi determinístico.")

    def test_pulo_maximo_esquerda(self):
        """
        Test a maximum jump to the left (30 frames).
        """
        resultado = self.agente.verificar_determinismo(
            self.start_lvl, self.start_x, self.start_y, 'esquerda', 30
        )
        self.assertTrue(resultado, "O teste de pulo máximo para a esquerda não foi determinístico.")

if __name__ == "__main__":
    unittest.main()