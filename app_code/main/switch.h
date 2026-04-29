#pragma once
#include "Arduino.h"

#define SWITCH_PIN 12

class Switch {
  private:
    int input;
  
  public:
    Switch(int input) {
      this->input = input;
    }

    void pinSetup() {
      pinMode(this->input, INPUT);
    }

    bool isOn() {
      return digitalRead(this->input);
    }
};