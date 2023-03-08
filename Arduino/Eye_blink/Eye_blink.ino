int D3 = 3;
int D2 = 2;

void setup() {
  pinMode(D3, INPUT);
  pinMode(D2, INPUT);
  Serial.begin(9600);
}

void loop() {
  int stateIR = digitalRead(D2);
  int stateIR2 = digitalRead(D3);

    if(stateIR == 0) {
      Serial.println("LEFT"); 
      delay(1000);
      } 
      //Debugging
      /*else {
      Serial.println("RELEASED-L");
      }*/

    if(stateIR2 == 0) {
      Serial.println("RIGHT"); 
      delay(1000);
      } 
      //Debugging
      /*else {
      Serial.println("RELEASED-R");
      }*/
}


