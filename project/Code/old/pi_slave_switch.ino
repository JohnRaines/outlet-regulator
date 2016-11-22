int inPin = 48; //pin the pi is spiking
int outPin = 50; //pin the arduino will control the relay with
int val = 0;    //holds the value the digital pin reads
/*Basic code for using the Arduino to drive a relay.
 *Takes digital signal from pi and beefs it up to 5v
 *
 *@author: John Raines
 *@Version 1 - 11/22/16
 */
void setup() {
  // put your setup code here, to run once:
  pinMode(inPin, INPUT);
  pinMode(outPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = digitalRead(inPin); 
  if (val == HIGH)
  {
     digitalWrite(outPin, HIGH);
  }
  else
  {
      digitalWrite(outPin, LOW);
  }
  

}
