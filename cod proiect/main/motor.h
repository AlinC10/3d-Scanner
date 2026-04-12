#pragma once
#include "Arduino.h"

#define Z_MOTOR_OUTPUT1 7
#define Z_MOTOR_OUTPUT2 6
#define Z_MOTOR_OUTPUT3 5
#define Z_MOTOR_OUTPUT4 4
#define ROTATION_STEPS_Z_MOTOR 2048

#define TURNTABLE_MOTOR_OUTPUT1 11
#define TURNTABLE_MOTOR_OUTPUT2 10
#define TURNTABLE_MOTOR_OUTPUT3 9
#define TURNTABLE_MOTOR_OUTPUT4 8
#define ROTATION_STEPS_TURNTABLE_MOTOR 4096

#define MEASUREMENTS_PER_ROTATION 64

class Motor {
private:
  int output1;
  int output2;
  int output3;
  int output4;
  int rotationSteps; // how much it rotates on a step
  static const int DELAY = 2;

public:
  Motor(int output1, int output2, int output3, int output4, int rotationSteps) {
    this->output1 = output1;
    this->output2 = output2;
    this->output3 = output3;
    this->output4 = output4;
    this->rotationSteps = rotationSteps;
  }

  void pinSetup() {
    pinMode(this->output1, OUTPUT);
    pinMode(this->output2, OUTPUT);
    pinMode(this->output3, OUTPUT);
    pinMode(this->output4, OUTPUT);
  }

  int stepsBetweenMeasurements() {
    return this->rotationSteps / MEASUREMENTS_PER_ROTATION;
  }

  int getRotationSteps() const {
    return this->rotationSteps;
  }

  void fullStepRotation(int output1, int output2, int output3, int output4) {
    digitalWrite(output1, HIGH);
    digitalWrite(output2, HIGH);
    digitalWrite(output3, LOW);
    digitalWrite(output4, LOW);
    delay(DELAY);
  }

  void halfStepRotation(int output1, int output2, int output3, int output4) {
    digitalWrite(output1, HIGH);
    digitalWrite(output2, LOW);
    digitalWrite(output3, LOW);
    digitalWrite(output4, LOW);
    delay(DELAY);
  }

  void fullStepForward() {
    this->fullStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->fullStepRotation(this->output2, this->output3, this->output1, this->output4);
    this->fullStepRotation(this->output3, this->output4, this->output1, this->output2);
    this->fullStepRotation(this->output1, this->output4, this->output2, this->output3);
  }

  void fullStepBackward() {
    this->fullStepRotation(this->output3, this->output4, this->output1, this->output2);
    this->fullStepRotation(this->output2, this->output3, this->output1, this->output4);
    this->fullStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->fullStepRotation(this->output1, this->output4, this->output2, this->output3);
  }

  void halfStepForward() {
    this->halfStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->fullStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->halfStepRotation(this->output2, this->output1, this->output3, this->output4);
    this->fullStepRotation(this->output2, this->output3, this->output1, this->output4);
    this->halfStepRotation(this->output3, this->output1, this->output2, this->output4);
    this->fullStepRotation(this->output3, this->output4, this->output1, this->output2);
    this->halfStepRotation(this->output4, this->output1, this->output2, this->output3);
    this->fullStepRotation(this->output1, this->output4, this->output2, this->output3);
  }

  void halfStepBackward() {
    this->halfStepRotation(this->output4, this->output1, this->output2, this->output3);
    this->fullStepRotation(this->output3, this->output4, this->output1, this->output2);
    this->halfStepRotation(this->output3, this->output1, this->output2, this->output4);
    this->fullStepRotation(this->output2, this->output3, this->output1, this->output4);
    this->halfStepRotation(this->output2, this->output1, this->output3, this->output4);
    this->fullStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->halfStepRotation(this->output1, this->output2, this->output3, this->output4);
    this->fullStepRotation(this->output1, this->output4, this->output2, this->output3);
  }

  void stop() {
    digitalWrite(this->output1, LOW);
    digitalWrite(this->output2, LOW);
    digitalWrite(this->output3, LOW);
    digitalWrite(this->output4, LOW);
  }
};