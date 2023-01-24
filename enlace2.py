import serial #biblioteca pyserial para comunicação através da porta serial
import base64 #biblioteca para codificação em base64, assim conseguimos transformar qualquer coisa em string em strings


# abre um arquivo do computador e salva seu conteudo na variável Data de maneira já encodada em base64
with open("teste.png", "rb") as file:
    Data = base64.b64encode(file.read())

# verifica o tamanho do arquivo em "bytes", nesse caso quantidade de caracteres
print(len(Data))

#inicia comunicação com a porta serial
ser = serial.Serial('/dev/ttyS0', timeout=1)  # open serial port

#Data = 'Lorem Ipsum is simply dummy text of the printing' #and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'



# inicia o contador de iterações de envios de pacotes
i = 0
# inicia o contador de tentativas
tries = 0




# inicia uma variável em binário para concatenar nossas respostas e depois decodar ela
response = b''

if Data:

    # inicia uma lista para salvar os pacotes organizados em ordem
    packages = []
    # define o tamanho de cada pacote
    N = 1000
    # a cada N caracteres adiciona a porção da string referente ao caractere i até o i+n na lista packages
    for i in range(0, len(str(Data)), N): #é necessário usar o conversor para string pois o python transforma o conteudo pra bytes automaticamente
        packages.append(Data[i:i+N])
   
    # adiciona um finalizador aos pacotes, assim ambos computadores sabem q a entrega foi sucedida
    packages.append(b'$')

    while i < len(packages):
        # envia um pacote (criado anteriormente) concatenado com um \n em bytes para mostrar que é o fim do pacote
        ser.write(packages[i]+b'\n')

        confBytes = ser.readline()   # le a resposta do outro computador

        if packages[i]+b'\n' == confBytes: # verifica se o enviado é igual a resposta, se for verdadeiro vai para o próximo pacote, caso contrario envia o mesmo pacote novamente e adicona as tentativas
            i += 1
            print(f'Pacote enviado {i}') 
            if confBytes == b'$': # se receber $ termina a transmissão
                print('Transmissão concluída com sucesso!')
        else:
            tries += 1
            print('Erro na transmissão')

        # se chegar em 500 tentativas ele desiste
        if tries > 500:
            print('Limite de tentativas atingido! Encerrando transmissão')
            break

# caso não tenha dado para ser enviado ele escuta a porta serial para receber os dados
else:
    while(True):
        # espera até receber um pacote
        sBytes = ser.readline()

        # envia o q foi recebido de volta para realizar teste
        ser.write(sBytes)

        # se for o caractere finalizador de envio ele interrompe o laço,
        if(sBytes == b'$'):
            print('Envio Finalizado')
            break

        # ele junta todos os pacotes novamente para recuperar a informação, ignorando o \n de cada pacote
        response = response + sBytes[0:-1]   

    print(b"String transferida: " + response)

    # salva o arquivo recebido na mesma pasta q a execução do código
    with open("gubert-enviado.jpg", 'wb') as file:
        file.write(base64.b64decode(response))