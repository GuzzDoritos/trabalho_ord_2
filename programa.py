from sys import argv
import struct

arquivo = "games.dat"

def main():
    '''Esse programa lê os dados gravados no arquivo criado pelo programa
    escreve_registros
    Os registros devem ser lidos do arquivo um a um e apresentados em tela'''
    NOME_ARQ = 'games.dat'
    ENTRADA = open(NOME_ARQ, 'rb')# n preciso do encoding pq é binário, e o encoding é para arquivos de texto, e aqui eu vou ler bytes, entao n preciso do encoding

    if argv[1] == '-b':
        print("Modo de construção de índice")

        lista_inv = []
        indicesec = construir_indice_sec(registros, lista_inv)
        print(indicesec)

        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        indicepri = construir_indice_pri(registros)
        print(indicepri)
        registros = lista_de_registros(ENTRADA)

    elif argv[1] == '-e':
        print("Modo de leitura de arquivo de operações")

        busca_pri("348", indicepri, ENTRADA)
        busca_sec_genero("Action", indicesec[0], lista_inv, ENTRADA)
        busca_sec_publicadora("Electronic Arts", indicesec[1], lista_inv, ENTRADA)

    elif argv[1] == '-c':
        print("Modo compactação do arquivo")

    ENTRADA.close()
'''
def importa_registros(arquivo):
    BUFFER = le_registro(arquivo)
    registros = []

    while BUFFER:
        lista_campos = BUFFER.rstrip('|').split('|')
        registros.append(lista_campos)
        BUFFER = le_registro(arquivo)
    return registros #[[reg1], [reg2], [reg3]]
'''
def le_registro(arquivo):
    tam = arquivo.read(2)

    tam = int.from_bytes(tam, 'little')

    if tam > 0:
        BUFFER = arquivo.read(tam) #se for maior que 0, le o registro, se for 0, n tem mais registro pra ler
        BUFFER = BUFFER.decode('utf-8')
        return BUFFER
    else:
        return ""

#===========CONSTRUIR ÍNDICE ====================

def construir_indice_pri(registros):
    #id (chave) + referencia (byteoffset)
    indice_pri = []

    for reg in registros:
        indice_pri.append([reg[1], reg[0]])

    indice_pri.sort()
    return indice_pri


def lista_de_registros(arquivo):
    BUFFER = le_registro(arquivo)
    lista = []
    byte_off_set = 0

    while BUFFER:
        lista_aux = []
        lista_campos = BUFFER.rstrip('|').split('|')
        lista_aux.append(byte_off_set) #uma tupla com o primeiro elemento da lista campos (id) e byteoffset dele
        for campo in lista_campos:
            lista_aux.append(campo)
        byte_off_set = arquivo.tell() #posição do seek agora
        BUFFER = le_registro(arquivo) #move o seek pro próximo, "incremento"
        lista.append(lista_aux)
    return lista

def construir_indice_sec(registros, lista_inv):
    indice_sec_genero = {}
    index_sec_publicadora = {}

    for i in range(len(registros)):
        genero = registros[i][4]
        publicadora = registros[i][5]
        lista_inv.append([registros[i][0], -1, -1])  # registros[i][0] é o byte_offset 

        if genero not in indice_sec_genero:
            indice_sec_genero[genero] = len(lista_inv) - 1
        else:
            reg = lista_inv[indice_sec_genero[genero]]
            while reg[1] != -1:
                reg = lista_inv[reg[1]]
            reg[1] = len(lista_inv) - 1
        

        if publicadora not in index_sec_publicadora:
            index_sec_publicadora[publicadora] = len(lista_inv) - 1
        else:
            reg = lista_inv[index_sec_publicadora[publicadora]]
            while reg[2] != -1:
                reg = lista_inv[reg[2]]
            reg[2] = len(lista_inv) - 1

    return [indice_sec_genero, index_sec_publicadora]


#================== BUSCA ======================

def busca_binaria(chave, indice_pri): #código da valéria
    esq, dir = 0, len(indice_pri) - 1
    chave = int(chave)
    
    while esq <= dir:
        meio = (esq + dir) // 2
        id_meio = int(indice_pri[meio][0])
        if id_meio == chave:
            return indice_pri[meio][1]
        elif id_meio < chave:
            esq = meio + 1
        else:
            dir = meio - 1
    return -1


def busca_pri(chave, indice_pri, arquivo): #DÚVIDA
    print(f'Busca pelo registro de ID: "{chave}"')

    offset = busca_binaria(chave, indice_pri)

    if offset == -1:
        print("Registro não encontrado")
        return
    
    arquivo.seek(offset) #move o seek para o byte_offset encontrado na binaria
    registro = le_registro(arquivo) #le o registro do byte_offset atual

    if registro.startswith('*'): #remocao logica
        print("Registro não encontrado")
    else:
        print(registro)
    
def busca_sec_genero(chave, indice_sec_genero, lista_inv, arquivo):
    if chave not in indice_sec_genero:
        print("Registro não encontrado")
        return
    
    indice = indice_sec_genero[chave]
    encontrados = []

    while indice != -1: #enquanto tiver um indice válido, aponta para nada (-1)
        offset = lista_inv[indice][0] #pega o byte_offset do registro atual
        arquivo.seek(offset)
        registro = le_registro(arquivo) 

        if not registro.startswith('*'): #se o registro n tiver sido removido logico, add ele na lista de encontrados
            encontrados.append(registro)
        else:
            print("Registro removido")

        indice = lista_inv[indice][1] #pega o próximo indice/reg do mesmo gênero 

    print(f'Busca por registros de gênero "{chave}" ({len(encontrados)} registros)')
    for reg in encontrados:
        print(reg)


def busca_sec_publicadora(chave, indice_sec_publicadora, lista_inv, arquivo):
    if chave not in indice_sec_publicadora:
        print("Registro não encontrado")
        return
    indice = indice_sec_publicadora[chave]
    encontrados = []

    while indice != -1:
        offset = lista_inv[indice][0]
        arquivo.seek(offset)
        registro = le_registro(arquivo)

        if not registro.startswith('*'):
            encontrados.append(registro)
        else:
            print("Registro removido")

        indice = lista_inv[indice][2]

    print(f'Busca por registros de publicadora "{chave}" ({len(encontrados)} registros)')
    for reg in encontrados:
        print(reg)


#================INSERCAO =================

def insercao(chave, num_bytes):
    print(f'Inserção do registro de chave "{chave}" ({num_bytes} bytes)')



#================REMOCAO==================

def remocao(chave, offset):
    print(f'Remoção do registro de chave "{chave}" (offset = {offset})')

#================COMPACTACAO===============

def compactacao():
    pass

if __name__ == "__main__":
    main()


#O QUE FALTA
'''
Argumentos da linha de comando (-b, -e, -c)
Gravar os índices em arquivos (primario.ind, genero.ind, publicadora.ind, listaInvertida.lst)
Arquivo de operações
Inserção
Remoção
Compactação
Sobrescrever índices no -b
Persistência dos índices no -e
Falta ignorar removidos na construção dos índices no -b
Estrutura dos arquivos de índice
Tratamento obrigatório quando índices não existirem
Ver se vai utilizar o struct e busca binária
'''