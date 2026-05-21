def construir_indice_pri(registros):
    #id (chave) + referencia (byteoffset)
    indice_pri = [] #lista de listas, onde cada lista tem o ID do jogo e o byteoffset do registro correspondente no arquivo de dados

    for reg in registros: #para cada jogo, reg[1] é o ID do jogo e reg[0] é o byteoffset
        indice_pri.append([reg[1], reg[0]])

    indice_pri.sort() #ordena a lista de listas pelo ID do jogo (chave), para a busca binária (obrigatório ser ordenado)
    return indice_pri #retorna a lista de listas, cada lista tem o ID do jogo e o byteoffset do registro correspondente no arquivo de dados

def construir_indice_sec(registros, lista_inv):
    indice_sec_genero = {} 
    index_sec_publicadora = {}
    #cria dois dicionários para os índices secundários, onde a chave é o gênero ou a publicadora e o valor é o índice do primeiro registro na lista de índices invertidos (lista_inv) que tem aquele gênero ou publicadora

    for i in range(len(registros)):
        genero = registros[i][4] #registros[i][4] é o gênero do jogo
        publicadora = registros[i][5] #registros[i][5] é a publicadora do jogo
        chave_pri = registros[i][1] # registros[i][1] é o ID do jogo
        lista_inv.append([chave_pri, -1, -1]) #adiciona o ID do jogo, o índice do próximo registro com o mesmo gênero e o índice do próximo registro com a mesma publicadora na lista de índices invertidos (lista_inv)
        #-1 para indicar que não tem próximo reg (aponta para nada)

        atualiza_lst_inv_index_sec(genero, indice_sec_genero, lista_inv, 1) #atualiza o índice secundário de gênero, passando o gênero do jogo, o dicionário do índice secundário de gênero, a lista de índices invertidos e a coluna da lista de índices invertidos que aponta para o próximo registro com o mesmo gênero (1)
        atualiza_lst_inv_index_sec(publicadora, index_sec_publicadora, lista_inv, 2) #atualiza o índice secundário de publicadora, passando a publicadora do jogo, o dicionário do índice secundário de publicadora, a lista de índices invertidos e a coluna da lista de índices invertidos que aponta para o próximo registro com a mesma publicadora (2)

    return [indice_sec_genero, index_sec_publicadora] #retorna uma lista com os dois dicionários, onde cada um tem a chave e o valor do índice do primeiro registro na lista de índices invertidos (lista_inv) que tem aquele gênero ou publicadora

def atualiza_lst_inv_index_sec(chave, index_sec, lst_inv, lst_inv_coluna):
        #coluna 1 para gênero e coluna 2 para publicadora
        if chave not in index_sec: #se a chave não estiver no dicionário do índice secundário, aponta index_sec[chave] para o índice do último registro adicionado na lista de índices invertidos (lista_inv), que é len(lista_inv) - 1
            index_sec[chave] = len(lst_inv) - 1
        else:
            reg = lst_inv[index_sec[chave]] #reg é o registro na lista de índices invertidos (lista_inv) que tem a chave do índice secundário (gênero ou publicadora) que estamos atualizando, ou seja, o primeiro registro com aquele gênero ou publicadora
            while reg[lst_inv_coluna] != -1: #enquanto o índice do próximo registro com o mesmo gênero ou publicadora for diferente de -1
                reg = lst_inv[reg[lst_inv_coluna]] #percorre a cadeia de ponteiros daquela chave até encontrar o último(-1)
            reg[lst_inv_coluna] = len(lst_inv) - 1 #faz esse nó apontar para o novo elemento 

            #late binding -> o índice secundário aponta para o primeiro, e cada nozinho aponta pro próximo com o mesmo gênero/publicadora