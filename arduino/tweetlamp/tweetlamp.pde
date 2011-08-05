#define RELAY_MODULE 13

void setup() {
  pinMode(RELAY_MODULE, OUTPUT); //set the digital pin where the realy module is connected to output
  Serial.begin(9600); //start the serial communication with the PC/Python software
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read(); //read one character sent by Python software
    
    if (c == 'H') {
      digitalWrite(RELAY_MODULE, HIGH); //lights up!
    }
    else if (c == 'L') {
      digitalWrite(RELAY_MODULE, LOW); //turn off
    } 
    //else -> ignores the character received
  }
}
