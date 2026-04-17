#include "motor.h"
#include "endstop.h"
#include "switch.h"
#include "IR_Senzor.h"
#include "scanner_functions.h"
#include <Wire.h>

#define M8_THREAD_STEP_MM 1.25
#define DISTANCE_TO_CENTER_MM 130.0
#define DISTANCE_TO_END_MM 230.0

Motor zMotor(Z_MOTOR_OUTPUT1, Z_MOTOR_OUTPUT2, Z_MOTOR_OUTPUT3, Z_MOTOR_OUTPUT4, ROTATION_STEPS_Z_MOTOR);
Motor turntableMotor(TURNTABLE_MOTOR_OUTPUT1, TURNTABLE_MOTOR_OUTPUT2, TURNTABLE_MOTOR_OUTPUT3, TURNTABLE_MOTOR_OUTPUT4, ROTATION_STEPS_TURNTABLE_MOTOR);

Endstop upperEndstop(UPPER_ENDSTOP_INPUT);
Endstop bottomEndstop(BOTTOM_ENDSTOP_INPUT);

Switch chargerSwitch(SWITCH_PIN);

IR_Senzor sensor(SENZOR_PIN);
long currentLevel = 0;

void setup() {
  Serial.begin(115200);

  // setup components pin
  zMotor.pinSetup();
  turntableMotor.pinSetup();

  upperEndstop.pinSetup();
  bottomEndstop.pinSetup();

  chargerSwitch.pinSetup();
}

void setupScanner() {
  Serial << "Start";

  if (!chargerSwitch.isOn()) {
    Serial << "Alimentare motoare oprita";

    // wait to turn on charger
    while (!chargerSwitch.isOn()) {
      delay(5000);
    }
  }

  if (!bottomEndstop.reachRodLimit()) {
    Serial << "Se ajusteaza inaltimea senzorului";

    // get IR sensor at the bottom of the threaded rod
    while (!bottomEndstop.reachRodLimit()) {
      zMotor.fullStepBackward();
    }
  }

  zMotor.stop();
  delay(2000);
}

void scanning() {
  // variable used to automate stop scanner in case it finished object scanning
  bool hasScanned = false;

  Serial << "\n\nNivelul curent: " << currentLevel << "\n";

  if (checkStoppingConditions(hasScanned, upperEndstop.reachRodLimit(), zMotor, turntableMotor))
    return;

  const int stepsBetweenMeasurements = turntableMotor.stepsBetweenMeasurements();

  for (int i = 0; i < MEASUREMENTS_PER_ROTATION; i++) {

    for (int j = 0; j < stepsBetweenMeasurements / 8; j++) {
      turntableMotor.halfStepForward();
    }

    if (checkStoppingConditions(hasScanned, upperEndstop.reachRodLimit(), zMotor, turntableMotor))
      return;

    delay(50);

    float const distance = sensor.getDistance();

    turntableMotor.stop();
    if (distance > 40.0 && distance < DISTANCE_TO_CENTER_MM) {
      const float objRadius = DISTANCE_TO_CENTER_MM - distance;

      if (objRadius > 2.0) {
        float currentAngle = (360.0 / MEASUREMENTS_PER_ROTATION) * i;
        currentAngle *= (PI / 180.0);

        const float xPos = objRadius * cos(currentAngle);
        const float yPos = objRadius * sin(currentAngle);
        const float zPos = (currentLevel * zMotor.getRotationSteps() / 2 * 6.0 * M8_THREAD_STEP_MM) / zMotor.getRotationSteps();
        Serial << xPos << ", " << yPos << ", " << zPos << "\n";

        // create object base surface
        if (currentLevel == 0) {
          Serial << xPos * 0.75 << ", " << yPos * 0.75 << ", 0.0\n";
          Serial << xPos * 0.50 << ", " << yPos * 0.50 << ", 0.0\n";
          Serial << xPos * 0.25 << ", " << yPos * 0.25 << ", 0.0\n";
          Serial << "0.0, 0.0, 0.0\n";
        }

        hasScanned = true;
      }
    }
  }

  for (int j = 0; j < zMotor.getRotationSteps() / 2; j++) {
    if (checkStoppingConditions(hasScanned, upperEndstop.reachRodLimit(), zMotor, turntableMotor))
      return;

    zMotor.fullStepForward();
  }
  currentLevel++;

  zMotor.stop();

  if (checkStoppingConditions(hasScanned, upperEndstop.reachRodLimit(), zMotor, turntableMotor))
    return;
}

void readSerial() {
  // wait for user to select start scanning option
  // answer it's received by python and send through the serial to arduino
  if (Serial.available() > 0) {
    String pythonCommand = Serial.readStringUntil("\n");
    pythonCommand.trim();

    // start scanning
    if (pythonCommand == "START") {
      setupScanner();
      scanning();
    }

    else if (pythonCommand == "STOP") {
      return;
    }

    // command to change variables values
    else {
    }
  }
}

// run loop while arduino is turn on
void loop() {
  readSerial();
  delay(1000);
}