#include <Servo.h>

const int TRIG_ENTRADA = 2;
const int ECHO_ENTRADA = 3;
const int TRIG_SALIDA  = 4;
const int ECHO_SALIDA  = 5;

const int PIN_MQ2    = A0;
const int PIN_BUZZER = 8;
const int PIN_SERVO  = 9;

const int DISTANCIA_DETECCION = 5;
const int UMBRAL_GAS          = 300; // Ajustar según tu ambiente

const int ANGULO_CERRADO = 180;
const int ANGULO_ABIERTO = 90;

Servo barrera;

bool detectadoEntrada = false;
bool detectadoSalida  = false;

unsigned long ultimoTiempoGas = 0;
const unsigned long INTERVALO_GAS = 5000; // 5 segundos

void setup() {
  pinMode(TRIG_ENTRADA, OUTPUT);
  pinMode(ECHO_ENTRADA, INPUT);
  pinMode(TRIG_SALIDA, OUTPUT);
  pinMode(ECHO_SALIDA, INPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  barrera.attach(PIN_SERVO);
  barrera.write(ANGULO_CERRADO);

  Serial.begin(9600);
}

void loop() {
  long distEntrada = medirDistancia(TRIG_ENTRADA, ECHO_ENTRADA);
  long distSalida  = medirDistancia(TRIG_SALIDA, ECHO_SALIDA);

  // Control Detección ENTRADA
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

  // Control Detección SALIDA
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

  // Monitoreo de Gas continuo para la alarma física
  int nivelGas = analogRead(PIN_MQ2);
  if (nivelGas > UMBRAL_GAS) {
    tone(PIN_BUZZER, 1000);
  } else {
    noTone(PIN_BUZZER);
  }

  // Envío periódico del valor de gas a Python cada 10 segundos
  if (millis() - ultimoTiempoGas >= INTERVALO_GAS) {
    ultimoTiempoGas = millis();
    Serial.print("GAS:");
    Serial.println(nivelGas);
  }

  delay(100);
}

long medirDistancia(int pinTrig, int pinEcho) {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  long duracion = pulseIn(pinEcho, HIGH, 30000);
  if (duracion == 0) return 999;

  return duracion * 0.034 / 2;
}