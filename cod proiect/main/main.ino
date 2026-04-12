#include "motor.h"
#include "endstop.h"
#include "switch.h"
#include <Wire.h>
#include "Adafruit_VL53L0X.h"

#define MEASUREMENTS_PER_ROTATION 64
#define M8_THREAD_STEP_MM 1.25
#define DISTANCE_TO_CENTER_MM 135.0

template<class T> inline Print& operator<<(Print& obj, T arg) {
  obj.print(arg);
  return obj;
}

Motor zMotor(Z_MOTOR_OUTPUT1, Z_MOTOR_OUTPUT2, Z_MOTOR_OUTPUT3, Z_MOTOR_OUTPUT4, ROTATION_STEPS_Z_MOTOR);
Motor turntableMotor(TURNTABLE_MOTOR_OUTPUT1, TURNTABLE_MOTOR_OUTPUT2, TURNTABLE_MOTOR_OUTPUT3, TURNTABLE_MOTOR_OUTPUT4, ROTATION_STEPS_TURNTABLE_MOTOR);

Endstop upperEndstop(UPPER_ENDSTOP_INPUT);
Endstop bottomEndstop(BOTTOM_ENDSTOP_INPUT);

Switch chargerSwitch(SWITCH_PIN);

Adafruit_VL53L0X lidarSensor = Adafruit_VL53L0X();
int currentZ = 0;


void setup() {
  Serial.begin(115200);

  zMotor.pinSetup();
  turntableMotor.pinSetup();

  upperEndstop.pinSetup();
  bottomEndstop.pinSetup();

  chargerSwitch.pinSetup();

  while (!chargerSwitch.isOn() || !lidarSensor.begin()) {
    delay(5000);
  }

  while (!bottomEndstop.reachRodLimit() && chargerSwitch.isOn()) {
    zMotor.fullStepBackward();
  }

  zMotor.stop();
  delay(2000);
}

int k = 0;

void loop() {
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

    for (int j = 0; j < stepsBetweenMeasurements / 8; j++)
      turntableMotor.halfStepForward();

    turntableMotor.stop();
    // read distance from the sensor
    VL53L0X_RangingMeasurementData_t measure;
    lidarSensor.rangingTest(&measure, false);

    // send data to laptop
    // 4 = 'Out of Range'
    if (measure.RangeStatus != 4) {
      float currentAngle = (360.0 / MEASUREMENTS_PER_ROTATION) * i; // in degrees
      currentAngle *= (PI / 180.0); // in radians

      const int distanceToObj = measure.RangeMilliMeter;

      if (distanceToObj < DISTANCE_TO_CENTER_MM) {
        float const objRadius = DISTANCE_TO_CENTER_MM - distanceToObj;

        float const coord_X = objRadius * cos(currentAngle);
        float const coord_Y = objRadius * sin(currentAngle);

        float const coord_Z = (currentZ * 4.0 * M8_THREAD_STEP_MM) / zMotor.getRotationSteps(); // nush cu ce trb inlocuit

        Serial << coord_X << ", " << coord_Y << ", " << coord_Z << "\n";
      }

    }

    }
    // Serial << "Ultimul for: \n" ;
    for (int j = 0; j < zMotor.getRotationSteps() / 4; j++) {
      // check upper endstop
      // Serial << j << " "
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
}