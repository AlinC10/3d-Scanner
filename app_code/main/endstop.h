#pragma once
#include "Arduino.h"

#define BOTTOM_ENDSTOP_INPUT 2
#define UPPER_ENDSTOP_INPUT 3

class Endstop {
  private:
    int input;

  public:
    Endstop(int input) {
      this->input = input;
    }

    void pinSetup() {
      pinMode(this->input, INPUT_PULLUP);
    }

    // true = sensor activated endstop
    // false = sensor did not reach endstop
    bool reachRodLimit() {
      const int endpointState = digitalRead(this->input);

      return endpointState == HIGH ? true : false;
    }
};