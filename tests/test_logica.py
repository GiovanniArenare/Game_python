import unittest
import os
# Importando as funções lógicas do seu próprio projeto para testá-las
from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, tomar_dano
from src.dados import salvar_recorde, carregar_recorde

class TestSonicaRunner(unittest.TestCase):

    def setUp(self):
        """Executado antes de cada teste. Configura um ambiente limpo."""
        self.arquivo_teste_recorde = "recorde_teste.txt"
        if os.path.exists(self.arquivo_teste_recorde):
            os.remove(self.arquivo_teste_recorde)

    def tearDown(self):
        """Executado após cada teste. Limpa os arquivos temporários gerados."""
        if os.path.exists(self.arquivo_teste_recorde):
            os.remove(self.arquivo_teste_recorde)

    # --- TESTES DAS FUNÇÕES DE PONTUAÇÃO E MECÂNICA ---
    def test_calcular_pontos_adiciona_corretamente(self):
        """Garante que a pontuação acumula os valores passados de forma exata."""
        pontos_iniciais = 0
        novos_pontos = calcular_pontos(pontos_iniciais, 15)  # Coleta de coelho dourado
        self.assertEqual(novos_pontos, 15)

        pontos_com_obstaculo = calcular_pontos(novos_pontos, 5) # Passar por obstáculo
        self.assertEqual(pontos_com_obstaculo, 20)

    def test_limitar_valor_da_velocidade(self):
        """Verifica se o teto e o piso da velocidade progressiva funcionam."""
        vel_inicial = 5
        vel_maxima = 15
        
        # Caso 1: Velocidade abaixo do limite máximo deve retornar ela mesma
        vel_calculada = 8
        self.assertEqual(limitar_valor(vel_calculada, vel_inicial, vel_maxima), 8)
        
        # Caso 2: Velocidade ultrapassando o máximo deve ser travada no limite máximo
        vel_calculada_alta = 20
        self.assertEqual(limitar_valor(vel_calculada_alta, vel_inicial, vel_maxima), 15)

    def test_tomar_dano_reduz_vidas(self):
        """Verifica se o contador de vidas diminui corretamente ao tomar dano."""
        vidas_iniciais = 3
        vidas_restantes = tomar_dano(vidas_iniciais, 1)
        self.assertEqual(vidas_restantes, 2)

    def test_jogador_perdeu_quando_vidas_chegam_a_zero(self):
        """Valida se o estado de fim de jogo ativa somente quando as vidas acabam."""
        self.assertFalse(jogador_perdeu(3))  # Com 3 vidas não perdeu
        self.assertFalse(jogador_perdeu(1))  # Com 1 vida ainda não perdeu
        self.assertTrue(jogador_perdeu(0))   # Com 0 vidas o jogo deve acabar

    # --- TESTES DE PERSISTÊNCIA DE DADOS (RECORDES) ---
    def test_salvar_e_carregar_recorde(self):
        """Garante que o High Score está sendo salvo e lido corretamente do arquivo txt."""
        pontuacao_alta = 150
        
        # Salva o valor no arquivo de teste
        salvar_recorde(self.arquivo_teste_recorde, pontuacao_alta)
        
        # Carrega o valor e valida se continua igual
        recorde_carregado = carregar_recorde(self.arquivo_teste_recorde)
        self.assertEqual(recorde_carregado, 150)

    def test_carregar_recorde_arquivo_inexistente(self):
        """Testa o comportamento do jogo quando o arquivo de recorde ainda não existe."""
        # Se o arquivo não existir, o jogo deve tratar o erro e retornar 0 por padrão
        recorde_carregado = carregar_recorde("arquivo_que_nao_existe.txt")
        self.assertEqual(recorde_carregado, 0)

if __name__ == '__main__':
    unittest.main()