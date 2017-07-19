/*
 * this is a code to set the eeprom to store the values to identify microcontrollers 
 * This will be ran once per Arduino board in the controls box to set values
 * the values should not be changed after being ran
 * value 64 will be set for PWM controller
 * Value 130 will be set for GPS module
 */

#include <EEPROM.h>

int addr = 0;

//int SetValue = 80;  //PWM value 'P'
int SetValue = 71; //GPS value 'G'


void setup() {
  //set the EEPROM value
  EEPROM.write(addr, SetValue);
  //Start Serial to ensure Value is set 
  Serial.begin(9600);
}

void loop() {

Serial.write(EEPROM.read(addr));
Serial.write('\n');
delay(10000);
}


