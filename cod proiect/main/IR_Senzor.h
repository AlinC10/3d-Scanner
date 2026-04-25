#pragma once
#include "Arduino.h"
#define SENZOR_PIN A0

int readings = 10;  // can be change by user through python script

class IR_Senzor {
private:
  int input;

public:
  IR_Senzor(int input) {
    this->input = input;
  }

  // read distance from the sensor
  float getDistance() {
    long sum = 0;

    for (int i = 0; i < readings; i++) {
      sum += analogRead(this->input);
      delay(10);
    }

    const float avg = sum / (float)readings;

    float distance_cm = 2076.0 / (avg - 11);
    distance_cm = distance_cm > 30 ? 31 : distance_cm < 4 ? 4 : distance_cm;

    return distance_cm * 10.0;
  }
};