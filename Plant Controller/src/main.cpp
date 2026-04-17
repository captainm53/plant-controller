#include <Arduino.h>
#include <data_schema.h>

#define vlv0_pin 6
#define vlv1_pin 7
#define vlv2_pin 8
#define vlv3_pin 11
#define vlv4_pin 12
#define vlv5_pin 13
#define light0_pin 9
#define light1_pin 10

// put function declarations here:
int myFunction(int, int);

PlanterToPC dataschema;

void setup()
{
  Serial.begin(115200);
  int result = myFunction(2, 3);

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
  dataschema.sns0 = analogRead(A0);
  dataschema.sns1 = analogRead(A1);
  dataschema.sns2 = analogRead(A2);
  dataschema.sns3 = analogRead(A3);
  dataschema.sns4 = analogRead(A4);
  dataschema.sns5 = analogRead(A5);
  dataschema.sns6 = analogRead(A6);
  dataschema.sns7 = analogRead(A7);
  dataschema.time = millis() / 1000.0;

  if (millis() % 10000 > 5000)
  {
    dataschema.vlv0 = 1;
    dataschema.vlv1 = 1;
    dataschema.vlv2 = 1;
    dataschema.vlv3 = 1;
    dataschema.vlv4 = 1;
    dataschema.vlv5 = 1;
    dataschema.light0 = 1;
    dataschema.light1 = 1;
  }
  else
  {
    dataschema.vlv0 = 0;
    dataschema.vlv1 = 0;
    dataschema.vlv2 = 0;
    dataschema.vlv3 = 0;
    dataschema.vlv4 = 0;
    dataschema.vlv5 = 0;
    dataschema.light0 = 0;
    dataschema.light1 = 0;
  }

  Serial.write(dataschema.make_data_buffer());
}

// put function definitions here:
int myFunction(int x, int y)
{
  return x + y;
}