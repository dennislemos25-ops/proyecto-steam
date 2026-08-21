#include <Servo.h>

// Definición de pines para los sensores ultrasónicos
const int TRIG_ENTRADA = 2;
const int ECHO_ENTRADA = 3;
const int TRIG_SALIDA  = 4;
const int ECHO_SALIDA  = 5;

// Definición de pines para el sensor de gas y buzzer
const int PIN_MQ2    = A0;
const int PIN_BUZZER = 8;

// Definición de pin para el Servomotor
const int PIN_SERVO = 9;

// Umbrales de configuración
const int DISTANCIA_DETECCION = 10; // Distancia en cm para detectar vehículo
const int UMBRAL_GAS          = 300; // Nivel de gas para activar la alarma (0 a 1023)

// Ángulos del servomotor
const int ANGULO_CERRADO = 0;
const int ANGULO_ABIERTO = 90;

Servo barrera;

void setup() {
  // Configuración de pines ultrasónico entrada
  pinMode(TRIG_ENTRADA, OUTPUT);
  pinMode(ECHO_ENTRADA, INPUT);

  // Configuración de pines ultrasónico salida
  pinMode(TRIG_SALIDA, OUTPUT);
  pinMode(ECHO_SALIDA, INPUT);

  // Configuración del módulo buzzer (pin de señal)
  pinMode(PIN_BUZZER, OUTPUT);

  // Inicialización del servomotor
  barrera.attach(PIN_SERVO);
  barrera.write(ANGULO_CERRADO);

  Serial.begin(9600);
}

void loop() {
  // 1. Lectura de distancias
  long distEntrada = medirDistancia(TRIG_ENTRADA, ECHO_ENTRADA);
  long distSalida  = medirDistancia(TRIG_SALIDA, ECHO_SALIDA);

  // 2. Control de la barrera (Entrada o Salida)
  if (distEntrada <= DISTANCIA_DETECCION || distSalida <= DISTANCIA_DETECCION) {
    barrera.write(ANGULO_ABIERTO); // Abre la barrera
    delay(3000);                   // Espera 3 segundos para que pase el vehículo
  } else {
    barrera.write(ANGULO_CERRADO); // Mantiene o regresa la barrera a cerrado
  }

  // 3. Lectura del sensor de gas MQ-2
  int nivelGas = analogRead(PIN_MQ2);

  if (nivelGas > UMBRAL_GAS) {
    tone(PIN_BUZZER, 1000); // Activa el tono a 1000 Hz
  } else {
    noTone(PIN_BUZZER);     // Desactiva el sonido
  }

  delay(100);
}

// Función auxiliar para obtener la distancia de un sensor HC-SR04 en cm
long medirDistancia(int pinTrig, int pinEcho) {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  long duracion = pulseIn(pinEcho, HIGH, 30000); // Timeout de 30ms
  if (duracion == 0) return 999; // Si no recibe eco, retorna valor alto

  return duracion * 0.034 / 2;
}
