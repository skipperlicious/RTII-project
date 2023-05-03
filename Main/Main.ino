#include <ResponsiveAnalogRead.h>

// I2C device class (I2Cdev) demonstration Arduino sketch for MPU9150
// 1/4/2013 original by Jeff Rowberg <jeff@rowberg.net> at https://github.com/jrowberg/i2cdevlib
//          modified by Aaron Weiss <aaron@sparkfun.com>
//
// Changelog:
//     2011-10-07 - initial release
//     2013-1-4 - added raw magnetometer output

/* ============================================
I2Cdev device library code is placed under the MIT license

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
*/

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
    int delayTime = 500; // changed delay time to 500ms
    int leftCounter = 0;
  }

void loop() {
  int stateIR = digitalRead(D2);
  int stateIR2 = digitalRead(D3);
  /*
  Serial.print("STATES 1: ");
  Serial.print(stateIR);
  Serial.print(" ");
  Serial.print("STATE 2: ");
  Serial.print(stateIR2);
  Serial.println("\n");
  */
    calcXTilt();
    if (stateIR == 0) {
            if (millis() - lastLeftPrintTime > delayTime) {
            if (leftCounter == 1) {
              clickValL = 3;
                //Serial.println(clickVal); // print "3" if LEFT is pressed twice within 500ms
                
                leftCounter = 0; // reset leftCounter after printing "3"
            } else {
               clickValL = 1;
                //Serial.println(clickVal);
                
                leftCounter = 1; // increment leftCounter if "LEFT" is pressed
            }
            lastLeftPrintTime = millis();
            }
        } else {
          clickValL = 0;
            //Serial.println(0);
            
            leftCounter = 0; // reset leftCounter if "LEFT" is released
        }

        if (stateIR2 == 0) {
            if (millis() - lastRightPrintTime > delayTime) {
              clickValR = 2;
            //Serial.println(clickVal); // RIGHT click
            
            lastRightPrintTime = millis();
            }
        } else {
          clickValR = 0;
            //Serial.println(0);
            
        }
     
     
    // read raw accel/gyro measurements from device
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

    // read from your ADC
    // update the ResponsiveAnalogRead object every loop
    int xReading = ax;
    int yReading = ay;
    analog4.update(xReading);
    analog4.update(yReading);
    //Serial.println(analog4.getValue());
    //Serial.println("DEBUG");
    

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


