const int RLED=11;
const int GLED=10;
const int BLED=9;
const int TMP=A0;

const int echoPin = 5;
const int trigPin = 6;

const int piezo=3;

const int Button=8;


boolean lastButton=LOW;
boolean currentButton=LOW;
boolean changemode=false;
float temperature;
int startTmp;
float changeTMP;

boolean debounse(boolean last)
  {
    boolean current=digitalRead(Button);
    if(last!=current)
    {
      delay(5);
      current=digitalRead(Button);
    }
    return current;
}

void setup() {
  // put your setup code here, to run once:
  analogReference(INTERNAL);
  Serial.begin(9600);
  pinMode(RLED,OUTPUT);
  pinMode(GLED,OUTPUT);
  pinMode(BLED,OUTPUT);
  pinMode(TMP,INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(Button,INPUT);
  pinMode(piezo,OUTPUT);
  
  startTmp=analogRead(TMP);
  temperature = (startTmp)/9.28;
  Serial.println(temperature);

}

void loop() {
  float duration,distance;
  
  currentButton=debounse(lastButton);
  
  if(lastButton==LOW&&currentButton==HIGH)
  {
    if(changemode==false){
      changemode=true;
    }
    else{
      changemode=false;
    }
    Serial.println("----------------change the mode----------------");
    analogWrite(GLED,255);
    analogWrite(BLED,255);
    analogWrite(RLED,255);
  }
  lastButton=currentButton;
  
  if(changemode==false)
  {
    delay(200);
    startTmp=analogRead(TMP);
    changeTMP=(startTmp)/9.28;
    Serial.print("start");
    Serial.print(temperature);
    Serial.print("change");
    Serial.println(changeTMP);
    
    if((changeTMP)<temperature-1.00&&(changeTMP)>temperature-3)
    {
      analogWrite(GLED,0);
      analogWrite(BLED,255);
      analogWrite(RLED,255);
      Serial.println("level 1");
    }
    else if((changeTMP)<temperature-3&&(changeTMP)>temperature-4)
    {
      analogWrite(BLED,0);
      analogWrite(GLED,255);
      analogWrite(RLED,255);
      Serial.println("level 2");
    }
    else if((changeTMP)<temperature-4)
    {
      analogWrite(RLED,0);
      analogWrite(GLED,255);
      analogWrite(BLED,255);
      Serial.println("level 3");
    }
    else
    {
      analogWrite(GLED,255);
      analogWrite(BLED,255);
      analogWrite(RLED,255);
    }
  }
  else if(changemode==true)
  {
    digitalWrite(trigPin, LOW);
    digitalWrite(echoPin, LOW);
    delay(10);
    digitalWrite(trigPin, HIGH);
    delay(10);
    digitalWrite(trigPin, LOW);
   
    duration= pulseIn(echoPin,HIGH);
    distance = ((float)(340*duration)/10000)/2;
   
    Serial.print(distance);
    Serial.println("cm");
    delay(500);
    if(distance<30){
      Serial.println("ghost!");
      tone(piezo,500,1000);
    }
    
  }

}
