#include <TimerOne.h>

#define MOTOR_PIN 9
#define SERVO_PIN 10
#define LED_PIN 10
String data;
bool armed = false; // used to check if we have armed to UAV
 
void setup() 
{
  Serial.begin(115200);
  Serial.print("Setup....");
  
  Timer1.initialize(20000); // set a timer of length 10000 microseconds (or 0.02 sec - or 50Hz)
  Timer1.pwm(MOTOR_PIN, 0); // initially duty is set 0
  //Timer1.pwm(SERVO_PIN, 75); // initially duty is set to middle point (1,5 ms for this value)
  Timer1.pwm(LED_PIN,500);
  
  pinMode(LED_BUILTIN, INPUT);

  Serial.println("Setup done!");
}
 
void loop()
{
      // send data only when you receive data:
    while(Serial.available()) {
        data= Serial.readString();// read the incoming data as string

        int dataSize = data.length();
        String command = data.substring(0,1);
        int commandInt = command.toInt(); 
        String valueStr = data.substring(1,dataSize);
        Serial.print("Command chosen: ");
        Serial.println(command);
       
        switch (commandInt) {
          case 1:
            if(armed)
              setMotorSpeedESC(valueStr.toInt()); // set duty from 0 - 100%, uses pin 9
            else
              Serial.println("You need to arm the UAV before applying throttle");
            break;
          case 2: // arm 
            arm(true);
            break;
          case 3: // disarm
            arm(false);
            break;
          case 4: // calibrate esc
            calibrateESC();
            break;
          case 5: // set servo position, uses pin 10
            setServoPosition(valueStr.toInt());
            break;
          default:
            Serial.println("Wrong command, use first number to specify action followed by the desired value\n"
            "Actions:\n"
            "1=Set duty cycle between 0 to 100%(e.g. type \"1100\" for 100%) \n"
            "2=Arm (no need to specify value)\n"
            "3=Disarm (no need to specify value)"
            "4=Calibrate ESC (no need to specify value)\n"
            "5=Set servo positition (from -100 to 100%)");
        }
    }
}

void setMotorSpeedESC(int d){
  if(d > 100) // clamp to max 100%
    d = 100;
  else if(d < 0) // clamp to zero
    d = 0;
  if(d > 10){ // need at least 10% of throttle before spinning)
     int duty = 60+(d*0.4); // corrected value to match signal width
     setLEDwithRC(d);
     Timer1.pwm(MOTOR_PIN,duty);
     Serial.print("Duty set to: ");
     Serial.print(d);
     Serial.println("%");
  }else{
    Timer1.pwm(MOTOR_PIN,0);
  }
  
}

void setLEDwithRC(int duty){
  Timer1.pwm(LED_PIN,duty*10);
}

void setServoPosition(int pos){
    if(pos > 90)// clamp to max 100%
    pos = 90;
  else if(pos < -90) // clamp to min -100%
    pos = -90;
  int posCorrected = 75 +(pos*0.4); // corrected signal to match +- signal width
  Timer1.pwm(SERVO_PIN,posCorrected);
  Serial.print("Servo position set to: ");
  Serial.print(pos);
  Serial.println(" degree");
}

void arm(bool arm){
  armed = arm; // used both to arm and disarm
  if(arm)
    Serial.println("ARMED");
  else
    Serial.println("DISARMED");
}

void calibrateESC(){
    // Set max trottle followed by minimum throttle. Same as swiping stick up and down to calibrate signal range
  Serial.print("Calibrating...");
  setMotorSpeedESC(100);
  delay(500);
  setMotorSpeedESC(11);
  Serial.println("Calibrating done");
}



