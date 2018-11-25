import functions
import consts
import random
from time import sleep

"""
Esta classe representa o jogo.
"""
class Game:
    # Disposição de palitos do jogo.
    # Cada elemento da matriz representa uma linha, com o número representando
    # os palitos disponíveis.
    straws = [1, 3, 5, 7]

    # Indica se o computador realizará a próxima jogada.
    # False = Jogador humano fará a próxima jogada
    # True = Computador fará a jogada
    computerPlay = False

    # Qual jogador inicia a rodada
    # False = Jogador humano
    # True = Computador
    roundStarter = False

    # Escore dos jogadores
    score = [0,0]

    # Inicia a próxima rodada do jogo.
    # O jogador que iniciou a jogada anterior passa a fazer a segunda jogada.
    def nextRound(self):
        self.roundStarter = not self.roundStarter
        
        self.computerPlay = self.roundStarter

        self.straws = [1, 3, 5, 7]

    # Remove a quantidade de palitos da linha especificada.
    # 
    # row: Linha da qual deseja remover os palitos
    # howMany: Quantos palitos deseja que sejam removidos
    def remove(self, row, howMany):
        row = int(row) - 1
        howMany = int(howMany)

        if row < 0:
            raise ValueError(
                "A linha para remoção de palitos deve ser um valor maior ou igual a um.")

        if row >= len(self.straws):
            raise ValueError(
                "A linha para remoção de palitos deve ser um valor igual ou menor que " + str(len(self.straws)))

        if howMany < 1:
            raise ValueError(
                "Indique uma quantidade de palitos maior ou igual a um.")

        if howMany > self.straws[row]:
            raise ValueError(
                "A linha " + str(row + 1) + " possui " + str(self.straws[row]) + " palito(s) e "
                + "você tentou remover " + str(howMany) + " palito(s).")

        self.straws[row] -= howMany

    # Caso ainda exista a possibilidade de fazer jogadas, esta função exibe os
    # palitos na tela para o usuário com o placar logo acima. Caso não existam
    # mais rodadas as serem feitas, é exibido o resultado da última rodada.
    def showStraws(self):
        if self.availablePlays() > 0 :
            if self.score[0] < self.score[1] :
                functions.changeColor(consts.COLOR_SCORE_LOSE)
            elif self.score[0] > self.score[1] :
                functions.changeColor(consts.COLOR_SCORE_WIN)
            else :
                functions.changeColor(consts.COLOR_STRAWS)

            print(("       VOCÊ " + str(self.score[0]) + " x " + str(self.score[1]) + " COMPUTADOR").center(consts.COLUMNS))
            print(" " * consts.COLUMNS);
            print(" " * consts.COLUMNS)
            
            functions.changeColor(consts.COLOR_STRAWS)

            for i, straw in enumerate(self.straws):
                head = str(i + 1) + ". "
                straws = ("I" * straw).center(16, " ")

                print((head + straws).center(consts.COLUMNS, " "))
        else :
            if self.computerPlay == False :
                self.score[0] += 1

                functions.changeColor(consts.COLOR_WIN)

                print(" " * consts.COLUMNS)    
                print(" " * consts.COLUMNS)
                print("VOCÊ VENCEU!".center(consts.COLUMNS))
            else :
                self.score[1] += 1

                functions.changeColor(consts.COLOR_LOSE)
            
                print(" " * consts.COLUMNS)    
                print(" " * consts.COLUMNS)
                print("O COMPUTADOR VENCEU".center(consts.COLUMNS))

            print(("VOCÊ " + str(self.score[0]) + " x " + str(self.score[1]) + " COMPUTADOR").center(consts.COLUMNS))
            print(" " * consts.COLUMNS)

        print(' ' * consts.COLUMNS)
        functions.changeColor(consts.COLOR_DEFAULT)

    # Exibe a mensagem de saída do jogo, indicando se o usuário venceu ou não
    # o computador.
    def showExitMessage(self):
        print(" " * consts.COLUMNS)
        print((consts.TITLE + " foi finalizado").center(consts.COLUMNS))

        if(self.score[0] > self.score[1]):
            functions.changeColor(consts.COLOR_SCORE_WIN)
            print("VOCÊ VENCEU O COMPUTADOR".center(consts.COLUMNS))
        elif(self.score[0] < self.score[1]):
            functions.changeColor(consts.COLOR_SCORE_LOSE)
            print("VOCÊ PERDEU PARA O COMPUTADOR".center(consts.COLUMNS))
        else:
            functions.changeColor(consts.COLOR_STRAWS)
            print("VOCÊ E O COMPUTADOR EMPATARAM".center(consts.COLUMNS))

        print(("VOCÊ " + str(self.score[0]) + " x " + str(self.score[1]) + " COMPUTADOR").center(consts.COLUMNS))
        print(" " * consts.COLUMNS)

        functions.changeColor(consts.COLOR_INIT)


    # Caso ainda existam jogadas possíveis para o jogador, exibe inputs para
    # inserção da linha e da quantidade de palitos a serem removidos da linha.
    # Caso não existam mais jogadas possíveis, pergunta ao jogador se ele 
    # deseja continuar jogando ou não.
    # 
    def waitPlayerPlay(self):
        try:
            print("Insira abaixo a linha e quantidade de palitos a serem removidos.".center(consts.COLUMNS))
            print("Ex.: Linha 2  Palitos 1.".center(consts.COLUMNS))
            print(" " * consts.COLUMNS)

            functions.changeColor(consts.COLOR_STRAWS)
            functions.moveCursor(0, consts.ROWS - 2)
            row = input("Linha: ")

            functions.moveCursor(20, consts.ROWS - 2)
            straws = input("Palitos: ")

            self.remove(row, straws)

        except ValueError as e:
            raise

    # Aguarda a jogada do computador.
    # 
    def waitComputerPlay(self):
        print("Aguarde a jogada do computador.".center(consts.COLUMNS))
        sleep(1) # Aguarda alguns segundos para o jogo parecer natural

        nim = self.binarySum()

        if nim == 0:
            for i, val in enumerate(self.straws):
                if val > 0:
                    self.straws[i] = 0
                    break
        else :
            targetIndex = None
            targetValue = None

            for i, val in enumerate(self.straws):
                if val ^ nim < val:
                    targetIndex = i
                    targetValue = val - (val ^ nim)
                    break 

            haveManyStraws = 0

            for i, val in enumerate(self.straws):
                if targetIndex == i:
                    result = val - targetValue
                else:
                    result = val

                if result > 1:
                    haveManyStraws += 1

            # Caso não existam linhas com mais de uma linha, deixa uma
            # linha de 1 palito 
            if haveManyStraws == 0:
                targetIndex = self.straws.index(max(self.straws))

                haveOneStraw = sum(straws == 1 for straws in self.straws)

                if haveOneStraw % 2 != 1:
                    targetValue = self.straws[targetIndex] - 1
                else:
                    targetValue = self.straws[targetIndex]

            self.straws[targetIndex] -= targetValue

    # Retorna a soma binária dos palitos disponíveis no jogo. O valor dessa
    # soma binária é utilizado para determinar se o próximo jogador tem changes
    # de vencer o jogo ou não.
    def binarySum(self):
        xor = 0
        
        for i, val in enumerate(self.straws):
            xor = xor ^ val

        return xor

    # Pergunta ao usuário se ele deseja jogar mais uma rodada. Caso o jogador
    # insira S, uma nova rodada se inicia. Caso o jogador insira N, o programa
    # é encerrado.
    def showPlayAgainInput(self):
        playAgain = input("Jogar mais uma partida [S para SIM, N para NAO]?".center(consts.COLUMNS - 10))

        if playAgain.upper() == 'S' :
            self.nextRound()
        elif playAgain.upper() == 'N' :
            self.showExitMessage()
            exit()
        else :
            raise ValueError("Responda apenas com S para jogar novamente ou N para sair.")

    # Retorna quantas jogadas ainda podem ser feitas no jogo.
    def availablePlays(self):
        addition = 0;

        for straw in self.straws:
            addition += straw

        return addition
