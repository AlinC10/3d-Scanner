#define OUTPUT1   7
#define OUTPUT2   6
#define OUTPUT3   5
#define OUTPUT4   4
#define DELAY 3

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

void loop() {
  for (int i = 0; i < 256; i++) {
    halfStepForward(); // jumatate de rotatie inainte
  }

  delay(1000); // pauza

  for (int i = 0; i < 256; i++) {
    halfStepBackward(); // jumatate de rotatie inapoi
  }

  delay(2000); // asteapta inainte sa repete
}