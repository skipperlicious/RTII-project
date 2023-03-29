int D2 = 2;
int D3 = 3;
int lastLeftPrintTime = 0;
int lastRightPrintTime = 0;
int delayTime = 500; // changed delay time to 500ms
int leftCounter = 0;

void setup() {
  pinMode(D2, INPUT);
  pinMode(D3, INPUT);
  Serial.begin(38400);
}

void loop() {
  int stateIR = digitalRead(D2);
  int stateIR2 = digitalRead(D3);

  if (stateIR == 0) {
    if (millis() - lastLeftPrintTime > delayTime) {
      if (leftCounter == 1) {
        Serial.println("DOUBLELEFT"); // print "DOUBLELEFT" if LEFT is pressed twice within 500ms
        leftCounter = 0; // reset leftCounter after printing "DOUBLELEFT"
      } else {
        Serial.println("LEFT");
        leftCounter = 1; // increment leftCounter if "LEFT" is pressed
      }
      lastLeftPrintTime = millis();
    }
  } else {
    Serial.println("RELEASED");
    leftCounter = 0; // reset leftCounter if "LEFT" is released
  }

  if (stateIR2 == 0) {
    if (millis() - lastRightPrintTime > delayTime) {
      Serial.println("RIGHT");
      lastRightPrintTime = millis();
    }
  } else {
    Serial.println("RELEASED");
  }
}