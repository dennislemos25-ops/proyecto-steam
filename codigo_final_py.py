import threading
import time
from flask import Flask, jsonify, render_template_string
import serial

PUERTO_COM = 'COM10'  # Ajustá según tu puerto COM
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


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Control de Estacionamiento</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e2e; color: #cdd6f4; text-align: center; margin: 0; padding: 20px; }
        h1 { color: #89b4fa; }
        .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 30px; }
        .card { background-color: #313244; padding: 25px; border-radius: 12px; min-width: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .card h2 { margin: 0; font-size: 1.1rem; color: #a6adc8; }
        .card .val { font-size: 2.5rem; font-weight: bold; margin-top: 10px; color: #a6e3a1; }
        .card.main .val { color: #f9e2af; font-size: 3.5rem; }
        
        .btn-gas { background-color: #89b4fa; color: #11111b; border: none; padding: 12px 20px; font-size: 1rem; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 15px; }
        .btn-gas:hover { background-color: #b4befe; }
        .gas-info { margin-top: 15px; font-size: 1.1rem; display: none; line-height: 1.6; }
        
        .alert-banner { display: none; background-color: #f38ba8; color: #11111b; padding: 15px; font-size: 1.3rem; font-weight: bold; border-radius: 8px; margin-bottom: 20px; animation: blink 1s infinite alternate; }
        @keyframes blink { from { opacity: 1; } to { opacity: 0.5; } }
    </style>
</head>
<body>

    <div id="alertBanner" class="alert-banner">
        ⚠️ ¡ALERTA DE GAS PELIGROSO DETECTADO! ⚠️
    </div>

    <h1>Control de Estacionamiento</h1>
    
    <div class="container">
        <div class="card main">
            <h2>Vehículos Adentro</h2>
            <div class="val" id="adentro">0</div>
        </div>
        <div class="card">
            <h2>Entradas Totales</h2>
            <div class="val" id="entradas">0</div>
        </div>
        <div class="card">
            <h2>Salidas Totales</h2>
            <div class="val" id="salidas">0</div>
        </div>
        <div class="card">
            <h2>Calidad del Aire</h2>
            <button class="btn-gas" onclick="toggleGasInfo()">Mostrar Calidad del Aire</button>
            <div class="gas-info" id="gasArea">
                <div>Estado: <span id="estadoAire" style="font-weight:bold;">--</span></div>
                <div style="font-size:0.9rem; color:#a6adc8;">(Valor MQ-2: <span id="nivelGas">--</span>)</div>
            </div>
        </div>
    </div>

    <script>
        let mostrandoGas = false;
        
        // Carga del audio MP3
        const sonidoAlarma = new Audio('/static/alarma.mp3');
        sonidoAlarma.loop = true; // Bucle continuo

        function toggleGasInfo() {
            const area = document.getElementById('gasArea');
            const btn = document.querySelector('.btn-gas');
            mostrandoGas = !mostrandoGas;
            if (mostrandoGas) {
                area.style.display = 'block';
                btn.innerText = 'Ocultar Calidad del Aire';
            } else {
                area.style.display = 'none';
                btn.innerText = 'Mostrar Calidad del Aire';
            }
        }

        function actualizar() {
            fetch('/datos')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('adentro').innerText = data.adentro;
                    document.getElementById('entradas').innerText = data.entradas;
                    document.getElementById('salidas').innerText = data.salidas;
                    document.getElementById('nivelGas').innerText = data.nivel_gas;
                    
                    const elEstado = document.getElementById('estadoAire');
                    elEstado.innerText = data.estado_aire;
                    elEstado.style.color = data.color_estado;

                    const banner = document.getElementById('alertBanner');
                    
                    if (data.alerta_gas) {
                        banner.style.display = 'block';
                        
                        // Si la alarma no está sonando, iniciar reproducción
                        if (sonidoAlarma.paused) {
                            sonidoAlarma.play().catch(e => {
                                console.log("El navegador bloqueó el auto-play. Haz clic en la página.");
                            });
                        }
                    } else {
                        banner.style.display = 'none';
                        
                        // Si la alarma finalizó, pausar y reiniciar audio al inicio
                        if (!sonidoAlarma.paused) {
                            sonidoAlarma.pause();
                            sonidoAlarma.currentTime = 0;
                        }
                    }
                });
        }

        setInterval(actualizar, 1000);
        actualizar();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


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
