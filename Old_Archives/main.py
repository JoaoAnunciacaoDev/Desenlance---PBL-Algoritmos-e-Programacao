from Old_Archives.funcoes import Entrada_Texto, Quantidade_Partidas, Escolha_palavra, Unicode_letras_certas, Resultado, Pontuação, Limpar_Terminal  

fim_cor = '\033[0;0m'
letra_local_errado = '\033[91m'      
letra_local_correto = '\033[92m'

jogador_1 = input('Nome do Jogador_1: ')
jogador_2 = input('Nome do Jogador_2: ')

texto = Entrada_Texto()

n_partidas = Quantidade_Partidas(texto)

Limpar_Terminal()

vez_1 = True
pontos_1 = 0
pontos_2 = 0

while n_partidas > 0:  
    tentativas_1 = 6  
    tentativas_2 = 6  
    palavra_escolhida, letras_certas, texto = Escolha_palavra(texto)  

    while vez_1 == True:  

        tentativa_jogador_1 = input(f'\n{jogador_1}, insira uma palavra: \n')  
        tentativa_jogador_1 = Unicode_letras_certas(tentativa_jogador_1)  

        if len(tentativa_jogador_1) != 5:  
            print('Insira uma palavra de 5 letras, por favor.')  
            continue  
        elif not tentativa_jogador_1.isalpha():  
            print('A palavra deve conter apenas letras.')  
            continue  
        
        tentativa_jogador_1 = list(tentativa_jogador_1)  
        contador = 0  
        letras_tentativas = []  

        for letra in tentativa_jogador_1:  
            letras_tentativas.append(letra)  

            if letra not in letras_certas:  
                letras_tentativas[contador] = letras_tentativas[contador]

            elif letra == letras_certas[contador]:  
                letras_tentativas[contador] = letra_local_correto + letras_tentativas[contador] + fim_cor

            else:  
                letras_tentativas[contador] = letra_local_errado + letras_tentativas[contador] + fim_cor

            print(letras_tentativas[contador], end='')  
            contador += 1  
                
        if tentativa_jogador_1 == letras_certas:  

            print(f'\nParabéns {jogador_1}, você ganhou essa rodada!\nA resposta era: {palavra_escolhida}.')  

            ponto_rodada_1 = Pontuação(tentativas_1)  
            pontos_1 += ponto_rodada_1  
            print(f'Você ganhou {ponto_rodada_1} pontos, com {tentativas_1} tentativas restantes.')  

            vez_1 = False  
            texto.remove(palavra_escolhida)  
            
        else:
            tentativas_1 -= 1  
            
        if tentativas_1 == 0 and tentativa_jogador_1 != letras_certas:  
            print(f'\n{jogador_1}, você perdeu a rodada.\nA resposta era {palavra_escolhida}.')  
            vez_1 = False  
            texto.remove(palavra_escolhida)  

    if vez_1 == False:  

        palavra_escolhida, letras_certas, texto = Escolha_palavra(texto)  

        while True:  

            tentativa_jogador_2 = input(f'\n{jogador_2}, insira uma palavra: \n')  
            tentativa_jogador_2 = Unicode_letras_certas(tentativa_jogador_2)  

            if len(tentativa_jogador_2) != 5:  
                print('Insira uma palavra de 5 letras, por favor.')  
                continue  
            elif not tentativa_jogador_2.isalpha():  
                print('A palavra deve conter apenas letras.')  
                continue  
        
            tentativa_jogador_2 = list(tentativa_jogador_2)  
            contador = 0  
            letras_tentativas = []  

            for letra in tentativa_jogador_2:  
                letras_tentativas.append(letra)  

                if letra not in letras_certas:  
                    letras_tentativas[contador] = letras_tentativas[contador]

                elif letra == letras_certas[contador]:  
                    letras_tentativas[contador] = letra_local_correto + letras_tentativas[contador] + fim_cor

                else:  
                    letras_tentativas[contador] = letra_local_errado + letras_tentativas[contador] + fim_cor

                print(letras_tentativas[contador], end='')  
                contador += 1  
                
            if tentativa_jogador_2 == letras_certas:  

                print(f'\nParabéns {jogador_2}, você ganhou essaa rodada! A resposta era: {palavra_escolhida}.')  

                ponto_rodada_2 = Pontuação(tentativas_2)  
                pontos_2 += ponto_rodada_2  

                print(f'Você ganhou {ponto_rodada_2} pontos, com {tentativas_2} tentativas restantes.')  
                print(f'\n{jogador_1} tem {pontos_1} ponto(s), e {jogador_2} tem {pontos_2} ponto(s).')
                vez_1 = True  
                n_partidas -= 1  
                texto.remove(palavra_escolhida)  
                break  
            else:
                tentativas_2 -= 1  
             
            if tentativas_2 == 0 and tentativa_jogador_2 != letras_certas:
                print(f'\n{jogador_2}, você perdeu a rodada.\nA resposta era {palavra_escolhida}.')
                print(f'\n{jogador_1} tem {pontos_1} ponto(s), e {jogador_2} tem {pontos_2} ponto(s).')
                vez_1 = True
                n_partidas -= 1
                texto.remove(palavra_escolhida)
                break

Resultado(jogador_1, jogador_2, n_partidas, pontos_1, pontos_2)