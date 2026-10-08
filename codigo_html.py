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
