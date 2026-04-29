int readings = 10;

void setup() {
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  long sum = 0;

  for (int i = 0; i < readings; i++) {
    sum += analogRead(A0);
    delay(10);
  }

  const float avg = sum / (float)readings;

  float distance_cm = 2076.0 / (avg - 11);
  distance_cm = distance_cm > 30 ? 31 : distance_cm < 4 ? 4
                                                        : distance_cm;

  Serial.println(distance_cm * 10.0);
  delay(2500);
}
