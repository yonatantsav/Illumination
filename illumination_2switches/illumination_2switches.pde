 const int fsrPin = 3;    // Analog input pin that the potentiometer is attached to
 const int switchPin = 2;   //Digital input pin that the switch is attached to
 int fsrValue = 0;   // value read from the fsr
 int switchValue = 0;   // value read from the switch
 
 const int OPEN = 1;   // clip is open, in transit (fsr low, switch low)
 const int EMPTY = 2;   // clip is closed, no paper in (fsr high, switch high)
 const int READY = 3;   // clip is closed, paper in place (fsr high, switch low)
 const int UNKNOWN = 4;   // initial state
 
 int state = UNKNOWN;
 
 boolean debug = false;
 
 
 void setup() {
   pinMode(switchPin, INPUT);
   // initialize serial communications at 9600 bps:
   Serial.begin(9600); 
 }

 void loop() {
   int newState = UNKNOWN;
   
   // measure inputs
   fsrValue = digitalRead(fsrPin); // read the fsr value
   switchValue = digitalRead(switchPin); // read the switch value
   
   // calculate current state
   newState = calcState(fsrValue,switchValue);
 /*  if (debug){
     Serial.print("state ");
     Serial.println(state, DEC);
     Serial.print("newState ");
     Serial.println(newState, DEC);
     Serial.print("fsr ");
     Serial.println(fsrValue, DEC);
     Serial.print("switch ");
     Serial.println(switchValue, DEC);
     //Serial.println(-1, DEC);
   }*/
   // calculate change. report if change detected
   if (newState != state && newState != UNKNOWN){
     if (debug){
         Serial.print("change detected, old = ");
         Serial.print(state, DEC);
         Serial.print(", new = ");
         Serial.println(newState, DEC);
         
     }
     delay(10);
     // check again to make sure reading wasn't a fluke
     if (newState == calcState(fsrValue,switchValue)){
       state = newState;
       if (debug){
         Serial.print("Change reported, state = ");
         Serial.println(state, DEC);
         Serial.println("");
         delay(2000);
       }
       //report change
     //  Serial.print(state, DEC);
     }
   }
   delay(20); 
   if (debug){ 
     delay(1000);
   }
   
   
   /*
   if(fsrValue>100){
   //  Serial.print(1, BYTE);
     //Serial.println(sensorValue);   // print the pot value back to the debugger pane
   }
   else{
    //Serial.print(0);
   }
   delay(10);                     // wait 10 milliseconds before the next loop
   */
   
 }
 
 int calcState(int fsr, int sw){
   int newState = UNKNOWN;
   if (fsr == HIGH && sw == HIGH){
     newState = EMPTY;
     if (debug){ 
       Serial.println("EMPTY");
     }
   }
   else if (fsr == HIGH && sw == LOW){
     newState = READY;
     if (debug){ 
       Serial.println("READY");
     }
   }
   else if (fsr == LOW && sw == LOW){
     newState = OPEN;
     if (debug){ 
       Serial.println("OPEN");
     }
   }
   else {
    //error 
    newState = UNKNOWN;
    if (debug){ 
      Serial.println("ERROR");
    }
   }
   return newState;
 }
