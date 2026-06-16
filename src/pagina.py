from constantes import *

class Pagina:
    def __init__(self) -> None:
        self.numChaves: int = 0
        self.chaves: list = [NULO] * (ORDEM - 1)
        self.offsets: list = [NULO] * (ORDEM - 1) #ela pediu pra add esse
        self.filhos: list = [NULO] * ORDEM