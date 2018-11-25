# Jogo de Nim
# Desenvolvido por 
# Compatível apenas com Windows.
  
import functions # Biblioteca de funções
import consts # Valores constantes
from game import Game # Classe do jogo

# Objeto que armazena da partida atual.
game = Game()

# Loop do programa.
# Caso precise encerrar o programa antes do final da rodada, precione CTRL+C
while True:
    # Limpa a tela completamente
    functions.clearScreen()

    # Caso tenha acontecido algum erro no loop anterior, o exibe
    functions.showError()

    # Exibe o cabeçalho do programa
    functions.showHeader()

    # Exibe o palitos disponíveis no jogo ou o resultado da rodada anterior.
    game.showStraws()
    
    functions.horizontalLine()

    try :
        if(game.availablePlays() > 0) :
            if(game.computerPlay == False):
                game.waitPlayerPlay()
                game.computerPlay = True # Computador é o próximo
            else :
                game.waitComputerPlay()
                game.computerPlay = False # Jogador é o próximo
        else :
            # Fim da rodada. Pergunta ao jogador se ele quer jogar novamente.
            game.showPlayAgainInput()
    except ValueError as e :
        # Registra o erro para ser exibido no próximo loop
        functions.registerError(e)
