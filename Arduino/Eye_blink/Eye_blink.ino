int D3 = 3;
int D2 = 2;

void setup() {
  pinMode(D2, INPUT);
  pinMode(D3, INPUT);
  Serial.begin(9600);

  int stateIR = digitalRead(D2);
  int stateIR2 = digitalRead(D3);
}

void loop() {
  int stateIR = digitalRead(D2);
  int stateIR2 = digitalRead(D3);
    if(stateIR == 0) {
      Serial.println("LEFT"); 
      delay(500);} 
      else {
      Serial.println("RELEASED"); }

    if(stateIR2 == 0) {
      Serial.println("RIGHT"); 
      delay(500);} 
      else {
      Serial.println("RELEASED"); }
}


