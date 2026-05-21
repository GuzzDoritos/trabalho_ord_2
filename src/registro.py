def lista_de_registros(arquivo):
    lista = []

    byte_off_set = arquivo.tell() #posição atual do ponteiro, ou seja, o byte onde começa o registro
    BUFFER = le_registro(arquivo) #le o reg e move o o ponteiro pro próximo

    while BUFFER: #enquanto tiver registro pra ler, enquanto o BUFFER n for vazio
        if BUFFER[0] != '*': #para cada reg (sem ser removido logicamente)
            lista_campos = BUFFER.rstrip('|').split('|') #rstrip pra tirar o | do final da string  e split pra separar os campos em uma lista
            lista_aux = [byte_off_set, int(lista_campos[0])] + lista_campos[1:] #lista_aux é a lista que vai ser adicionada na lista de registros, ela tem o byte_off_set, o ID do jogo e os outros campos do jogo 
            lista.append(lista_aux) #adiciona a lista_aux na lista de registros -> a lista de registros é uma lista de listas

        byte_off_set = arquivo.tell() #atualiza o byte_off_set para a posição do próximo registro, ou seja, o byte onde começa o próximo registro
        BUFFER = le_registro(arquivo) #le o reg e move o seek pro próximo, "incremento"
    return lista

def le_registro(arquivo):
    tam = arquivo.read(2) #le os 2 bytes do tamanho do registro e move o ponteiro para o próximo campo do registro

    if len(tam) < 2:  # EOF
        return ""

    tam = int.from_bytes(tam, 'little') #from_bytes = bytes para int e armazena o tamanho do registro em tam

    if tam > 0: #se for maior que 0, le o registro, se for 0, n tem mais registro pra ler
        BUFFER = arquivo.read(tam) #le o registro e move o ponteiro para o próximo registro
        BUFFER = BUFFER.decode('utf-8') #decode = bytes para string e armazena o registro em BUFFER
        return BUFFER #retorna o registro lido (string)
    
    return "" #se tam for 0, retorna uma string vazia, ou seja, n tem mais registro pra ler