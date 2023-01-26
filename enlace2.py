import serial #biblioteca pyserial para comunicação através da porta serial
import base64 #biblioteca para codificação em base64, assim conseguimos transformar qualquer coisa em string em strings

#inicia comunicação com a porta serial
ser = serial.Serial('/dev/ttyS0', timeout=1)  # open serial port

print('''Digite o número referente a ação que você deseja realizar.
Enviar: 1
Receber: 2
''')

choice = input()

# abre um arquivo do computador e salva seu conteudo na variável Data de maneira já encodada em base64
if choice == '1':

    print('Digite o nome do arquivo que deseja receber com a extensão dele')
    fileName = input()

    try:
        with open(fileName, "rb") as file:
            Data = base64.b64encode(file.read())
    except:
        print('Arquivo inexistente.')

    # verifica o tamanho do arquivo em "bytes", nesse caso quantidade de caracteres
    print(len(Data))

    # inicia o contador de iterações de envios de pacotes
    i = 0
    # inicia o contador de tentativas
    tries = 0

    # inicia uma variável em binário para concatenar nossas respostas e depois decodar ela
    response = b''


    # inicia uma lista para salvar os pacotes organizados em ordem
    packages = []

    packages.append(str.encode(fileName))
    # define o tamanho de cada pacote
    N = 250
    # a cada N caracteres adiciona a porção da string referente ao caractere i até o i+n na lista packages
    for i in range(0, len(str(Data)), N): #é necessário usar o conversor para string pois o python transforma o conteudo pra bytes automaticamente
        packages.append(Data[i:i+N])
   
    # adiciona um finalizador aos pacotes, assim ambos computadores sabem q a entrega foi sucedida
    packages.append(b'$')
    i=0
    print(len(packages), i)
    
    while i < len(packages):
        print(f'Enviando pacote {i}/{len(packages)}')
        # envia um pacote (criado anteriormente) concatenado com um \n em bytes para mostrar que é o fim do pacote
        framedPackage = str.encode(str(i))+b'--'+packages[i]+b'\n'
        
        ser.write(framedPackage)

        confBytes = ser.readline()   # le a resposta do outro computador
        
        if framedPackage == confBytes: # verifica se o enviado é igual a resposta, se for verdadeiro vai para o próximo pacote, caso contrario envia o mesmo pacote novamente e adicona as tentativas
            i += 1
            # print('Pacote enviado '+str(i)) 
            if confBytes == b'$\n': # se receber $ termina a transmissão
                print('Transmissão concluída com sucesso!')
        else:
            tries += 1
            print('Erro na transmissão. Tentativa número '+str(tries))

        # se chegar em 500 tentativas ele desiste
        if tries > 500:
            print('Limite de tentativas atingido! Encerrando transmissão')
            break

# caso não tenha dado para ser enviado ele escuta a porta serial para receber os dados
else:
    packagesReceived = []
    fileName = ''
    # response = b""

    while(True):
        # i = i + 1
        sBytes = ser.readline()#ser.read(1)

        # ser.write(crc32_func(sBytes))
        # sBytes = sBytes.decode('utf-8')
        try:
            ser.write(sBytes)#.encode("utf-8")

            sBytesSplited = str(sBytes).split("--")
            packageIndex = int(sBytesSplited[0].replace("b'", ""))
            packageBody = sBytesSplited[1].replace(r"\n'", "")
        
            if packageIndex == 0:
                fileName = packageBody
                continue

            print(packageBody)
            if packageBody == "$":
                print("ACK recebido, fim da transmissao")
                break

            packagesReceived.insert(packageIndex - 1, packageBody)

        except:
            print('Erro ao ler pacote')

    response = "".join(packagesReceived)

    with open(fileName,"wb") as image_file:
        image_file.write(base64.b64decode(response))