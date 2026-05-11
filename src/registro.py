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

def le_registro(arquivo):
    tam = arquivo.read(2)

    if len(tam) < 2:  # EOF
        return ""

    tam = int.from_bytes(tam, 'little')

    if tam > 0:
        BUFFER = arquivo.read(tam) #se for maior que 0, le o registro, se for 0, n tem mais registro pra ler
        BUFFER = BUFFER.decode('utf-8')
        return BUFFER
    
    return ""