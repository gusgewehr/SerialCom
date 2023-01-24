import serial
import base64

#Luis-Gubert.jpg
'''
import base64
from io import BytesIO
from PIL import Image
img = Image.open('test.jpg')
im_file = BytesIO()
img.save(im_file, format="JPEG")
im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
im_b64 = base64.b64encode(im_bytes)
'''

with open("teste.png", "rb") as image_file:
    Data = base64.b64encode(image_file.read())

print(len(Data))


ser = serial.Serial('/dev/ttyS0', timeout=1)  # open serial port

#Data = 'Lorem Ipsum is simply dummy text of the printing' #and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'

packages = []
N = 1000
for i in range(0, len(str(Data)), N):
    packages.append(Data[i:i+N])

i =0
tries = 0

packages.append(b'$')

response = b''

if Data:
    while i < len(packages):
        ser.write(packages[i]+b'\n')

        confBytes = ser.readline()   

        #confBytes = base64.b64decode(confBytes)

        if packages[i]+b'\n' == confBytes:
            i += 1
            print('Pacote enviado {}'.format(i))
            if confBytes == '$':
                print('Transmissão concluída com sucesso!')
        else:
            tries += 1
            print('Erro na transmissão')

        if tries > 500:
            print('Limite de tentativas atingido! Encerrando transmissão')
            break
else:
    while(True):
        sBytes = ser.readLine()

        ser.write(sBytes)

        if(sBytes == b'$'):
            print('Envio Finalizado')
            break
        
        response = response + sBytes    

    print(b"String transferida: " + response)

    with open("luis-enviado.jpg", 'wb') as image_file:
        image_file.write(base64.b64decode(response))