/*
  
  Illumination switch and pressure sensor.
 
 */

// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin1 = A0;  // Analog input pin that the potentiometer is attached to
const int analogInPin2 = A5; // Analog output pin that the LED is attached to
const int pressureThreshold = 350;
const int switchthreshold = 350;
int sensor1Value = 0;        // value read from the pot
int sensor2Value = 0;        // value output to the PWM (analog out)
int lastval = 0;
//int output1Value = 0;        // value read from the pot
//int output2Value = 0;        // value output to the PWM (analog out)
int NOTHING = 0;
int OPEN = 1;// clip is open, in transit (fsr low, switch low)
int EMPTY = 2;//   # clip is closed, no paper in (fsr high, switch high)
int READY = 3;//   # clip is closed, paper in place (fsr high, switch low)
		

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  int returnval = NOTHING;
  // read the analog in value:
  sensor1Value = analogRead(analogInPin1);            
  sensor2Value = analogRead(analogInPin2);
  if (sensor2Value < switchthreshold) {
    returnval = OPEN;
    if (sensor1Value > pressureThreshold){
      returnval = READY;
    }
  }
  else {
    returnval = EMPTY;
  }
  if (lastval != returnval){
    lastval = returnval;
    Serial.print(returnval); 
  }
  // map it to the range of the analog out:
  //output1Value = map(sensor1Value, 0, 1023, 0, 255); 
  //output2Value = map(sensor2Value, 0, 1023, 0, 255);  
  // change the analog out value:
  //analogWrite(analogOutPin, outputValue);           

/*
  // print the results to the serial monitor:
  Serial.print("sensor1 = " );                       
  Serial.print(sensor1Value); 
  Serial.print("\t sensor2 = " );                       
  Serial.println(sensor2Value);   
  //Serial.print("\t output1 = ");      
  //Serial.print(output1Value);
  //Serial.print("\t output2 = ");      
  //Serial.println(output2Value);  
*/

  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000);                     
}
