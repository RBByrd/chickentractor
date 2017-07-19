#include <EEPROM.h>


int addr = 0;//EEPROM Address for identifing signiture (IS)

char checkCon = 'N'; //checks to make sure IS is passed to Rasppi 

char dataString[50] = {0};

int a =0; 

int vector[6] = {0,0,0,0,0,0};//vector for passing serial data

int maxWidth = 255;

int baud = 9600; //baud rate communication to rasppi

int relay1 = 2; //left motor direction
int pwm1 = 3;   //left motor pwm
int width1 = 0; //size of the width left motor (0-255)

int relay2 = 4; //right motor direction
int pwm2 = 5;   //right motor pwm
int width2 = 0; //size of the width right motor (0-255)

int relay3 = 7; //ramp motor direction
int pwm3 = 6;   //ramp motor pwm
int width3 = 0; //size of the width right motor (0-255)
int liftUp = 9;
int liftDown = 11;



void setup() {
  pinMode(relay1, OUTPUT);//set the relays as outputs
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(liftUp, OUTPUT);
  pinMode(liftDown, OUTPUT);
  
  digitalWrite(relay1,LOW); //set motors to low for start of program
  digitalWrite(relay2,LOW);
  digitalWrite(relay3,LOW);
  




  Serial.begin(9600);              //Starting serial communication
  checkConnect();
}
  
void loop() {
  if(Serial.available()){
    //this is best ran through a function instead of to a data set
    String test = Serial.readString();
    parseSerial(test, vector);
    //Serial.write(vector[0]); //write to rasppi for troubleshooting
    //Serial.write(vector[1]);
  } 
  //for loop for testing just pwmcontrol
  //for(int i = 2; i < 255; i = i * 2){
   //vector[1] = -255;
   
   pwmControl2(vector[0], vector[1]);
   //delay(5000);
  //}
  
   liftFunc(vector[4], vector[2]);
  
}


void liftFunc(int up, int down){
  start:
     if (down == 0 && up == 1){
        while(down == 0 && up == 1){
         digitalWrite(liftDown, LOW);
         digitalWrite(liftUp, HIGH);
         goto start;
       }  
     }
  
     else if (down == 1 && up == 0){
        while(down == 1 && up == 0){
         digitalWrite(liftUp, LOW); 
         digitalWrite(liftDown, HIGH);
         goto start;
        }
     }

     else if (down == 1 && up == 1){
       while(up == 1 && down == 1){
         digitalWrite(liftDown, LOW);
         digitalWrite(liftUp, LOW);
         goto start;
       } 
     }
}

     


void pwmControl2(int angle, int mag){

    int angleMod = 0;
    
    if(mag >= 0){
      
        
      
      //set motors to HIGH for forward movement
      digitalWrite(relay1,HIGH); 
      digitalWrite(relay2,HIGH);
      
      //set the PWM compared to the mag
      width1 = (mag * maxWidth)/100;    // left motor
      
      width2 = (mag * maxWidth)/100;    // right motor
      if (angle < 0){
        angleMod = angle + 90;
        width2 = (angleMod * width2)/90; 
        
      }
      
      else if (angle > 0) {
        angleMod = -angle + 90;
        width1 = (angleMod * width1)/90;
      }
      
      analogWrite(pwm1, width1);
      analogWrite(pwm2, width2);
      
    }

      
    else if (mag<0){
      //set motors to LOW for reverse movement
      digitalWrite(relay1,LOW); 
      digitalWrite(relay2,LOW);
      
      //set the PWM compared to the neg of the mag
      width1 = (-mag * maxWidth)/200;
      width2 = (-mag * maxWidth)/200;
      
        
      if (angle < 0){
        angleMod = angle + 90;
        width1 = (angleMod * width1)/90;
        
      }
      
      else if (angle > 0){
        angleMod = -angle + 90;
        width2 = (angleMod * width2)/90;
      }
      
      analogWrite(pwm1, width1);
      analogWrite(pwm2, width2);
    }
  
  
  
}


//checks to make sure rasppi has SI
void checkConnect(){

  while(checkCon != 'Y'){
    Serial.write(EEPROM.read(addr));
    delay(1000);  
    if(Serial.available()){
      checkCon = Serial.read();
    }
  
  }

}

int parseSerial(String input, int *serialRead){
  
  int stringSize = sizeof(input);
  int twos = 0;
  
  for(int j = 0 ; j < stringSize -1;j++){
    if (input[j] < 128){
      vector[j] = input[j];
    }  
    else{
      vector[j] = input[j] & -256;
    } 
    }

   for(int j = 0; j < 5;j++){
     twos = input[2]|2^j;
     vector[j+2] = twos / (2^j);
   }
}



// converts data from serial read to an array of ints
int parseSerial2(String input, int *serialRead){
  

  // i is the location in the string array 
  int i = 0;
  int stringSize = sizeof(input);
  //serial read set variables to 0 
  serialRead[0] = 0;
  serialRead[1] = 0;


  //loop through the string converting it into an array ints
  for(int j = 0 ; j < stringSize ;j++){
    if (input[j] == '-'){
      j++;
      serialRead[i] = serialRead[i] - (input[j] - '0'); 
    }
    else if(input[j]== ','){
      i++;
    }
    else if(serialRead[i] < 0){
      serialRead[i] = serialRead[i] * 10;
      serialRead[i] = serialRead[i] - (input[j] - '0'); 
    }
    else {
      serialRead[i] = serialRead[i] * 10;
      serialRead[i] = serialRead[i] + (input[j] - '0'); 
    }
  }
//set the variables into the array location. (this may be redundant) 
vector[0] = serialRead[0];
vector[1] = serialRead[1];
vector[2] = serialRead[2];
vector[3] = serialRead[3];
vector[4] = serialRead[4];
vector[5] = serialRead[5];

}


