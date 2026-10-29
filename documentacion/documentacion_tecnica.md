# Documentación Técnica

Fecha: 22 de octubre de 2026

Este documento contiene la documentación técnica para el proyecto STEAM del curso **Laboratorio STEAM+** de la tecnicatura **Redes y Software** del **Instituto Tecnológico de Informática** de **UTU** año 2026.

# Proyecto: [SmartParking]

## 1. Integrantes
- Jim Birriel
- Noemí Dupasus
- Dennis Lemos

## 2. Descripción
- Se trata de un estacionamiento inteligente, donde detecta un vehículo y abre la barrera automáticamente, también tendrá un sensor de gas para la detección de monóxido de carbono, por si un vehículo queda prendido.
- Se brinda la implementación de un parking donde detecta la presencia de Monóxido de Carbono (CO) que es un gas sumamente tóxico y peligroso la acumulación en espacios cerrados, ya que el mismo se considera como un "asfixiante silencioso" porque es tóxico, invisible y sin olor. Por eso es importante la detección en espacios como estacionamientos de shoppings, edificios, etc.

## 3. Materiales

| Imagen       | Descripción |
| ------------ | ----------- |
| <img src="imagenes/arduino_uno.jpg" width="300" alt="arduino_uno"> | Arduino uno|
| <img src="imagenes/protoboard.jpg" width="300" alt="protoboard"> | Protoboard |
| <img src="imagenes/servomotor.jpg" width="300" alt="servomotor"> | Servomotor |
| <img src="imagenes/buzzer_arduino.jpg" width="300" alt="buzzer_arduino"> | Buzzer |
| <img src="imagenes/sensor_ultrasonico.jpg" width="300" alt="sensor_ultrasonico"> | Sensor ultrasónico x2 |
| <img src="imagenes/cables_arduino.jpg" width="300" alt="cables_arduino"> | Cables |
| <img src="imagenes/sensor_de_gas.jpg" width="300" alt="sensor_de_gas"> | Sensor de gas |


## 4. Diseño Mecánico
- Se aproxima el vehículo al estacionamiento, el sensor ultrasónico lo detecta, la barrera se levanta y luego que el mismo ingresa la barrera se baja automáticamente a los segundos.
- Si la persona se olvida del vehículo prendido se detecta el nivel monóxido de carbono y se prende una alarma sonora hasta que los valores vuelvan a la normalidad. 
- [¿Cómo se arma la solución? Incluir instrucciones de ensamblaje]
  - [Sugerencia: inspirarse en la forma como https://www.instructables.com detalla el armado de un proyecto]
- [Incluir fotografías ilustrativas]

## 5. Diseño Electrónico
Se presenta de conexión de los componentes (Sensores y Servo motor) al Arduino.
<img width="1280" height="596" alt="SmartParkingTinkercad" src="https://github.com/user-attachments/assets/e3f6103c-4f0b-4430-8611-3afdcd7295c8" />

**Conexión de los pines del sensor de proximidad con Arduino (Entrada)**
  - VCC (Rojo): Se conectó en la zona positiva de la Protoboard, la cual, a su vez, está alimentada a 5v.
  - GND (Negro): Se conecta al negativo de la Protoboard, la cual, a su vez, está conectada al GND del Arduino.
  - Trig (Naranja): Se conecta al pin 2 del Arduino. Este es el encargado de la activación.
  - Echo (Azul): Se conecta al pin 3 del Arduino. Es la recepción del pulso.

**Conexión de los pines del sensor de proximidad con Arduino (Salida)**
  - VCC (Rojo): Se conectó en la zona positiva de la Protoboard, la cual, a su vez, está alimentada a 5v.
  - GND (Negro): Se conecta al negativo de la Protoboard, la cual, a su vez, está conectada al GND del Arduino.
  - Trig (Naranja): Se conecta al pin 4 del Arduino. Este es el encargado de la activación.
  - Echo (Azul): Se conecta al pin 5 del Arduino. Es la recepción del pulso.

**Conexión de los pines del sensor de gas con el Arduino**
  - VCC (Rojo): Se conectó en la zona positiva de la Protoboard, la cual, a su vez, está alimentada a 5v.
  - GND (Negro): Se conecta al negativo de la Protoboard, la cual, a su vez, está conectada al GND del Arduino.
  - A0 (Naranja): Se conectó al pin A0 del Arduino.

**Conexión de los pines del Servo Motor al Arduino**
  - VCC (Rojo): Se conecta al positivo de la Protoboard, la cual, a su vez, está alimentada a los 5v del Arduino.
  - GND (Negro): Se conecta al negativo de la Protoboard, la cual, a su vez, está conectada al GND del Arduino.
  - PWM - Pulso (Naranja): Se conectó al pin 9 del Arduino.

**Conexión de los pines del Buzzer al Arduino**
  - VCC (Rojo): Se conecta al positivo de la Protoboard, la cual, a su vez, está alimentada a los 5v del Arduino.
  - GND (Negro): Se conecta al negativo de la Protoboard, la cual, a su vez, está conectada al GND del Arduino.
  - S / OUT / I/O (Naranja): Se conecta al pin 8 del Arduino. (En Tinkercad el buzzer no tiene 3 pines).

## 6. Diseño Software
**Explicación de los códigos utilizados en el proyecto**
En primera instancia aclaramos que utilizamos dos códigos diferentes, uno para la funcionalidad del Arduino (En C++) y otro para la conexión del Arduino con la web (En Python), donde se detalla el estado del estacionamiento.

**Medición del sensor de proximidad:**
El sensor de proximidad está siempre esperando movimiento en un rango de hasta 5cm, una vez detectado el movimiento o presencia de un vehículo, el mismo se activa y envía la señal al Servo Motor, donde este se levanta hasta que el vehículo haya pasado y cuenta tres segundos antes de cerrar.

```cpp
  const int DISTANCIA_DETECCION = 5;
  bool detectadoEntrada = false;
  bool detectadoSalida  = false;

  void loop() {
  long distEntrada = medirDistancia(TRIG_ENTRADA, ECHO_ENTRADA);
  long distSalida  = medirDistancia(TRIG_SALIDA, ECHO_SALIDA);

  if (distEntrada <= DISTANCIA_DETECCION) {
    if (!detectadoEntrada) {
      Serial.println("ENTRADA");
      detectadoEntrada = true;
      barrera.write(ANGULO_ABIERTO);
      delay(3000);
    }
  } else {
    detectadoEntrada = false;
  }
  if (distSalida <= DISTANCIA_DETECCION) {
    if (!detectadoSalida) {
      Serial.println("SALIDA");
      detectadoSalida = true;
      barrera.write(ANGULO_ABIERTO);
      delay(3000);
    }
  } else {
    detectadoSalida = false;
  }
  if (!detectadoEntrada && !detectadoSalida) {
    barrera.write(ANGULO_CERRADO);
  }
```

**Medición del sensor de gas:**
El sensor de gas está configurado para detectar el gas cada 5 segundos, esto con un umbral pre-configurado de hasta 300. Esto permite que la información esté actualizada en la web y se pueda detectar vehículos encendidos.

```cpp
  const int UMBRAL_GAS = 300;
  unsigned long ultimoTiempoGas = 0;
  const unsigned long INTERVALO_GAS = 5000;

  // Monitoreo de Gas continuo para la alarma física
  int nivelGas = analogRead(PIN_MQ2);
  if (nivelGas > UMBRAL_GAS) {
    tone(PIN_BUZZER, 1000);
  } else {
    noTone(PIN_BUZZER);
  }

  // Envío periódico del valor de gas a Python cada 5 segundos
  if (millis() - ultimoTiempoGas >= INTERVALO_GAS) {
    ultimoTiempoGas = millis();
    Serial.print("GAS:");
    Serial.println(nivelGas);
  }

  delay(100);
}
```

**Configuración del Buzzer**
El buzzer será activado una vez que el sensor detecte un umbral de gas mayor a 300, lo que disparará el sonido hasta que el nível de gas haya disminuido.

```cpp
  int nivelGas = analogRead(PIN_MQ2);
  if (nivelGas > UMBRAL_GAS) {
    tone(PIN_BUZZER, 1000);
  } else {
    noTone(PIN_BUZZER);
  }
```

**Configuración de la comunicación entre el Arduino y Python, para la web del estacionamiento:**
Se utilizó un código de Python para realizar la conexión del Arduino con la web del proyecto, lo que nos permite monitorear el estado del estacionamiento.

```python
  //Conexión con el Arduino.
  PID_ARDUINO = 0x0043
  VID_ARDUINO = 0x2341
  TIMEOUT = 0.1

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

  //Función encargada de evaluar el gas en el aire.
  def evaluar_calidad_aire(valor):
    if valor >= UMBRAL_PELIGROSO:
        return "Peligroso ⚠️", "#f38ba8", True
    elif valor >= UMBRAL_MODERADO:
        return "Moderado ⚠️", "#f9e2af", False
    else:
        return "Bueno 🟢", "#a6e3a1", False

  //Función encargada de evaluar los vehículos dentro del estacionamiento.
  def escuchar_arduino():
    global entradas, salidas, adentro, nivel_gas, estado_aire, color_estado, alerta_gas

    try:
     
        arduino = find_comport(PID_ARDUINO, VID_ARDUINO, BAUDIOS)
        time.sleep(2)
       

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
```

## 7. Referencias y recursos
- Programación de Arduino usando Python : https://keepcoding.io/blog/como-programar-arduino-con-python/
- Herramienta para diseño de circuitos Tikercad : https://www.tinkercad.com/
- Gemini como apoyo en la programación en general del proyecto : https://gemini.google.com/app?hl=es
- Arduino IDE para el código del Arduino + Visual Studio Code para el código Python.
