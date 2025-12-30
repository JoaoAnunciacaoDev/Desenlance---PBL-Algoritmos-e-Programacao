import re, unicodedata, random, os  

def Entrada_Texto():  
    texto = input('Insira um texto: ')  
    texto = re.sub(r'[^\w]',' ', texto)  
    texto = texto.split(' ')  
    contador = 0  
    for palavra in range(len(texto)):  
        if len(texto[contador]) != 5 or not texto[contador].isalpha:  
            texto.remove(texto[contador])  
        else:  
            contador += 1  
    if len(texto) < 4:  
        print('Palavras insuficientes.')  
        exit()  
    return texto  

def Quantidade_Partidas(texto):  
    while True:  

        n_partidas = input('Insira um número par de partidas: ')  
        if not n_partidas.isnumeric():  
            print('Insira um número inteiro, por favor')  
            continue  
        else: 
            n_partidas = int(n_partidas)  

        if len(texto) < (n_partidas * 2):  
            print('Palavras insuficientes para o número de partidas.')  
            Entrada_Texto()  

        elif not n_partidas % 2 == 0:  
            print('Por favor, insira um número PAR de partidas.')  
            continue  
        else: 
            break  

    return n_partidas  

def Escolha_palavra(texto):  
    texto = Remover_repetidos(texto)  
    palavra_escolhida = random.choice(texto)  
    letras_certas = palavra_escolhida  
    letras_certas = Unicode_letras_certas(letras_certas)  
    letras_certas = list(letras_certas)  
    return palavra_escolhida, letras_certas, texto  

def Unicode_letras_certas(string: str) -> str:  
    normalized = unicodedata.normalize('NFD', string)
    palavra_semacento = normalized.encode('ascii', 'ignore').decode('utf8').upper()
    return palavra_semacento

def Resultado(jogador_1, jogador_2, n_partidas, pontos_1, pontos_2):  
    if n_partidas == 0:  
        if pontos_1 > pontos_2:  
            print(f'{jogador_1} venceu o Jogo com {pontos_1} pontos!\n')  
            print('Fim') 
        elif pontos_2 > pontos_1:  
            print(f'{jogador_2} venceu o Jogo com {pontos_2} pontos!\n')  
            print('Fim')
        else:  
            print(f'O jogo empatou com {pontos_1} ponto(s) para cada.\n')  
            print('Fim')

def Remover_repetidos(texto):  
    texto = [elemento.upper() for elemento in texto]  
    não_repetidos = []  
    for palavra in texto:  
        if palavra not in não_repetidos:  
            não_repetidos.append(palavra)  
    return(não_repetidos)   

def Pontuação(tentativas):  
    if tentativas == 6:  
        pontos = 120
    elif tentativas == 5:  
        pontos = 100
    elif tentativas == 4:  
        pontos = 80
    elif tentativas == 3:  
        pontos = 60
    elif tentativas == 2:  
        pontos = 40
    elif tentativas == 1:  
        pontos = 20
    else:  
        pontos = 0
    return pontos  

def Limpar_Terminal():  
    os.system('cls') 