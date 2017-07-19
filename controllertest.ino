char dataString[50] = {0};
int a =0; 
int vector[2] = {0,0};



void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  if(Serial.available()){
    //this is best ran through a function instead of to a data set
    parseSerial(Serial.readString(), vector);
  } 
   pwmControl(vector[0], vector[1]);
}

void pwmControl(int angle, int mag){
 int i;
 int relay2 = 8;
 int relay = 11;
 int inputVariable = mag*10;
 int varNeg;
 int relay3 = 7;
 
    for (int i=0; i<100; i++){
    digitalWrite(relay3, HIGH);
    delay(500);
    digitalWrite(relay3, LOW);
    delay(500);
    }
 
 
   if (mag>0){
     
    digitalWrite(relay2, LOW); 
    digitalWrite(relay, HIGH);
    

    delayMicroseconds(inputVariable);
    //if (inputVariable != 1000){
        
        digitalWrite(relay,LOW);
        delayMicroseconds(1000-inputVariable);
    
     //}
   }
   
    else{
     varNeg = inputVariable*-1;
     digitalWrite(relay2, HIGH);
     digitalWrite(relay, HIGH);
     delayMicroseconds(varNeg);
     //if (varNeg =!1000){
      
       digitalWrite(relay, LOW);
       delayMicroseconds(1000 - varNeg);
    
       //  }
       }    
//  digitalWrite(relay2, HIGH);
//  int x;
//  for (x=0; x<10000; x++){
//  int inputVariable = 700;
//  digitalWrite(11, HIGH);
//  delayMicroseconds(inputVariable);
//  digitalWrite(11, LOW);
//  delayMicroseconds(1000 - inputVariable);
//  }

  digitalWrite(relay2, LOW);
}




// converts data from serial read to an array of ints


int parseSerial(String input, int *serialRead){
  

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

vector[0] = serialRead[0];
vector[1] = serialRead[1];
}
