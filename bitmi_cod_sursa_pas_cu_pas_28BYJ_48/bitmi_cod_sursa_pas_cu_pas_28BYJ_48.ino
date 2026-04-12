#define OUTPUT1   7
#define OUTPUT2   6
#define OUTPUT3   5
#define OUTPUT4   4
#define DELAY 2

void setup() {
  pinMode(OUTPUT1, OUTPUT);
  pinMode(OUTPUT2, OUTPUT);
  pinMode(OUTPUT3, OUTPUT);
  pinMode(OUTPUT4, OUTPUT);
}

void halfStepForward() {
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
}

void halfStepBackward() {
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
}

void fullStepForward() {
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
}

void fullStepBackward() {
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
  digitalWrite(OUTPUT1, LOW); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, HIGH); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, HIGH); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, LOW); delay(DELAY);
  digitalWrite(OUTPUT1, HIGH); digitalWrite(OUTPUT2, LOW); digitalWrite(OUTPUT3, LOW); digitalWrite(OUTPUT4, HIGH); delay(DELAY);
}

void loop() {
    fullStepForward();
}