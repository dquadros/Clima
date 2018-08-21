# Informacoes de clima no Raspberry Pi Zero
# com sensor DHT11 e display OLED I2C 128x64

import Adafruit_SSD1306
import Adafruit_DHT
import requests
import json
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Iniciacao sensor
sensor = Adafruit_DHT.DHT11
pino_sensor = 25

#Iniciacoes de display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3c, i2c_bus=1)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height)) #imagem binaria (somente 1's e 0's)
draw = ImageDraw.Draw(image)

#Fontes para os caracteres
font = ImageFont.load_default()
font8 = ImageFont.truetype('Minecraftia-Regular.ttf', 8)
font16 = ImageFont.truetype('ManualDisplay.ttf', 16)
font40 = ImageFont.truetype('ManualDisplay.ttf', 40)

#Icones de tempo
icon_sol = Image.open("01d.png")
icon_lua = Image.open("01n.png")
icon_nuvem = Image.open("02.png")
icon_chuva = Image.open("09.png")
icon_tempes = Image.open("11.png")
icon_nevoa = Image.open("50.png")

#Posicoes das informacoes na tela
top = 2
col1 = 2
col2 = 72
col3 = 96

#Informacoes do clima
def le_infos_clima():
    #coloque aqui a sua chave e o id da sua cidade
    api_key_openweather = "minha chave"
    cidade_id = "3448439"

    url_http_req = "http://api.openweathermap.org/data/2.5/forecast?id="+cidade_id+"&appid="+api_key_openweather
    dados = requests.get(url_http_req).json()

    #extrai as informacoes
    cidade = dados["city"]["name"]
    lista = dados["list"]
    icon_id = lista[0]["weather"][0]["icon"]
    if icon_id == "01d":
        icon = icon_sol
    elif icon_id == "01n":
        icon = icon_lua
    elif icon_id in ["02d", "02n", "03d", "03n", "04d", "04n"]:
        icon = icon_nuvem
    elif icon_id in ["09d", "09n", "10d", "10n"]:
        icon = icon_chuva
    elif icon_id in ["11d", "11n"]:
        icon = icon_tempes
    elif icon_id in ["50d", "50n"]:
        icon = icon_nevoa
    else:
        icon = None
    min = 999.0
    max = 0.0
    for i in range(8):
        temp = float(lista[i]["main"]["temp_min"])
        if temp < min:
            min = temp
        temp = float(lista[i]["main"]["temp_max"])
        if temp > max:
            max = temp
    min = min - 273.15
    max = max - 273.15
    
    return cidade,icon,int(min),int(max)

prox_consulta = time.time()
temp = ""
while(True):
    try:
        #Atualizar as informacoes
        if time.time() > prox_consulta:
            (cidade,icon,min,max) = le_infos_clima()
            prox_consulta = time.time()+610  # maximo eh 1 consulta cada 10 minutos
        agora = time.localtime()
        hora = "{0:02d}:{1:02d}".format(agora.tm_hour, agora.tm_min)
        (umid, new_temp) = Adafruit_DHT.read_retry(sensor, pino_sensor);
        if not new_temp is None:
            temp = str(int(new_temp)) + "C"
        
        #Escreve informacoes no display OLED
        draw.text((col1, top),    cidade, font=font, fill=255)
        draw.text((col3, top),    hora, font=font, fill=255)
        
        draw.text((col1, top+15), "Temp",font=font8,fill=255)
        draw.text((col1, top+25), temp, font=font40, fill=255)

        if not icon is None:
            image.paste(icon,(col2, top+15))
        
        draw.text((col2, top+41), "Min",font=font8,fill=255)
        draw.text((col2, top+50), str(min)+"C", font=font16, fill=255)
        draw.text((col3, top+41), "Max",font=font8,fill=255)
        draw.text((col3, top+50), str(max)+"C",font=font16, fill=255)

        disp.image(image)
        disp.display()
        time.sleep(60)

        #Limpa display: desenha um retangulo preto em todo o display (para apagar "restos" de dados na area de imagem)
        draw.rectangle((0,0,width,height), outline=0, fill=0)

    except KeyboardInterrupt:
	    exit(1)
