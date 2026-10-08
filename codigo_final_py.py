import threading
import time
from flask import Flask, jsonify, render_template_string
import serial
import codigo_html

#PUERTO_COM = 'COM10'  # Ajustá según tu puerto COM
#Nuevo fragmento - Puerto Automatico
PID_MICROBIT = 0043
VID_MICROBIT = 2341
TIMEOUT = 0.1

def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None

BAUDIOS = 9600

UMBRAL_MODERADO = 200
UMBRAL_PELIGROSO = 350

entradas = 0
salidas = 0
adentro = 0
nivel_gas = 0
estado_aire = "Bueno"
color_estado = "#a6e3a1"
alerta_gas = False

app = Flask(__name__)


def evaluar_calidad_aire(valor):
    if valor >= UMBRAL_PELIGROSO:
        return "Peligroso ⚠️", "#f38ba8", True
    elif valor >= UMBRAL_MODERADO:
        return "Moderado ⚠️", "#f9e2af", False
    else:
        return "Bueno 🟢", "#a6e3a1", False



def escuchar_arduino():
    global entradas, salidas, adentro, nivel_gas, estado_aire, color_estado, alerta_gas

    try:
        arduino = serial.Serial(PUERTO_COM, BAUDIOS, timeout=1)
        time.sleep(2)
        print(f"--> CONECTADO EN {PUERTO_COM} <--")

        while True:
            if arduino.in_waiting > 0:
                linea = (
                    arduino.readline().decode("utf-8", errors="ignore").strip()
                )

                if linea == "ENTRADA":
                    entradas += 1
                    adentro += 1
                elif linea == "SALIDA":
                    salidas += 1
                    if adentro > 0:
                        adentro -= 1
                elif linea.startswith("GAS:"):
                    try:
                        valor = int(linea.split(":")[1])
                        nivel_gas = valor
                        estado_aire, color_estado, alerta_gas = (
                            evaluar_calidad_aire(nivel_gas)
                        )
                        print(
                            f"[MQ-2] Valor: {nivel_gas} | Estado: {estado_aire}"
                        )
                    except ValueError:
                        pass

            time.sleep(0.05)
    except Exception as e:
        print(f"Error de conexión: {e}")

@app.route("/")
def index():
    return render_template_string(codigo_html.HTML_TEMPLATE)


@app.route("/datos")
def datos():
    return jsonify(
        {
            "entradas": entradas,
            "salidas": salidas,
            "adentro": adentro,
            "nivel_gas": nivel_gas,
            "estado_aire": estado_aire,
            "color_estado": color_estado,
            "alerta_gas": alerta_gas,
        }
    )


if __name__ == "__main__":
    hilo = threading.Thread(target=escuchar_arduino, daemon=True)
    hilo.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
