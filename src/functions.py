import consts # Constantes
import ctypes # Biblioteca com tipos compatíveis com C
from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

# Armazena uma referência para dispositivo padrão de saída do Windows, que neste
# caso é o terminal (console) (indicado pelo valor -11 passado como parametro).
gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

# Armazena as mensagens de erro do programa.
gError = None

# Move o cursor do console para a posição especificada.
# Essa função só tem efeito no terminal do Windows.
def moveCursor(x, y):
    value = (x + (y << 16))
    ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong (value))

# Limpa a tela do terminal completamente. Essa função é utilizada no inicio de
# cada loop para evitar que caracteres do loop anterior permaneçam na tela.
def clearScreen():
    changeColor(consts.COLOR_DEFAULT)
    moveCursor(0,0)

    # Imprime linhas de espaços para substituir os caracteres impressos na tela
    for y in range(0, consts.ROWS + 1):
        print(" " * (consts.COLUMNS + 1))
 
    moveCursor(0,0)

# Imprime uma linha horizontal na tela.
def horizontalLine():
    print('=' * consts.COLUMNS)

# Exibe o cabeçalho do programa.
def showHeader():
    horizontalLine()
    print(consts.TITLE.center(consts.COLUMNS))
    horizontalLine()
    print(" " * consts.COLUMNS)
    print("Bem vindo ao jogo de Nim.".center(consts.COLUMNS))
    print(" " * consts.COLUMNS)
    print("A meta do jogo de Nim é forçar seu oponente a retirar o último palito.".center(consts.COLUMNS))
    print("Para isso, você pode remover quantos palitos desejar das linhas dispostas.".center(consts.COLUMNS))
    print(" " * consts.COLUMNS)
    horizontalLine()

# Armazena uma mensagem de erro para ser impressa no console no próximo loop
# do programa.
def registerError(msg):
    global gError
    gError = str(msg).center(consts.COLUMNS)

# Caso a última instrução tenha resultado em um erro, existe a mensagem de erro
# ao usuário indicando o erro que aconteceu.
def showError():
    global gError

    moveCursor(0, consts.ROWS - 1)

    if gError :
        
        changeColor(consts.COLOR_ERROR)
        print(gError)
        changeColor(consts.COLOR_DEFAULT)
        
        gError = None
    else :
        print(" " * consts.COLUMNS)

    moveCursor(0, 0)

# Muda a cor do texto a ser impresso no console.
# Essa função só tem funcionalidade no terminal do Windows.
def changeColor(color):
    ctypes.windll.kernel32.SetConsoleTextAttribute(gHandle, color)