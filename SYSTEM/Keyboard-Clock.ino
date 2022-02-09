//This script is for using Arduino UNO as an 8MHz oscillator and keyboard emulator
//for Liv85 project
const byte CLOCKOUT = 9;   // Uno, Duemilanove, etc.

void setup ()
  {
  // set up 8 MHz timer on CLOCKOUT (OC1A)
  pinMode (CLOCKOUT, OUTPUT); 
  // set up Timer 1
  TCCR1A = bit (COM1A0);  // toggle OC1A on Compare Match
  TCCR1B = bit (WGM12) | bit (CS10);   // CTC, no prescaling
  OCR1A =0 ;       // output every cycle
  Serial.begin(9600);
  for(int i=0; i<=6; i++) pinMode(i+2,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  }  // end of setup

void sen(byte x){
  int temp;
  for(int i=6; i>=0; i--){
    if(bitRead(x,i)==0) temp = LOW;
    else temp = HIGH;
    digitalWrite(i+2,temp);
  }
}

void cls(){
  for(int i =0; i<=6; i++){
    digitalWrite(i+2,LOW);
  }
  digitalWrite(10,LOW);
}
//using arduino to ouput keys from Serial and also ouput the key as char in Serial monitor
void loop ()
  {
  digitalWrite(11,LOW);
  while(Serial.available()<=0);
  int t = Serial.read();
  if(t!="")
  {
  sen(t);
  delay(10);
  digitalWrite(11,HIGH);
  delay(100);
  Serial.print((char)t);
  digitalWrite(11,LOW);
  cls();
  }
  }  // end of loop
