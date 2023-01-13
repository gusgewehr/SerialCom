import serial


ser = serial.Serial('/dev/ttyS0', timeout=1)  # open serial port

text = 'Lorem Ipsum is simply dummy text of the printing' #and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'

packages = []
for byte in text:
   packages.append(byte)

i =0
trys = 0

packages.append('$')

response = ''

if packages:
    while i < len(packages):

        ser.write(packages[i].encode('utf-8'))

        confBytes = ser.read(1)

        confBytes = confBytes.decode('utf-8')

    

        if packages[i] == confBytes:
            i += 1
            print('Pacote enviado')
            if confBytes == '$':
                print('Transmissão concluída com sucesso!')
        else:
            trys += 1
            print('Erro na transmissão')

        if trys > 500:
            print('Limite de tentativas atingido! Encerrando transmissão')
            break
else:
    while(True):
        sBytes = ser.read(1)

        response = response.join(sBytes.decode('utf-8')
)

