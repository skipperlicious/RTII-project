int D3 = 3;
int D2 = 2;

void setup() {
  pinMode(D3, INPUT);
  pinMode(D2, INPUT);
  Serial.begin(9600);

  int stateIR = digitalRead(D3);
  int stateIR2 = digitalRead(D2);
}

void loop() {
  int stateIR = digitalRead(D3);
    if(stateIR == 0) {
       Serial.println("CLICKED"); 
      delay(1000);} 
      else {
      Serial.println("RELEASED"); }

  /*if(stateIR2 == 0) {
    int stateIR2 = digitalRead(D2);
      Serial.println("CLICKED"); 
      delay(1000);} 
      else {
      Serial.println("RELEASED"); }*/
}


