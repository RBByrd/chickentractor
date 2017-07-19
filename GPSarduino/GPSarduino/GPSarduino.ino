#include <EEPROM.h>

int addr = 0;//EEPROM Address for identifing signiture (IS)

char checkCon = 'N'; //checks to make sure IS is passed to Rasppi 


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);              //Starting serial communication
  checkConnect();
  Serial.end();
}

void loop() {
  // put your main code here, to run repeatedly:

}

void checkConnect(){

  while(checkCon != 'Y'){
    Serial.write(EEPROM.read(addr));
    delay(1000);
    if(Serial.available()){
      checkCon = Serial.read();
    }
  }
  
}
