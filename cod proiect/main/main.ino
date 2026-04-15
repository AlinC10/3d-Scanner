#include "motor.h"
#include "endstop.h"
#include "switch.h"
#include <Wire.h>
#include "IR_Senzor.h"

#define M8_THREAD_STEP_MM 1.25
#define DISTANCE_TO_CENTER_MM 130.0
#define DISTANCE_TO_END_MM 230.0

template<class T> inline Print& operator<<(Print& obj, T arg) {
  obj.print(arg);
  return obj;
}

Motor zMotor(Z_MOTOR_OUTPUT1, Z_MOTOR_OUTPUT2, Z_MOTOR_OUTPUT3, Z_MOTOR_OUTPUT4, ROTATION_STEPS_Z_MOTOR);
Motor turntableMotor(TURNTABLE_MOTOR_OUTPUT1, TURNTABLE_MOTOR_OUTPUT2, TURNTABLE_MOTOR_OUTPUT3, TURNTABLE_MOTOR_OUTPUT4, ROTATION_STEPS_TURNTABLE_MOTOR);

Endstop upperEndstop(UPPER_ENDSTOP_INPUT);
Endstop bottomEndstop(BOTTOM_ENDSTOP_INPUT);

Switch chargerSwitch(SWITCH_PIN);

IR_Senzor sensor(SENZOR_PIN);
long currentZ = 0;

void setup() {
  Serial.begin(115200);
  // Serial << "Start";

  zMotor.pinSetup();
  turntableMotor.pinSetup();

  upperEndstop.pinSetup();
  bottomEndstop.pinSetup();

  chargerSwitch.pinSetup();

  while (!chargerSwitch.isOn()) {
    // Serial << "Eroare setup 1";
    delay(5000);
  }

  while (!bottomEndstop.reachRodLimit()) {
    zMotor.fullStepBackward();
  }

  zMotor.stop();
  delay(1000);

  for (int i = 0; i < zMotor.getRotationSteps(); i++)
    zMotor.fullStepForward();

  zMotor.stop();
  delay(2000);
}

int k = 0;

void loop() {
  bool hasScanned = false;
  // Serial << k++ << "\n";
  // add upper endpoint limit check to the if
  if (!chargerSwitch.isOn()) {
    zMotor.stop();
    turntableMotor.stop();

    Serial << "end";
    exit(1);
  }
  // Serial << "dupa !chargerSwitch.isOn()" << "\n";
  const int stepsBetweenMeasurements = turntableMotor.stepsBetweenMeasurements();

  for (int i = 0; i < MEASUREMENTS_PER_ROTATION; i++) {

    for (int j = 0; j < stepsBetweenMeasurements / 8; j++) {
      turntableMotor.halfStepForward();
    }

    // read distance from the sensor
    if (!chargerSwitch.isOn()) {
      zMotor.stop();
      turntableMotor.stop();

      Serial << "end";
      exit(1);
    }

    float const distance = sensor.getDistance();

    turntableMotor.stop();

    if (distance <= DISTANCE_TO_END_MM) {
      float currentAngle = (360.0 / MEASUREMENTS_PER_ROTATION) * i;  // in degrees
      currentAngle *= (PI / 180.0);                                  // in radians

      const float objRadius = DISTANCE_TO_CENTER_MM - distance;

      // x, y, z
      Serial << objRadius * cos(currentAngle)
             << ", " << objRadius * sin(currentAngle) << ", " << (currentZ * 4.0 * M8_THREAD_STEP_MM) / zMotor.getRotationSteps() << "\n";

      hasScanned = true;
    }
  }
  // Serial << "Ultimul for: \n" ;
  for (int j = 0; j < zMotor.getRotationSteps() / 2; j++) {
    // check upper endstop
    // Serial << j << " ";
    // if (upperEndstop.reachRodLimit()) {
    //   zMotor.stop();
    //   turntableMotor.stop();
    //   exit(1);
    // }

    zMotor.fullStepForward();
    currentZ++;
  }

  zMotor.fullStepForward();
  zMotor.stop();

  if (!hasScanned) {
    zMotor.stop();
    turntableMotor.stop();

    Serial << "end";
    exit(1);
  }
}