def lista_de_registros(arquivo):
    lista = []

    byte_off_set = arquivo.tell()
    BUFFER = le_registro(arquivo)

    while BUFFER:
        if BUFFER[0] != '*':
            lista_campos = BUFFER.rstrip('|').split('|')
            lista_aux = [byte_off_set, int(lista_campos[0])] + lista_campos[1:]
            lista.append(lista_aux)

        byte_off_set = arquivo.tell()
        BUFFER = le_registro(arquivo) #move o seek pro próximo, "incremento"
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