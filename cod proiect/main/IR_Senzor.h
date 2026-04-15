#include "Arduino.h"
#define SENZOR_PIN A0

class IR_Senzor {
  private:
    int input;

  public:
    IR_Senzor(int input) {
      this->input = input;
    }

    float getDistance() {
      long sum = 0;
      const int readings = 10;

      for (int i = 0; i < readings; i++) {
        sum += analogRead(this->input);
        delay(50);
      }

      const float avg = sum / (float)readings;

      float voltage = avg * (5.0 / 1023.0);

      if (voltage < 0.1) voltage = 0.1;

      const float distance_cm = 12.08 * pow(voltage, -1.058);

      return distance_cm * 10.0;
    }
};