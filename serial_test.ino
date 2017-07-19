char dataString[50] = {0};
int a =0; 

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  if(Serial.available()){
    //this is best ran through a function instead of to a data set
    dataString = Serial.read();
  }
}
