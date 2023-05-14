#include <ResponsiveAnalogRead.h>

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#include "Wire.h"

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"
#include "MPU6050.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;

float x_percent_tilt;
float y_percent_tilt;

float stillMargin = 5.0;

ResponsiveAnalogRead analog4(A4, true);

#define LED_PIN 13
bool blinkState = false;

int D2 = 2;
int D3 = 3;
int lastLeftPrintTime = 0;
int lastRightPrintTime = 0;
int delayTime = 500; // changed delay time to 500ms
int leftCounter = 0;
int clickVal;

bool ableToPrint;
int counter;
int lastPrintCheckTime;
int printInterval = 5000;
int prev;

int clickValL = 0;
int clickValR = 0;

String data;

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.begin();

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(38400);

    // initialize device
    //Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    //Serial.println("Testing device connections...");
    //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    analog4.setAnalogResolution(16000);
    analog4.setSnapMultiplier(0.0001);
    
    // configure Arduino LED for
    pinMode(LED_PIN, OUTPUT);
    pinMode(D2, INPUT);
    pinMode(D3, INPUT);

    int lastLeftPrintTime = 0;
    int lastRightPrintTime = 0;
    int delayTime = 1000; // changed delay time to 500ms
    int leftCounter = 0;
  }

void loop() {

    calcXTilt();
     
    // read raw accel/gyro measurements from device
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

    // update the ResponsiveAnalogRead object every loop
    int xReading = ax;
    int yReading = ay;
    analog4.update(xReading);
    analog4.update(yReading);
    

    if(x_percent_tilt <= stillMargin && x_percent_tilt >= -stillMargin)
    {
      if(y_percent_tilt <= stillMargin && y_percent_tilt >= -stillMargin)
      {
      x_percent_tilt = 0;
      y_percent_tilt = 0;
      }
    }

    //Serial.println(x_percent_tilt);
    //Serial.println(y_percent_tilt);
    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
    String string1 = String(clickValL);
    String string2 = String(clickValR);
     String string3 = String(x_percent_tilt);
     String string4 = String(y_percent_tilt);
     
     data = string1 + ',' + string2 + ',' + string3 + ',' + string4;
    Serial.println(data);
    //delay(300);
}

    void calcXTilt() 
    {
        //Calculate the x and y axis tilt
        if(ax < 16000.0)
        {
            x_percent_tilt = 50.0 / 8000.0 * ax;
        } 
        else
        {
            x_percent_tilt = 50.0 / 8000.0 * ax - 100;
        }

        if(ay < 16000.0)
        {
            y_percent_tilt = 50.0 / 8000.0 * ay;
        } 
        else
        {
            y_percent_tilt = 50.0 / 8000.0 * ay - 100;
        }
    }


