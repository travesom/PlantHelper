
#include <SoftwareSerial.h>
#include "DHT.h"
#define TIMEOUT 5000 // mS
#define DHTPIN 2   
#define DHTTYPE DHT11
SoftwareSerial mySerial(7, 6); // RX, TX
const char* ssid     = "tester";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "haslohaslo";     // The password of the Wi-Fi network
String GET = "GET /data?temp=2&lumi=3&hum=4";
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200);
  delay(5000);
  SendCommand("AT+RST", "Ready");
  delay(5000);
  SendCommand("AT+CWMODE=1", "OK");
  delay(10000);
  //SendCmd("AT+CWJAP=\"tester\",\"haslohaslo\"");
  //delay(30000);
  SendCmd("AT+CIFSR");
  delay(40000);
  Serial.print("AT+CIPSTART=\"UDP\",\"192.168.0.18\",5005");
  SendCommand("AT+CIPSTART=\"UDP\",\"192.168.0.18\",5005","OK");
  delay(5000);
  //Serial.begin(115200);
  Serial.println(F("DHTxx test!"));
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  dht.begin();
}

void loop() {
delay(10000);
float h = dht.readHumidity(); //hum
float t = dht.readTemperature(); //temp
int   l = analogRead(A0);  //lux

  if(h<=10.0||t>=35.0||t<=15.0)
  {
  alarm(0);
  
  }
  else if(h<=30.0||t>=28.0||t<=20.0)
  {
    alarm(1);
    
    }
  else
  {
    alarm(2);
    }  
  



if (isnan(h) || isnan(t) ) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
}
float hic = dht.computeHeatIndex(t, h, false);
Serial.print(F(" Humidity: "));
Serial.print(h);
Serial.print(F("%  Temperature: "));
Serial.print(t);
Serial.print(F("°C "));
Serial.print(F("  Heat index: "));
Serial.print(hic);
Serial.print(F("°C "));
Serial.print("lux Value :");
Serial.println(l); 
String buffor=String(t)+" "+String(h)+" "+String(l);
String cmd="AT+CIPSEND="+String(buffor.length())+",\"192.168.0.18\",5005";
SendCommand(cmd,"OK");
SendCommand(buffor,"SEND OK");




}

boolean SendCommand(String cmd, String ack) {
  mySerial.println(cmd); // Send "AT+" command to module
  if (!echoFind(ack)) // timed out waiting for ack string
    return true; // ack blank or ack found
}
void SendCmd(String cmd) {
  mySerial.println(cmd);
  Serial.println();
}

boolean echoFind(String keyword) {
  byte current_char = 0;
  byte keyword_length = keyword.length();
  long deadline = millis() + TIMEOUT;
  while (millis() < deadline) {
    if (mySerial.available()) {
      char ch = mySerial.read();
      Serial.write(ch);
      if (ch == keyword[current_char])
        if (++current_char == keyword_length) {
          Serial.println();
          return true;
        }
    }
  }
  return false; // Timed out
}



void alarm(int code)
{
  
  if (code==0)//red
  {
    digitalWrite(13, LOW);
    digitalWrite(12, HIGH); 
  }
  if (code==1)//yellow
  {
    
    digitalWrite(12, HIGH);
    digitalWrite(13, HIGH); 
  }
  if (code==2)//red
  {
    
    digitalWrite(13, HIGH);
    digitalWrite(12, LOW); 
  }
}
