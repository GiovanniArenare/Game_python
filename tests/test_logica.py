from src.funcoes import calcular_pontos, jogador_perdeu, tomar_dano

def test_calcular_pontos():
    """Testa se a pontuação soma corretamente."""
    assert calcular_pontos(10, 5) == 15
    assert calcular_pontos(10, 0) == 10

def test_tomar_dano():
    """Testa se o jogador perde vida corretamente ao ser atingido."""
    assert tomar_dano(3, 1) == 2

def test_jogador_perdeu():
    """Testa se o sistema reconhece quando o jogo deve acabar."""
    assert jogador_perdeu(3) is False
    assert jogador_perdeu(0) is True