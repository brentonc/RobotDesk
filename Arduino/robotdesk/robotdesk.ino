/*
  This is the main robotdesk runtime.



REFERENCE:
http://www.firgelliauto.com/blogs/news/18090523-how-to-use-an-arduino-with-firgelli-automations-linear-actuators


*/

const int RELAY_1_A = 0;
const int RELAY_1_B = 1;
const int FULLEXTEND_TIME = 30000;
const int IN_PER_SEC = 0.6;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  //Serial.begin(9600);
  
  //initialize the pins
  pinMode(RELAY_1_A, OUTPUT);
  pinMode(RELAY_1_B, OUTPUT);
  
}

// the loop routine runs over and over again forever:
void loop() {

  
  
  //hello_actuator();
  reset_to_closed();
  //fully_extend();
  
}

// "Hello World" for the linear actuator
void hello_actuator(){
  //lets give it a few seconds before we start.
  delay(5000);
  
  //lets extend the actuator for a bit
  extendActuator(0);
  delay(10000);
  
  // then wait for a few seconds
  stopActuator(0);
  delay(3000);
    
  // then retract for 10 seconds
  retractActuator(0);
  delay(10000);
  
  //stop
  stopActuator(0);

  //lets wait before starting again...
  delay(5000);
}

void reset_to_closed(){
  
 retractActuator(0);
 delay(FULLEXTEND_TIME + 1000);
  while(true){};
}

void fully_extend() {
  extendActuator(0);
  delay(FULLEXTEND_TIME + 1000);
  while(true){};
}

void listen_on_serial(){
   // read the input on analog pin 0:
  //int sensorValue = analogRead(A0);
  // print out the value you read:
  //Serial.println(sensorValue);
  //delay(1);        // delay in between reads for stability 
}


void extendActuator(int actuator) {
  //Set one relay one and the other off
  //this will move extend the actuator
  //todo: update this to extend the passed-in actuator
  
  digitalWrite(RELAY_1_A, HIGH);
  digitalWrite(RELAY_1_B, LOW);
}

void retractActuator(int actuator) { 
  //Set one relay off and the other on 
  //this will move retract the actuator 
    //todo: update this to retract the passed-in actuator
  digitalWrite(RELAY_1_A, LOW);
  digitalWrite(RELAY_1_B, HIGH); 
}

void stopActuator(int actuator) {
 //Set both relays off
 //this will stop the actuator in a braking
   //todo: update this to stop the passed-in actuator
 digitalWrite(RELAY_1_A, LOW);
 digitalWrite(RELAY_1_B, LOW); } 

