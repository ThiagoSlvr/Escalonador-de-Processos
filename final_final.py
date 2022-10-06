#encoding: utf-8
#Thiago Silvera - 110668, Nicolas Daltrozo - 112871
#COMO EXECUTAR: deve haver um arquivo "entrada.txt" na mesma pasta do código, a função main vai abrir o arquivo e analisar qual o tipo de escalonamento no arquivo e executar-lo
#Para criar um novo processo durante a execução, basta escrever ou colar o processo no formato padrão e pressionar enter

#Primeiramente importamos as livrarias que vamos utilizar
import time
from operator import itemgetter
import random
import threading

#Definimos algumas variaveis globais para a utilização nas threads
global Novo_Input
Novo_Input = None
global fim

'''Começo Round_Robin'''

#A função input é utilizada para ler, formatar e transformar o texto de entrada em um array manipulavel com os tipos de variaveis corretas
#Nesse caso, ela tambem pega o quantum que é o periodo que o processo vai ficar na CPU
def Input():																							
	f = open("entrada.txt", "r")
	txt = f.readlines()														
	f.close()
	cont = 0
	while (cont<len(txt)):						
		txt[cont] = txt[cont].split("|")
		cont = cont + 1
	cont = 1
	while (cont<(len(txt))):									
		for i in range(1, 5):
			txt[cont][i] = int(txt[cont][i])
		cont = cont + 1
	quantum = int(txt[0][1])
	return txt, quantum										

#Aqui temos a função principal do escalonamento, utilizando a variavel rr para definir de quem é a vez na CPU e o q_cont para saber se uma rodada ja foi completa
#clock é um simples contador para ver os passos, "a" é o array de entrada
#Há um print mostrando qual processo está sendo executado e quanto tempo resta para sua finalização
#Se um processo for utilizado o número de vezes que foi pedido, ele é retirado do array e um print informa que ele foi finalizado
#No final ele retorna tudo de volta para que, caso seja necessario, executar novamente
def Loop_Round_Robin(clock, a, quantum, rr, q_cont):													
	if (len(a) > 0):																		
		if (rr >= len(a)):																		
			rr = 1
		print ("Clock %d, Processo %s, PID %d, UID %d, Tempo Restante %s" % (clock, a[rr][0], a[rr][1], a[rr][4], a[rr][2]))																	
		a[rr][2] = a[rr][2]-1														
		q_cont = q_cont + 1																			
		if (a[rr][2] == 0):															
			print ("Clock %d, Processo %s, PID %d, UID %d, Finalizado" % (clock, a[rr][0], a[rr][1], a[rr][4]))						
			a.pop(rr)
			q_cont = 0
		if (q_cont >= quantum):																			
			rr = rr + 1
			q_cont = 0
		time.sleep(0.2)
		return clock, a, rr, q_cont															
	else:																								
		return clock, a, rr, q_cont

#Aqui tanto o loop do Round Robin, quanto sua inicialização e definição de variaveis
#Também recebemos o input durante a execução, onde ele vai transforma-lo em um inteiro para manipulação futura
#Há o loop do Round Robin, onde é chamada a função acima, e onde o clocl é incrementado
#Por final, utilizamos a variavel end para definir se o escalonador já executou todos processos e a variavel fim para finalizar a thread de input
def Round_Robin():
    a, quantum = Input()
    end = False
    global fim
    clock = 1
    rr = 1
    q_cont = 0
    global Novo_Input
    Novo_Input = None
    while (end != True):
        if (Novo_Input != None):
            for cont in range(1, 5):
                Novo_Input[cont] = (int(Novo_Input[cont]))
            a.append(Novo_Input)
            Novo_Input = None
        clock, a, rr, q_cont = Loop_Round_Robin(clock, a, quantum, rr, q_cont)
        clock = clock + 1
        if (len(a)==1):
            end = True
    fim = True


'''Final Round Robin --- Começo Prioridade'''

#Prioridade: Esta funçao de escalonador ocorre de forma que abre o arquivo, separa por linhas e depois separa de novo por "|" fazendo assim um array. 
#O primeiro elemento da lista se encontra o nome do escalonador e o quantum, portanto se exclui esta informaçao, 
# logo em seguida organiza-se a lista por nivel de prioridade onde 100 é o mais importante e 1 o menos,
# logo após, é realizado os processos em ordem, onde realiza-se todo o primeiro processo por total 
# Após, retira-se este processo da lista e pula para o proximo. Durante esta execuçao a funçao verifica se não há novas entradas. Caso haja é adicionada na lista de processos e 
# organizada novamente conforme suas prioridades. 
# Este processo ocorre ate o fim do programa onde quando acaba os processos, não se pode adicionar novos processos.
def Prioridade():
	global fim
	global Novo_Input
	entrada=open ('entrada.txt' , 'r')
	processos=entrada.read()
	processos=processos.split("\n")
	processos.pop()
	Novo_Input = 0
	x=0
	while x<len(processos):
		processos[x]=processos[x].split("|")
		x=x+1

	processos.pop(0)

	x=0
	while x<len(processos):
		processos[x][2]=int(processos[x][2])
		processos[x][3]=int(processos[x][3])
		x=x+1
	processos=sorted(processos, key=itemgetter(3), reverse=True)
	print (processos)
	while len(processos):
		while processos[0][2]>=0:
			print(processos[0][0] + " falta: "+ str(processos[0][2]))
			processos[0][2]=processos[0][2]-1
			time.sleep(0.2)
		processos.pop(0)
		if Novo_Input != 0:
			Novo_Input[2]=int(Novo_Input[2])
			Novo_Input[3]=int(Novo_Input[3])
			processos.append(Novo_Input)
			processos=sorted(processos, key=itemgetter(3), reverse=True)
			print (processos)
			Novo_Input = 0

	fim = True
	entrada.close()


'''Final Prioridade --- Começo Loteria'''

#Função executa é a forma de execução do loteria, onde ocorre o funcionamento do escalonador
#Recebe as informações de um processo, como pid, nome, bilhetes e quantum
#Por final, ele printa qual processo foi executado e quanto tempo falta para sua finalização
def executa (pid, processos, bilhetes, quantum):
	try:
		ind = processos.index(next(proc for proc in processos if proc[1]==pid))
	except StopIteration:
		print ("Processo nao encontrado!!!!!!")
		return
	for i in range(quantum):
		time.sleep(0.2)
		if processos[ind][2]:
			print(processos[ind][0] + " falta: "+ str(processos[ind][2]))
			processos[ind][2]=processos[ind][2]-1
		else:
			print(processos[ind][0] + " falta: "+ str(processos[ind][2]))
			for i in [bilhetes.index(x) for x in bilhetes if x==pid]:
				bilhetes.pop(i)
			processos.pop(ind)
			break

#Loteria: Nesta funçao le-se a entrada, separa por linhas, depois separa novamente por "|". 
# Logo após se cria uma lista bilhetes, onde nela são armazenadas os id's de cada processo n, vezes sendo n a quantidade de bilhetes de cada processo. 
# Logo apos é feito um sorteio e o sorteado é executado, executa o numero de quantums e em seguida é sorteado outro numero, e durante esta execuçao é verificado 
# se não há novas entradas, caso tenha, se coloca na lista bilhetes o id do novo processo n vezes, e é sorteado novos id's para serem executados ate o fim da funçao.
def Loteria():
	global fim
	global Novo_Input
	Novo_Input = 0
	pid=1
	tempo=2
	bilhete=3
	entrada=open ('loteria.txt' , 'r')
	processos=entrada.read()
	processos=processos.split("\n")
	processos.pop()
	x=0
	while x<len(processos):
		processos[x]=processos[x].split("|")
		x=x+1
	quantum = int(processos[0][1])
	processos.pop(0)
	x=0
	while x<len(processos):
		processos[x][tempo]=int(processos[x][tempo])
		processos[x][bilhete]=int(processos[x][bilhete])
		x=x+1
	bilhetes=[]
	x=0
	while x<len(processos):
		y=0
		while y<processos[x][bilhete]:
			bilhetes.append(processos[x][pid])
			y=y+1
		x=x+1
	x=0
	while len(processos):
		sorteado=bilhetes[random.randint(0, len(bilhetes)-1)]
		executa(sorteado, processos, bilhetes, quantum)
		if Novo_Input != 0:
			Novo_Input[2]=int(Novo_Input[2])
			Novo_Input[3]=int(Novo_Input[3])
			y=0
			while y<Novo_Input[bilhete]:
				bilhetes.append(Novo_Input[pid])
				y=y+1
			processos.append(Novo_Input)
			Novo_Input = 0
	fim = True

'''Final Prioridade --- Começo Main'''

#Função utilizado com a segunda thread para que ocorra o input simultaneo com a execução do escalonador
#Utilizamos duas variaveis globais que vão ser utilizadas em todas as função de escalonação
#Ela também formata a entrada de forma que facilite sua futura manipulação
def t2_input():
    global Novo_Input
    global fim
    fim = False
    while (fim != True):
        Novo_Input = input()
        Novo_Input = Novo_Input.split("|")

#Função main, primeiramente ela le a entrada e identifica qual o tipo de escalonador que é requerida, além de formata-la para futura utilização
#Também é criado duas threads, t1 será utilizada para a execução do escalonador escolhido, enquanto a segunda aguarda um input durante a execução
def main():
    a = open("entrada.txt", "r")
    txt = a.readlines()
    a.close()
    cont = 0
    while (cont<len(txt)):
        txt[cont] = txt[cont].split("|")
        cont = cont + 1
    x = str(txt[0][0])
    t2 = threading.Thread(target=t2_input)
    t2.start()
    if (x == "alternanciaCircular"):
        t1 = threading.Thread(target=Round_Robin)
        t1.start()
        exit()
    elif (x == "prioridade"):
        t1 = threading.Thread(target=Prioridade)
        t1.start()
        exit()
    elif (x == "loteria"):
        t1 = threading.Thread(target=Loteria)
        t1.start()
        exit()
    else:
        print("Input Incorreto")
        exit()


main()