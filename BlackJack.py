# BlackJack 1.0
#Sujeito a melhorias futuras / May have future implements
#Meu segundo projeto do curso de python / My second python course project

from random import shuffle
naipes = ("Espadas","Copas","Paus","Ouros")
rank = ("Dois","Tres","Quatro","Cinco","Seis","Sete","Oito","Nove","Dez","Valete","Dama","Rei","Ás")
valores = {"Dois":2,"Tres":3,"Quatro":4,"Cinco":5,"Seis":6,"Sete":7,"Oito":8,"Nove":9,"Dez":10,"Valete":10,"Dama":10,"Rei":10,"Ás":11}

#Criação das Cartas / Card creation
class Carta:
    def __init__(self,rank,naipe):
        self.rank = rank
        self.naipe = naipe
        self.valor = valores[rank]
    def __str__(self):
        return self.rank + " D. " + self.naipe

#Criação de um baralho com 52 Cartas únicas / Deck creation with 52 unic cards
#Esse é o baralho "ja definido"! / This is the "predefined" deck!
class Baralho:

    def __init__(self):

        self.todas_as_cartas = []

        for naipe in naipes:
            for numero in rank:
                carta_criada = Carta(numero,naipe)

                self.todas_as_cartas.append(carta_criada)

    def embaralhar(self):
        shuffle(self.todas_as_cartas)

    def vender_carta(self):
        return self.todas_as_cartas.pop()
    
#Sistema de banco para as apostas no jogo / Bank system for the bet in the game
class Banco:
    def __init__(self):
        
        self.saldo = int(input("Quantas moedinhas você quer comprar? : "))
        self.aposta = int(input("Quantas moedinhas você quer apostar? : "))

        if self.saldo < self.aposta :              
            self.aposta = int(input("Você não tem tantas moedinhas, abaixa a bola ai: "))
        
    def perder_aposta(self):
        self.saldo -= self.aposta
    def ganhar_aposta(self):
        self.saldo += self.aposta

#Criação de um 'baralho' a parte por meio do outro baralho ja definido / Creation of a separete "deck" using the predefined one
class Mão:
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.ases = 0
    
    #Adiciona uma carta à mão / Add one card to the hand
    def ganhar_carta(self,carta):
        self.cartas.append(carta)
        self.valor += valores[carta.rank]
        if carta.rank == 'Ás':
            self.ases += 1
    #Tomada de decisão automática em relação ao valor do Ás / Automatic decision making about the ace value   
    # Pode ser onze ou um / It can be eleven or one
    def arrumando_ases(self):
        while self.valor > 21 and self.ases:
            self.valor -= 10
            self.ases -= 1
        
#Função de jogada, que no caso é comprar uma carta / Play function, in the case the play is to buy one card 
def jogada(novo_deck,lista_mão,user):
    carta_comprada = novo_deck.vender_carta()
    lista_mão.append(str(carta_comprada))
    user.ganhar_carta(carta_comprada)
    user.arrumando_ases()
    print(lista_mão)

#Parte do código que roda apenas uma vez / Part of the code that runs once
#Definição de variaveis e coisas unicas fora do loop / Variables definitions and unic things outside the loop
sim = ["Sim", "s", "S", "SIM", "sim","YES","yes","y","Yes","sIM"]
nao = ["Não", "Nao", "nao", "não", "n", "N","NO","no","No","nAO"]
menu1 = '''
|=====================================|
|        Bem vindo ao BlackJack       |
|                                     |
'''
print(menu1)
pacto = input("Você quer jogar um jogo?? :) ")
banco = Banco()

#Loop
try:
    while sim.index(pacto):
        #Criação das listas de mão / Hand list creation
        lista_mão_jogador = []
        lista_mão_dealer = []
        
        #Cria e embaralha um novo baralho / Creates and shuffles a new deck
        novo_deck = Baralho()
        novo_deck.embaralhar()
        
        #Criação dos "Jogadores" / "Players" creation
        player1 = Mão()
        dealer = Mão()
        
        #Valor da aposta para ser perguntada depois da primeira rodada / Question for the bet value after the first turn
        if banco.aposta == 0:
            banco.aposta = int(input("Quantas moedinhas você quer apostar? : "))
        else:
            pass

        #Criação da mão de inicio do jogo (2 cartas para cada) / Inicial hand creation (2 cards for each)
        #Para a Casa (dealer) / To de House (dealer)
        for i in range(2):
            carta_comprada = novo_deck.vender_carta()
            lista_mão_dealer.append(str(carta_comprada))
            dealer.ganhar_carta(carta_comprada)
            dealer.arrumando_ases()
        print(f'Mão da Casa:\n {lista_mão_dealer[0]}, Carta Oculta')
        
        #Para o player / for the player
        for i in range(2):
            carta_comprada = novo_deck.vender_carta()
            lista_mão_jogador.append(str(carta_comprada))
            player1.ganhar_carta(carta_comprada)
            player1.arrumando_ases()
        print(f'Sua mão:\n {lista_mão_jogador}')
        
        #Escolha da rodada / Turn choice
        escolha = input("Vai comprar ou passar? c/p: ")
        
        if escolha in ('c','C','comprar','Comprar'):
            print('Mão da Casa:')
            #tomada de decisão para o computador / Automatic decision for the computer
            if dealer.valor < 17:
                jogada(novo_deck, lista_mão_dealer, dealer)
            else:
                print(lista_mão_dealer)

            print('Sua mão:')
            jogada(novo_deck, lista_mão_jogador, player1)

            #Condicionais de vitoria/ derrota // Victory/ Deafeat condicions
            if dealer.valor > 21:
                print('Ganhou')
                banco.ganhar_aposta()
                print('Ganhou {} moedinhas! Saldo atual igual a {}'.format(banco.aposta, banco.saldo))
                
            elif player1.valor > 21:
                print('Perdeu meu fi')
                banco.perder_aposta()
                print(f'Perdeu {banco.aposta} moedinhas !! Saldo atual igual a {banco.saldo} burro')
                
            else:
                if player1.valor > dealer.valor:
                    print("Parabens, ganhou!")
                    banco.ganhar_aposta()
                    print('Ganhou {} moedinhas! Saldo atual igual a {}'.format(banco.aposta, banco.saldo))
                    
                elif dealer.valor > player1.valor:
                    print('Perdeu meu fi')
                    banco.perder_aposta()
                    print(f'Perdeu {banco.aposta} moedinhas !! Saldo atual igual a {banco.saldo} burro')
                    
                elif player1.valor == dealer.valor:
                    print("Vixi, impato")
                    

        elif escolha in ('p', 'P','Passar','passar'):
            #tomada de decisão para o computador / Automatic decision for the computer
            print('Mão da Casa:')
            if dealer.valor < 17:
                jogada(novo_deck, lista_mão_dealer, dealer)
            else:
                print(lista_mão_dealer)

            print(f'Sua mão:\n {lista_mão_jogador}')

            #Condicionais de vitória/derrota // Victory/ Deafeat condicions
            if dealer.valor > 21:
                print('Ganhou')
                banco.ganhar_aposta()
                print('Ganhou {} moedinhas! Saldo atual igual a {}'.format(banco.aposta, banco.saldo))
                
            elif player1.valor > 21:
                print('Perdeu meu fi')
                banco.perder_aposta()
                print(f'Perdeu {banco.aposta} moedinhas !! Saldo atual igual a {banco.saldo} burro')
                
            else:
                if player1.valor > dealer.valor:
                    print("Parabens, ganhou!")
                    banco.ganhar_aposta()
                    print('Ganhou {} moedinhas! Saldo atual igual a {}'.format(banco.aposta, banco.saldo))
                    
                elif dealer.valor > player1.valor:
                    print('Perdeu meu fi')
                    banco.perder_aposta()
                    print(f'Perdeu {banco.aposta} moedinhas !!  Saldo atual igual a {banco.saldo} burro')
                    
                elif player1.valor == dealer.valor:
                    print("Vixi, impato")
        #Reset do valor da aposta após cada rodada / Bet value reset after each round       
            #Para q seja redefinida pelo jogador / To be redefined by the player
        banco.aposta = 0
        
        #Continuar ou parar o loop / Continue or break the loop
        pacto = input("Quer continuar com o jogo? :)")
        try:
            if sim.index(pacto):
                continue
        except ValueError:
            if nao.index(pacto):
                print('Obrigado por jogar :)')
                break
#Catch para caso algum erro na entrada / Catch for an error on the input
except ValueError:
    print("Pedido invalido :)")