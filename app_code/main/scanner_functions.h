#pragma once
#include "motor.h"

template<class T> inline Print& operator<<(Print& obj, T arg) {
  obj.print(arg);
  return obj;
}

bool shouldStop(bool boolCondition) {
  if (boolCondition)
    return true;

  if (Serial.available() > 0) {
    String pythonCommand = Serial.readStringUntil("\n");
    pythonCommand.trim();
    pythonCommand.toLowerCase();

    if (pythonCommand == "stop") {
      Serial << "end";
      return true;
    }
  }

  return false;
}

void turnOffScanner(Motor& zMotor, Motor& turntableMotor) {
  zMotor.stop();
  turntableMotor.stop();

  return;
}

bool checkStoppingConditions(bool boolCondition, Motor& zMotor, Motor& turntableMotor) {
  if (shouldStop(boolCondition)) {
    turnOffScanner(zMotor, turntableMotor);
    Serial << "end";
    return true;
  }

  return false;
}