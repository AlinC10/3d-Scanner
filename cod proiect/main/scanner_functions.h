#pragma once
#include "motor.h"

template<class T> inline Print& operator<<(Print& obj, T arg) {
  obj.print(arg);
  return obj;
}

bool shouldStop(bool& hasScanned, bool upperEndstopReached) {
  if (!hasScanned || upperEndstopReached)
    return true;

  if (Serial.available() > 0) {
    String pythonCommand = Serial.readStringUntil("\n");
    pythonCommand.trim();
    pythonCommand.toLowerCase();

    if (pythonCommand == "stop")
      return true;
  }

  return false;
}

// TODO: change exit to return and modify scanning() function to return to the void loop()
void turnOffScanner(Motor& zMotor, Motor& turntableMotor) {
  zMotor.stop();
  turntableMotor.stop();

  Serial << "end";
  exit(0);
}

bool checkStoppingConditions(bool& hasScanned, bool upperEndstopReached, Motor& zMotor, Motor& turntableMotor) {
  if (shouldStop(hasScanned, upperEndstopReached)) {
    turnOffScanner(zMotor, turntableMotor);
    return true;
  }

  return false;
}