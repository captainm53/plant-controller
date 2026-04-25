#include <Arduino.h>
#include <data_schema.h>

#define vlv0_pin 2
#define vlv1_pin 3
#define vlv2_pin 4
#define vlv3_pin 7
#define vlv4_pin 8
#define vlv5_pin 9
#define light0_pin 5
#define light1_pin 6

PlanterToPC dataschema;

uint8_t real_time = 0; // Realworld time. Divide by 10 to get time in hours
unsigned long real_time_recieved = 0;

void setup()
{
  Serial.begin(115200);

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);

  pinMode(vlv0_pin, OUTPUT);
  pinMode(vlv1_pin, OUTPUT);
  pinMode(vlv2_pin, OUTPUT);
  pinMode(vlv3_pin, OUTPUT);
  pinMode(vlv4_pin, OUTPUT);
  pinMode(vlv5_pin, OUTPUT);
  pinMode(light0_pin, OUTPUT);
  pinMode(light1_pin, OUTPUT);

  dataschema.vlv0 = 0;
  dataschema.vlv1 = 0;
  dataschema.vlv2 = 0;
  dataschema.vlv3 = 0;
  dataschema.vlv4 = 0;
  dataschema.vlv5 = 0;
  dataschema.light0 = 0;
  dataschema.light1 = 0;
}

void loop()
{
  if (Serial.available() > 1)
  {
    int channel_name = Serial.read();
    int channel_value = Serial.read();

    if (channel_name == 0)
    {
      dataschema.vlv0 = channel_value;
    }
    if (channel_name == 1)
    {
      dataschema.vlv1 = channel_value;
    }
    if (channel_name == 2)
    {
      dataschema.vlv2 = channel_value;
    }
    if (channel_name == 3)
    {
      dataschema.vlv3 = channel_value;
    }
    if (channel_name == 4)
    {
      dataschema.vlv4 = channel_value;
    }
    if (channel_name == 5)
    {
      dataschema.vlv5 = channel_value;
    }
    if (channel_name == 6)
    {
      dataschema.light0 = channel_value;
    }
    if (channel_name == 7)
    {
      dataschema.light1 = channel_value;
    }
    if (channel_name == 255)
    {
      if (real_time != channel_value)
      {
        real_time = channel_value; // Real time in hours, only precise to 10ths
        real_time_recieved = millis();
      }
    }
  }
  dataschema.sns0 = analogRead(A0) / 1023 * 5;
  dataschema.sns1 = analogRead(A1) / 1023 * 5;
  dataschema.sns2 = analogRead(A2) / 1023 * 5;
  dataschema.sns3 = analogRead(A3) / 1023 * 5;
  dataschema.sns4 = analogRead(A4) / 1023 * 5;
  dataschema.sns5 = analogRead(A5) / 1023 * 5;
  dataschema.sns6 = analogRead(A6) / 1023 * 5;
  dataschema.sns7 = analogRead(A7) / 1023 * 5;
  dataschema.time = millis() / 1000.0;
  dataschema.real_time = real_time / 10.0 + (millis() - real_time_recieved) / 1000.0 / 60.0 / 60.0;
  while (dataschema.real_time > 24)
  {
    dataschema.real_time = dataschema.real_time - 24;
  }

  digitalWrite(vlv0_pin, dataschema.vlv0);
  digitalWrite(vlv1_pin, dataschema.vlv1);
  digitalWrite(vlv2_pin, dataschema.vlv2);
  digitalWrite(vlv3_pin, dataschema.vlv3);
  digitalWrite(vlv4_pin, dataschema.vlv4);
  digitalWrite(vlv5_pin, dataschema.vlv5);
  digitalWrite(light0_pin, dataschema.light0);
  digitalWrite(light1_pin, dataschema.light1);

  if (dataschema.real_time > 8 && dataschema.real_time < 9)
  {
    dataschema.light0 = 1;
    dataschema.light1 = 1;
  }
  else if (dataschema.real_time > 20 && dataschema.real_time < 21)
  {
    dataschema.light0 = 0;
    dataschema.light1 = 0;
  }

  Serial.write(dataschema.make_data_buffer(), dataschema.size);
  Serial.flush();
  delay(200);
}
